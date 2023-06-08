# -----------------------------------------------------------------#
def PRIVMSG_handler(conexao, mensagem, _nick_dict):
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
def PRIVMSG_handler_canal(conexao, sender, canal, conteudo, _canal_dict):
    # montando mensagem
    canal = canal.replace(b'#', b'')
    mensagem = b':' + sender + b' PRIVMSG #' + canal + b' :' + conteudo + b'\r\n'
    # Enviar mensagem para todos do canal
    for conex in _canal_dict[canal]:
        if (conex != conexao):
            conex.enviar(mensagem)
    return conexao, b''
# -----------------------------------------------------------------#