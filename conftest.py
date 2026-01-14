import pytest
import subprocess
from urllib import request
import os
import sys
import json
from time import time
import unittest
import signal

# Add the repository root to Python path so 'lightning' module can be imported
# This is needed for imports like: from lightning.tests.test_invoices import ...
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)


def pytest_configure(config):
    """Register custom markers to avoid warnings."""
    config.addinivalue_line("markers",
                            "slow_test: slow tests aren't run under Valgrind")
    config.addinivalue_line("markers",
                            "openchannel: Limit this test to only run 'v1' or 'v2' openchannel protocol")


def pytest_collection_modifyitems(config, items):
    """
    Filter out any tests collected from lightning/tests/* modules.
    
    When our wrapped tests import from lightning.tests.*, pytest also discovers
    all the original test functions from those modules. We only want to run our
    wrapped versions in tests/*, not the originals.
    """
    filtered_items = []
    for item in items:
        # Get the module path of the test item
        # Try both .fspath (older pytest) and .path (newer pytest)
        if hasattr(item, 'path'):
            fspath = str(item.path)
        else:
            fspath = str(item.fspath)
        
        # Skip tests that are in the lightning/tests directory
        if '/lightning/tests/' in fspath or '\\lightning\\tests\\' in fspath:
            continue
            
        filtered_items.append(item)
    
    # Update the items list in place
    items[:] = filtered_items

server = os.environ.get("CI_SERVER_URL", None)

github_sha = (
    subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ASCII").strip()
)

github_ref_name = (
    subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    .decode("ASCII")
    .strip()
)

run_id = os.environ.get("GITHUB_RUN_ID", None)
run_number = os.environ.get("GITHUB_RUN_NUMBER", None)

result = {
    "github_repository": os.environ.get("GITHUB_REPOSITORY", None),
    "github_sha": os.environ.get("GITHUB_SHA", github_sha),
    "github_ref": os.environ.get("GITHUB_REF", None),
    "github_ref_name": github_ref_name,
    "github_run_id": int(run_id) if run_id else None,
    "github_head_ref": os.environ.get("GITHUB_HEAD_REF", None),
    "github_run_number": int(run_number) if run_number else None,
    "github_base_ref": os.environ.get("GITHUB_BASE_REF", None),
    "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", None),
}


@pytest.fixture(scope="session", autouse=True)
def cleanup_stale_vlsd2_processes():
    """Clean up any stale vlsd2 processes before starting tests."""
    try:
        # Find all vlsd2 processes
        result = subprocess.run(
            ["pgrep", "-f", "vlsd2.*--integration-test"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"Found {len(pids)} stale vlsd2 processes, cleaning up...")
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"Killed stale vlsd2 process: {pid}")
                except Exception as e:
                    print(f"Failed to kill process {pid}: {e}")
            # Give the OS time to clean up
            import time
            time.sleep(1)
    except Exception as e:
        print(f"Error cleaning up stale vlsd2 processes: {e}")

    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    global result
    result = result.copy()
    result["testname"] = pyfuncitem.name
    result["start_time"] = int(time())
    outcome = yield
    result["end_time"] = int(time())
    # outcome.excinfo may be None or a (cls, val, tb) tuple

    if outcome.excinfo is None:
        result["outcome"] = "success"
    elif outcome.excinfo[0] == unittest.case.SkipTest:
        result["outcome"] = "skip"
    else:
        result["outcome"] = "fail"

    print(result)

    if not server:
        return

    try:
        req = request.Request(f"{server}/hook/test", method="POST")
        req.add_header("Content-Type", "application/json")

        request.urlopen(
            req,
            data=json.dumps(result).encode("ASCII"),
        )
    except ConnectionError as e:
        print(f"Could not report testrun: {e}")
    except Exception as e:
        import warnings

        warnings.warn(f"Error reporting testrun: {e}")
