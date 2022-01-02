
cpp_template = '''\
#include<iostream>
#include<algorithm>
#include<functional>
#include<vector>
#include<unordered_map>
#include<unordered_set>
#include<map>
#include<set>
#include<string>
#include<cstdlib>
#include <math.h> 


#define int int64_t
using namespace std;

#define verify(condition) { \
  if(!(condition)) { \
    cout << "line: " << __LINE__ << ", expected: " << #condition << endl; \
    exit(0); \
  } \
} 


int n;
int m;
vector<int> vec;


void test(){

    verify(1 == 1);
    cout << "OK" << endl;
}

int32_t main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);


    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
        
        }
    }

    cin >> n;
    cout << 2*n;
    return 0;
}
'''