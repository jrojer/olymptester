# Olymtester
A convinient **tool** to code and test competitive programming apps (i.e. single file stdin-stdout apps).

## Usage: 

1. Install olymptester package: `python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps olymptester`.
2. Create an app (in C++, Java or Python). See `examples`.
3. Define tests. See `examples`.
4. Run the tester to test your solution. `python3 -m olymptester path/to/exe path/to/tests.txt`.

## Example:

In the example, a program that inputs integer `x` from stdin and outputs `2*x` to stdout is being tested by olymptester.

In `example/cpp` there is 
 * `app.cpp` file containing the program 
 * tests file `app.txt`, containing stdin and stdout values of 2 test cases
 * Makefile (it's optional)
 * `run.sh` - a convinience script that runs make and olymptester
