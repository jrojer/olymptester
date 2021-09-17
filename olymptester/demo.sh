root=$PWD
cd $root/example/app/cpp && make
cd $root/example/app/java && make
cd $root

echo "C++:"
python3 tester.py $root/example/app/cpp/app $root/example/tests/app.txt

echo "Java:"
python3 tester.py $root/example/app/java/App.class $root/example/tests/app.txt

echo "Python:"
python3 tester.py $root/example/app/py/app.py $root/example/tests/app.txt
