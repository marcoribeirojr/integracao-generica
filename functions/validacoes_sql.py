import os

def pasta_existe(path):
    """
        Verifica se uma pasta existe
    """
    if os.path.exists(path) == True:
        return True
    return False

def pasta_vazia(path):
    """
        Verifica se a pasta está vazia
    """
    arquivos = os.listdir(path)
    if len(arquivos) > 0:
        return False
    return True

def verifica_arquivos_sql(path):
    """
        Verifica se existem somente arquivos sql na pasta
    """
    arquivos = os.listdir(path)
    confirmacao = list(map(lambda x: x[-4:] == '.sql', arquivos))
    if False in confirmacao: 
        return False
    return True

def valida_clausulas(path):
    """
        Verifica se na query tem as clausulas select e where
    """ 
    arquivos = os.listdir(path)
    validacao = {
        'ok' : True,
        'arquivos' : []
    }
    
    for arquivo in arquivos:
        linhas = ''
        clausulas = ['select', 'from']     
        endereco = os.path.join(path, arquivo)
        with open(endereco, 'r') as f:
            linhas = f.read()
            
        linhas.replace('\n', '')
        
        validacoes = list(map(lambda x: x in linhas, clausulas))
        
        if (False in validacoes) or ('*' in linhas):
            validacao['ok'] = False
            validacao['arquivos'].append(arquivo)        
    
    return validacao       