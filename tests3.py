import sys
import inspect
from example2 import iffer, looper, continuer

def test_iffer():
    assert iffer(True) == 3
    assert iffer(False) == 10

def test_looper():
    assert looper() == 45

def test_continuer():
    assert continuer() == (50, 50, 50)

def run_tests():
    test_iffer()
    test_looper()
    test_continuer()
