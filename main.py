# Receive point
# Create display
# Create point
# Receive Operation
# Update display

import OpenGL
import random
from transformation import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import transformation

vertices = []
edges = []
is2D = False
is3D = False
window_name = 'cartesian'
currentCommand = ""
moveX = 0.1
moveY = 0.1
moveZ = 0.1
eyeX = 0
eyeY = 0
eyeZ = 0

def displayObject():
	#Menampilkan object saat ini
	shape.output()

def displayCartesian2D():
	#Menampilkan sumbu x dan y
	glColor3f(1.0, 1.0, 1.0)
	glBegin(GL_LINES)
	glVertex3fv((-500,0,0))
	glVertex3fv((500,0,0))
	glEnd()
	glBegin(GL_LINES)
	glVertex3fv((0,-500,0))
	glVertex3fv((0,500,0))
	glEnd()

def displayCartesian3D():
	#Menampilkan sumbu x, y, dan z
	glColor3f(0.0, 0.0, 0.0)
	glBegin(GL_LINES)
	glVertex3fv((-1,0,0))
	glVertex3fv((1,0,0))
	glEnd()
	glBegin(GL_LINES)
	glVertex3fv((0,-1,0))
	glVertex3fv((0,1,0))
	glEnd()
	glBegin(GL_LINES)
	glVertex3fv((0,0,-1))
	glVertex3fv((0,0,1))
	glEnd()

def input2D():
	#Meminta input untuk objek 2D
	global shape
	N = int(input("Masukkan nilai N\n"))
	print("Masukkan " + str(N) + " buah titik 2 dimensi")
	for i in range(N):
		x, y = map(float, input().split())
		z = 0
		arr = [x/10,y/10,z]
		vertices.insert(len(vertices), arr)
		edges.insert(len(edges),[i,(i+1)%N])
	shape = Object2D(vertices, edges)

def input3D():
	#Meminta input untuk objek 3D
	global shape
	N = int(input("Masukkan nilai N\n"))
	print("Masukkan " + str(N) + " buah titik 3 dimensi")
	for i in range(N):
		x, y, z = map(float, input().split())
		arr = [x/25,y/25,z/25]
		vertices.insert(len(vertices), arr)
		edges.insert(len(edges),[i,(i+1)%N])
	shape = Object3D(vertices, edges)

def inputDimensionChoice():
	#Meminta input dimensi yang diinginkan
	global is2D,is3D
	x = int(input("Keluarkan 2 jika ingin 2 dimensi, dan 3 jika ingin 3D\n"))
	while(x != 2 and x != 3):
		print("Masukkan salah")
		x = int(input("Keluarkan 2 jika ingin 2 dimensi, dan 3 jika ingin 3D\n"))
	if(x == 2):
		is2D = True
	else:
		is3D = True

def keyPressed(key, x, y):
	#Menampilkan output pada terminal saat OpenGL telah dijalankan
	global currentCommand
	if(key == "\n"):
		currentCommand = ""
		print('\n', end='\n', flush=True)
		return
	elif(ord(key) == 8):
		key = '\b \b'
		print('\b \b', end='', flush=True)
		currentCommand = currentCommand[:-1]
	else:
		currentCommand += key.decode('utf-8')
		print(key.decode('utf-8'), end='', flush=True)

def specialKey(key, x, y):
	global eyeX,eyeY,eyeZ,moveX,moveY,moveZ
	if(key == GLUT_KEY_UP):
		eyeY += moveY
	elif(key == GLUT_KEY_DOWN):
		eyeY -= moveY
	elif(key == GLUT_KEY_LEFT):
		eyeX -= moveX
	elif(key == GLUT_KEY_RIGHT):
		eyeX += moveX
	elif(key == GLUT_KEY_F1):
		eyeZ += moveZ
	elif(key == GLUT_KEY_F2):
		eyeZ -= moveZ

def display():
	#Menampilkan objek dan sumbu kartesius
	global eyeX, eyeY, eyeZ, is2D
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	if(is2D):
		gluLookAt(eyeX, eyeY, eyeZ, eyeX, eyeY, -1.0, 0.0, 1.0,  0.0);
		displayCartesian2D()
		displayObject()
		gluLookAt(0, 0, 0, 0, 0, -1.0, 0.0, 1.0,  0.0);
	else:
		gluLookAt(0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0,  0.0);
		displayCartesian3D()
		displayObject()
	eyeX = 0
	eyeY = 0
	eyeZ = 0
	glutSwapBuffers()
	glutPostRedisplay()
	return

def changeSize(w, h):
	#Menormalisasi windows saat terjadi perubahan skala
	if(h == 0):
		h = 1
	ratio = 1.0* w / h
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glViewport(0, 0, w, h)
	gluPerspective(45,ratio,1,1000)
	glMatrixMode(GL_MODELVIEW)

def transformationInput():
	print("Masukkan transformasi yang diinginkan")
	print(">>> ", end='')

def openGLDisplay():
	#Menampilkan tampilan openGL
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(600,600)
	glutInitWindowPosition(0,0)
	glutCreateWindow(window_name)
	glutDisplayFunc(display)
	#glutReshapeFunc(changeSize)
	glutKeyboardFunc(keyPressed)
	transformationInput()
	glutSpecialFunc(specialKey)
	glutMainLoop()
	return

def outputInstructions():
	print("Selamat datang di simulasi transformari geometri")
	print("Untuk berpindah-pindah di ruang kartesian, silakan menekan arrow keys pada keyboard")

def main():
	outputInstructions()
	inputDimensionChoice()
	if(is2D):
		input2D()
	else:
		input3D()
	openGLDisplay()

main()
