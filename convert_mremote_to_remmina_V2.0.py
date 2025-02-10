import csv
import os
import logging
import shutil
import zipfile

# Configura o logging
logging.basicConfig(filename='conversao.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def converter_mremoteng_para_remmina(arquivo_csv, pasta_destino):
    """
    Converte um arquivo CSV do mRemoteNG para arquivos Remmina, 
    tratando grupos aninhados e evitando nomes duplicados.
    """

    with open(arquivo_csv, 'r', encoding='utf-8') as arquivo:
        leitor_csv = csv.DictReader(arquivo)
        grupos = {}  # Dicionário para armazenar os grupos
        contador = 1  # Contador para evitar nomes de arquivos duplicados
        conexões = []  # Lista para armazenar as conexões

        # Primeira passagem: armazenar todos os grupos e conexões
        for linha in leitor_csv:
            if linha['NodeType'] == 'Container':
                grupos[linha['Id']] = linha['Name']
            elif linha['NodeType'] == 'Connection':
                conexões.append(linha)

        def gerar_string_grupo(grupo_id, grupos_dict):
            if grupo_id in grupos_dict:
                nome_grupo = grupos_dict[grupo_id]
                parent_id = None

                # Encontra o parent_id do grupo atual
                arquivo.seek(0)
                leitor_interno = csv.DictReader(arquivo)
                for linha_interna in leitor_interno:
                    if linha_interna['NodeType'] == 'Container' and linha_interna['Id'] == grupo_id:
                        parent_id = linha_interna['Parent']
                        break

                if parent_id:  # Se o grupo tem um pai, chama recursivamente
                    nome_grupo_pai = gerar_string_grupo(parent_id, grupos_dict)
                    if nome_grupo_pai:
                      return nome_grupo_pai + ">" + nome_grupo
                    else:
                      return nome_grupo
                else:  # Se não tem pai, é um grupo raiz
                    return nome_grupo
            else:
                return None  # Retorna None se o grupo não for encontrado

        # Loop para gerar os arquivos .remmina para cada conexão
        for linha in conexões:
            try:
                nome = linha['Name']
                protocolo = linha['Protocol']
                hostname = linha['Hostname']
                usuario = linha['Username']
                senha = linha['Password']
                porta = linha['Port']

                grupo_id = linha['Parent']
                grupo = "Default Group"

                # Encontra o grupo pai e gera a string de grupo aninhado
                grupo_encontrado = gerar_string_grupo(grupo_id, grupos)
                if grupo_encontrado:
                    grupo = grupo_encontrado

                if protocolo == 'SSH2':
                    protocolo = 'SSH'

                # Verifica se o nome já existe e adiciona um contador se necessário
                nome_arquivo = f"{nome}.remmina"
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                while os.path.exists(caminho_arquivo):
                    nome_arquivo = f"{nome}_{contador}.remmina"
                    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                    contador += 1

                conteudo_remmina = f"""
[remmina]
name={nome}
group={grupo}
protocol={protocolo}
hostname={hostname}
username={usuario}
password={senha}
port={porta}
"""

                with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo_remmina:
                    arquivo_remmina.write(conteudo_remmina)

            except KeyError as e:
                mensagem_erro = f"Erro: Chave não encontrada: {e}\nLinha problemática: {linha}"
                logging.error(mensagem_erro)  # Registra o erro no arquivo de log
                print(mensagem_erro) # Exibe o erro no console
                continue

            except Exception as e: # Captura outros erros
                mensagem_erro = f"Erro desconhecido: {e}\nLinha problemática: {linha}"
                logging.exception(mensagem_erro) # Registra o erro com stack trace
                print(mensagem_erro)
                continue

# Exemplo de uso
arquivo_csv = 'mRemoteNG.csv'  # Substitua pelo caminho do seu arquivo CSV
pasta_destino = 'remmina_connections'  # Substitua pelo caminho da pasta de destino

# Cria a pasta de destino, se não existir
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

converter_mremoteng_para_remmina(arquivo_csv, pasta_destino)

print("Conversão concluída. Verifique a pasta 'remmina_connections' e o arquivo de log 'conversao.log'.")

# Pergunta ao usuário se deseja mover os arquivos para o diretório padrão do Remmina
mover_para_remmina = input("Deseja mover os arquivos .remmina para o diretório padrão do Remmina (~/.local/share/remmina)? (s/n): ")

if mover_para_remmina.lower() == 's':
    diretorio_remmina = os.path.expanduser("~/.local/share/remmina")
    if not os.path.exists(diretorio_remmina):
        os.makedirs(diretorio_remmina)
    
    for arquivo_remmina in os.listdir(pasta_destino):
        if arquivo_remmina.endswith(".remmina"):
            caminho_arquivo_remmina = os.path.join(pasta_destino, arquivo_remmina)
            shutil.move(caminho_arquivo_remmina, diretorio_remmina)
    print("Arquivos .remmina movidos para o diretório padrão do Remmina.")
else:
    print("Arquivos .remmina não foram movidos.")

# Cria um arquivo .zip do diretório atual
nome_arquivo_zip = "remmina_connections.zip"
with zipfile.ZipFile(nome_arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as arquivo_zip:
    for arquivo in os.listdir(pasta_destino):
        caminho_arquivo = os.path.join(pasta_destino, arquivo)
        arquivo_zip.write(caminho_arquivo, arcname=arquivo)

print(f"Arquivo .zip '{nome_arquivo_zip}' criado com os arquivos .remmina.")

print("\nGemini 2.0 Flash - Uma criação colaborativa de Junovan Fantin e Gemini.")
