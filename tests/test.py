from olymptester import olymptester
from pathlib import Path

result = []


def mock_print_func(text):
    result.append(text)


olymptester.run(Path('exe.py'), Path('exe_test.txt'), mock_print_func)

assert(len(result) > 0)
for res in result:
    assert('OK' in res)
