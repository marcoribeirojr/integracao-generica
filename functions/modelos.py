import os

def gera_modelos(nome_arquivo):
    """
        Gera modelos de acordo com sql do arquivo
    """
    linhas = ''
    with open(nome_arquivo, 'r') as f:
        linhas = f.read()
        
    linhas = linhas.replace('\n', '').lower()    
    partes = linhas.split('from')
    elementos = partes[0].split(',')
    sem_alias = list(filter(lambda x : ' as' not in x, elementos))
    com_alias_temp = list([x for x in elementos if x not in sem_alias])
    com_alias = []
    for i in com_alias_temp:
        temp = i.split(' as')
        com_alias.append(temp[-1])
    clausulas = com_alias + sem_alias
    count = 0
    for clausula in clausulas:
        if 'select ' in clausula:
            clausulas[count] = clausulas[count][6:]
        clausulas[count] = clausulas[count].strip(' ')
        count = count +1
    modelo = {}
    for clausula in clausulas:
        modelo[clausula] = ''
    
    return modelo