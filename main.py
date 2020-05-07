import os
import sys
import json
from functions.validacoes_sql import *
from functions.config_conexao import *
from functions.modelos import *

def main():
    """
        Função de geração de modelos, metadados, execução
        de consulta sql baseada em arquivos fornecidos e
        geração em um arquivo com os dados da integração.
    """
    # Validação da pasta com as consultas
    
    print('Validando pastas...')
    
    local = os.getcwd()
    pasta_sql = '/queries'
    addr_pasta_sql = f'{local}{pasta_sql}'
    
    pasta_existente = pasta_existe(addr_pasta_sql)
    if not pasta_existente:
        os.mkdir(addr_pasta_sql, 777)
        
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
    
    pasta_modelos = '/modelos'
    addr_modelos = f'{local}{pasta_modelos}'
    if not os.path.exists(addr_modelos):
        os.mkdir(addr_modelos)
    
    arquivos = os.listdir(addr_pasta_sql)
    for arquivo in arquivos:
        path_sql = f'{addr_pasta_sql}/{arquivo}'
        nome_modelo = arquivo[:-4]
        modelo = gera_modelos(path_sql)
        with open(f'{addr_modelos}/{nome_modelo}.json', 'w') as f:
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
                    3 - SQL Server                    
                    """)
        
        if int(valor_sgbd) in [1,2,3]:            
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
    
    if os.path.exists('.env'):
        os.remove('.env')
        
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
            Se quiser pode acessar o arquivo no local:
            {nome_arquivo}
            """)          
    
        
if __name__ == '__main__':
    main()