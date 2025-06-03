#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <limits>
#include <numeric>
#include <chrono>
#include <time.h>
#include <climits>

using namespace std;
using namespace std::chrono;

// ***************************************************
// n = número de tarefas
// m = número de ferramentas
// c = capacidade do magazine
// toolLife = tempo de vida últil de cada ferramenta nova
// executionTime = tempo de execução de cada tarefa
// matrix = matriz de ferramentas
// ***************************************************

unsigned int m, n, c;
vector<vector<int>> matrix;
vector<int> toolLife;
vector<int> executionTime;

vector<int> processos;

std::random_device rd;
std::mt19937 g(rd());

long opt2(bool debug);
int KTNS(vector<int> solucao, bool debug);
long swap2(bool debug);
vector<int> opt(vector<int> solucao, int a, int b);
vector<int> swap(vector<int> solucao, int a, int b);

int main() {
    
    auto start = high_resolution_clock::now();
    
    cin >> n >> m >> c;
    
    toolLife.resize(m);
    executionTime.resize(n);
    matrix.resize(m, vector<int>(n));
    processos.resize(n);

    for (int i = 0; i < m; ++i)
        cin >> toolLife[i];

    for (int i = 0; i < n; ++i)
        cin >> executionTime[i];

    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            cin >> matrix[i][j];

    iota(processos.begin(), processos.end(), 0);

    shuffle(processos.begin(), processos.end(), g);
    
    long initialSolution = KTNS(processos, false);
    opt2(false);
    long finalSolution = swap2(false);

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    
    cout << duration.count() / 1000000.0 << endl;
    cout << initialSolution << endl;
    cout << finalSolution << endl;

    return 0;

}

long opt2(bool debug = false) {
    vector<int> solucaoAtual = processos;
    long resultadoAtual = KTNS(processos, false);

    vector<int> melhorSolucao = solucaoAtual;
    long melhorResultado = resultadoAtual;

    vector<int> solucaoNova;
    long resultadoNovo;

    bool melhorou = true;

    while(melhorou) {
        melhorou = false;

        for(int i = 0 ; i < n - 1; ++i) {
            for(int j = i + 1; j < n; ++j) {
                solucaoNova = solucaoAtual;
                solucaoNova = opt(solucaoNova, i, j);

                resultadoNovo = KTNS(solucaoNova, false);

                if(resultadoNovo < melhorResultado) {
                    melhorResultado = resultadoNovo;
                    melhorSolucao = solucaoNova;
                    melhorou = true;
                }
            }
        }

        solucaoAtual = melhorSolucao;

    }

    processos = solucaoAtual;

    return melhorResultado;
}

vector<int> opt(vector<int> solucao, int a, int b) {
    if(a > b) {
        int tmp = a;
        a = b;
        b = tmp;
    }

    for(int i = a; i <= b; ++i) {
        int tmp = solucao[i];
        solucao[i] = solucao[b];
        solucao[b] = tmp;
        --b;
    }

    return solucao;
}

long swap2(bool debug = false) {
    vector<int> solucaoAtual = processos;
    long resultadoAtual = KTNS(processos, false);

    vector<int> melhorSolucao = solucaoAtual;
    long melhorResultado = resultadoAtual;

    vector<int> solucaoNova;
    long resultadoNovo;

    bool melhorou = true;

    while(melhorou) {
        melhorou = false;

        for(int i = 0 ; i < n - 1; ++i) {
            for(int j = i + 1; j < n; ++j) {
                solucaoNova = solucaoAtual;
                solucaoNova = swap(solucaoNova, i, j);

                resultadoNovo = KTNS(solucaoNova, false);

                if(resultadoNovo < melhorResultado) {
                    melhorResultado = resultadoNovo;
                    melhorSolucao = solucaoNova;
                    melhorou = true;
                }
            }
        }

        solucaoAtual = melhorSolucao;

    }

    processos = solucaoAtual;

    return melhorResultado;
}

vector<int> swap(vector<int> solucao, int a, int b) {
    if(a > b) {
        int tmp = a;
        a = b;
        b = tmp;
    }

    int tmp = solucao[a];
    solucao[a] = solucao[b];
    solucao[b] = tmp;

    return solucao;
}

