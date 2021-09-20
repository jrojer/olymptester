# Olymptester
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
 * `run.sh` - a convinience script that runs compilation and olymptester

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

Tests:
```
Test 1
input begin
1
input end

output begin
2
output end

Test 2
input begin
33
input end

output begin
66
output end
```

Running:
```
$ ./run.sh app.cpp 
Test   0 OK, 0.008 sec
Test   1 OK, 0.008 sec
```