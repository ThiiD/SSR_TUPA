import socket
import json
from time import sleep
from datetime import datetime
import serial

class Cliente():
    """
    Classe Cliente - Supervisorio Supernova Rocketry - API Socket
    """

    def __init__(self, server_ip, port):
        """
        Construtor da classe cliente
        :param server_ip: ip do servidor
        :param port: porta do servidor
        """
        self._serverIP = server_ip
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        


    def start(self):
        """
        Método que inicializa a execução do cliente
        """
        endpoint = (self._serverIP, self._port)
        try:
            self._tcp.connect(endpoint)
            print("Conexao realiza com sucesso.")
            # self._method()
        except Exception as e:
            print(f'Erro ao conectar {e.args}')
            raise e


    def _method(self):
        """
        Método que implementa as requisições do cliente e a IHM
        """
        try:
            msg = 'y'
            self._tcp.send(msg.encode())
            self._resp = self._tcp.recv(1024)
            self._resp = self._resp.decode()
            self._resp = eval(self._resp)
            self._resp['timestamp'] = datetime.now()
        except Exception as e:
            print(f'Erro ao realizar a comunicacao com o servidor {e.args}')
            raise e

        return self._resp

    def disconect(self):
        self._tcp.close()
        print("Desconectar!")

        

class UART():
    _firstData = True
    _requests = {
        "Controle_IAC"      :   0,
        "Controle_Estado"   :   0,
        "Antena_IAC"        :   0,
        "Antena_Estado"     :   0,
        "Missao_IAC"        :   0,
        "Missao_Estado"     :   0,
        "Setpoint_IAC"      :   0,
        "Setpoint_Value"    :   0,
    }

    def __init__(self, porta, baudrate):
        self._porta = porta
        self._baudrate = baudrate
        self._minAltValue = 0
        

    def start(self):
        try:
            self._ser = serial.Serial(self._porta, self._baudrate)
            print("Connecting...")
            sleep(3)
            print(self._ser.name)
        except Exception as e:
            print(e)
            raise e


    def recieveData(self):
        try:
            sleep(0.1)
            self._data = self._ser.readline().decode('ascii')
            print(self._data)
            print(type(self._data))
            self._data = json.loads(self._data)
            self._data['timestamp'] = datetime.now()
            if self._firstData == True:
                self._minAltValue = self._data['Alt']
                self._firstData = False
            self._data['Alt'] = self._data['Alt'] - self._minAltValue
            return self._data
        except Exception as e:
            print(e)

    def _sendData(self):
        print(f"Enviando dados!: {self._requests}")
        print(self._requests.values())
        byteData = bytearray(list(self._requests.values()))
        print(byteData)
        self._ser.write(byteData)

        pass

    def _getCommand(self, name, status):
        if status == True: self._requests[name] = 1
        elif status == False: self._requests[name] = 0
        else: self._requests[name] = int(status)
# class WiFi():
#     """
#     Classe WiFI - Supervisório Supernova Rocketry - Comunicação WiFi
#     """
#     def __init__(self):
        