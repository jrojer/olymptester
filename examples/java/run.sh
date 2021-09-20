if [ "$#" -ne 1 ]; then
    echo "Usage: ./run.sh [app.cpp | App.java | app.py]"
fi
file=$@
if [[ $file == app.cpp ]]
then
    g++ -std=c++11 -o app app.cpp
    python3 -m olymptester app app.txt 
fi

if [[ $file == App.java ]]
then
    javac App.java
    python3 -m olymptester App.class app.txt 
fi

if [[ $file == app.py ]]
then
    python3 -m olymptester app.py app.txt 
fi