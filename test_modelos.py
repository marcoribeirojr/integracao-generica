import os
import json
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
    
def test_deve_retornar_modelo_de_acordo_com_nome_passado():
    local = os.getcwd()
    nome_arquivo = 'teste.json'
    path = f'{local}/{nome_arquivo}'
    modelo_teste = {
        'nome' : '',
        'addr' : ''
    }
    with open(path, 'w') as f:
        json.dump(modelo_teste, f)
        
    retorno = retorna_modelo(path)
    os.remove(path)
    assert retorno == modelo_teste

def test_deve_salvar_dados_no_modelo():
    local = os.getcwd()
    nome_arquivo = 'modelo_teste.json'
    path = f'{local}/{nome_arquivo}'    
    teste = [
        {
            'nome' : 'teste',
            'nota' : 0
        },
        {
            'nome' : 'teste2',
            'nota' : 2
        }        
    ]
    retorno = salva_dados_modelo(path, teste)
    retorno_chamada = ''
    with open(path, 'r') as f:
        retorno_chamada = json.load(f)
    os.remove(path)
    assert retorno_chamada == teste
    