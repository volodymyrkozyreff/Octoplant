import numpy as np
import cv2
import math
import PIL
from PIL import Image
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # определение сервера

client.connect(("127.0.0.1", 2500))        # подключаем клиента к серверу


car = list()
cars = [[0,0], [0,0], [0,0]]
color_size = 5
color_line = 150
area_min = 100
area_max = 1000000
ph_path = 'test1.png'
area_correct = 0
color_correct = 0

def color(ch, ch1):
    image = Image.open(ph_path)

    w1, h1 = int(ch)-color_size, int(ch1)-color_size  # середина -5
    w2, h2 = int(ch)+color_size, int(ch1)+color_size # середина +5
    rr, gg, bb = 0, 0, 0

    for x in range(w1, w2):
        for y in range(h1, h2):
            r, g, b = image.getpixel((x, y))
            rr += r
            gg += g
            bb += b

    cnt = (w2-w1) * (h2-h1)
    #print(rr//cnt, gg//cnt, bb//cnt)
    red = rr//cnt
    green = gg//cnt
    blue = bb//cnt
    #return red, green, blue
    if max(red, green, blue) == red and max(red, green, blue) > color_line:
        return 'red'
    elif max(red, green, blue) == green and max(red, green, blue) > color_line:
        return 'green'
    elif max(red, green, blue) == blue and max(red, green, blue) > color_line:
        return 'blue'
    else:
        return 0


def dr(cars):
	ax=cars[0][0]
	bx=cars[1][0]
	cx=cars[2][0]

	ay=cars[0][1]
	by=cars[1][1]
	cy=cars[2][1]

	ax_bx=ax-bx
	bx_cx=bx-cx
	cx_ax=cx-ax

	ay_by=ay-by
	by_cy=by-cy
	cy_ay=cy-ay

	axpbx=ax+bx
	bxpcx=bx+cx
	cxpax=cx+ax

	aypby=ay+by
	bypcy=by+cy
	cypay=cy+ay

	ax_bx=ax_bx**2
	bx_cx=bx_cx**2
	cx_ax=cx_ax**2

	ay_by=ay_by**2
	by_cy=by_cy**2
	cy_ay=cy_ay**2

	if (((ax_bx + ay_by) > (bx_cx + by_cy)) and ((ax_bx + ay_by) > (cx_ax + cy_ay))):
		dx=axpbx/2
		dy=aypby/2
		nx=cx
		ny=cy

	if (((bx_cx + by_cy) > (ax_bx + ay_by)) and ((bx_cx + by_cy) > (cx_ax + cy_ay))):
		dx=bxpcx/2
		dy=bypcy/2
		nx=ax
		ny=ay

	if (((cx_ax + cy_ay) > (ax_bx + ay_by)) and ((cx_ax + cy_ay) > (bx_cx + by_cy))):
		dx=cxpax/2
		dy=cypay/2
		nx=bx
		ny=by

	#print(dx)
	#print(dy)
	#print(nx)
	#print(ny)

	nx_dx = nx - dx
	ny_dy = ny - dy

	#print(nx_dx)
	#print(ny_dy)

	if (nx_dx == 0 and ny_dy > 0):
		grad=90
	elif (nx_dx == 0 and ny_dy < 0):
		grad =-90
	else:
		ngrad = ny_dy / nx_dx
		grad = math.atan(ngrad)
		grad = grad * 180
		grad = grad / math.pi

	if (nx_dx < 0 and ny_dy > 0):
		grad = 180 + grad
	elif (nx_dx < 0 and ny_dy < 0):
		grad = -180 + grad

	return round(grad)


def tochka(x1, y1, x2, y2, x3, y3):
	a = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # 3
	b = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)  # 1
	c = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)  # 2
	return a, b, c


def areas(a, b, c):
	p = (a + b + c) / 2
	return math.sqrt(p * (p - a) * (p - b) * (p - c))


