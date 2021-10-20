from random import randint, random
import time


# Classe do pacote RDT
class RDT_packet_t():
    def init(self):
        super(RDT_packet_t).init()
        self.seqnum = None
        self.acknum = None
        self.checksum = None
        self.payload = None
        self.echo = False


# Classe Alice
class Alice():
    def __init__(self):
        super(Alice, self).__init__()
        self.acknum = None
        self.seqnum = None 
        self.numerodamensagem = 0  # Mensagem atual
        self.mensagem = []  # Mensagens que a alice vai enviar
        self.rdt = RDT_packet_t()
       

# Classe Bob
class Bob():
    def __init__(self):
        super(Bob, self).__init__()
        self.acknum = None
        self.seqnum = None
        self.rdt = RDT_packet_t()


# Classe para o Timer
class Timer():
    def __init__(self):
        super(Timer, self).__init__()
        self.start = 0
        self.end = 0.000
        self.max_time = 0.4
        self.to_wait = None

    def start_timer(self):
        self.start = time.time()  # Tempo atual

    def stop_timer(self):
        self.end = time.time()  # Tempo atual

    def set_to_wait(self):
        self.to_wait = random()  # Gera um valor aleatorio para o tempo de envio do pacote

    def waiting_time(self):  # Simula o tempo para o time out
        i = 0
        while i < 100000:
            i += 1
        self.stop_timer() 
        return self.end * randint(1, 3) - self.start
        
        
# Função de inicialização para Alice
def transport_layer_init_A(alice): 
    alice.acknum = 0
    alice.seqnum = 0
    alice.rdt = RDT_packet_t()
    alice.rdt.echo = False
    alice.rdt.seqnum = alice.seqnum
    alice.rdt.acknum = alice.acknum
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
def communication_network(rdt, user, ip, timer):
    if ip == 0:  # Alice realiza a comunicação com Bob 
        casualidade = randint(0, 15)  # O que vai ocorrer com o pacote (enviar ou corromper)
        print('Casualidade:', casualidade)

        user.rdt = rdt
        if casualidade == 7:
            user.rdt = rdt
            user.rdt.payload[4] = 'z'  # Corrompe o pacote    
            # Trocas entre seqnum e acknum               
            user.rdt.acknum = rdt.seqnum
            user.rdt.seqnum = rdt.acknum
            user.acknum = rdt.seqnum
            user.seqnum = rdt.acknum  
            timer.set_to_wait()  # Define o tempo de espera
        else:
            user.rdt = rdt
            # Trocas entre seqnum e acknum    
            user.rdt.acknum = rdt.seqnum
            user.rdt.seqnum = rdt.acknum
            user.acknum = rdt.seqnum
            user.seqnum = rdt.acknum
            timer.set_to_wait()  # Define o tempo de espera
    elif ip == 1:  # Bob realiza a comunicação com Alice
        user.rdt = rdt
        # Trocas entre seqnum e acknum  
        user.rdt.seqnum = rdt.acknum
        user.rdt.acknum = rdt.seqnum
        user.acknum = rdt.seqnum
        user.seqnum = rdt.acknum


# Camada de transporte Alice - Input
def transport_layer_input_A(alice):
    if alice.rdt.echo is True:  # Se chegou um echo
        if alice.seqnum == (alice.rdt.seqnum + 1):  # E o echo tem seqnum + 1
            return (True, True)
        elif alice.seqnum == (alice.rdt.seqnum):  # Se o echo for igual a mensagem anterior
            return(True, False)
    else:  # Se não chegou nenhum echo
        return (False, False)


