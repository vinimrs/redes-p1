import re
def Message_Handler(conexao,dados):

    #switch dos tipos de dados
    if dados == b'':
        return sair(conexao)
    if dados[0:4] == 'PING':
        response = PING_handler(dados)

    elif dados[0:4] == 'NICK':
        response = NICK_handler(dados)

    elif dados[0:4] == 'JOIN':
        response = JOIN_handler(dados)

    elif dados[0:7] == 'PRIVMSG':
        response = PRIVMSG_handler(dados)
    
    elif dados[0:4] == 'PART':
        response = PART_handler(dados)

    
    
    #retorna o erro ou sucesso da dados
    return response

def NICK_handler(conexao,dados):
    
def PING_handler(conexao,dados):
    conexao.enviar(b':server PONG server :' + dados.split(b' ', 1)[1])
    print(conexao, dados)

def validar_nome(nome):
    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None

def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()