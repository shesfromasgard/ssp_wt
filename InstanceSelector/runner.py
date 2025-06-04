import os
import random
import shutil

def selecionar_e_copiar_arquivos(pasta_origem, pasta_destino, porcentagem_selecao=0.10):
    """
    Seleciona uma porcentagem de arquivos .txt de uma pasta e os copia para outra.

    Args:
        pasta_origem (str): O caminho para a pasta onde os arquivos .txt estão localizados.
        pasta_destino (str): O caminho para a pasta onde os arquivos selecionados serão copiados.
        porcentagem_selecao (float): A porcentagem de arquivos a serem selecionados (e.g., 0.10 para 10%).
    """

    # 1. Listar todos os arquivos .txt
    arquivos_txt = []
    try:
        for nome_arquivo in os.listdir(pasta_origem):
            if nome_arquivo.endswith('.txt') and os.path.isfile(os.path.join(pasta_origem, nome_arquivo)):
                arquivos_txt.append(nome_arquivo)
    except FileNotFoundError:
        print(f"Erro: A pasta de origem '{pasta_origem}' não foi encontrada.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao listar arquivos na pasta de origem: {e}")
        return

    if not arquivos_txt:
        print(f"Nenhum arquivo .txt encontrado na pasta '{pasta_origem}'.")
        return

    total_arquivos = len(arquivos_txt)
    print(f"Total de arquivos .txt encontrados: {total_arquivos}")

    # 2. Calcular 10% do número de arquivos
    num_a_selecionar = int(total_arquivos * porcentagem_selecao)
    if num_a_selecionar == 0 and total_arquivos > 0:
        # Garante que pelo menos 1 arquivo seja selecionado se houver arquivos,
        # a menos que a porcentagem seja muito baixa.
        num_a_selecionar = 1 
    elif total_arquivos == 0:
        num_a_selecionar = 0

    print(f"Serão selecionados {num_a_selecionar} arquivos ({porcentagem_selecao*100:.0f}% do total).")

    if num_a_selecionar == 0:
        print("Nenhum arquivo para selecionar.")
        return

    # 3. Selecionar uniformemente os arquivos
    arquivos_selecionados = random.sample(arquivos_txt, num_a_selecionar)
    print(f"Arquivos selecionados: {arquivos_selecionados}")

    # 4. Criar a pasta de destino (se não existir)
    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta de destino '{pasta_destino}' criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar a pasta de destino '{pasta_destino}': {e}")
            return
    else:
        print(f"Pasta de destino '{pasta_destino}' já existe.")

    # 5. Copiar os arquivos
    print("Copiando arquivos...")
    for arquivo in arquivos_selecionados:
        origem_completa = os.path.join(pasta_origem, arquivo)
        destino_completo = os.path.join(pasta_destino, arquivo)
        try:
            shutil.copy2(origem_completa, destino_completo)
            print(f"Copiado: '{arquivo}' para '{pasta_destino}'")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{origem_completa}' não encontrado durante a cópia.")
        except Exception as e:
            print(f"Erro ao copiar '{arquivo}': {e}")

    print("Processo de cópia concluído.")

if __name__ == "__main__":
    # Defina as pastas de origem e destino
    PASTA_DE_ORIGEM = 'input_files'  # Substitua pelo caminho da sua pasta de entrada
    PASTA_DE_DESTINO = 'selected_files' # Nova pasta para os arquivos selecionados

    # Crie alguns arquivos de teste na pasta de origem para testar o script
    if not os.path.exists(PASTA_DE_ORIGEM):
        os.makedirs(PASTA_DE_ORIGEM)
        print(f"Pasta '{PASTA_DE_ORIGEM}' criada para teste.")
        for i in range(25): # Criar 25 arquivos de teste
            with open(os.path.join(PASTA_DE_ORIGEM, f'arquivo_teste_{i:02d}.txt'), 'w') as f:
                f.write(f"Conteúdo do arquivo {i}")
        print(f"25 arquivos de teste .txt criados em '{PASTA_DE_ORIGEM}'.")
        print("-" * 30)

    selecionar_e_copiar_arquivos(PASTA_DE_ORIGEM, PASTA_DE_DESTINO, porcentagem_selecao=0.10)