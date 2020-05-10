import os
import json

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

def retorna_modelo(path):
    """
        Lê arquivo json com o modelo e retorna o mesmo
    """
    modelo = ''
    with open(path, 'r') as f:
        modelo = json.load(f)
        
    return modelo

def salva_dados_modelo(path, dados):
    """
        Salva no arquivo os dados recuperados do banco de dados
        Parâmetros:
            path : local e nome do arquivo de modelos 
                    a ser salvo
            dados : dados a serem salvos no arquivo
        Retorno:
            - True : Sucesso em salvar os dados
            - False : Não foram salvos os dados
    """
    try: 
        with open(path, 'w') as f:
            json.dump(dados, f)
    except: 
        return False        
    
    return True

def apaga_arquivos(path):
    lista = os.listdir(path)
    for item in lista:
        try: 
            endereco = os.path.join(path, item)
            if os.path.isfile(endereco):
                os.remove(endereco)
        except:
            return False
    return True

def apaga_pastas(path):
    r = apaga_arquivos(path)
    lista = os.listdir(path)
    for item in lista:
        try: 
            endereco = os.path.join(path, item)
            r = apaga_arquivos(endereco)
            if os.path.isdir(endereco):
                os.removedirs(endereco)                
        except:
            return False
    return True