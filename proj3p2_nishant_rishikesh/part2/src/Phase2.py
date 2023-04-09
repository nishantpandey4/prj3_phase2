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
def getMatrixIndices(self, node):
		x,y,a = node[1], node[2], node[3]
		shiftx, shifty = 0,0
		x += shiftx
		y = abs(shifty + y)
		i = int(round(y/self.threshold))
		j = int(round(x/self.threshold))
		k = int(round(a/self.thetaStep))
		return i,j,k

	def checkVisited(self, node):
		i,j,k = self.getMatrixIndices(node)
		if self.explored[i, j, 3] != 0:
			return True 
		else:
			return False 

	def findVisited(self, node):
		i,j,k = self.getMatrixIndices(node)
		return self.explored[i, j, :], self.actionIndexMatrix[i,j]

	def addVisited(self, node, parentNode, actionIndex):
		i,j,k = self.getMatrixIndices(node)
		self.plotData_X.append(parentNode[1])
		self.plotData_Y.append(parentNode[2])
		self.plotData_A.append(parentNode[3])
		self.whcihAction.append(actionIndex)
		self.explored[i, j, :] = np.array(parentNode)
		self.actionIndexMatrix[i,j] = actionIndex
		return

	def plotPath(self, path, trackIndex):
		print(len(trackIndex), len(path))
		for i in range(len(path)):
			Xi = path[i][1]
			Yi = path[i][2]
			Thetai = path[i][3]
			actionIndex = int(trackIndex[i])
			UL, UR = self.actions[actionIndex][0], self.actions[actionIndex][1]
			self.plotCurve(Xi, Yi, Thetai, UL, UR, color="red", lw=1.2)
			plt.pause(0.001)
		plt.ioff()
		plt.show(block=False)
		pass

	def explorationPlot(self):
		for i in range(len(self.plotData_X)):
			Xi = self.plotData_X[i]
			Yi = self.plotData_Y[i]
			Thetai = self.plotData_A[i]
			actionIndex = self.whcihAction[i]
			UL, UR = self.actions[actionIndex][0], self.actions[actionIndex][1]
			self.plotCurve(Xi, Yi, Thetai, UL, UR)
			if i%100==0:
				plt.pause(0.000001)
		pass

	def plotCurve(self, Xi, Yi, Thetai, UL, UR,color="blue",lw=0.5):
		r = self.wheelRadius
		L = self.wheelLength
		t = 0
		dt = 0.1
		Xn = Xi
		Yn = Yi
		Thetan = math.pi * Thetai / 180
		x_s, x_n, y_s, y_n = [],[],[],[] 
		while t<1:
			t = t + dt
			Xs = Xn
			Ys = Yn
			Xn += 0.5 * r * (UL + UR) * math.cos(Thetan) * dt
			Yn += 0.5 * r * (UL + UR) * math.sin(Thetan) * dt
			Thetan += (r / L) * (UR - UL) * dt
			x_s.append(Xs)
			x_n.append(Xn)
			y_s.append(Ys)
			y_n.append(Yn)
		self.ax.plot([x_s, x_n], [y_s, y_n], color=color, linewidth=lw)