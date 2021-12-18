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
import yaml



cpp_template = '''
#include<iostream>
#define int int64_t
using namespace std;

int32_t main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int x;
    cin >> x;
    cout << 2*x;
    return 0;
}
'''

tests_file_template='''
Test 1 simple:
  input: |+
    1
  output: |+
    2

Test 2:
  input: |+
    33
  output: |+
    66 
'''


usage_string = '''Welcome to Olymptester!
    Usage: 
    > olymptester path/to/app path/to/tests'''


def fail_message(s1, s2, s3, elapsed):
    return '''FAILED test {:3s}, {:5.3f} sec
Output:
{}
Correct:
{}'''.format(s1, elapsed, s2, s3)


def pass_message(s1, elapsed):
    return '{:20s} {:10s} {:5.3f} sec'.format(s1, 'OK', elapsed)


def run_test(subproc, input_text, output_text):
    with Popen(subproc, stdin=PIPE, stdout=PIPE, universal_newlines=True) as proc:
        return proc.communicate(input_text)[0]


def compile_if_needed_and_get_path_to_exe(path_to_file: pathlib.Path):
    if path_to_file.suffix == '.cpp':
        path_to_exe = path_to_file.parent / 'app'
        subproc = ['g++', '-std=c++11', '-o', str(path_to_exe), str(path_to_file)]
    elif path_to_file.suffix == '.java':
        path_to_exe = path_to_file.parent / (path_to_file.stem + '.class')
        subproc = ['javac', path_to_file]
    else:
        subproc = None
        path_to_exe = path_to_file
    if subproc:
        result = subprocess.run(subproc)
        if result.returncode != 0 :
            raise Exception("Build failed.")
    return path_to_exe


def init_exe_subproc(path_to_exe):
    if path_to_exe.suffix == '.py':
        subproc = ['python3', str(path_to_exe)]
    elif path_to_exe.suffix == '.class':
        subproc = ['java', '-cp',
                   str(path_to_exe.absolute().parent), str(path_to_exe.stem)]
    else:
        subproc = [str(path_to_exe)]

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
    assert path_to_tests.suffix in ['.yml', '.yaml'], str(path_to_tests.name) + ' is not a yaml file'
    with open(str(path_to_tests), 'r') as fd:
        return fd.read()


def parse_args():
    def path(s):
        return pathlib.Path(s).absolute()
    size = len(sys.argv)
    arr = sys.argv
    assert size in [1,2,3,4], usage_string
    if size == 1 or size == 2 and arr[1] == 'run':
        solution = path('solution.cpp')
        tests = path('tests.yml')
        assert solution.is_file(), f'file {solution.name} does not exist'
        assert tests.is_file(), f'file {tests.name} does not exist'
        return {
            'path_to_program': solution,
            'path_to_tests' : tests,
            'mode' : 'run',
        }
    if size == 2:
        assert arr[1] == 'init', usage_string
        return {'mode': 'init', 'dir': path('.')}
    if size == 3:
        assert arr[1] in ['run','init'], usage_string
        if arr[1] == 'run':
            workdir = path(arr[2])
            solution = workdir/'solution.cpp'
            tests = workdir/'tests.yml'
            assert workdir.is_dir(), f'directory "{workdir.name}" does not exist'
            assert solution.is_file(), f'file {solution.name} does not exist'
            assert tests.is_file(), f'file {tests.name} does not exist'
            return {
                'path_to_program': solution,
                'path_to_tests' : tests,
                'mode' : 'run',
            }
        else:
            return {'mode': 'init', 'dir': arr[2]}
    if size == 4:
        assert arr[1] == 'run', usage_string
        solution = path(arr[1])
        tests = path(arr[2])
        assert solution.is_file(), f'file {solution.name} does not exist'
        assert tests.is_file(), f'file {tests.name} does not exist'
        return {
            'path_to_program': solution,
            'path_to_tests'  : tests,
            'mode' : 'run'
        }


def run_testing_subprocess(subproc, test_file_yml, print_func):
    yml = yaml.safe_load(test_file_yml)
    for test_name in yml.keys():
        test_input = yml[test_name]['input'].strip()
        test_output = yml[test_name]['output'].strip()

        start_time = time.time()
        out = run_test(subproc, test_input, test_output)
        passed = out.strip() == test_output
        end_time = time.time()
        elapsed = end_time - start_time
        if passed:
            print_func(pass_message(test_name, elapsed))
        else:
            print_func(fail_message(test_name, out.strip(), test_output.strip(), elapsed))    


def run(path_to_program, path_to_tests, print_func):
    try:
        path_to_exe = compile_if_needed_and_get_path_to_exe(path_to_program)
        subproc = init_exe_subproc(path_to_exe)
        test_file_text = try_read_test_file(path_to_tests)
    except Exception as e:
        print(e)
        return
    run_testing_subprocess(subproc, test_file_text, print_func)


def init_cpp_template(dirname: str):
    def assert_file_not_exists(p : pathlib.Path):
        assert not (p.is_file() or p.is_dir()), f'file {p.name} already exists'
    workdir = pathlib.Path(dirname)
    solution_path = (workdir/'solution.cpp').absolute()
    tests_path = (workdir/'tests.yml').absolute()
    if workdir.absolute() != pathlib.Path('.').absolute():
        assert_file_not_exists(workdir)
    else:
        assert_file_not_exists(solution_path)
        assert_file_not_exists(tests_path)
    workdir.mkdir(parents=True, exist_ok=True)
    with open(solution_path, 'w') as f:
        print(cpp_template, file=f)
    with open(tests_path, 'w') as f:
        print(tests_file_template, file=f)


def main():
    try:
        args = parse_args()
        if args['mode'] == 'run':
            run(args['path_to_program'], args['path_to_tests'], print)
        elif args['mode'] == 'init':
            init_cpp_template(args['dir'])
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    main()