# Camada de transporte Bob - Input
def transport_layer_input_B(bob, alice, timer):
    if (timer.waiting_time() * 100) < timer.to_wait: 
        rdtecho = RDT_packet_t()  # Cria um novo packet
        rdtecho.echo = False
        rdtecho.acknum = bob.acknum
        rdtecho.seqnum = bob.seqnum
        communication_network(rdtecho, alice, 1, timer)  # Tenta o reenvio da mesma mensagem

        return False

    elif checksum(bob.rdt.payload) == bob.rdt.checksum:  # Se o checksum está correto
        print('Bob: Arquivo confirmado')
        rdtecho = RDT_packet_t()  # Cria um novo packet
        rdtecho.echo = True
        rdtecho.acknum = bob.acknum + 1  # Adiciona +1 ao acknum
        rdtecho.seqnum = bob.seqnum
        communication_network(rdtecho, alice, 1, timer)  # Manda um echo com a mensagem confirmada

        return True

    else:  # Se o checksum deu erro
        print('Bob: Arquivo corrompido')
        rdtecho = RDT_packet_t()  # Cria um novo packet
        rdtecho.echo = True
        rdtecho.acknum = bob.acknum
        rdtecho.seqnum = bob.seqnum
        communication_network(rdtecho, alice, 1, timer)  # Manda um echo com a mesma mensagem para reenvio

        return False


# Camada de transporte Alice - Output
def transport_layer_output_A(app_payload, alice, bob, verificacao, timer):
    rdt = RDT_packet_t()  # Cria um novo packet
    rdt.checksum = checksum(app_payload)  # Atribui o checksum
    rdt.payload = app_payload  # Atribui a mensagem
    rdt.seqnum = alice.seqnum  # Atribui o seqnum
    rdt.echo = False

    if verificacao is True:  # Se o echo retornado para alice é verdadeiro     
        rdt.acknum = alice.acknum + 1
    else:  # Se o echo retornado para alice é falso
        rdt.acknum = alice.acknum

    alice.rdt = rdt  # Atribui o packet criado para a alice
    alice.rdt.payload = alice.rdt.payload.copy()  # Atribui uma cópia da mensagem
    communication_network(rdt, bob, 0, timer)  # Envia o packet da alice para a rede
    timer.start_timer()  # Inicia o temporizador
    

# Alice aplicação
def app_layer_A(alice, bob, timer, primeira):
    if alice.numerodamensagem < 20:
        print('Mensagem: ', alice.numerodamensagem + 1)
        if timer.waiting_time() <= timer.max_time and primeira is False:  # Se o tempo ainda está dentro do tempo maximo
            var1, var2 = transport_layer_input_A(alice)
            if var1:  # Se existe um echo na alice
                if(var2):  # Se o echo é +1        
                    alice.numerodamensagem += 1
                    transport_layer_output_A(alice.mensagem[alice.numerodamensagem], alice, bob, True, timer)  # Alice manda a proxima mensagem
                else:  # Se o echo é igual
                    transport_layer_output_A(alice.mensagem[alice.numerodamensagem], alice, bob, False, timer)  # Alice reenvia a mensagem         
            else:
                # Se não chegou nenhum echo: continua esperando
                pass
        else:
            if primeira is False:
                print('Timed Out: tentando um novo envio...')  # Se o tempo máximo de espera acabou
            transport_layer_output_A(alice.mensagem[alice.numerodamensagem], alice, bob, False, timer)  # alice reenvia a mensagem


# Bob aplicação
def app_layer_B(bob, alice, timer):
    verificador = transport_layer_input_B(bob, alice, timer)

    if verificador is True:  # Se o checksum estava correto
        print('Enviado com sucesso:', bob.rdt.payload)  # Imprime a mensagem enviada
        print()
        alice.numerodamensagem += 1  # Adiciona +1 ao número de mensagens enviadas

    else:  # Se o checksum estava incorreto ou ocorreu timed out
        pass
    pass


#  Função principal, realiza a simulação
def main():
    # Inicializa valores
    alice = Alice()  # Emissor
    bob = Bob()  # Receptor
    timer = Timer()  # Timer
    timer.start_timer()
    parar = False
    primeira = True
    transport_layer_init_A(alice)  # Inicializa a variável da alice (emissora)
    while alice.numerodamensagem < 20:  # Enquanto tiver mensagens para ser enviadas
        app_layer_A(alice, bob, timer, primeira)  # Realiza os procedimentos do lado do emissor (Alice)
        primeira = parar

        if parar is False:
            app_layer_B(bob, alice, timer)  # Realiza os procedimentos do lado do receptor (Bob)

if __name__ == '__main__':
    main()