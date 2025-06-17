import subprocess
import os
import sys
import csv

# Altere 'CPP_EXECUTABLE' para o caminho do seu executável C++
# Exemplo Linux/macOS: './meu_programa_exec'
# Exemplo Windows: 'meu_programa.exe' ou 'C:\caminho\para\meu_programa.exe'

CPP_EXECUTABLE = './main.exe' 

INPUT_FOLDER = 'input_files'
OUTPUT_FOLDER = 'output_files'
REPORT_FILENAME = 'relatorio.csv'

relatorio_filepath = os.path.join(os.path.dirname(__file__), REPORT_FILENAME)

with open(relatorio_filepath, 'w', encoding='utf-8', newline='') as csvfile:
    relatorio_csv_writer = csv.writer(csvfile)
    relatorio_csv_writer.writerow(['Instance_Name', 'Execution_Time', 'Initial_Solution', 'Final_Solution'])


def run_cpp_with_file_input(input_filepath, output_filepath, cpp_executable_path):
    print(f"Processando '{os.path.basename(input_filepath)}' -> '{os.path.basename(output_filepath)}'")

    try:
        if not os.path.exists(cpp_executable_path):
            if sys.platform == "win32" and not cpp_executable_path.endswith('.exe'):
                if os.path.exists(cpp_executable_path + '.exe'):
                    cpp_executable_path += '.exe'
                else:
                    print(f"  Erro: Executável C++ '{cpp_executable_path}' (ou .exe) não encontrado.")
                    return False, None
            else:
                print(f"  Erro: Executável C++ '{cpp_executable_path}' não encontrado.")
                return False, None

        # Lê o conteúdo do arquivo de entrada
        with open(input_filepath, 'r', encoding='utf-8') as f_in:
            input_data = f_in.read()
        
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
            print(f"  Sucesso: Saída salva em '{os.path.basename(output_filepath)}'")
            return True, stdout
        else:
            print(f"  Erro ao executar com entrada de '{os.path.basename(input_filepath)}':")
            print(f"    Código de Retorno: {process.returncode}")
            print(f"    Mensagem de Erro (stderr): {stderr.strip()}")
            return False, stderr
            

    except FileNotFoundError:
        print(f"  Erro: Arquivo de entrada '{input_filepath}' não encontrado.")
        return False, None
    except Exception as e:
        print(f"  Ocorreu um erro inesperado ao processar '{input_filepath}': {e}")
        return False, None

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.isdir(INPUT_FOLDER):
    print(f"Erro: Pasta de entrada '{INPUT_FOLDER}' não encontrada.")
    print("Por favor, crie a pasta e coloque seus arquivos .txt de entrada nela.")
    exit()

try:
    input_files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith('.txt')])
except Exception as e:
    print(f"Erro ao listar arquivos na pasta '{INPUT_FOLDER}': {e}")
    exit()

if not input_files:
    print(f"Nenhum arquivo '.txt' encontrado na pasta '{INPUT_FOLDER}'.")
    exit()

print(f"Encontrados {len(input_files)} arquivos de entrada em '{INPUT_FOLDER}'. Iniciando processamento...")
print("-" * 30)

total_success_runs = 0
total_error_runs = 0
runs_per_file = 10

for input_filename in input_files:
    input_filepath = os.path.join(INPUT_FOLDER, input_filename)
    base_filename_no_ext = os.path.splitext(input_filename)[0]

    print(f"\n--- Processando instâncias de '{input_filename}' ({runs_per_file} vezes) ---")

    for i in range(runs_per_file):
        run_number = i + 1
        output_filename = f"saida_{base_filename_no_ext}_{run_number}.txt"
        output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)

        success, cpp_output = run_cpp_with_file_input(input_filepath, output_filepath, CPP_EXECUTABLE)
        
        execution_time = "N/A"
        initial_solution = "N/A"
        final_solution = "N/A"

        if success:
            total_success_runs += 1
            lines = cpp_output.strip().splitlines()

            if len(lines) >= 3:
                execution_time = lines[0].strip()
                initial_solution = lines[1].strip()
                final_solution = lines[2].strip()
            else:
                print(f"  Aviso: Saída do arquivo '{output_filename}' não contém as 3 linhas esperadas para o relatório. Saída completa: '{cpp_output.strip()}'")

            with open(relatorio_filepath, 'a', encoding='utf-8', newline='') as csvfile:
                relatorio_csv_writer = csv.writer(csvfile)
                relatorio_csv_writer.writerow([
                    f"{base_filename_no_ext}_{run_number}.txt",
                    execution_time, 
                    initial_solution, 
                    final_solution
                ])
        else:
            total_error_runs += 1
            error_details = cpp_output if cpp_output else "No output/error details"
            raw_output_preview = error_details[:200].replace('\n', '\\n') + ('...' if len(error_details) > 200 else '')

            with open(relatorio_filepath, 'a', encoding='utf-8', newline='') as csvfile:
                relatorio_csv_writer = csv.writer(csvfile)
                relatorio_csv_writer.writerow([
                    f"{base_filename_no_ext}_{run_number}.txt", 
                    "ERROR", 
                    "ERROR", 
                    "ERROR"
                ])

        print("-" * 10)

print("-" * 30)
print("Processamento Concluído.")
print(f"Total de arquivos de entrada: {len(input_files)}")
print(f"Total de execuções tentadas: {len(input_files) * runs_per_file}")
print(f"  Sucessos: {total_success_runs}")
print(f"  Falhas:   {total_error_runs}")