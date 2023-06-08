from util_functions import validar_nome
# -----------------------------------------------------------------#
def JOIN_handler(conexao, mensagem, _canal_dict, _nick_dict):
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