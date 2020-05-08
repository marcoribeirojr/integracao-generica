import os
from functions.validacoes_sql import *

def test_retorna_true_se_pasta_existir():
    local = os.getcwd()
    path = f'{local}/testando'
    os.mkdir(path)
    retorno = pasta_existe(path)
    os.rmdir(path)
    assert retorno == True

def test_retorna_false_se_pasta_nao_existir():
    local = os.getcwd()
    path = f'{local}/testando'
    retorno = pasta_existe(path)
    assert retorno == False
    
def test_retorna_true_para_pasta_vazia():
    local = os.getcwd()
    path = f'{local}/testando'
    os.mkdir(path)
    retorno = pasta_vazia(path)
    os.rmdir(path)
    assert retorno != False

def test_retorna_false_pasta_nao_vazia():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste.txt'
    os.mkdir(path)
    with open(nome_arquivo, 'w') as f:
        f.write('testando')
    retorno = pasta_vazia(path)
    os.remove(nome_arquivo)
    os.rmdir(path)
    assert retorno != True
    
def test_retorna_true_se_existe_somente_arquivo_sql():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste'
    if not os.path.exists(path):
        os.mkdir(path)
    tipos = ['.sql']
    for extensao in tipos: 
        with open(f'nome_arquivo{extensao}', 'w') as f:
            f.write('testando')
    retorno = verifica_arquivos_sql(path)
    for extensao in tipos:
        os.remove(f'nome_arquivo{extensao}')
    os.rmdir(path)
    assert retorno == True

def test_retorna_false_se_nao_existe_somente_arquivo_sql():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste'
    if not os.path.exists(path):
        os.mkdir(path)
    tipos = ['sql', 'txt']
    for extensao in tipos: 
        with open(f'{nome_arquivo}.{extensao}', 'w') as f:
            f.write('testando')
    retorno = verifica_arquivos_sql(path)
    for extensao in tipos:
        os.remove(f'{nome_arquivo}.{extensao}')
    os.rmdir(path)
    assert retorno != True

def test_retorna_false_caso_nao_haja_select_e_from():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste.sql'
    if not os.path.exists(path):
        os.mkdir(path)
    texto = 'select nome, tipo, erro tabela'
    with open(nome_arquivo, 'w') as f:
        f.write(texto)
    retorno = valida_clausulas(path)
    os.remove(nome_arquivo)
    os.rmdir(path)
    assert retorno['ok'] != True

def test_retorna_true_caso_haja_select_e_from():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste.sql'
    if not os.path.exists(path):
        os.mkdir(path)
    texto = 'select nome, tipo, from tabela'
    with open(nome_arquivo, 'w') as f:
        f.write(texto)
    retorno = valida_clausulas(path)
    os.remove(nome_arquivo)
    os.rmdir(path)
    assert retorno['ok'] == True

def test_retorna_false_caso_haja_asteristico_from():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste.sql'
    if not os.path.exists(path):
        os.mkdir(path)
    texto = 'select * from tabela'
    with open(nome_arquivo, 'w') as f:
        f.write(texto)
    retorno = valida_clausulas(path)
    os.remove(nome_arquivo)
    os.rmdir(path)
    assert retorno['ok'] != True
