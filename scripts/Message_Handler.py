def Message_Handler(mensagem):

    #switch dos tipos de mensagem
    if mensagem[0:4] == 'PING':
        response = PING_handler(mensagem)

    if mensagem[0:4] == 'NICK':
        response = NICK_handler(mensagem)

    if mensagem[0:4] == 'JOIN':
        response = JOIN_handler(mensagem)

    if mensagem[0:7] == 'PRIVMSG':
        response = PRIVMSG_handler(mensagem)
    
    if mensagem[0:4] == 'PART':
        response = PART_handler(mensagem)
    
    #retorna o erro ou sucesso da mensagem
    return response