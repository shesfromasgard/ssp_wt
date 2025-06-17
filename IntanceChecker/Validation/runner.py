import subprocess
import os
import sys
import re

# Altere 'CPP_EXECUTABLE' para o caminho do seu executável C++
# Exemplo Linux/macOS: './meu_programa_exec'
# Exemplo Windows: 'meu_programa.exe' ou r'C:\caminho\para\meu_programa.exe'

CPP_EXECUTABLE = './main' 

INPUT_FOLDER = 'input_files'
OUTPUT_FOLDER = 'output_files'

# Lista para armazenar informações de todas as instâncias processadas
all_instance_results = []
incorrect_instances_list = []

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
report_filepath = os.path.join(OUTPUT_FOLDER, "relatorio_instancias.txt")

def run_cpp_with_file_input(input_filepath, cpp_executable_path):
    """
    Executa o programa C++ com o conteúdo de um arquivo como entrada padrão
    e captura a saída.

    Args:
        input_filepath (str): Caminho completo para o arquivo de entrada.
        cpp_executable_path (str): Caminho para o executável C++.

    Returns:
        dict: Um dicionário contendo o nome da instância, status (Correta/Incorreta),
              saída padrão, erro padrão e código de retorno.
    """
    instance_name = os.path.basename(input_filepath)
    print(f"Processando '{instance_name}'")

    result = {
        'instance_name': instance_name,
        'status': 'Erro Interno', # Estado inicial, pode ser atualizado
        'stdout': '',
        'stderr': '',
        'returncode': None,
        'error_message': ''
    }

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f_in:
            input_data = f_in.read()

        # Verifica se o executável C++ existe
        actual_cpp_executable_path = cpp_executable_path
        if not os.path.exists(actual_cpp_executable_path):
            if sys.platform == "win32" and not actual_cpp_executable_path.endswith('.exe'):
                if os.path.exists(actual_cpp_executable_path + '.exe'):
                    actual_cpp_executable_path += '.exe'
                else:
                    result['status'] = 'Falha'
                    result['error_message'] = f"Executável C++ '{cpp_executable_path}' (ou .exe) não encontrado."
                    print(f"   Erro: {result['error_message']}")
                    return result
            else:
                result['status'] = 'Falha'
                result['error_message'] = f"Executável C++ '{cpp_executable_path}' não encontrado."
                print(f"   Erro: {result['error_message']}")
                return result

        # Executa o processo C++
        process = subprocess.Popen(
            [actual_cpp_executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Para que stdout/stderr sejam strings, não bytes
            encoding='utf-8'
        )

        stdout, stderr = process.communicate(input=input_data)

        result['stdout'] = stdout.strip()
        result['stderr'] = stderr.strip()
        result['returncode'] = process.returncode

        if process.returncode == 0:
            result['status'] = 'Correta'
            print(f"Instância '{instance_name}' correta.")
        else:
            result['status'] = 'Incorreta'
            print(f"Instância '{instance_name}' **INCORRETA** (código de retorno: {process.returncode}).")
            if stderr:
                print(f"   Stderr: {stderr.strip()}")
            
    except FileNotFoundError:
        result['status'] = 'Falha'
        result['error_message'] = f"Arquivo de entrada '{input_filepath}' não encontrado."
        print(f"   Erro: {result['error_message']}")
    except Exception as e:
        result['status'] = 'Erro Inesperado'
        result['error_message'] = f"Ocorreu um erro inesperado ao processar '{input_filepath}': {e}"
        print(f"   {result['error_message']}")
    
    return result

# --- Início do Script Principal ---

if not os.path.isdir(INPUT_FOLDER):
    print(f"Erro: Pasta de entrada '{INPUT_FOLDER}' não encontrada.")
    print("Por favor, crie a pasta e coloque seus arquivos .txt de entrada nela.")
    exit()

input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.txt')]

if not input_files:
    print(f"Nenhum arquivo '.txt' com instância par encontrado na pasta '{INPUT_FOLDER}'.")
    print("Por favor, adicione arquivos .txt na pasta 'input_files'.")
    exit()

print(f"Encontrados {len(input_files)} arquivos de entrada (instâncias pares) em '{INPUT_FOLDER}'. Iniciando processamento...")
print("-" * 30)

success_count = 0
error_count = 0 # Inclui 'Incorreta' e 'Falha'

for input_filename in input_files:
    input_filepath = os.path.join(INPUT_FOLDER, input_filename)
    current_result = run_cpp_with_file_input(input_filepath, CPP_EXECUTABLE)
    all_instance_results.append(current_result)

    if current_result['status'] == 'Correta':
        success_count += 1
    else:
        error_count += 1
        incorrect_instances_list.append(current_result['instance_name'])
        
    print("-" * 10)

print("-" * 30)
print("Processamento Concluído.")
print(f"Total de arquivos processados: {len(input_files)}")
print(f"   Sucessos: {success_count}")
print(f"   Falhas:   {error_count}")

# --- Geração do Relatório Detalhado ---
with open(report_filepath, 'w', encoding='utf-8') as f_out:
    f_out.write("--- Relatório de Validação de Instâncias ---\n")
    f_out.write(f"Data e Hora do Relatório: {os.path.getmtime(report_filepath)}\n")
    f_out.write(f"Total de instâncias processadas: {len(input_files)}\n")
    f_out.write(f"   Instâncias VÁLIDAS: {success_count}\n")
    f_out.write(f"   Instâncias INVÁLIDAS/FALHAS: {error_count}\n")
    f_out.write("\n")
    f_out.write("--- Detalhes por Instância ---\n\n")

    for result in all_instance_results:
        f_out.write("=" * 40 + "\n")
        f_out.write(f"Instância: {result['instance_name']}\n")
        f_out.write(f"Status: {result['status']}\n")
        
        if result['returncode'] is not None:
            f_out.write(f"Código de Retorno: {result['returncode']}\n")

        if result['error_message']:
            f_out.write(f"Mensagem de Erro do Script: {result['error_message']}\n")

        if result['stdout']:
            f_out.write("\n--- Saída Padrão do Executável ---\n")
            f_out.write(result['stdout'])
            if not result['stdout'].endswith('\n'): # Garante uma nova linha após a saída
                f_out.write('\n')
        
        if result['stderr']:
            f_out.write("\n--- Erro Padrão do Executável ---\n")
            f_out.write(result['stderr'])
            if not result['stderr'].endswith('\n'): # Garante uma nova linha após o erro
                f_out.write('\n')
        f_out.write("\n") # Espaço entre as entradas

    if incorrect_instances_list:
        f_out.write("--- Resumo de Instâncias INVÁLIDAS/COM FALHAS ---\n")
        for instance_name in incorrect_instances_list:
            f_out.write(f"- {instance_name}\n")
    else:
        f_out.write("Todas as instâncias processadas são VÁLIDAS!\n")
    f_out.write("----------------------------------------------\n")

print(f"\nRelatório de validação salvo em: '{report_filepath}'")
