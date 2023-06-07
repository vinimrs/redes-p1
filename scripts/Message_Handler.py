import re
_nick_dict = {}
#--------------------------------------------------------------------------------#
def Message_Handler(conexao,dados):

    #tirar espacos no comeco e no fim da msg
    dados = dados.strip()

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
#--------------------------------------------------------------------------------#
def NICK_handler(conexao,dados):
    #separar comando de conteudo e tirar espacos da mensagem
    comando, apelido = dados.split(' ',1)

    #vejo se essa conexao ja tem nick
    apelido_atual = _nick_dict.get(conexao)

    #se nao tiver marco como *
    if apelido_atual is None:
        apelido_atual = '*'

    #caso se o nome nao eh valido da erro
    if not validar_nome(apelido):
        #envia msg de erro apelido invalido
        conexao.enviar(b':server 432 '+apelido_atual+' '+apelido+' :Erroneous nickname')

    #caso se o nome q quer colocar ja ta em uso
    if apelido in _nick_dict.values():
        #msg de erro ja existe esse aplido
        conexao.enviar(b':server 433 '+apelido_atual+' '+apelido+' :Nickname is already in use')

    #casos deu bom 
    #deu bom e primeira vez
    if apelido_atual == '*' :
        #adiciona no dict
        _nick_dict[conexao] = apelido

        #envia msg
        conexao.enviar(b':server 001 '+apelido+' :Welcome')
        conexao.enviar(b':server 422 '+apelido+' :MOTD File is missing')

    #deu bom e ta trocando de apelido
    if apelido_atual != '*':
        conexao.enviar(b':'+apelido_atual+' NICK '+apelido)
#--------------------------------------------------------------------------------#


def validar_nome(nome):
    return re.match(br'^[a-zA-Z][a-zA-Z0-9_-]*$', nome) is not None
#--------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------#

def PING_handler(conexao,dados):

    conexao.enviar(b':server PONG server :' + dados.split(b' ', 1)[1])
    print('respondendo PING com PONG')
    print(conexao, dados)
#--------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------#
def sair(conexao):
    print(conexao, 'conexão fechada')
    conexao.fechar()
#--------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------#
def dados_recebidos(conexao, dados):
    #caso da mensagem vazia
    if dados == b'':
        return sair(conexao)

    #tratar multiplas mensagens separando por /r/n
    fila_mensagens = Tratar_Dados_Recebidos(dados)

    #para cada mensagem da fila o servidor tem que lidar 
    while fila_mensagens:
        #tirando msg da fila
        msg = fila_mensagens.pop(0)
        
        #pega o que deve ser respondido para cada tipo de msg
        response = Message_Handler(conexao,msg)
#--------------------------------------------------------------------------------#


#--------------------------------------------------------------------------------#
def Tratar_Dados_Recebidos(dados):
    fila_mensagens = []

    #separa as mensagens pelo /r/n
    mensagens = dados.split('\r\n')

    #remove os espacos vazios que foram separados na msg
    mensagens = [parte for parte in mensagens if parte]

    #coloca mensagens na fila
    fila_mensagens.extend(mensagens)

    return fila_mensagens
#--------------------------------------------------------------------------------#
