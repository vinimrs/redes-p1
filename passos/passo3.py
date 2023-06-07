"""
Trate mensagens do tipo NICK.
Verifique se o apelido solicitado é válido usando a função validar_nome.
Se for inválido, responda com a mensagem de erro 432 (como descrita na seção Mensagens do protocolo).
Senão, responda com as mensagens 001 e 422, para indicar sucesso.
"""
import re

def NICK_handler(nome):
    #resposta de sucesso
    nick_response = '001'

    #nome tem caractere invalido
    if not validar_nome(nome):
        nick_response = '432' #erro nick invalido

    #nome ja existe
    

def validar_nome(nome):
    #nome tem caractere invalido

    #nome ja existe

    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None