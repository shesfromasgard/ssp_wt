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

incorrect_instances_list = []

def run_cpp_with_file_input(input_filepath, cpp_executable_path):
    print(f"Processando '{os.path.basename(input_filepath)}'")

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
            print(f"Instância '{os.path.basename(input_filepath)}' correta.")
            return True
        else:

            incorrect_instances_list.append(os.path.basename(input_filepath))
            print(f"Instância '{os.path.basename(input_filepath)}' **INCORRETA** (código de retorno: {process.returncode}).")

            if stderr:
                print(f"   Stderr: {stderr.strip()}")
            return False

    except FileNotFoundError:
        print(f"   Erro: Arquivo de entrada '{input_filepath}' não encontrado.")
        return False
    except Exception as e:
        print(f"   Ocorreu um erro inesperado ao processar '{input_filepath}': {e}")
        return False

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
report_filepath = os.path.join(OUTPUT_FOLDER, "relatorio_instancias.txt")

if not os.path.isdir(INPUT_FOLDER):
    print(f"Erro: Pasta de entrada '{INPUT_FOLDER}' não encontrada.")
    print("Por favor, crie a pasta e coloque seus arquivos .txt de entrada nela.")
    exit()


input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.txt')]


if not input_files:
    print(f"Nenhum arquivo '.txt' com instância par encontrado na pasta '{INPUT_FOLDER}'.")
    exit()

print(f"Encontrados {len(input_files)} arquivos de entrada (instâncias pares) em '{INPUT_FOLDER}'. Iniciando processamento...")
print("-" * 30)

success_count = 0
error_count = 0

for input_filename in input_files:
    input_filepath = os.path.join(INPUT_FOLDER, input_filename)

    if run_cpp_with_file_input(input_filepath, CPP_EXECUTABLE):
        success_count += 1
    else:
        error_count += 1
        
    print("-" * 10)

print("-" * 30)
print("Processamento Concluído.")
print(f"Total de arquivos processados: {len(input_files)}")
print(f"   Sucessos: {success_count}")
print(f"   Falhas:   {error_count}")

with open(report_filepath, 'w', encoding='utf-8') as f_out:
    f_out.write("--- Relatório de Validação de Instâncias ---\n")
    f_out.write(f"Total de instâncias processadas: {len(input_files)}\n")
    f_out.write(f"   Instâncias VÁLIDAS: {success_count}\n")
    f_out.write(f"   Instâncias INVÁLIDAS: {error_count}\n")
    f_out.write("\n")
    
    if incorrect_instances_list:
        f_out.write("--- Instâncias INVÁLIDAS ---\n")
        for instance_name in incorrect_instances_list:
            f_out.write(f"- {instance_name}\n")
    else:
        f_out.write("Todas as instâncias processadas são VÁLIDAS!\n")
    f_out.write("----------------------------------------------\n")

print(f"\nRelatório de validação salvo em: '{report_filepath}'")
