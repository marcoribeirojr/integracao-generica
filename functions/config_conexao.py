import os

def is_string(parametro = 1):
    """
        Verifica se o valor passado como parâmetro é uma string
    """
    if isinstance(parametro, str):
        return True
    
    return False

def is_number(parametro = 'a'):
    """
        Verifica se o valor passado como parâmetro é um inteiro
    """
    if isinstance(parametro, int):
        return True
    
    return False

def valida_dados_acesso_sgbd(**kwargs):
    """
        Valida dados de acesso ao SGBD
        Parâmetros:
            - sgdb : <class 'str'>
            - host : <class 'str'>
            - porta : <class 'int'>
            - banco : <class 'str'>
            - usuario : <class 'str'>
            - senha : <class 'str'>
    """
    argumentos = [
        'sgbd',
        'host',
        'porta',
        'banco',
        'usuario',
        'senha'
    ]
    valido = True
    for argumento in argumentos:
        if argumento not in kwargs:
            valido = False
            break
        
        if argumento == 'porta':
            valido = is_number(kwargs[argumento])   
        else:                   
            valido = is_string(kwargs[argumento])
        
        if not valido:
            break
        
            
    return valido
    

def cria_arquivo_configuracao(**kwargs):
    """
        Cria arquivo de configuração de acesso ao banco de dados
        Parâmetros:
            - arquivo : <class 'str'> Local e nome do arquivo
            - sgdb : <class 'str'>
            - host : <class 'str'>
            - porta : <class 'int'>
            - banco : <class 'str'>
            - usuario : <class 'str'>
            - senha : <class 'str'>
    """
    path = os.getcwd()
    arquivo = '.env'
    nome_arquivo = os.path.join(path, arquivo)
    
    for chave, valor in kwargs.items():
        texto = f'{chave}={valor}'
        with open(nome_arquivo, 'a') as f:
            f.writelines(f'{texto}\n')
                
    return nome_arquivo
        
            
    

