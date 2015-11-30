#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, pygame, sys, thread, time
from pygame.locals import *
from mpu6050 import *

y_offset = 0
rotation = 0

def mpu6050_read():
	global y_offset
	global rotation

	mpu = MPU6050()
	mpu.initialize()

	# Set calibration data
	mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
	mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

	accel_data = mpu.get_accel()
	x_rotation = mpu.get_x_rotation(accel_data)
	y_rotation = mpu.get_y_rotation(accel_data)
	last_time = time.time()
	alpha = 0.98;

	while True:
		new_time = time.time()
		gyro_data = mpu.get_gyro()
		accel_data = mpu.get_accel()

		dt = new_time - last_time
		last_time = new_time
		gyro_angle_x = gyro_data['x']*dt + x_rotation

		if gyro_angle_x > 360:
			gyro_angle_x -= 360
		if gyro_angle_x < 0:
			gyro_angle_x = 360 + gyro_angle_x

		accel_angle_x = mpu.get_x_rotation(accel_data)

		if abs(gyro_angle_x - accel_angle_x) > 180:
			gyro_angle_x = accel_angle_x

		x_rotation = alpha*gyro_angle_x + (1.0 - alpha)*accel_angle_x;

		gyro_angle_y = gyro_data['y']*dt + y_rotation
		y_rotation = alpha*gyro_angle_y + (1.0 - alpha)*mpu.get_y_rotation(accel_data)

		y_offset = y_rotation * 2
                rotation = x_rotation

		time.sleep(0.001)





FPS = 100
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('MPU-6050')

    thread.start_new_thread(mpu6050_read,())
    while True:
        runGame()


def runGame():
    global y_offset
    global rotation

    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('MPU-6050', True, WHITE)

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
		if event.key == K_ESCAPE:
                    terminate()


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()

	rotatedSurf1 = pygame.transform.rotate(titleSurf1, rotation)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + y_offset)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
