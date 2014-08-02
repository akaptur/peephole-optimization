import sys
import inspect
from example3 import iffer, continuer

def test_iffer():
    assert iffer(True) == 3
    assert iffer(False) == 10

def test_continuer():
    assert continuer() == (50, 50, 50)

def run_tests():
    test_iffer()
    test_continuer()
