#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame, sys, thread, time
from pygame.locals import *
from hmc5883 import *
sys.path.append('../MPU-6050')
from mpu6050 import *

rotation = 0

def hmc5883l_read():
	global rotation

	# MPU-6050
	mpu = MPU6050()
	mpu.initialize()
	# calibration data
	mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
	mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

	# HMC5883L
	compass = hmc5883l()
	# calibration data
	compass.calibration_matrix = [  [1.259098, 0.013830, 0.039295],
			[0.01380, 1.245928, -0.018922],
			[0.039295, -0.018922, 1.360489]]
	compass.bias = [11.16, -43.55, -52.62]

	accel_data = mpu.get_accel()
	x_rotation = mpu.get_x_rotation(accel_data)
	y_rotation = mpu.get_y_rotation(accel_data)

	last_time = time.time()
	alpha = 0.85;

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

		x_rotation = alpha*gyro_angle_x + (1.0 - alpha)*mpu.get_x_rotation(accel_data)

		gyro_angle_y = gyro_data['y']*dt + y_rotation
		y_rotation = alpha*gyro_angle_y + (1.0 - alpha)*mpu.get_y_rotation(accel_data)

		rotation = 360 - compass.heading(x_rotation, y_rotation)
		time.sleep(0.01)


FPS = 25
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
    pygame.display.set_caption('HMC5883L & MPU6050')

    thread.start_new_thread(hmc5883l_read,())
    while True:
        runGame()


def runGame():
    global rotation

    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('HMC5883L', True, WHITE)
    img = pygame.image.load('compas.png')
    imgx = 10
    imgy = 10

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
		if event.key == K_ESCAPE:
                    terminate()


        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()

	rotatedSurf1 = pygame.transform.rotate(img, rotation)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
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
