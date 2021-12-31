import pathlib
import argparse

usage_string = '''Welcome to Olymptester!
    Usage: 
    > olymptester run|test|init [-d dirname] [-p path/to/app] [-t path/to/tests]'''



def path(s):
    return pathlib.Path(s).absolute()


def validate_paths(d):
    if d['mode'] in ['run', 'test']:
        workdir = path(d['workdir'])
        solution = workdir / d['path_to_program']
        tests = workdir / d['path_to_tests']
        assert workdir.is_dir(), f'directory "{workdir.name}" does not exist'
        assert solution.is_file(), f'file {solution.name} does not exist'
        assert tests.is_file(), f'file {tests.name} does not exist'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="mode")
    parser.add_argument("-d", "--dir", help="directory")
    parser.add_argument("-p", "--program", help="path to program")
    parser.add_argument("-t", "--tests", help="path to tests")
    parser.add_argument("-n", "--name", help="test name")
    args = parser.parse_args()
    assert args.mode in ['init', 'test', 'run'], usage_string

    if args.mode == 'init':
        dir = '.' if args.dir is None else args.dir
        return {
                'mode': args.mode, 
                'dir': dir
        }    

    path_to_program = 'solution.cpp' if args.program is None else args.program
    path_to_tests = 'tests.yml' if args.tests is None else args.tests
    
    return {
            'workdir' : '.',
            'path_to_program': path_to_program,
            'path_to_tests' : path_to_tests,
            'mode' : args.mode,
            'test_name': args.name
    }
