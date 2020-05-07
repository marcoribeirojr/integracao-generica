import os

def gera_modelos(nome_arquivo):
    """
        Gera modelos de acordo com sql do arquivo
    """
    linhas = ''
    with open(nome_arquivo, 'r') as f:
        linhas = f.read()
        
    linhas = linhas.replace('\n', '')
    arr = linhas.split(',')
    arr = list(map(lambda x: x.strip(' '), arr))
    modelo = {}
    for elem in arr:
        dado = elem.lower()
        if 'select' in dado:
            temp = dado.split(' ')
            temp = list(map(lambda x: x.strip(' '), temp))
            dado_final = temp[1]
            modelo[dado_final] = ''  
            continue   
           
        if 'from' in elem:
            temp = dado.split(' ')
            temp = list(map(lambda x: x.strip(' '), temp))
            dado_final = temp[0]
            modelo[dado_final] = '' 
            break
        
        modelo[dado] = ''
        
    return modelo