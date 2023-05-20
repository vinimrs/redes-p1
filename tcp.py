import socket
import asyncio


class Servidor:
    # Classe que representa um servidor TCP
    # que aceita conexões de clientes.
    # O construtor recebe a porta em que o servidor
    # deve escutar por conexões.
    def __init__(self, porta):
        # Cria um socket IRC
        s = self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Permite reutilizar a porta imediatamente
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Associa o socket à porta
        s.bind(('', porta))
        # Começa a escutar por conexões
        s.listen(5)

    # Registra um callback para ser chamado quando
    # uma nova conexão for aceita.
    # O callback deve receber um objeto Conexao
    # como parâmetro.
    def registrar_monitor_de_conexoes_aceitas(self, callback):
        asyncio.get_event_loop().add_reader(
            self.s, lambda: callback(Conexao(self.s.accept())))


# Classe que representa uma conexão TCP
class Conexao:
    def __init__(self, accept_tuple):
        # accept_tuple é uma tupla (socket, endereço)
        self.s, _ = accept_tuple

    def registrar_recebedor(self, callback):
        # Registra um callback para ser chamado quando
        # dados forem recebidos.
        asyncio.get_event_loop().add_reader(
            self.s, lambda: callback(self, self.s.recv(8192)))

    def enviar(self, dados):
        # Envia dados para o outro lado da conexão.
        self.s.sendall(dados)

    def fechar(self):
        asyncio.get_event_loop().remove_reader(self.s)
        self.s.close()
