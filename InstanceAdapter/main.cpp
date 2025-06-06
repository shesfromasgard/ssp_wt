#include <iostream>
#include <vector>
#include <climits>
#include <random>
#include <cmath>
#include <iomanip>

using namespace std;

unsigned int m, w, t, c, p;
vector<int> executionTime;
vector<int> toolLife;
vector<vector<int>> magazine;

int main() {

    random_device rd;
    mt19937 generator(rd());
    normal_distribution<double> distribution(1.0, 0.33);

    cin >> m >> w >> t >> c >> p;

    executionTime.resize(w);
    toolLife.resize(t);
    magazine.resize(t, vector<int>(w));

    for(int i = 0; i < w; ++i)
        cin >> executionTime[i];
    
    for (int i = 0; i < t; ++i)
        for (int j = 0; j < w; ++j)
            cin >> magazine[i][j];

    for (int i = 0; i < t; ++i) {
        int maior = INT_MIN;

        for (int j = 0; j < w; ++j) {
            if(magazine[i][j] == 1 && executionTime[j] > maior) {
                maior = executionTime[j];
            }
        }

        double number;
        do {
            number = distribution(generator);
        } while (number < 1.0 || number > 3.0);
        
        toolLife[i] = static_cast<int>(round(number * maior));
    }

    cout << w << " " << t << " " << c << endl;

    for(int i = 0; i < t; ++i)
        cout << toolLife[i] << " ";
    
    cout << endl;

    for(int i = 0; i < w; ++i)
        cout << executionTime[i] << " ";

    cout << endl;
    
    for(int i = 0; i < t; ++i) {
        for(int j = 0; j < w; ++j) {
            cout << magazine[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}
