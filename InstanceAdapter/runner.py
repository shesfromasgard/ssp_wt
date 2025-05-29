import subprocess
import os
import sys
import re

# Altere 'CPP_EXECUTABLE' para o caminho do seu executável C++
# Exemplo Linux/macOS: './meu_programa_exec'
# Exemplo Windows: 'meu_programa.exe' ou r'C:\caminho\para\meu_programa.exe'

CPP_EXECUTABLE = './main.exe' 

INPUT_FOLDER = 'input_files'
OUTPUT_FOLDER = 'output_files'

def run_cpp_with_file_input(input_filepath, output_filepath, cpp_executable_path):
    print(f"Processando '{os.path.basename(input_filepath)}' -> '{os.path.basename(output_filepath)}'")

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f_in:
            input_data = f_in.read()

        if not os.path.exists(cpp_executable_path):
            if sys.platform == "win32" and not cpp_executable_path.endswith('.exe'):
                if os.path.exists(cpp_executable_path + '.exe'):
                    cpp_executable_path += '.exe'
                else:
                    print(f"   Erro: Executável C++ '{cpp_executable_path}' (ou .exe) não encontrado.")
                    return False
            else:
                print(f"   Erro: Executável C++ '{cpp_executable_path}' não encontrado.")
                return False

        process = subprocess.Popen(
            [cpp_executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        stdout, stderr = process.communicate(input=input_data)

        if process.returncode == 0:
            with open(output_filepath, 'w', encoding='utf-8') as f_out:
                f_out.write(stdout)
            print(f"   Sucesso: Saída salva em '{os.path.basename(output_filepath)}'")
            return True
        else:
            print(f"   Erro ao executar com entrada de '{os.path.basename(input_filepath)}':")
            print(f"      Código de Retorno: {process.returncode}")
            print(f"      Mensagem de Erro (stderr): {stderr.strip()}")
            return False

    except FileNotFoundError:
        print(f"   Erro: Arquivo de entrada '{input_filepath}' não encontrado.")
        return False
    except Exception as e:
        print(f"   Ocorreu um erro inesperado ao processar '{input_filepath}': {e}")
        return False

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.isdir(INPUT_FOLDER):
    print(f"Erro: Pasta de entrada '{INPUT_FOLDER}' não encontrada.")
    print("Por favor, crie a pasta e coloque seus arquivos .PMTC de entrada nela.")
    exit()

try:
    all_input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.PMTC')]
except Exception as e:
    print(f"Erro ao listar arquivos na pasta '{INPUT_FOLDER}': {e}")
    exit()


def get_instance_number(filename):
    match = re.search(r'instanceLarge(\d+)_', filename)
    if match:
        return int(match.group(1))
    return None

filtered_input_files = []
for filename in all_input_files:
    instance_num = get_instance_number(filename)
    if instance_num is not None and instance_num % 2 == 0:
        filtered_input_files.append(filename)
    else:
        print(f"Ignorando '{filename}': Não é uma instância par ou não segue o padrão 'instanceLargeX_'.")

input_files = filtered_input_files
if not input_files:
    print(f"Nenhum arquivo '.PMTC' com instância par encontrado na pasta '{INPUT_FOLDER}'.")
    exit()

print(f"Encontrados {len(input_files)} arquivos de entrada (instâncias pares) em '{INPUT_FOLDER}'. Iniciando processamento...")
print("-" * 30)

success_count = 0
error_count = 0

for input_filename in input_files:
    input_filepath = os.path.join(INPUT_FOLDER, input_filename)

    output_filename = "adapted_" + input_filename.replace("entrada_", "").replace("input_", "").replace(".PMTC", ".txt")
    if not output_filename.startswith("adapted_"):
        output_filename = "adapted_" + input_filename.replace(".PMTC", ".txt")
    output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)

    if run_cpp_with_file_input(input_filepath, output_filepath, CPP_EXECUTABLE):
        success_count += 1
    else:
        error_count += 1

    print("-" * 10)

print("-" * 30)
print("Processamento Concluído.")
print(f"Total de arquivos processados: {len(input_files)}")
print(f"   Sucessos: {success_count}")
print(f"   Falhas:   {error_count}")
