# Olymtester
A convinient **tool** and **project template** to code and test competitive programming apps (i.e. single file stdin-stdout apps).

## Usage: 

1. Create an app (cpp/java/py). See `olymptester/example/app/cpp` as example.
2. Define the tests. See `olymptester/example/tests/app.txt` as example.
3. Run the tester to test your solution. `python3 tester.py path/to/exe path/to/tests.txt`.

## Demo:
You can find a demo script at `olymptester/demo.sh`.
It runs makefiles for cpp and java. Then it runs cpp executable, java class and python script against `app.txt` tests file.
Each example app takes integer `x` from `stdin` and outputs `2*x` to `stdout`.