int KTNS(vector<int> solucao, bool debug = false) {

    vector<int> carregadas(m, 0);
    vector<vector<int>> prioridades(m, vector<int>(solucao.size()));
    vector<vector<int>> magazine(m, vector<int>(solucao.size()));
    vector<int> remainingLife = toolLife;

    int u = 0; // ferramentas no magazine
    int trocas = 0;

    if(solucao.size() == 0) {
        cout << "Vetor solucao vazio." << endl;
        return 0;
    }

    if(debug) cout << "----------- Iniciando a função KTNS -------------" << endl;
    if(debug) cout << "Iniciando solucao[0]" << endl;

    for (unsigned int j = 0; j < m; j++) {
        // preenche o magazine com as ferramentas para a primeira tarefa
		carregadas[j] = matrix[j][solucao[0]];
		if (matrix[j][solucao[0]] == 1) {
			++u;
            // já decrementa o tempo de execução da tarefa 0 das ferramentas carregadas
            remainingLife[j] -= executionTime[solucao[0]];
        }
        // preenche o vetor magazine
		for (unsigned i = 0; i < solucao.size(); i++) {
            magazine[j][i] = matrix[j][solucao[i]];
        }
	}
	// Preenche a matriz de prioridades
	for (unsigned i = 0; i < m; ++i){
		for (unsigned j = 0; j < solucao.size(); ++j){
			if (magazine[i][j]==1)
				prioridades[i][j] = 0;
			else {
				int proxima = 0;
				bool usa = false;
				for (unsigned k = j + 1; k < solucao.size(); ++k){
					++proxima;
					if (magazine[i][k] == 1){
						usa = true;
						break;
					}
				}
				if (usa)
					prioridades[i][j] = proxima;
				else
					prioridades[i][j] = -1;
			}
		}
	}

    for(unsigned i = 1; i < solucao.size(); ++i) { // i = tarefa
        for(unsigned j = 0; j < m; ++j) { // j = ferramenta
            // troca preditiva por desgaste
            if(magazine[j][i] == 1 && carregadas[j] == 1) {
                if(remainingLife[j] < executionTime[solucao[i]]) {
                    trocas++;
                    remainingLife[j] = toolLife[j];
                }
            }
        }
        for(int j = 0; j < m; ++j) {
            // carrega as ferramentas necessárias para a próxima tarefa
            if((magazine[j][i] == 1) && (carregadas[j] == 0)) {
                carregadas[j] = 1;
                ++u;
                if(remainingLife[j] < executionTime[i]) {
                    remainingLife[j] = toolLife[j];
                }
            }

        }

            while(u > c) {
                int remove = -1;
                bool removed = false;

                for(unsigned j = 0; j < m; ++j) {
                    if(carregadas[j] == 1 && magazine[j][i] != 1 && prioridades[j][i] == -1) {
                        remove = j;
                        removed = true;
                        break;
                    }
                }

                if(!removed) {
                    int min = INT_MAX;
                    int index;

                    for(unsigned j = 0; j < m; ++j) {
                        if(carregadas[j] == 1 && magazine[j][i] != 1 && prioridades[j][i] > 0) {
                            // próxima vez que a ferramenta j será usada
                            int nextIndex = i + prioridades[j][i];

                            int current = remainingLife[j] - executionTime[solucao[nextIndex]];

                            if(current < min) {
                                min = current;
                                index = j;
                            }
                        }
                    }

                    // se a ferramenta index não tiver tempo suficiente para realizar a sua próxima tarefa, remove ela de uma vez
                    if(min < 0) {
                        remove = index;
                    } else {
                        min = 0;
                        for (unsigned j = 0; j < m; ++j) {
                            if (magazine[j][i] != 1){
                                if ((prioridades[j][i] > min) && carregadas[j] == 1) {
                                    min = prioridades[j][i];
                                    remove = j;
                                }
                            }
                        }
                    }
                }

                carregadas[remove] = 0;
                --u;
                trocas++;
            }

        for(unsigned j = 0; j < m; ++j) {
            if(magazine[j][i] == 1 && carregadas[j] == 1) {
                remainingLife[j] -= executionTime[solucao[i]];
            }
        }
    }

    return trocas + c;

}