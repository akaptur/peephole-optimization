import sys
import inspect
from example import iffer, looper

def test_iffer():
    assert iffer(True) == 3
    assert iffer(False) == 10

def test_looper():
    assert looper() == 45

def run_tests():
    test_iffer()
    test_looper()

