import os
from functions.metadados import *

def test_retorna_metadados_de_um_modelo():
    modelo = {
        'nome': 'Fulano de Tal',
        'idade': 37,
        'preco': 5.60,
        'verdadeiro': True
    }
    retorno = gera_metadados(modelo)
    metadado = {
        'nome': 'str',
        'idade': 'int',
        'preco': 'float',
        'verdadeiro': 'bool'
    }
    assert retorno == metadado