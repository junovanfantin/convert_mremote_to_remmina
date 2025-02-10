# Conversor mRemoteNG para Remmina

Este script em Python converte um backup `.csv` do programa **mRemoteNG** para arquivos de conexão `.remmina`, permitindo sua importação no **Remmina**, um popular cliente de acesso remoto.

## 📌 Funcionalidades
- Converte conexões armazenadas no backup do **mRemoteNG** em arquivos `.remmina`.
- Mantém a estrutura de grupos e subgrupos.
- Evita nomes duplicados para conexões.
- Permite mover automaticamente os arquivos `.remmina` para o diretório padrão do Remmina (`~/.local/share/remmina`).
- Gera um arquivo `.zip` com todas as conexões convertidas.
- Registra erros no log `conversao.log`.

## 🔧 Requisitos
- Python 3.x

## 🚀 Como Usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/junovanfantin/convert_mremote_to_remmina.git
   cd mremoteng-to-remmina
   ```

2. **Coloque o arquivo de backup do mRemoteNG (.csv) no diretório do script.**

3. **Execute o script:**
   ```bash
   python convert_mremote_to_remmina_V2.0.py
   ```

4. **Escolha se deseja mover os arquivos convertidos para o diretório do Remmina.**

5. **Um arquivo `.zip` com as conexões será gerado automaticamente.**

## 📁 Estrutura dos Arquivos Gerados
Os arquivos `.remmina` são salvos na pasta `remmina_connections/` e podem ser movidos para:
```
~/.local/share/remmina/
```

## 📝 Exemplo de Arquivo `.remmina` Gerado
```ini
[remmina]
name=Minha Conexão
protocol=SSH
hostname=192.168.1.100
username=meu_usuario
password=minha_senha
port=22
group=MeuGrupo
```

## 🛠 Possíveis Erros e Soluções
- **Chave não encontrada no CSV:** Verifique se o arquivo de backup contém todas as colunas esperadas.
- **Falha na conversão:** Certifique-se de que o arquivo CSV está salvo no formato correto (`utf-8`).
- **Erro ao mover arquivos:** Verifique se o diretório `~/.local/share/remmina` existe e tem permissões de escrita.

## 📜 Licença
Este projeto é distribuído sob a licença MIT.

## 👨‍💻 Autor
Criado por **Junovan Fantin** e aprimorado por **Gemini 2.0 Flash**.

