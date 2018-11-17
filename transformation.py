from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin,cos,radians
import random
import numpy as np


class Matriks:

	def __init__(self,m = [[0]]):
		# Inisialisasi semua elemen matriks diisi 0
		self.M = np.array(m)
		self.brs = np.size(m,0)
		self.kol = np.size(m,1)

	def AddRow(self,m):
		self.M = np.append(self.M,m,axis = 0)
		self.brs += 1

	def AddColumn(self,m):
		self.M = np.append(self.M,m,axis = 1)
		self.kol += 1

	def GetNBrsEff(self):
		return self.brs

	def GetNKolEff(self):
		return self.kol

	def GetElmt(self,brs,kol):
		return self.M[brs,kol]

	def SetElmt(self,brs,kol,x):
		self.M[brs,kol] = x

	def transpose(self):
		m, n = self.kol, self.brs
		mat = Matriks([[self.GetElmt(j,i) for j in range (n)] for i in range (m)])
		return mat

	def __str__(self):
		s = ""
		for i in range(self.brs):
			for j in range(self.kol):
				s += "%f" % self.GetElmt(i, j)
				if (j<self.kol-1):
					s += " "
				else:
					s += "\n"
		return s

	def __add__(self, mat):
		# Penjumlahan matriks
		mhsl = Matriks([[0]*self.GetNKolEff() for x in range(self.GetNBrsEff())])
		mhsl.M = self.M + mat.M
		return mhsl

	def __sub__(self, mat):
		# Pengurangann matriks
		mhsl = Matriks([[0]*self.GetNKolEff() for x in range(self.GetNBrsEff())])
		mhsl.M = self.M - mat.M
		return mhsl

	def __mul__(self,m1):
		# Mengali matriks ini dengan matriks lain tanpa mengubah value keduanya
		# Input selalu benar : neff kolom Matriks ini = neff baris matriks lainnya
		mat = Matriks(np.matmul(self.M,m1.M))
		return mat

class Object():

	initVertices = Matriks()
	vertices = Matriks()
	edges = Matriks()

	# Object
	def __init__(self, vertices, edges):
		self.vertices = vertices
		self.initVertices = vertices
		self.edges = edges

	def reset(self):
		self.vertices = self.initVertices


