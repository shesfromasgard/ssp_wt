#include <iostream>
#include <vector>
#include <climits>

using namespace std;

// As variáveis globais permanecem as mesmas
unsigned int m, n, c;
vector<int> toolLife;
vector<int> executionTime;
vector<vector<int>> magazine;

int main() {

    cin >> n >> m >> c;

    toolLife.resize(m);
    executionTime.resize(n);
    magazine.resize(m, vector<int>(n));

    bool instanceIsOk = true;

    for(int i = 0; i < m; ++i)
        cin >> toolLife[i];

    for(int i = 0; i < n; ++i)
        cin >> executionTime[i];

    for(int i = 0; i < m; ++i)
        for(int j = 0; j < n; ++j)
            cin >> magazine[i][j];

    cout << "--- Iniciando Validacao ---" << endl;

    for(int j = 0; j < n; ++j) {
        int taskTime = executionTime[j];

        for(int i = 0; i < m; ++i) {

            if(magazine[i][j] == 1) {

                if (taskTime > toolLife[i]) {
                    cout << "ERRO: Tarefa " << (j + 1) << " (tempo: " << taskTime << ")"<< " requer a Ferramenta " << (i + 2) << ", mas sua vida util ( " << toolLife[i] << ") e insuficiente." << endl;
                    instanceIsOk = false;
                }
            }
        }
    }

    cout << "--- Validacao Finalizada ---" << endl << endl;

    if(instanceIsOk) {
        cout << "Instancia VALIDA." << endl;
        return 0;
    } else {
        cout << "Instancia INVALIDA." << endl;
        return 1;
    }
}