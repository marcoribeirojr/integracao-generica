import psycopg2
from decouple import config

def consultar(query = ''):
    """
        Abre uma conexão com o banco e retorna um conjunto de dados 
        de acordo com a consulta
        Argumentos:
            - query
        Retorno:
            - list() - em caso de sucesso
            - None em caso de erro
    """

    host = config('host')
    user = config('usuario')
    password = config('senha')
    database = config('banco')
    port = config('porta')        
    
    try:
        conexao = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        with conexao:
            cursor = conexao.cursor()           
            try :
                cursor.execute(query)
                dados = cursor.fetchall()
                return dados           
            except:
                return None         
    except: 
        return None 