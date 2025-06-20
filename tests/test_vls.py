from fixtures import *  # noqa: F401,F403
from fixtures import TEST_NETWORK
from pyln.client import RpcError
from utils import wait_for, sync_blockheight, COMPAT, TIMEOUT, scid_to_int, only_one

import base64
import os
import pytest
import re
import shutil
import subprocess
import time
import unittest

from test_pay import test_pay, test_pay_amounts

def test_start(node_factory):
    l1 = node_factory.get_node()
    print(l1)
