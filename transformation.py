from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin,cos,radians
import random
import numpy as np


class Matriks:
	
	def __init__(self,brs=1,kol=1):
		# Inisialisasi semua elemen matriks diisi 0
		self.M = np.array([[0.0]*kol for x in range(brs)])
		self.brs = brs
		self.kol = kol

	def BangunMatriks(self,m):
		# Konstruktor kedua yang membuat matriks baru
		self.M = np.array(m)
		self.brs = np.size(m,0)
		self.kol = np.size(m,1)
	
	def GetNBrsEff(self):
		return self.brs

	def GetNKolEff(self):
		return self.kol

	def GetElmt(self,brs,kol):
		return self.M[brs,kol]

	def SetElmt(self,brs,kol,x):
		self.M[brs,kol] = x

	def __str__(self):
		s = ""
		for i in range(self.brs):
			for j in range(self.kol):
				s += "%.3f" % self.GetElmt(i, j)
				if (j<self.kol-1):
					s += " "
				else:
					s += "\n"
		return s

	def __add__(self, mat):
		# Penjumlahan matriks
		mhsl = Matriks(self.brs,self.kol)
		mhsl.M = self.M + mat.M
		return mhsl

	def __sub__(self, mat):
		# Pengurangann matriks
		mhsl = Matriks(self.brs,self.kol)
		mhsl.M = self.M - mat.M
		return mhsl

	def __mul__(self,m1):
		# Mengali matriks ini dengan matriks lain tanpa mengubah value keduanya
		# Input selalu benar : neff kolom Matriks ini = neff baris matriks lainnya
		mhsl = Matriks(self.GetNBrsEff(),m1.GetNKolEff())
		sum = 0.0
		for i in range(mhsl.GetNBrsEff()):
			for j in range(mhsl.GetNKolEff()):
				for k in range (self.GetNKolEff()):
					sum += self.GetElmt(i,k) * m1.GetElmt(k,j)
				mhsl.SetElmt(i,j,sum)
				sum = 0.0
		return mhsl

class Object():

	initVertices = Matriks()
	vertices = Matriks()
	edges = Matriks()

	# Object
	def __init__(self, vertices, edges):
		self.vertices = vertices
		self.initVertices = vertices
		self.edges = edges

	def output(self):
		glColor3f(random.random(),random.random(),random.random())
		glBegin(GL_POLYGON)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.vertices[vertex])
		glEnd()


class Object2D(Object):
	def translate(self, dx, dy):
		#Melakukan translasi tiap point sejauh dx,dy
		mhsl = Matriks()
		mhsl.BangunMatriks([[self.vertices.GetElmt(0,0)],[self.vertices.GetElmt(1,0)],[1]])
		mtrans = Matriks()
		mtrans.BangunMatriks([[1,0,dx],[0,1,dy],[0,0,1]])
		mhsl = mtrans*mhsl
		for i in range(mhsl.brs-1): #buang baris terakhir
			for j in range(mhsl.kol):
				self.vertices.SetElmt(i,j,mhsl.GetElmt(i,j))

	def dilate(self, k):
		#Melakukan dilatasi tiap point sebesar k
		mtrans = Matriks()
		mtrans.BangunMatriks([[k,0],[0,k]])
		self.vertices = mtrans*self.vertices 

	def rotate(self, deg, a, b):
		#Melakukan rotasi tiap titik dengan deg derajat dengan titik pusat (a,b)
		angle = radians(deg)
		mtrans = Matriks()
		mtrans.BangunMatriks([[cos(angle),-1*sin(angle)],[sin(angle),cos(angle)]])
		mpusat = Matriks()
		mpusat.BangunMatriks([[a],[b]])
		self.vertices = mtrans*(self.vertices - mpusat) + mpusat 

	def reflect(self, param):
		#Melakukan refleksi dengan parameter
		mtrans = Matriks()
		if (param == "y"):
			mtrans.BangunMatriks([[-1,0],[0,1]])
			self.vertices = mtrans*self.vertices
		elif (param == "x"):
			mtrans.BangunMatriks([[1,0],[0,-1]])
			self.vertices = mtrans*self.vertices
		elif (param == "y=x"):
			mtrans.BangunMatriks([[0,1],[1,0]])
			self.vertices = mtrans*self.vertices
		elif (param == "y=-x"):
			mtrans.BangunMatriks([[0,-1],[-1,0]])
			self.vertices = mtrans*self.vertices
		else : # pencerminan (a,b) = rotasi 180 derajat terhadap titik a,b
			p = param.split(',')
			p[0] = p[0].replace(' ',"") # menghapus spasi apabila ada
			p[0] = p[0].replace('(',"") # menghapus kurung apabila ada
			p[1] = p[1].replace(' ',"") # menghapus spasi apabila ada
			p[1] = p[1].replace(')',"") # menghapus kurung apabila ada
			a = float(p[0])
			b = float(p[1])
			angle = 180
			mtrans.BangunMatriks([[a],[b]])
			self.rotate(self.vertices,mtrans,angle)
		
	def shear(self, param, k):
		#Melakukan operasi shear pada objek
		mtrans = Matriks()
		if (param == "x"):
			mtrans.BangunMatriks([[1,k],[0,1]])
		elif (param == "y"): #y
			mtrans.BangunMatriks([[1,0],[k,1]])
		self.vertices = mtrans*self.vertices

	def stretch(self, param, k):
		#Melakukan operasi stretch pada objek
		mtrans = Matriks()
		if (param == "x"):
			mtrans.BangunMatriks([[1,0],[0,k]])
		elif (param == "y"): #y
			mtrans.BangunMatriks([[k,0],[0,1]])
		self.vertices = mtrans*self.vertices

	def custom(self, a, b, c, d):
		#Melakukan transformasi dengan matriks [[a,b][c,d]]
		mtrans = Matriks()
		mtrans.BangunMatriks([[a,b],[c,d]])
		self.vertices = mtrans * self.vertices

	def multiple(self, n):
		#Melakukan n buah transformasi
		return

