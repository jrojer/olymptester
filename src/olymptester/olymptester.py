#!/usr/bin/python3
# Copyright (c) 2021 Alexey Roussanov

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import subprocess
from subprocess import Popen
from subprocess import PIPE
import pathlib
import sys
import re
import time
import os


def fail_message(s1, s2, s3, elapsed):
    return '''FAILED test {:3d}, {:5.3f} sec
Output:
{}
Correct:
{}'''.format(s1, elapsed, s2, s3)


def pass_message(s1, elapsed):
    return 'Test {:3d} OK, {:5.3f} sec'.format(s1, elapsed)


def run_test(subproc, test):
    input_text = test[0].strip()
    output_text = test[1].strip()
    with Popen(subproc, stdin=PIPE, stdout=PIPE, universal_newlines=True) as proc:
        proc_output = proc.communicate(input_text)[0]
        passed = proc_output.strip() == output_text.strip()
        return proc_output, passed


def try_init_subproc(path_to_exe):
    subproc = [str(path_to_exe)]
    if path_to_exe.suffix == '.py':
        subproc = ['python3', str(path_to_exe)]
    elif path_to_exe.suffix == '.class':
        subproc = ['java', '-cp',
                   str(path_to_exe.absolute().parent), str(path_to_exe.stem)]

    devnull = open(os.devnull, 'w')
    try:
        subprocess.check_call(subproc, timeout=1,
                              stdout=devnull, stderr=devnull)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise AssertionError(
            '''bad process call:
            Error: %s
            Subprocess: %s''' % (e, subproc))
    except subprocess.TimeoutExpired:
        pass
    return subproc


def try_read_test_file(path_to_tests):
    with open(str(path_to_tests), 'r') as fd:
        return fd.read()


def try_read_arguments():
    if len(sys.argv) != 3:
        raise AssertionError(
            'Usage: [python3 -m] olymptester path/to/app path/to/tests')
    path_to_exe = pathlib.Path(sys.argv[1]).absolute()
    path_to_tests = pathlib.Path(sys.argv[2]).absolute()
    return path_to_exe, path_to_tests


def test_subprocess(subproc, test_file_text, print_func):
    pattern = r'\s*input begin(.+?)input end\s+?output begin(.+?)output end\s*'
    r = re.compile(pattern, flags=re.DOTALL)
    for i, test in enumerate(r.findall(test_file_text)):
        start_time = time.time()
        out, passed = run_test(subproc, test)
        end_time = time.time()
        elapsed = end_time - start_time
        if passed:
            print_func(pass_message(i, elapsed))
        else:
            print_func(fail_message(i, out.strip(), test[1].strip(), elapsed))


def run(path_to_exe, path_to_tests, print_func):
    try:
        subproc = try_init_subproc(path_to_exe)
        test_file_text = try_read_test_file(path_to_tests)
    except Exception as e:
        print(e)
        return
    test_subprocess(subproc, test_file_text, print_func)


def main():
    try:
        path_to_exe, path_to_tests = try_read_arguments()
        run(path_to_exe, path_to_tests, print)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    main()
