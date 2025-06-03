#include <iostream>
#include <vector>
#include <numeric> // Para std::accumulate

using namespace std;

// ***************************************************
// n = número de tarefas
// m = número de ferramentas
// c = capacidade do magazine (não utilizada neste cálculo)
// toolLife = tempo de vida útil de cada ferramenta nova
// executionTime = tempo de execução de cada tarefa
// matrix = matriz de ferramentas (indica qual ferramenta é usada por qual tarefa)
// ***************************************************

unsigned int m, n, c;
vector<int> toolLife;
vector<int> executionTime;
vector<vector<int>> matrix;

int main() {
    cin >> n >> m >> c;

    toolLife.resize(m);
    executionTime.resize(n);
    matrix.resize(m, vector<int>(n));

    for (int i = 0; i < m; ++i)
        cin >> toolLife[i];

    for (int i = 0; i < n; ++i)
        cin >> executionTime[i];

    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            cin >> matrix[i][j];

    float totalToolLife = 0.0;
    for (int life : toolLife) {
        totalToolLife += life;
    }

    float totalConsumedToolLife = 0.0;
    for (int i = 0; i < m; ++i) {
        float consumedByThisTool = 0.0;
        for (int j = 0; j < n; ++j) {
            if (matrix[i][j] == 1) {
                consumedByThisTool += executionTime[j];
            }
        }
        totalConsumedToolLife += min((float)toolLife[i], consumedByThisTool);
    }

    float totalRemainingToolLife = totalToolLife - totalConsumedToolLife;

    float percentageRemaining = 0.0;
    if (totalToolLife > 0) {
        percentageRemaining = (totalRemainingToolLife / totalToolLife);
    }

    cout.precision(4);
    cout << fixed << percentageRemaining << endl;

    return 0;
}