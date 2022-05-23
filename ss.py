import socket     # библиотека

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # определение сервера

server.bind(('127.0.0.1', 2500))            # открываем сервер по ip



print('26.151.248.193')



server.listen()         # включаем сервер

typeUser = None

while True:         # сервер работает бесконечно
	if (typeUser == None):
		typeUser, userAdres = server.accept()        # определяем пользователя(П) и тип его подключения
	else:
		data = typeUser.recv(1024)
		print(data.decode('utf-8'))          # выводим данные П в кодировке utf-8

		typeUser.send(data)