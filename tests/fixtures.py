from utils import TEST_NETWORK, VALGRIND  # noqa: F401,F403
from pyln.testing.fixtures import (
    directory,
    test_base_dir,
    test_name,
    chainparams,
    node_factory,
    bitcoind,
    teardown_checks,
    db_provider,
    executor,
    setup_logging,
    jsonschemas,
)  # noqa: F401,F403
from pyln.testing.utils import reserve_unused_port, drop_unused_port
from pyln.testing import utils
from utils import COMPAT
from pathlib import Path
from lssd import lssd  # noqa: F401,F403
from pathlib import Path
from vls import ValidatingLightningSignerD
import os
import pytest
import re


def signer_subdaemon():
    root = Path(__file__).parent.parent
    mode = os.environ.get("VLS_MODE", "cln:native")

    subdaemon = {
        "cln:native": None,
        "cln:socket": f"hsmd:{root / 'target' / 'debug' / 'remote_hsmd_socket'}",
    }[mode]

    return subdaemon


class VlsLightningNode(utils.LightningNode):
    def __init__(self, node_id, lightning_dir, bitcoind, *args, **kwargs):
        utils.LightningNode.__init__(
            self, node_id, lightning_dir, bitcoind, *args, **kwargs
        )

        # Yes, we really want to test the local development version, not
        # something in out path.
        self.subdaemon = signer_subdaemon()
        self.use_vlsd = self.subdaemon is not None
        self.daemon.executable = "lightningd"
        self.vlsd: ValidatingLightningSignerD | None = None
        self.vls_dir = Path(lightning_dir) / "vlsd"
        self.vlsd_port: int = reserve_unused_port()
        self.vlsd_rpc_port: int = reserve_unused_port()
        self.node_id: int = node_id
        self.network = "regtest"
        if self.use_vlsd:
            self.daemon.opts["subdaemon"] = self.subdaemon

    def start(self, wait_for_bitcoind_sync=True, stderr_redir=False):
        self.vls_dir.mkdir(exist_ok=True, parents=True)

        # We start the signer first, otherwise the lightningd startup hangs on the init message
        if self.use_vlsd:
            self.vlsd = ValidatingLightningSignerD(
                vlsd_dir=self.vls_dir,
                vlsd_port=self.vlsd_port,
                vlsd_rpc_port=self.vlsd_rpc_port,
                node_id=self.node_id,
                network=self.network,
            )
            import threading

            threading.Timer(3, self.vlsd.start).start()
            self.daemon.env["VLS_PORT"] = str(self.vlsd_port)
            self.daemon.env["VLS_LSS"] = os.environ.get("LSS_URI", "")
        utils.LightningNode.start(
            self,
            wait_for_bitcoind_sync=wait_for_bitcoind_sync,
            stderr_redir=stderr_redir,
        )

    def stop(self, timeout: int = 10):
        utils.LightningNode.stop(self, timeout=timeout)
        if self.vlsd is not None and self.use_vlsd:
            rc = self.vlsd.stop(timeout=timeout)
            print(f"VLSD2 exited with rc={rc}")


LightningNode = VlsLightningNode


@pytest.fixture
def node_cls(lssd):
    print(lssd)
    return VlsLightningNode


class CompatLevel(object):
    """An object that encapsulates the compat-level of our build."""

    def __init__(self):
        makefile = os.path.join(os.path.dirname(__file__), "..", "Makefile")
        lines = [l for l in open(makefile, "r") if l.startswith("COMPAT_CFLAGS")]
        assert len(lines) == 1
        line = lines[0]
        flags = re.findall(r"COMPAT_V([0-9]+)=1", line)
        self.compat_flags = flags

    def __call__(self, version):
        return COMPAT and version in self.compat_flags


@pytest.fixture
def compat():
    return CompatLevel()


def is_compat(version):
    compat = CompatLevel()
    return compat(version)
