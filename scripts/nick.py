from util_functions import validar_nome
#-----------------------------------------------------------------#
def NICK_handler(conexao, dados, _nick_dict):
    # separar comando de conteudo e tirar espacos da mensagem
    comando, apelido = dados.split(b' ', 1)

    # vejo se essa conexao ja tem nick
    apelido_atual = _nick_dict.get(conexao)

    # se nao tiver marco como *
    if apelido_atual is None:
        apelido_atual = b'*'

    # caso se o nome nao eh valido da erro
    if not validar_nome(apelido):
        # envia msg de erro apelido invalido
        return conexao, b':server 432 '+apelido_atual+b' '+apelido+b' :Erroneous nickname\r\n'

    # caso se o nome q quer colocar ja ta em uso
    if apelido.lower() in _nick_dict.values():
        # msg de erro ja existe esse aplido
        return conexao, b':server 433 '+apelido_atual+b' '+apelido+b' :Nickname is already in use\r\n'

    # casos deu bom

    # deu bom e primeira vez
    if apelido_atual == b'*':
        # adiciona no dict
        _nick_dict[conexao] = apelido.lower()

        # envia msg
        return conexao, b':server 001 '+apelido+b' :Welcome\r\n:server 422 '+apelido+b' :MOTD File is missing\r\n'

    # deu bom e ta trocando de apelido
    if apelido_atual != b'*':
        _nick_dict[conexao] = apelido.lower()
        return conexao, b':'+apelido_atual+b' NICK '+apelido+b'\r\n'
#-----------------------------------------------------------------#
    