# -----------------------------------------------------------------#
def PART_handler(conexao, dados, _canal_dict, _nick_dict):
    # pegar o nome do canal
    canal = dados.split(b' ', 2)[1].replace(b'#', b'').lower()
    # enviar mensagem de saida do canal para todos do canal
    for conex in _canal_dict[canal]:
        conex.enviar(b':'+_nick_dict[conexao]+b' PART #'+canal+b'\r\n')

    # remover a conexao do canal
    _canal_dict[canal].pop(conexao)

    return conexao, b''
# -----------------------------------------------------------------#