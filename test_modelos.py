import os
from functions.modelos import *
    
def test_confirma_modelos_por_querie():
    local = os.getcwd()
    path = f'{local}/testando'
    nome_arquivo = f'{path}/arquivo_teste.sql'
    os.mkdir(path)
    texto = 'select   nome, a   as ano, tipo from tabela where algo = 2'
    with open(nome_arquivo, 'w') as f:
        f.write(texto)
    retorno = gera_modelos(nome_arquivo)
    os.remove(nome_arquivo)
    os.rmdir(path)
    modelo = {
        'nome': '',
        'ano' : '',
        'tipo': '',
    }
    assert retorno == modelo