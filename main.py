import os
import sys
import json
import importlib
from functions.validacoes_sql import *
from functions.config_conexao import *
from functions.modelos import *


def main():
    """
        Função de geração de modelos, metadados, execução
        de consulta sql baseada em arquivos fornecidos e
        geração em um arquivo com os dados da integração.
    """
    pasta_raiz = os.getcwd() 
    
    # Limpeza de dados
    pastas_gerenciamento = [
        'output',
        'modelos',
    ]
    for pasta in pastas_gerenciamento:
        endereco = os.path.join(pasta_raiz, pasta)
        if os.path.exists(endereco):
            r = apaga_pastas(endereco)    
            os.removedirs(endereco)        
        os.mkdir(endereco)      
        
    arquivos_gerenciamento = [
        '.env'
    ]
    for arq in arquivos_gerenciamento:
        if arq in os.listdir(pasta_raiz):
            os.remove(os.path.join(pasta_raiz, arq))
            
    # Validação da pasta com as consultas
    
    print('Validando pastas...')
    
    pasta_saida = 'output'
    addr_pasta_saida = os.path.join(pasta_raiz, pasta_saida)
    
    addr_pasta_sql = ''
    
    valida_pasta_sql = False
    while not valida_pasta_sql:
        addr_pasta_sql = input("""
                        Informe o endereço da pasta com os arquivos .sql
                        """)
        
        valida_pasta_sql = pasta_existe(addr_pasta_sql)
        if not valida_pasta_sql:
            print('Pasta inválida. Vamos começar novamente.')
                
    pasta_esta_vazia = pasta_vazia(addr_pasta_sql)
    if pasta_esta_vazia:
        print('A pasta está vazia. Coloque os arquivos na pasta.')
        sys.exit()
        
    # Validação dos arquivos com as queries
    print('Validando arquivos com as queries...')
    
    verifica_arquivos = verifica_arquivos_sql(addr_pasta_sql)
    if not verifica_arquivos:
        print('É preciso que hajam somente arquivos com extensão .sql na pasta')
        sys.exit()
        
    clausulas_validadas = valida_clausulas(addr_pasta_sql)
    if not clausulas_validadas['ok']:
        print('Erro nas clausulas da consulta. Verifique os arquivos:')
        print(' '.join(clausulas_validadas['arquivos']))
        sys.exit()
    
    # Gera modelos de dados
    print('Gerando arquivos com modelos de dados...')
    
    pasta_modelos = 'modelos'
    addr_modelos = os.path.join(pasta_raiz, pasta_modelos)
    if not os.path.exists(addr_modelos):
        os.mkdir(addr_modelos)
    
    arquivos = os.listdir(addr_pasta_sql)
    for arquivo in arquivos:
        path_sql = os.path.join(addr_pasta_sql, arquivo)
        nome_modelo = arquivo[:-4]
        modelo = gera_modelos(path_sql)
        with open(f'{os.path.join(addr_modelos, nome_modelo)}.json', 'w') as f:
            json.dump(modelo, f)
        print(f'Modelo {nome_modelo} gerado.')
    
    # gera arquivos de configuração de acesso ao banco de dados
    sgdb = ''
    host = ''
    porta = ''
    banco = ''
    usuario = ''
    senha = ''
    
    dados_validos = False
    while not dados_validos:
        sgbds = {
            '1' : 'mysql',
            '2' : 'postgres',
            '3' : 'sqlserver'
        }
        valor_sgbd = input("""
                    Digite o número de acordo com o tipo do SGBD:
                    1 - MySQL
                    2 - Postgres                    
                    """)
        
        if int(valor_sgbd) in [1,2]:            
            sgbd = sgbds[valor_sgbd]
            dados_validos = True
            print(f'Banco selecionado: {sgbd.upper()}')
            
    dados_validos = False
    while not dados_validos:        
        host = input('Digite o host do banco: ')
        
        porta = input('Digite a porta de acesso: ')
        erro = False
        try:
            porta = int(porta)
        except:
            print("""
                Porta corresponde a um número inteiro.
                Vamos começar novamente.
                """)
            erro = True
        if erro: 
            continue
        banco = input('Digite o nome do banco: ')
        usuario = input('Digite o usuário de acesso: ')
        senha = input('Digite a senha de acesso ao banco: ')

        dados_validos = valida_dados_acesso_sgbd(
            sgbd=sgbd,
            host=host,
            porta=porta,
            banco=banco,
            usuario=usuario,
            senha=senha
        )
        
        if not dados_validos:
            print("""
                  
                  Dados inválidos, revise as informações.
                  
                  """)
    nome_arquivo = cria_arquivo_configuracao(
            sgbd=sgbd,
            host=host,
            porta=int(porta),
            banco=banco,
            usuario=usuario,
            senha=senha
        ) 
    
    print(f"""
            Arquivo criado. 
            Se quiser pode acessar o arquivo no pasta_raiz:
            {nome_arquivo}
            """)          
    
    # Executas as queries e salva em seus modelos
    db = importlib.import_module(f'bancos.{sgbd}')
    
    arquivos_modelo = os.listdir(addr_modelos)
    os.mkdir(os.path.join(addr_pasta_saida, pasta_modelos))
    
    count = 0
    for arquivo in arquivos_modelo:
        line = ''
        with open(f'{os.path.join(addr_pasta_sql, arquivo[:-5])}.sql', 'r') as f:
            line = f.read()
        line = line.replace('\n', '')
        resultado = db.consultar(line)
        
        if resultado == None:
            print(f"""
                  Houve problema na execução de uma das queries.
                  Query do arquivo {arquivo[:-5]}.sql
                  """)
            continue
        addr = os.path.join(addr_pasta_saida, arquivo)
        retorno_modelo = salva_dados_modelo(addr, resultado)
        
        if not retorno_modelo:
            print(f"""
                  Houve problema em salvar modelos.
                  Modelo: {arquivo[:-4]}
                  """)
            continue
            
        
        
    
    
if __name__ == '__main__':
    main()