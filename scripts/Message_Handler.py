import re
import tcp
_nick_dict = {}

def Message_Handler(conexao,dados):
    #tirar espacos no comeco e no fim da msg
    dados = dados.strip()

    #switch dos tipos de dados
    if dados == b'':
        return sair(conexao)
    
    if dados[0:4].upper() == b'PING':
        alvo, response = PING_handler(conexao, dados)

    elif dados[0:4].upper() == b'NICK':
        alvo, response = NICK_handler(conexao, dados)

    elif dados[0:4].upper() == b'JOIN':
        alvo, response = JOIN_handler(conexao, dados)

    elif dados[0:7].upper() == b'PRIVMSG':
        alvo, response = PRIVMSG_handler(conexao, dados)
    
    elif dados[0:4].upper() == 'PART':
        alvo, response = PART_handler(conexao, dados)

    #retorna o erro ou sucesso da dados
    return alvo, response

def PING_handler(conexao,dados):
    return conexao, b':server PONG server :' + dados.split(b' ', 1)[1] + b'\r\n'
    #print('respondendo PING com PONG')
    #print(conexao, dados)

def NICK_handler(conexao,dados):
    #separar comando de conteudo e tirar espacos da mensagem
    comando, apelido = dados.split(b' ',1)

    #vejo se essa conexao ja tem nick
    apelido_atual = _nick_dict.get(conexao)

    #se nao tiver marco como *
    if apelido_atual is None:
        apelido_atual = b'*'

    #caso se o nome nao eh valido da erro
    if not validar_nome(apelido):
        #envia msg de erro apelido invalido
        return conexao, b':server 432 '+apelido_atual+b' '+apelido+b' :Erroneous nickname\r\n'

    #caso se o nome q quer colocar ja ta em uso
    if apelido.lower() in _nick_dict.values():
        #msg de erro ja existe esse aplido
        return conexao, b':server 433 '+apelido_atual+b' '+apelido+b' :Nickname is already in use\r\n'

    
    #casos deu bom 

    #deu bom e primeira vez
    if apelido_atual == b'*' :
        #adiciona no dict
        _nick_dict[conexao] = apelido.lower()

        #envia msg
        return conexao, b':server 001 '+apelido+b' :Welcome\r\n:server 422 '+apelido+b' :MOTD File is missing\r\n'

    #deu bom e ta trocando de apelido
    if apelido_atual != b'*':
        _nick_dict[conexao] = apelido.lower()
        return conexao, b':'+apelido_atual+b' NICK '+apelido+b'\r\n'

def PRIVMSG_handler(conexao, mensagem):
    # Pegar o nick do sender
    sender = _nick_dict[conexao]
    # Pegar o nick do receiver (Na mensagem)
    mensagem = mensagem.split(maxsplit=2)
    receiver = mensagem[1]
    # (Passo 6) verificar se o receiver é um canal
    # Comparar com o dicionário de nicks
    if not (receiver.lower() in _nick_dict.values()):
        return conexao, b''
    # Enviar mensagem
    targetPos = list(_nick_dict.values()).index(receiver.lower())
    return list(_nick_dict.keys())[targetPos], b':' + sender + b' PRIVMSG ' + receiver + b' ' + mensagem[2] + b'\r\n'
    

def JOIN_handler(conexao, dados):
    return

def PART_handler(conexao, dados):
    return

def validar_nome(nome):
    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None

def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()


# def dados_recebidos(conexao, dados):
#     #caso da mensagem vazia
#     if dados == b'':
#         return sair(conexao)

#     #tratar multiplas mensagens separando por /r/n
#     fila_mensagens = Tratar_Dados_Recebidos(dados)

#     #para cada mensagem da fila o servidor tem que lidar 
#     while fila_mensagens:
#         #tirando msg da fila
#         msg = fila_mensagens.pop(0)
        
#         #pega o que deve ser respondido para cada tipo de msg
#         response = Message_Handler(conexao,msg)



# def Tratar_Dados_Recebidos(dados):
#     fila_mensagens = []

#     #separa as mensagens pelo /r/n
#     mensagens = dados.split('\r\n')

#     #remove os espacos vazios que foram separados na msg
#     mensagens = [parte for parte in mensagens if parte]

#     #coloca mensagens na fila
#     fila_mensagens.extend(mensagens)

#     return fila_mensagens