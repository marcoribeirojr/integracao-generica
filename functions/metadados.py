import os

def gera_metadados(modelo):
    """
        Gera metadados de acordo com um dicionario fornecido
    """
    chaves = list(modelo.keys())
    metadado = {}
    for chave in chaves:
        string = str(type(modelo[chave]))
        string = string[8:-2]
        metadado[chave] = string
    
    return metadado
    