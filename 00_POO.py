class Carro: 
    def __init__(self, modelo, cor):
        self.modelo = modelo 
        self.cor = cor 
        self.velocidade = 0 # o carro começa parado 

    def acelerar(self, incremento):
        self.velocidade += incremento 
        print(f'O {self.modelo} acelerou para {self.velocidade} km/h.')

    def desacelerar(self, decremento):
        self.velocidade -= decremento
        print(f'O {self.modelo} desacelerou para {self.velocidade} km/h.')

# criando um obejto carro
meu_carro = Carro('VW Up','Preto') 
outro_carro = Carro('Ferrari', 'Vermelho')


# usando os métodos
meu_carro.acelerar(20)
meu_carro.acelerar(20)
meu_carro.acelerar(20)
meu_carro.desacelerar(30)