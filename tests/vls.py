from pyln.testing.utils import TailableProc, env
import logging
import os
import signal
import time

class ValidatingLightningSignerD(TailableProc):
    def __init__(self, vlsd_dir, vlsd_port, vlsd_rpc_port, node_id, network):
        TailableProc.__init__(self, vlsd_dir, verbose=True)
        self.executable = env("REMOTE_SIGNER_CMD", 'vlsd2')
        os.environ['ALLOWLIST'] = env(
            'REMOTE_SIGNER_ALLOWLIST',
            'contrib/remote_hsmd/TESTING_ALLOWLIST')
        self.opts = [
            '--network={}'.format(network),
            '--datadir={}'.format(vlsd_dir),
            '--connect=http://localhost:{}'.format(vlsd_port),
            '--rpc-server-port={}'.format(vlsd_rpc_port),
            '--integration-test',
        ]
        self.prefix = 'vlsd2-%d' % (node_id)
        self.vlsd_port = vlsd_port
        self.vlsd_dir = vlsd_dir

    @property
    def cmd_line(self):
        return [self.executable] + self.opts

    def cleanup_stale_locks(self):
        """Clean up stale locks only if no other vlsd2 is using this directory."""
        import glob
        import subprocess

        # Check if there's already a vlsd2 process using this datadir
        try:
            result = subprocess.run(
                ["pgrep", "-f", "vlsd2.*--datadir={}".format(self.vlsd_dir)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                # There's already a process using this directory
                logging.warning(
                    "Found existing vlsd2 process for {}, not cleaning up".format(self.vlsd_dir)
                )
                return
        except Exception as e:
            logging.debug("Could not check for existing vlsd2 processes: {}".format(e))

        # No process is using this directory, safe to clean up stale locks
        # Note: We keep the .redb file itself for restart scenarios, only clean lock files
        for ext in [".redb-wal", ".redb-shm", ".redb-journal"]:
            for lock_file in glob.glob(os.path.join(self.vlsd_dir, "*" + ext)):
                try:
                    logging.info("Cleaning up stale lock file: {}".format(lock_file))
                    os.remove(lock_file)
                except Exception as e:
                    logging.warning("Failed to clean up {}: {}".format(lock_file, e))

    def start(self, stdin=None, stdout_redir=True, stderr_redir=True,
              wait_for_initialized=True):
        # Clean up any stale locks before starting
        self.cleanup_stale_locks()

        TailableProc.start(self, stdin, stdout_redir, stderr_redir)
        # We need to always wait for initialization
        self.wait_for_log("vlsd2 git_desc")
        logging.info("vlsd2 started (pid: {})".format(self.proc.pid))

    def stop(self, timeout=10):
        """Stop vlsd2 process more robustly to avoid database locks."""
        if self.proc is None:
            logging.info("vlsd2 process not running")
            return None

        logging.info("stopping vlsd2 (pid: {})".format(self.proc.pid))

        # First try graceful shutdown
        try:
            self.proc.terminate()
            rc = self.proc.wait(timeout)
            if rc is not None:
                logging.info("vlsd2 stopped gracefully (rc: {})".format(rc))
                self.logs_catchup()
                # Give the database lock time to be fully released
                time.sleep(0.5)
                return rc
        except Exception as e:
            logging.warning("vlsd2 graceful shutdown failed: {}".format(e))

        # If still running, try SIGKILL
        try:
            logging.info("vlsd2 still running, sending SIGKILL")
            self.proc.kill()
            rc = self.proc.wait(timeout=5)
            logging.info("vlsd2 killed (rc: {})".format(rc))
        except Exception as e:
            logging.error("Failed to kill vlsd2: {}".format(e))
            rc = None

        self.logs_catchup()

        # Ensure database lock is released
        time.sleep(0.5)

        return rc

    def __del__(self):
        self.logs_catchup()