class Object2D(Object):
	def translate(self, dx, dy):
		#Melakukan translasi tiap point sejauh dx,dy
		mhsl = Matriks([[self.vertices.GetElmt(i,j) for j in range(self.vertices.GetNKolEff())] for i in range(self.vertices.GetNBrsEff())])
		mhsl.AddRow([[1]*mhsl.GetNKolEff()])
		mtrans = Matriks([[1,0,dx],[0,1,dy],[0,0,1]])
		mhsl = mtrans*mhsl
		for i in range(mhsl.brs-1): #buang baris terakhir
			for j in range(mhsl.kol):
				self.vertices.SetElmt(i,j,mhsl.GetElmt(i,j))

	def dilate(self, k):
		#Melakukan dilatasi tiap point sebesar k
		mtrans = Matriks([[k,0],[0,k]])
		self.vertices = mtrans*self.vertices

	def rotate(self, deg, a, b):
		#Melakukan rotasi tiap titik dengan deg derajat dengan titik pusat (a,b)
		angle = radians(deg)
		mtrans = Matriks([[cos(angle),-1*sin(angle)],[sin(angle),cos(angle)]])
		mpusat = Matriks([[a/10]*self.vertices.GetNKolEff(),[b/10]*self.vertices.GetNKolEff()])
		self.vertices = mtrans*(self.vertices - mpusat) + mpusat

	def reflect(self, param):
		#Melakukan refleksi dengan parameter
		if (param == "y"):
			mtrans = Matriks([[-1,0],[0,1]])
			self.vertices = mtrans*self.vertices
		elif (param == "x"):
			mtrans = Matriks([[1,0],[0,-1]])
			self.vertices = mtrans*self.vertices
		elif (param == "y=x"):
			mtrans = Matriks([[0,1],[1,0]])
			self.vertices = mtrans*self.vertices
		elif (param == "y=-x"):
			mtrans = Matriks([[0,-1],[-1,0]])
			self.vertices = mtrans*self.vertices
		else : # pencerminan (a,b) = rotasi 180 derajat terhadap titik a,b
			p = param.split(',')
			p[0] = p[0].replace(' ',"") # menghapus spasi apabila ada
			p[0] = p[0].replace('(',"") # menghapus kurung apabila ada
			p[1] = p[1].replace(' ',"") # menghapus spasi apabila ada
			p[1] = p[1].replace(')',"") # menghapus kurung apabila ada
			a = float(p[0])
			b = float(p[1])
			mtrans = Matriks([[-1,0],[0,-1]])
			mpusat = Matriks([[a/10]*self.vertices.GetNKolEff(),[b/10]*self.vertices.GetNKolEff()])
			self.vertices = mtrans*(self.vertices-mpusat)+mpusat

	def shear(self, param, k):
		#Melakukan operasi shear pada objek
		if (param == "x"):
			mtrans = Matriks([[1,k],[0,1]])
		elif (param == "y"): #y
			mtrans = Matriks([[1,0],[k,1]])
		self.vertices = mtrans*self.vertices

	def stretch(self, param, k):
		#Melakukan operasi stretch pada objek
		if (param == "x"):
			mtrans = Matriks([[1,0],[0,k]])
		elif (param == "y"): #y
			mtrans = Matriks([[k,0],[0,1]])
		self.vertices = mtrans*self.vertices

	def custom(self, a, b, c, d):
		#Melakukan transformasi dengan matriks [[a,b][c,d]]
		mtrans = Matriks([[a,b],[c,d]])
		self.vertices = mtrans * self.vertices

	def multiple(self, n):
		#Melakukan n buah transformasi
		return

	def output(self):
		glColor3f(random.random(),random.random(),random.random())
		glBegin(GL_POLYGON)
		for edge in self.edges:
			for vertex in edge:
				glVertex2fv(self.vertices.transpose().M[vertex])
		glEnd()

