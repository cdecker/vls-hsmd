import pytest
from pyln.testing.utils import TailableProc, reserve_unused_port, TIMEOUT, drop_unused_port
import logging
import os

class LssD(TailableProc):
    def __init__(self, directory, rpcport=None):
        lss_dir = os.path.join(directory, 'lss')
        TailableProc.__init__(self, lss_dir, verbose=False)

        if rpcport is None:
            self.reserved_rpcport = reserve_unused_port()
            rpcport = self.reserved_rpcport
        else:
            self.reserved_rpcport = None

        self.rpcport = rpcport
        self.prefix = 'lss'
        os.environ["LSSD_PORT"] = str(rpcport)
        os.environ["LSSD_URI"] = f"http://127.0.0.1:{rpcport}"
        self.env['VLS_NETWORK'] = 'regtest'
        if not os.path.exists(lss_dir):
            os.makedirs(lss_dir)

        self.cmd_line = [
            'lssd',
            '--datadir={}'.format(lss_dir),
            '--port={}'.format(rpcport),
        ]

    def __del__(self):
        if self.reserved_rpcport is not None:
            drop_unused_port(self.reserved_rpcport)

    def start(self):
        self.env['RUST_LOG'] = 'debug'
        TailableProc.start(self)
        self.wait_for_log("ready on", timeout=TIMEOUT)

        logging.info("LssD started")

    def stop(self):
        logging.info("Stopping LssD")
        return TailableProc.stop(self)


@pytest.fixture(autouse=True)
def lssd(directory, bitcoind):
    lssd = LssD(directory)
    os.environ['BITCOIND_RPC_URL'] = f'http://rpcuser:rpcpass@127.0.0.1:{bitcoind.rpcport}'
    try:
        lssd.start()
    except Exception:
        lssd.stop()
        raise

    yield lssd

    try:
        lssd.stop()
    except Exception:
        lssd.proc.kill()
    lssd.proc.wait()



