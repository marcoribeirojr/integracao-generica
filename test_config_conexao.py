import os

from functions.config_conexao import *

def test_is_string_deve_retornar_true_para_string():
    texto = 'texto de teste'
    retorno = is_string(texto)
    assert retorno == True   

def test_is_string_deve_retornar_false_para_nao_string():
    parametro = 1
    retorno = is_string(parametro)
    assert retorno != True  

def test_is_number_deve_retornar_true_para_integer():
    parametro = 1
    retorno = is_number(parametro)
    assert retorno == True

def test_is_number_deve_retornar_false_para_nao_integer():
    parametro = 0.3
    retorno = is_number(parametro)
    assert retorno != True
    
def test_retorna_true_para_configuracao_valida():
    retorno = valida_dados_acesso_sgbd(
        sgbd =  'string',
        host =  'string',
        porta =  1,
        banco =  'string',
        usuario =  'string',
        senha =  'string'
    )
    assert retorno == True

def test_retorna_false_para_configuracao_nao_valida():
    retorno = valida_dados_acesso_sgbd(
        sgbd =  'string',
        host =  'string',
        porta =  1.2,
        banco =  'string',
        usuario =  'string',
        senha =  'string'
    )
    assert retorno != True

def test_deve_criar_dot_env_correto():
    path = os.getcwd()
    arquivo = '.env'
    nome_arquivo = os.path.join(path, arquivo)
    retorno = cria_arquivo_configuracao(
        sgbd =  'string',
        host =  'string',
        porta =  1,
        banco =  'string',
        usuario =  'string',
        senha =  'string'
    )
    dados = [
        'sgbd=string',
        'host=string',
        'porta=1',
        'banco=string',
        'usuario=string',
        'senha=string'
    ]
    valido = True
    with open(nome_arquivo, 'r') as f:
        for linha in f.readlines():
            temp = linha.replace('\n', '')
            if temp not in dados:
                valido = False
    os.remove(nome_arquivo)
    assert valido == True and retorno == nome_arquivo
    