class Object3D(Object):
	def translate(self, dx, dy, dz):
		mhsl = Matriks([[self.vertices.GetElmt(i,j) for j in range(self.vertices.GetNKolEff())] for i in range(self.vertices.GetNBrsEff())])
		mhsl.AddRow([[1]*mhsl.GetNKolEff()])
		mtrans = Matriks([[1,0,0,dx],[0,1,0,dy],[0,0,1,dz],[0,0,0,1]])
		mhsl = mtrans*mhsl
		for i in range(mhsl.brs-1): #buang baris terakhir
			for j in range(mhsl.kol):
				self.vertices.SetElmt(i,j,mhsl.GetElmt(i,j))

	def dilate(self, k):
		mtrans = Matriks([[k,0,0],[0,k,0],[0,0,k]])
		self.vertices = mtrans*self.vertices

	def rotate(self, deg, a, b, c):
		# rotasi terhadap sumbu x apabila a = 1
		angle = radians(deg)
		if (a == 1):
			mtrans = Matriks([[1,0,0],[0,cos(angle),-1*sin(angle)],[0,sin(angle),cos(angle)]])
		elif (b == 1):
			mtrans = Matriks([[cos(angle),0,sin(angle)],[0,1,0],[-1*sin(angle),0,cos(angle)]])
		elif (c == 1):
			mtrans = Matriks([[cos(angle), -1*sin(angle),0],[sin(angle), cos(angle),0],[0,0,1]])
		self.vertices = mtrans*self.vertices


	def reflect(self, param):
		if (param == "xy"):
			mtrans = Matriks([[1,0,0],[0,1,0],[0,0,-1]])
		elif (param == "xz"):
			mtrans = Matriks([[1,0,0],[0,-1,0],[0,0,1]])
		elif (param == "yz"):
			mtrans = Matriks([[-1,0,0],[0,1,0],[0,0,1]])
		self.vertices = mtrans*self.vertices


	def shear(self, param, k1 =0 ,k2=0):
		# Bentuk matriks transformasinya : [[1 sh(yx) sh (zx)],[sh(xy),1,sh(zy)],[sh(xz),sh(yz),1]]
		if (param == "x"):
			mtrans = Matriks([[1,0,0],[k1,1,0],[k2,0,1]])
		elif (param == "y"):
			mtrans = Matriks([[1,k1,0],[0,1,0],[0,k2,1]])
		elif (param == "z"):
			mtrans = Matriks([[1,0,k1],[0,1,k2],[0,0,1]])
		elif (param == "o"):
			mtrans = Matriks([[-1,0,0],[0,-1,0],[0,0,-1]])
		self.vertices = mtrans * self.vertices


	def stretch(self, param, k1=1,k2=1):
		if (param == "x"):
			mtrans = Matriks([[1,0,0],[0,k1,0],[0,0,k2]])
		elif (param == "y"):
			mtrans = Matriks([[k1,0,0],[0,1,0],[0,0,k2]])
		elif (param == "z"):
			mtrans = Matriks([[k1,0,0],[0,k2,0],[0,0,1]])
		self.vertices = mtrans * self.vertices

	def custom(self, a, b, c, d, e, f, g, h, i):
		mtrans = Matriks([[a,b,c],[d,e,f],[g,h,i]])
		self.vertices = mtrans * self.vertices

	def multiple(self, n):
		#for x in range(n)
			#...
		return

	def output(self):
		glColor3f(1.0,1.0,1.0)
		glBegin(GL_POLYGON)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.vertices.M[vertex])
		glEnd()


# Ini contoh cara memakai
if __name__ == "__main__":
	n = int(input("Input N : "))
	x = float(input("x : "))
	y = float(input("y : "))
	v = Matriks([[x],[y]])
	for x in range(n-1):
		x = float(input("x : "))
		y = float(input("y : "))
		v.AddColumn([[x],[y]])
	dua = Object2D(v,[[0]])
	menu = 0
	while (menu != 10):
		print("Pilih menu : ")
		print("1. Translasi\n2. Dilatasi\n3. Rotasi\n4. Refleksi\n5. Shear\n6. Stretch\n7. Custom\n8. Print\n9. Transpos\n10. Keluar")
		menu = int(input("Pilih : "))
		if (menu == 1):
			dx = float(input("dx : "))
			dy = float(input("dy : "))
			dua.translate(dx,dy)
			print(dua.vertices)
		elif (menu == 2):
			k = float(input("k : "))
			dua.dilate(k)
			print(dua.vertices)
		elif (menu == 3):
			d = float(input("sudut : "))
			a = float(input("pusat x : "))
			b = float(input("pusat y : "))
			dua.rotate(d,a,b)
			print(dua.vertices)
		elif (menu == 4):
			param = input("refleksi terhadap : ")
			dua.reflect(param)
			print(dua.vertices)
		elif (menu == 5):
			k = float(input("k : "))
			param = input("shear terhadap : ")
			dua.shear(param,k)
			print(dua.vertices)
		elif (menu == 6):
			k = float(input("k : "))
			param = input("stretch terhadap : ")
			dua.stretch(param,k)
			print(dua.vertices)
		elif (menu == 7):
			a = float(input("a : "))
			b = float(input("b : "))
			c = float(input("c : "))
			d = float(input("d : "))
			dua.custom(a,b,c,d)
			print(dua.vertices)
		elif (menu == 8) :
			print(dua.vertices)
		elif (menu == 9):
			m = dua.vertices.transpose()
			print(m)
		elif (menu != 10) :
			print("Input tidak valid!")
