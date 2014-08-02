import sys
import inspect
from example import iffer

def test_iffer():
    assert iffer(True) == 3
    assert iffer(False) == 10

def run_tests():
    test_iffer()

