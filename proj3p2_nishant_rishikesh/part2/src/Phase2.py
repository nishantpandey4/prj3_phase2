import math
import numpy as np
from heapq import heappush, heappop
import time
import matplotlib.pyplot as plt
import argparse
class Obstacle():
	def __init__(self, width = 6, height = 2, r = 1, c = 1, threshold=0.01, 
			thetaStep = 30, actions=None, wheelLength = 1, 
			wheelRadius = 1):
		self.threshold = threshold                                                # Resolution
		self.W = int(width/threshold) +1
		self.H = int(height/threshold) +1
		self.r = r
		self.c = c
		self.thetaStep = thetaStep
		self.explored = np.zeros([self.H, self.W, 4])
		self.actionIndexMatrix = np.zeros([self.H, self.W])
		self.plotData_X = []
		self.plotData_Y = []
		self.plotData_A = []
		self.plotData_U = []
		self.plotData_V = []
		self.whcihAction = []
		plt.ion()
		self.fig, self.ax = plt.subplots()
		plt.gca().set_aspect('equal',adjustable='box')
		self.plotSpace()
		self.actions = actions
		self.wheelRadius = wheelRadius
		self.wheelLength = wheelLength

	
		
	def plotSpace(self):
		centX, centY, radii = 3.5,0.1,0.5
		circle_1_X = [centX+radii*math.cos(i) for i in np.arange(0,2*math.pi,0.01)]
		circle_1_Y = [centY+radii*math.sin(i) for i in np.arange(0,2*math.pi,0.01)]

		quad_1_x, quad_1_y = [1, 1.15, 1.15, 1, 1],[ -0.25,  -0.25,  1.00,  1.00,  -0.25]
		quad_2_x, quad_2_y = [2, 2.15, 2.15, 2, 2],[ -1.0, -1.0, 0.25, 0.25,  -1.0]
		self.ax.plot(circle_1_X, circle_1_Y)
		self.ax.plot(quad_1_x, quad_1_y)
		self.ax.plot(quad_2_x, quad_2_y)
		self.ax.set_xlim(-0.5, 5.5)
		self.ax.set_ylim(-1, 1)
		pass

	def checkObstcaleSpace(self):
		xx = np.arange(-0.5,5.5,0.05)
		yy = np.arange(-1,1,0.05)
		x_ = []
		y_ = []
		for x in xx:
			for y in yy:
				if self.ObsCheck(x,y):
					x_.append(x)
					y_.append(y)
		plt.scatter(x_, y_, s=0.1)
		plt.show()
		pass

	def ObsCheck(self, i, j):
		if self.checkBoundary(i,j):
			# print("false boundary")
			return False
		elif self.checkInCircle(i, j, (3.5,0.1), 0.5):
			# print('false1')
			return False
		elif self.checkInQuad(i, j, 1.0, 1.15, 1.00, -0.25):
			# print('false2')
			return False
		elif self.checkInQuad(i, j, 2.0, 2.15, 0.25, -1.0):
			# print('false3')
			return False
		else:
			return True

	def checkInQuad(self, i, j, left, right, top, bottom):
		l_ = left - self.r - self.c
		r_ = right + self.r + self.c
		t_ = top + self.r + self.c
		b_ = bottom - self.r - self.c
		if (i<r_ and i>l_ and j<t_ and j>b_):
			return True
		else:
			return False

	def checkInCircle(self, i, j, center, radius):
		center_x, center_y = center[0], center[1]
		if ((i - center_x) ** 2 + (j - center_y) ** 2) <= (radius + self.r + self.c) ** 2:
			return True
		else:
			return False

	def checkBoundary(self,i,j):
		# print(i,j)
		if (i < (5.5 - self.r - self.c) and  
			i > (-0.5 + self.r + self.c) and 
			j < (1 - self.r - self.c) and  
			j > (-1 +self.r + self.c)):
			return False
		return True
