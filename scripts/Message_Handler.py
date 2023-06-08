#-----------------------------------------------------------------#
'''
    nick_dict = {conexao:nick,...}
    canal_dict = {nome_canal:nick_dict,...}
'''
_nick_dict  = {}
_canal_dict = {}
_dados_residuais = b''
#-----------------------------------------------------------------#
import util_functions as uf
#-----------------------------------------------------------------#
from ping    import PING_handler
from nick    import NICK_handler
from join    import JOIN_handler
from privmsg import PRIVMSG_handler
from part    import PART_handler
#-----------------------------------------------------------------#
def Message_Handler(conexao, dados):
    # tirar espacos no comeco e no fim da msg
    dados = dados.strip()

    #switch dos tipos de dados
    if dados == b'':
        return uf.sair(conexao)

    elif dados[0:4] == 'NICK':
        response = NICK_handler(dados)

    elif dados[0:4].upper() == b'NICK':
        alvo, response = NICK_handler(conexao, dados, _nick_dict)

    elif dados[0:4].upper() == b'JOIN':
        alvo, response = JOIN_handler(conexao, dados, _canal_dict, _nick_dict)

    elif dados[0:7].upper() == b'PRIVMSG':
        alvo, response = PRIVMSG_handler(conexao, dados, _nick_dict)

    elif dados[0:4].upper() == b'PART':
        alvo, response = PART_handler(conexao, dados, _canal_dict, _nick_dict)

    # retorna o erro ou sucesso da dados
    return alvo, response
#-----------------------------------------------------------------#
def dados_recebidos(conexao, dados):
    if dados == b'':
        return uf.sair(conexao)
    
    mensagens = []
    #if not dados.endswith(b'\r\n'):
        # Dividir os dados em substrings e filtrar strings vazias
        #dados = list(filter(bool, dados.split(b'\r\n')))
    global _dados_residuais
    lines = _dados_residuais + dados
    mensagens = lines.split(b'\r\n')
    
    # Armazenar os dados residuais para uso posterior
    if(mensagens[-1][:len(_dados_residuais)] == _dados_residuais):
        _dados_residuais = b''
    _dados_residuais += mensagens.pop(-1)

    # Processar cada mensagem separadamente
    for mensagem in mensagens:
        print(conexao, mensagem)
        alvo, resposta = Message_Handler(conexao, mensagem)
        print(alvo, resposta)
        if mensagem != b'':
            alvo.enviar(resposta)
#-----------------------------------------------------------------#
def conexao_aceita(conexao):
    print(conexao, 'nova conexão')
    conexao.registrar_recebedor(dados_recebidos)
#-----------------------------------------------------------------#

''''
def PING_handler(conexao, dados):
    return conexao, b':server PONG server :' + dados.split(b' ', 1)[1] + b'\r\n'
    # print('respondendo PING com PONG')
    # print(conexao, dados)
# -----------------------------------------------------------------#


def NICK_handler(conexao, dados):
    # separar comando de conteudo e tirar espacos da mensagem
    comando, apelido = dados.split(b' ', 1)

    # vejo se essa conexao ja tem nick
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

        # envia msg
        return conexao, b':server 001 '+apelido+b' :Welcome\r\n:server 422 '+apelido+b' :MOTD File is missing\r\n'

    # deu bom e ta trocando de apelido
    if apelido_atual != b'*':
        _nick_dict[conexao] = apelido.lower()
        return conexao, b':'+apelido_atual+b' NICK '+apelido+b'\r\n'
# -----------------------------------------------------------------#


def PRIVMSG_handler(conexao, mensagem):
    # Pegar o nick do sender
    sender = _nick_dict[conexao]
    # Pegar o nick do receiver (Na mensagem)
    mensagem = mensagem.split(maxsplit=2)
    receiver = mensagem[1]
    # (Passo 6) verificar se o receiver é um canal
    if (receiver.startswith(b'#')):
        return PRIVMSG_handler_canal(conexao, sender, receiver.lower(), mensagem[2].replace(b':', b''))
    # Comparar com o dicionário de nicks
    if not (receiver.lower() in _nick_dict.values()):
        return conexao, b''
    # Enviar mensagem
    targetPos = list(_nick_dict.values()).index(receiver.lower())
    return list(_nick_dict.keys())[targetPos], b':' + sender + b' PRIVMSG ' + receiver + b' ' + mensagem[2] + b'\r\n'
# -----------------------------------------------------------------#


def PRIVMSG_handler_canal(conexao, sender, canal, conteudo):
    # montando mensagem
    canal = canal.replace(b'#', b'')
    mensagem = b':' + sender + b' PRIVMSG #' + canal + b' :' + conteudo + b'\r\n'
    # Enviar mensagem para todos do canal
    for conex in _canal_dict[canal]:
        if (conex != conexao):
            conex.enviar(mensagem)
    return conexao, b''
# -----------------------------------------------------------------#


def JOIN_handler(conexao, mensagem):
    # verificar validade do nome do canal
    canal = mensagem.split(b' ', 1)[1].replace(b'#', b'').lower()
    if not validar_nome(canal):
        return conexao, b':server 403 '+mensagem+b' :No such channel\r\n'

    # se nao existe cria
    if _canal_dict.get(canal) is None:
        # cria o canal no dict
        _canal_dict[canal] = {}
        # cria a lista de nicks com essa conexao e adiciona o primeiro nick
        _canal_dict[canal][conexao] = _nick_dict[conexao]
        # envia a msg de criacao do canal
        return conexao, b':'+_nick_dict[conexao]+b' JOIN :#'+canal+b'\r\n'

    # se existe adiciona
    if _canal_dict.get(canal) is not None:
        # adiciona a conexao no dict
        _canal_dict[canal][conexao] = _nick_dict[conexao]
        # envia a msg de criacao do canal para todos do canal (menos o que entrou)
        for conex in _canal_dict[canal]:
            if (conex != conexao):
                conex.enviar(b':'+_nick_dict[conex]+b' JOIN :#'+canal+b'\r\n')

        # mensagem de join no canal para o recem chegado
        mensagemJoin = b':'+_nick_dict[conexao]+b' JOIN :#'+canal+b'\r\n'

        # mensagem de listar membros do canal para o recem chegado
        template = b':server 353 '+_nick_dict[conexao]+b' = :#'+canal+b' :'
        membros = b''
        for conexao in _canal_dict[canal]:
            membros += _nick_dict[conexao]+b' '
        mensagemMembros = template + membros + b'\r\n'
        memsagemFimMembros = b':server 366 ' + \
            _nick_dict[conexao]+b' #'+canal+b' :End of /NAMES list\r\n'

        mensagem = mensagemJoin + mensagemMembros + memsagemFimMembros

        # enviar mensagens para recem chegado
        return conexao, mensagem
# -----------------------------------------------------------------#

# -----------------------------------------------------------------#


def PART_handler(conexao, dados):
    # pegar o nome do canal
    canal = dados.split(b' ', 2)[1].replace(b'#', b'').lower()
    # enviar mensagem de saida do canal para todos do canal
    for conex in _canal_dict[canal]:
        conex.enviar(b':'+_nick_dict[conexao]+b' PART #'+canal+b'\r\n')

    # remover a conexao do canal
    _canal_dict[canal].pop(conexao)

    return conexao, b''
# -----------------------------------------------------------------#


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

#     return fila_mensagens
'''
