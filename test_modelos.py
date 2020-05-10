import os
import json
from functions.modelos import *
    
def test_confirma_modelos_por_querie():
    local = os.getcwd()
    path = os.path.join(local, 'testando')
    nome_arquivo = os.path.join(path, 'arquivo_teste.sql')
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
    path = os.path.join(local, nome_arquivo)
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
    path = os.path.join(local, nome_arquivo)
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

def test_deve_apagar_todos_arquivos_e_retornar_true_ou_false():
    local = os.getcwd()
    nome_pasta = 'teste'
    addr_pasta = os.path.join(local, nome_pasta)
    os.mkdir(addr_pasta)
    arquivos = [
        'arq1.txt',
        'arq2.txt'
    ]
    for arquivo in arquivos:
        with open(os.path.join(addr_pasta, arquivo), 'w') as f:
            f.write('teste')
    retorno = apaga_arquivos(addr_pasta)
    total_arquivos = os.listdir(addr_pasta)
    if len(total_arquivos) > 0:
        for item in total_arquivos:
            os.remove(os.path.join(addr_pasta, item))
    os.removedirs(addr_pasta)
    assert retorno == True
    
def test_deve_apagar_pastas_e_retornar_true_ou_false():
    local = os.getcwd()
    pasta_pai = 'teste'
    pastas_filho = [
        'teste1',
        'teste2'
    ]
    local_pasta_pai = os.path.join(local, pasta_pai)
    os.mkdir(local_pasta_pai)
    with open(os.path.join(local_pasta_pai, 'testez.txt'), 'w') as f:
            f.write('teste')
    for pasta in pastas_filho:
        addr = os.path.join(local_pasta_pai, pasta)
        os.mkdir(addr)    
        with open(os.path.join(addr, 'testez.txt'), 'w') as f:
            f.write('teste')
    retorno = apaga_pastas(local_pasta_pai)    
    existe = os.path.exists(local_pasta_pai)
    assert retorno == True and existe == False    
    