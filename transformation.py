from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

class Object:

	initVertices = []
	vertices = []
	edges = []

	#Menginisialisasi Object
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
		return

	def dilate(self, k):
		#Melakukan dilatasi tiap point sebesar k
		return

	def rotate(self, deg, a, b):
		#Melakukan rotasi tiap titik dengan deg derajat dengan titik pusat (a,b)
		return

	def reflect(self, param):
		#Melakukan refleksi dengan parameter
		return

	def shear(self, param, k):
		#Melakukan operasi shear pada objek
		return

	def stretch(self, param, k):
		#Melakukan operasi stretch pada objek
		return

	def custom(self, a, b, c, d):
		#Melakukan transformasi dengan matriks [[a,b][c,d]]
		return

	def multiple(self, n):
		#Melakukan n buah transformasi
		return

class Object3D(Object):
	def translate(self, dx, dy, dz):
		return

	def dilate(self, k):
		return

	def rotate(self, deg, a, b, c):
		return

	def reflect(self, param):
		return

	def shear(self, param, k):
		return

	def stretch(self, param, k):
		return

	def custom(self, a, b, c, d, e, f, g, h, i):
		return

	def multiple(self, n):
		return

	def output(self):
		return