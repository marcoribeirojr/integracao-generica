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
        
if __name__ == '__main__':
    main()