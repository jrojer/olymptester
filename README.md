# Olymptester
A convinient **tool** for creating and testing competitive programming solutions (i.e. single file stdin-stdout apps).

## Usage: 

0. Prerequisite: `pipx`
  ```
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath
  ```
1. Install olymptester package: 
  ```
  python3 -m pipx install git+https://github.com/jrojer/olymptester.git
  ```
  After installation, to upgrade to the version in this repo's master, do
  ```
  python3 -m pipx reinstall olymptester
  ```
2. Create an app (in C++, Java or Python). See `examples`.
3. Define tests. See `examples`.
4. Run the tester to test your solution. `python3 -m olymptester path/to/program path/to/tests.yml`.

## Example:

In the example, a program that inputs integer `x` from stdin and outputs `2*x` to stdout is being tested by olymptester.

In the `examples` there is 
 * `app.cpp` file containing the program 
 * tests file `app.yml`, containing stdin and stdout values of 2 test cases

Program: 
```c++
#include<iostream>

using namespace std;

int main() {
    int x;
    cin >> x;
    cout << 2*x;
    return 0;
}
```

app.yml
```
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
```

Running:
```
$ python3 -m olymptester ./examples/App.java ./examples/app.yml
Test 1 simple        OK         0.150 sec
Test 2               OK         0.139 sec
```

## Another example:

Yaml supports multiline strings.

knapsack.yml:
```
Test 1:
  input: |+
    1
    4 5
    1 8
    2 4
    3 0
    2 5
    2 3
  output: |+
    13
```