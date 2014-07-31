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

class Coverage(object):
    def __init__(self, file_to_watch):
        self.source_file = file_to_watch
        self.source_code = open(file_to_watch).readlines()
        self.executed_code = []

    def trace(self, frame, event, arg):
        current_file = inspect.getframeinfo(frame).filename

        if self.source_file in current_file and \
            (event == "line" or event == "call"):
            self.executed_code.append(frame.f_lineno)

        return self.trace

    def unexecuted_code(self):
        skipped = []
        for line_num in range(1, len(self.source_code)+1):
            if line_num not in self.executed_code:
                src = self.source_code[line_num - 1]
                if src != "\n" and 'else' not in src:
                    skipped.append(line_num)
        return skipped

    def report(self):
        skipped = self.unexecuted_code()
        if skipped:
            for line_num in skipped:
                print line_num, self.source_code[line_num - 1]
        else:
            print "100% coverage, go you!"

if __name__ == '__main__':
    t = Coverage('example2.py')
    sys.settrace(t.trace)
    run_tests()
    sys.settrace(None)
    t.report()
