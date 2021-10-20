from random import randint


# Classe do pacote RDT
class RDT_packet_t():
    def init(self):
        super(RDT_packet_t).init()
        self.seqnum = None
        self.acknum = None
        self.checksum = None
        self.payload = None


# Classe Alice
class Alice():
    def __init__(self):
        super(Alice, self).__init__()
        self.acknum = None
        self.seqnum = None
        self.numerodamensagem = 0
        self.mensagem = []
        self.rdt = RDT_packet_t()
        

# Classe Bob
class Bob():
    def __init__(self):
        super(Bob, self).__init__()
        self.acknum = None
        self.seqnum = None
        self.rdt = RDT_packet_t()
        

# Função de inicialização para Alice
def transport_layer_init_A(alice):
    alice.acknum = 0
    alice.seqnum = 0
    alice.rdt = RDT_packet_t()
    alice.rdt.seqnum = alice.seqnum
    alice.mensagem.append(list('edfhiewufhksfhalskiu'))
    alice.mensagem.append(list('fhuiadshfkaflwoeiofl'))
    alice.mensagem.append(list('ljkasdbvajsdkhjfgvbd'))
    alice.mensagem.append(list('asdhjkvboioefjlaskdf'))
    alice.mensagem.append(list('aksfaskjdskajfakfjaf'))
    alice.mensagem.append(list('gftjhyujyjyjyjyyjjyy'))
    alice.mensagem.append(list('asdasdaspolpopookffb'))    
    alice.mensagem.append(list('laskdaiwfmalfkafkakf'))
    alice.mensagem.append(list('asdgrgrfgrwwegwgwggw'))
    alice.mensagem.append(list('skflfslfskfslflsflsk'))
    alice.mensagem.append(list('poklopkomkikninoinvi'))
    alice.mensagem.append(list('ljferhmrumzxxxjtziyw'))
    alice.mensagem.append(list('efdxgbiaevuuqxigvupa'))
    alice.mensagem.append(list('aodfxrkqjjvkoagugoxv'))
    alice.mensagem.append(list('fhfzfyxgdgrujeudtodq'))
    alice.mensagem.append(list('vybygxmeveawteujhrpu'))
    alice.mensagem.append(list('voddpkpzfalnqwjfvkxf'))
    alice.mensagem.append(list('guvvbhitfqjnrzscqqjt'))
    alice.mensagem.append(list('bvgplxfjzspzdrfksqki'))
    alice.mensagem.append(list('vvivmhkzvobseypfblqk'))


# Função de inicialização para Bob
def transport_layer_init_B():
    pass


# Converte a letra para valor binário
def to_binary(a):
    l, m = [], []
    for i in a:
        l.append(ord(i))

    for i in l:
        m.append(int(bin(i)[2:]))
    return str(m[0])


# Função que calcula o checksum para oferecer proteção ao pacote
def checksum(app_payload):
    lista = []
    somatorio = 0

    for data in app_payload:
        lista.append(to_binary(data))

    for data in lista:
        somatorio += int(data, 2)
    checksum = str(bin(somatorio))    

    return checksum


# ------------------------------------------------------

# Camada de rede
def communication_network(rdt, destino, ip_origem):
    if ip_origem == 0:  # Alice realiza a comunicação com Bob
        casualidade = randint(0, 10)  # O que vai ocorrer com o pacote (enviar ou corromper)
        print('Casualidade:', casualidade)

        destino.rdt = rdt
        if casualidade == 7:
            destino.rdt.payload[4] = 'z'  # Corrompe o pacote
        else:  # Envia o pacote normalmente
            # Troca entre acknum e seqnum (passa para o próximo pacote)
            destino.acknum = rdt.seqnum
            destino.seqnum = rdt.acknum
    elif ip_origem == 1:  # Bob realiza a comunicação com Alice
        # Troca entre acknum e seqnum (passa para o próximo pacote)
        destino.acknum = rdt.seqnum
        destino.seqnum = rdt.acknum


