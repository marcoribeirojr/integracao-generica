import pymysql
from decouple import config


def consultar(query = ''):
    """
        Abre conexao com MySQL e retorna 
        o resultado da consulta
        Argumentos:
            - db

        Retorno:
            - list() - em caso de sucesso
            - None em caso de erro
    """
    try:
        conexao = None
        conexao= pymysql.connect(
            host= config('host'),
            port= config('porta'),
            user= config('usuario'),
            passwd= config('senha'),
            db= config('banco')
        )
        with conexao:
            cursor = None
            cursor = conexao.cursor()           
            try :
                cursor.execute(query)
                rows = None
                rows = cursor.fetchall()
                return rows           
            except:
                return None         
    except: 
        return None 