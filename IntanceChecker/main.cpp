#include <iostream>
#include <vector>
#include <climits>

using namespace std;

unsigned int m, n, c;
vector<int> toolLife;
vector<int> executionTime;
vector<vector<int>> magazine;

int main() {

    cin >> n >> m >> c;

    toolLife.resize(m);
    executionTime.resize(n);
    magazine.resize(m, vector<int>(n));

    for(int i = 0; i < m; ++i)
        cin >> toolLife[i];

    for(int i = 0; i < n; ++i)
        cin >> executionTime[i];

    for(int i = 0; i < m; ++i)
        for(int j = 0; j < n; ++j)
            cin >> magazine[i][j];

    for(int i = 0; i < m; ++i) {
        int maior = INT_MIN;
        for(int j = 0; j < n; ++j) {
            if(magazine[i][j] == 1 && executionTime[j] > maior)
                maior = executionTime[j];
        }

        if(maior > toolLife[i])
            return 1;
    }

    return 0;

}