# Camada de transporte Alice - Input
def transport_layer_input_A(alice):
    if alice.seqnum == (alice.rdt.seqnum + 1):  # Verifica se o seqnum da alice corresponde ao proximo pacote
        return True
    else:  # Se o seqnum da alice não foi atualizado significa que o pacote deve ser reenviado
        return False


# Camada de transporte Bob - Input
def transport_layer_input_B(bob, alice):
    if checksum(bob.rdt.payload) == bob.rdt.checksum:  # Se o checksum da mensagem recebida corresponder ao checksum do pacote
        print('Bob: Arquivo confirmado')

        rdtecho = RDT_packet_t()
        rdtecho.acknum = bob.acknum + 1  # Acknum faz referência ao próximo pacote
        rdtecho.seqnum = bob.seqnum

        communication_network(rdtecho, alice, 1)  # Envia um echo do RDT para a Alice
        return True
    else:  # Checksum diferente
        print('Bob: Arquivo corrompido')
        return False


# Camada de transporte Alice - Output
def transport_layer_output_A(app_payload, alice, bob, verificacao):  # Empacota os dados e encaminha para a camada de rede (comunicação)
    rdt = RDT_packet_t()
    rdt.checksum = checksum(app_payload)  # Calcula o checksum
    rdt.payload = app_payload
    rdt.seqnum = alice.seqnum
    if verificacao is True:
        rdt.acknum = alice.acknum + 1
    else:
        rdt.acknum = alice.acknum
    alice.rdt = rdt
    alice.rdt.payload = alice.rdt.payload.copy()

    communication_network(rdt, bob, 0)    
    

# Alice aplicação
def app_layer_A(alice, bob):
    if alice.numerodamensagem == 19:  # Última mensagem
        if transport_layer_input_A(alice):  # Verifica se o envio foi realizado com sucesso
            return True  # Termina a simulação
        else:
            print('Alice esta enviando a ultima mensagem:', alice.numerodamensagem + 1)
            transport_layer_output_A(alice.mensagem[alice.numerodamensagem], alice, bob, False)  # Envia a última mensagem
            return False
    else:
        if transport_layer_input_A(alice):  # Verifica se o seqnum da alice corresponde ao próximo pacote
            alice.numerodamensagem += 1  # Próxima mensagem
            print('Mensagem:', alice.numerodamensagem + 1)
        
            transport_layer_output_A(alice.mensagem[alice.numerodamensagem], alice, bob, True)  # Prepara o transporte (empacota o dado) e faz a ligação com a rede
            return False  # Continua a simulação

        else:  # É a primeira mensagem ou o seqnum da Alice continua o mesmo que o da mensagem anterior, portanto ela deve ser reenviada
            print('Mensagem:', alice.numerodamensagem + 1)
            if alice.numerodamensagem != 0:
                print('Reenviando a mensagem:', alice.numerodamensagem + 1)
            transport_layer_output_A(alice.mensagem[alice.numerodamensagem], alice, bob, False)  # Prepara o transporte (empacota o dado) e faz a ligação com a rede
        return False


# Bob aplicação
def app_layer_B(bob, alice):
    verificador = transport_layer_input_B(bob, alice)  # Verifica o recebimento da mensagem
    if verificador is True:
        print('Mensagem recebida:', bob.rdt.payload) 
    else:
        print("Bob: Falha ao carregar mensagem Arquivo corrompido ou em falta")


#  Função principal, realiza a simulação
def main():
    # Inicializa valores
    alice = Alice()  # Emissor
    bob = Bob()  # Receptor
    parar = False
    transport_layer_init_A(alice)  # Inicializa a variável da alice (emissora)
    while parar is False:  # Enquanto tiver mensagens para ser enviadas
        parar = app_layer_A(alice, bob)  # Realiza os procedimentos do lado do emissor (Alice)
        if parar is False:
            app_layer_B(bob, alice)  # Realiza os procedimentos do lado do receptor (Bob)
        print()

if __name__ == '__main__':
    main()