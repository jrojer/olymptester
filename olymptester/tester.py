#!/usr/bin/python3
import subprocess
from subprocess import Popen
from subprocess import PIPE
import pathlib
import sys
import re
import time
import os


def fail_message(s1,s2,s3,elapsed):
    return '''FAILED test {:3d}, {:5.3f} sec
Output:
{}
Correct:
{}'''.format(s1,elapsed,s2,s3)


def pass_message(s1,elapsed):
    return 'Test {:3d} OK, {:5.3f} sec'.format(s1,elapsed)


def run_test(subproc,test):
    input_text = test[0].strip()
    output_text = test[1].strip()
    with Popen(subproc, stdin=PIPE, stdout=PIPE, universal_newlines=True) as proc:
        proc_output = proc.communicate(input_text)[0]
        passed = proc_output.strip() == output_text.strip()
        return proc_output, passed


def try_init_subproc(path_to_exe):
    subproc = ['python',str(path_to_exe)] if path_to_exe.suffix == '.py' else [str(path_to_exe)]
    devnull = open(os.devnull,'w')
    try:
        subprocess.check_call(subproc,timeout=1, stdout=devnull, stderr=devnull)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise AssertionError('bad process call: %s' % subproc)
    except subprocess.TimeoutExpired:
        pass
    return subproc


def try_read_test_file(path_to_tests):
    with open(str(path_to_tests),'r') as fd:
        return fd.read()


def try_read_arguments():
    # check arguments
    if len(sys.argv) != 3:
        raise AssertionError('arguments are: executable, tests')
    path_to_exe = pathlib.Path(sys.argv[1]).absolute()
    path_to_tests = pathlib.Path(sys.argv[2]).absolute()
    return path_to_exe, path_to_tests


def main():
    try:
        path_to_exe, path_to_tests = try_read_arguments()
        subproc = try_init_subproc(path_to_exe)
        test_file_text = try_read_test_file(path_to_tests)
    except Exception as e:
        print(e)
        return

    r = re.compile(r'\s*input begin(.+?)input end\s+?output begin(.+?)output end\s*',flags=re.DOTALL)
    for i,test in enumerate(r.findall(test_file_text)):
        start_time = time.time()
        out,passed = run_test(subproc,test)
        end_time = time.time()
        elapsed = end_time - start_time
        if passed:
            print(pass_message(i,elapsed))
        else:
            print(fail_message(i,out.strip(),test[1].strip(),elapsed))


if __name__ == '__main__':
    main()
