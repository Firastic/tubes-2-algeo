class Object:

	initPoints = []
	points = []

	#Menginisialisasi Object
	def __init__(self, points, edges):
		self.points = points
		self.initPoints = points


class Object2D(Object):
	def translate(self, dx, dy):
		#Melakukan translasi tiap point sejauh dx,dy

	def dilate(self, k):
		#Melakukan dilatasi tiap point sebesar k

	def rotate(self, deg, a, b):
		#Melakukan rotasi tiap titik dengan deg derajat dengan titik pusat (a,b)

	def reflect(self, param):
		#Melakukan refleksi dengan parameter

	def shear(self, param, k):
		#Melakukan operasi shear pada objek

	def stretch(self, param, k):
		#Melakukan operasi stretch pada objek

	def custom(self, a, b, c, d):
		#Melakukan transformasi dengan matriks [[a,b][c,d]]

	def multiple(self, n):
		#Melakukan n buah transformasi

class Object3D(Object):
	def translate(self, dx, dy, dz):

	def dilate(self, k):

	def rotate(self, deg, a, b, c):

	def reflect(self, param):

	def shear(self, param, k):

	def stretch(self, param, k):

	def custom(self, a, b, c, d, e, f, g, h, i):

	def multiple(self, n):