class Object3D(Object):
	def translate(self, dx, dy, dz):	
		mhsl = Matriks()
		mhsl.BangunMatriks([[self.vertices.GetElmt(0,0)],[self.vertices.GetElmt(1,0)],[self.vertices.GetElmt(2,0)],[1]])
		mtrans = Matriks()
		mtrans.BangunMatriks([[1,0,0,dx],[0,1,0,dy],[0,0,1,dz],[0,0,0,1]])
		mhsl = mtrans*mhsl
		for i in range(mhsl.brs-1): #buang baris terakhir
			for j in range(mhsl.kol):
				self.vertices.SetElmt(i,j,mhsl.GetElmt(i,j))

	def dilate(self, k):
		mtrans = Matriks()
		mtrans.BangunMatriks([[k,0,0],[0,k,0],[0,0,k]])
		self.vertices = mtrans*self.vertices

	def rotate(self, deg, a, b, c):
		# rotasi terhadap sumbu x apabila a = 1
		angle = radians(deg)
		mtrans = Matriks()
		if (a == 1):
			mtrans.BangunMatriks([[1,0,0],[0,cos(angle),-1*sin(angle)],[0,sin(angle),cos(angle)]])
		elif (b == 1):
			mtrans.BangunMatriks([[cos(angle),0,sin(angle)],[0,1,0],[-1*sin(angle),0,cos(angle)]])
		elif (c == 1):
			mtrans.BangunMatriks([[cos(angle), -1*sin(angle),0],[sin(angle), cos(angle),0],[0,0,1]])
		self.vertices = mtrans*self.vertices


	def reflect(self, param):
		mtrans = Matriks()
		if (param == "xy"):
			mtrans.BangunMatriks([[1,0,0],[0,1,0],[0,0,-1]])
		elif (param == "xz"):
			mtrans.BangunMatriks([[1,0,0],[0,-1,0],[0,0,1]])
		elif (param == "yz"):
			mtrans.BangunMatriks([[-1,0,0],[0,1,0],[0,0,1]])
		self.vertices = mtrans*self.vertices


	def shear(self, param, k):
		# Bentuk matriks transformasinya : [[1 sh(yx) sh (zx)],[sh(xy),1,sh(zy)],[sh(xz),sh(yz),1]]
		mtrans = Matriks()
		if (param == "x"):
			mtrans.BangunMatriks([[1,0,0],[k,1,0],[k,0,1]])
		elif (param == "y"):
			mtrans.BangunMatriks([[1,k,0],[0,1,0],[0,k,1]])
		elif (param == "z"):
			mtrans.BangunMatriks([[1,0,k],[0,1,k],[0,0,1]])
		self.vertices = mtrans * self.vertices
		

	def stretch(self, param, k):
		mtrans = Matriks()
		if (param == "x"):
			mtrans.BangunMatriks([[1,0,0],[0,k,0],[0,0,k]])
		elif (param == "y"):
			mtrans.BangunMatriks([[k,0,0],[0,1,0],[0,0,k]])
		elif (param == "z"):
			mtrans.BangunMatriks([[k,0,0],[0,k,0],[0,0,1]])
		self.vertices = mtrans * self.vertices

	def custom(self, a, b, c, d, e, f, g, h, i):
		mtrans = Matriks()
		mtrans.BangunMatriks([[a,b,c],[d,e,f],[g,h,i]])
		self.vertices = mtrans * self.vertices

	def multiple(self, n):
		#for x in range(n)
			#...
		return