def main(x1, y1, x2, y2, x3, y3):
	a, b, c = tochka(x1, y1, x2, y2, x3, y3)
	p = areas(a, b, c)
	# return p
	# print(f'Площадь треугольника при а, b, c = {a}, {b}, {c} равна {p}')

	if p < area_min or p > area_max:
		# exit(0)
		return 0
	else:
		if max(a, b, c) == a:
			# return a
			# print(max(a, b, c))
			# print(x3, y3)
			xc = ((x1 + x2) // 2)
			yc = ((y1 + y2) // 2)
			# print((x1 + x2)//2, (y1 + y2)//2)
			return x3, y3, xc, yc, p


		elif max(a, b, c) == b:
			# return b
			# print(max(a, b, c))
			# print(x1, y1)
			xc = ((x3 + x2) // 2)
			yc = ((y3 + y2) // 2)
			# print((x3 + x2)//2, (y3 + y2)//2)
			return x1, y1, xc, yc, p


		elif max(a, b, c) == c:
			# return c
			# print(max(a, b, c))
			# print(x2, y2)
			xc = ((x1 + x3) // 2)
			yc = ((y1 + y3) // 2)
			# print((x1 + x3)//2, (y1 + y3)//2)
			return x2, y2, xc, yc, p



while True:

	car.clear()

	# Включаем первую камеру
	cap = cv2.VideoCapture(1)   #на ноутбуке 0 накомпьютере 1 или 2

	# "Прогреваем" камеру, чтобы снимок не был тёмным
	for i in range(30):
		cap.read()

	# Делаем снимок
	ret, frame = cap.read()

	# Записываем в файл
	cv2.imwrite('cam.png', frame)

	# Отключаем камеру
	cap.release()

	#read image
	img_src = cv2.imread('cam.png')

	#blur the image
	img_rst = cv2.blur(img_src, (10, 10))

	#save result image
	cv2.imwrite('cam.png',img_rst)

	# Получаем изображение !!!!!!! позже будет переделано на получение видеопотока с fps=1(возможно больше) !!!!!!
	font = cv2.FONT_HERSHEY_COMPLEX
	img2 = cv2.imread(ph_path, cv2.IMREAD_COLOR)

	# Получили изображение ещё раз для контуров
	# Перевод в чб для нахождения контуров
	img = cv2.imread(ph_path, cv2.IMREAD_GRAYSCALE)
	_, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY) #!!!!важно ограничения по цветам будут подобраны позже!!!!

	# Находим контуры
	contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Пробегаем все контуры
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)  # параметры подбираются позже
		# Во время пробежкт проверяем на треугольники
		if len(approx) == 3:
			cv2.drawContours(img2, [approx], 0, (50, 205, 50), 5)
			n = approx.ravel()
			i = 0
			for j in n:
				if (i % 2 == 0):
					x = n[i]
					y = n[i + 1]

					string = str(x) + " " + str(y)
					car.append(int(x))
					car.append(int(y))
					#print(car)

					if (i == 0):  # выбираем одну из координат
						cv2.putText(img2, "Треугольник" + string, (x, y),
									font, 0.5, (0, 0, 0))
					else:
						cv2.putText(img2, string, (x, y),
									font, 0.5, (0, 0, 0))
				i += 1

	if len(car) % 6 == 0 and len(car) > 0 and len(car) < 100:
		for i in range(len(car) // 6):
			cars[0][0] = car[0 + i * 6]
			cars[0][1] = car[1 + i * 6]
			cars[1][0] = car[2 + i * 6]
			cars[1][1] = car[3 + i * 6]
			cars[2][0] = car[4 + i * 6]
			cars[2][1] = car[5 + i * 6]
			x1, y1 = car[0 + i * 6], car[1 + i * 6]
			x2, y2 = car[2 + i * 6], car[3 + i * 6]
			x3, y3 = car[4 + i * 6], car[5 + i * 6]
			# print(cars, 'координаты точек') #весь список
			# print(main(x1, y1, x2, y2, x3, y3))#площадь противоположная координата середина(большая сторона)

			if main(x1, y1, x2, y2, x3, y3) is 0:
				area_correct = 0
			else:
				area_correct = 1

			if area_correct == 1:

				x20, y20 = main(x1, y1, x2, y2, x3, y3)[0], main(x1, y1, x2, y2, x3, y3)[1]  # точка
				x10, y10 = main(x1, y1, x2, y2, x3, y3)[2], main(x1, y1, x2, y2, x3, y3)[3]  # середина
				ch = (x10 + x20) // 2
				ch1 = (y10 + y20) // 2
				cv2.circle(img2, (int(ch), int(ch1)), 10, (255, 255, 255), -1)

				if color(ch, ch1) is 0:
					color_correct = 0
				else:
					color_correct = 1
				if color_correct == 1:
					print(dr(cars), 'угол')
					print(x10, y10, 'середина стороны')
					# print(ch, ch1, 'середина внутри')

					print(color(ch, ch1), 'цвет')

					client.send(f'{dr(cars)}/{x10}/{y10}/{color(ch, ch1)}'.encode('utf-8'))

					data = client.recv(1024)
					print(data.decode('utf-8'))
			else:
				pass


	#cv2.imshow('image2', img2)



	if cv2.waitKey(0) & 0xFF == ord('q'):
		cv2.destroyAllWindows()