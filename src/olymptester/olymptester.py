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

from olymptester.arg_parser import parse_args 
from olymptester.arg_parser import validate_paths 
from olymptester.arg_parser import path 
from olymptester.cpp_template import cpp_template

import subprocess
from subprocess import Popen
from subprocess import PIPE
import pathlib
import sys
import time
import os
import yaml

tests_file_template='''
Test 1:
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


def fail_message(s1, s2, s3, elapsed):
    return '''FAILED test {:3s}, {:5.3f} sec
Output:
{}
Correct:
{}'''.format(s1, elapsed, s2, s3)


def pass_message(s1, elapsed):
    return '{:20s} {:10s} {:5.3f} sec'.format(s1, 'OK', elapsed)


def exec_message(s1, s2, elapsed):
    return '''{:3s}, {:5.3f} sec
Output:
{}
'''.format(s1, elapsed, s2)

cpp_compilation_flags = ['-Wfatal-errors', '-std=c++17']

def compile_if_needed_and_get_path_to_exe(path_to_file: pathlib.Path):
    if path_to_file.suffix == '.cpp':
        path_to_exe = path_to_file.parent / 'app'
        subproc = ['g++', *cpp_compilation_flags, '-o', str(path_to_exe), str(path_to_file)]
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


def execute_on_input(subproc, input_text):
    def execute(input_text):
        with Popen(subproc, stdin=PIPE, stdout=PIPE, universal_newlines=True) as proc:
                return proc.communicate(input_text)[0]

    start_time = time.time()
    out = execute(input_text)
    end_time = time.time()
    elapsed = end_time - start_time
    return out, elapsed  


def run_exec_subprocess(subproc, yml, test_name):
    assert test_name in yml, f'"{test_name}" not found'
    test_input = yml[test_name]['input'].strip()
    out, elapsed = execute_on_input(subproc, test_input)
    print(exec_message(test_name, out.strip(), elapsed))


def run_testing_subprocess(subproc, yml, test_names = None):
    if test_names is None:
        test_names = yml.keys()

    for test_name in test_names:
        test_output = yml[test_name]['output'].strip()
        test_input = yml[test_name]['input'].strip()
        out, elapsed = execute_on_input(subproc, test_input) 
        if out.strip() == test_output:
            print(pass_message(test_name, elapsed))
        else:
            print(fail_message(test_name, out.strip(), test_output.strip(), elapsed)) 


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


def try_read_test_file(path_to_tests):
    assert path_to_tests.suffix in ['.yml', '.yaml'], str(path_to_tests.name) + ' is not a yaml file'
    with open(str(path_to_tests), 'r') as fd:
        return fd.read()


def main():
    try:
        args = parse_args()
        validate_paths(args)
        if args['mode'] in ['run', 'test']:
            path_to_program = path(args['workdir']) / args['path_to_program']
            path_to_tests = path(args['workdir']) / args['path_to_tests']

            path_to_exe = compile_if_needed_and_get_path_to_exe(path_to_program)
            test_file_text = try_read_test_file(path_to_tests)
            subproc = init_exe_subproc(path_to_exe)
            yml = yaml.safe_load(test_file_text)
            if args['test_name'] is None:
                args['test_name'] = list(yml.keys())[0]
            if args['mode'] == 'test':
                run_testing_subprocess(subproc, yml)
            elif args['mode'] == 'run':
                run_exec_subprocess(subproc, yml, args['test_name'])
        elif args['mode'] == 'init':
            init_cpp_template(path(args['dir']))
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    main()
