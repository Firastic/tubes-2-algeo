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
q = []

verticies3d = Matriks([
    ([0.1,-0.1,-0.1]),
    ([0.1,0.1,-0.1]),
    ([-0.1,0.1,-0.1]),
    ([-0.1,-0.1,-0.1]),
    ([0.1,-0.1,0.1]),
    ([0.1,0.1,0.1]),
    ([-0.1,-0.1,0.1]),
    ([-0.1,0.1,0.1])
])

verticies3d = verticies3d.transpose()

edges3d = ([
    [0,1],
    [0,3],
    [0,4],
    [2,1],
    [2,3],
    [2,7],
    [6,3],
    [6,4],
    [6,7],
    [5,1],
    [5,4],
    [5,7]
])

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
	glColor3f(1.0, 1.0, 1.0)
	glBegin(GL_LINES)
	glVertex3fv((-500,0,0))
	glVertex3fv((500,0,0))
	glEnd()
	glBegin(GL_LINES)
	glVertex3fv((0,-500,0))
	glVertex3fv((0,500,0))
	glEnd()
	glBegin(GL_LINES)
	glVertex3fv((0,0,-500))
	glVertex3fv((0,0,500))
	glEnd()

def input2D():
	#Meminta input untuk objek 2D
	global shape
	N = int(input("Masukkan nilai N\n"))
	print("Masukkan " + str(N) + " buah titik 2 dimensi")
	x, y = map(float, input().split())
	vertices = Matriks([[x/10],[y/10]])
	edges = []
	for i in range(N-1):
		x, y = map(float, input().split())
		vertices.AddColumn([[x/10],[y/10]])
		edges.insert(len(edges),[i,(i+1)%N])
	shape = Object2D(vertices, edges)

def input3D():
	#Meminta input untuk objek 3D
	global shape, verticies3d, edges3d
	shape = Object3D(verticies3d, edges3d)

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

def change():
	#Mengubah nilai titik sesuai yang diinginkan secara minimal
	if(q):
		q[0][-1] -= 1
		shape.vertices += q[0][0]
		if(q[0][-1] == 0):
			q.pop(0)

def processCommand(command):
	#Menjalankan command yang telah diberikan
	global q,is3D
	if(q):
		print("Sedang terjadi transformasi, silakan tunggu transformasi selesai")
		return
	parsedCommand = command.split(' ')
	func = parsedCommand[0].lower()
	iteration = 2000
	#try:
	if is3D:
		temp = Object3D(shape.vertices,shape.edges)
	else:
		temp = Object2D(shape.vertices,shape.edges)
	temp.initVertices = shape.initVertices
	if(func == "translate"):
		dx = float(parsedCommand[1])/10
		dy = float(parsedCommand[2])/10
		if is3D:
			dz = float(parsedCommand[3])/10
			temp.translate(dx,dy,dz)
		else:
			temp.translate(dx,dy)
	elif(func == "dilate"):
		k = float(parsedCommand[1])
		temp.dilate(k)
	elif(func == "rotate"):
		degree = float(parsedCommand[1])
		a = float(parsedCommand[2])
		b = float(parsedCommand[3])
		temp.rotate(degree,a,b)
	elif(func == "reflect"):
		param = parsedCommand[1]
		temp.reflect(param)
	elif(func == "shear"):
		param = parsedCommand[1]
		k = float(parsedCommand[2])
		temp.shear(param,k)
	elif(func == "stretch"):
		param = parsedCommand[1]
		k = float(parsedCommand[2])/10
		temp.stretch(param,k)
	elif(func == "custom"):
		a = float(parsedCommand[1])
		b = float(parsedCommand[2])
		c = float(parsedCommand[3])
		d = float(parsedCommand[4])
		a /= 10
		b /= 10
		c /= 10
		d /= 10
		temp.custom(a,b,c,d)
	elif(func == "help"):
		commandList()
		return
	elif(func == "reset"):
		temp.reset()
	elif(func == "exit"):
		exit()
		return
	else:
		print("Command tidak valid, silakan ulangi")
		return
	temp.vertices -= shape.vertices
	temp.vertices.M /= iteration
	q.append([temp.vertices,iteration])
	#except:
	#	print("Terdapat parameter yang salah, silakan ulangi")

def keyPressed(key, x, y):
	#Menampilkan output pada terminal saat OpenGL telah dijalankan
	global currentCommand
	if(ord(key) == 13):
		print(end='\n',flush=True)
		processCommand(currentCommand)
		currentCommand = ""
		transformationInput()
		return
	elif(ord(key) == 8):
		key = '\b \b'
		print('\b \b', end='', flush=True)
		currentCommand = currentCommand[:-1]
	else:
		currentCommand += key.decode('utf-8')
		print(key.decode('utf-8'), end='', flush=True)

def specialKey(key, x, y):
	#Special key untuk menggerakkan kamera
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
		glRotate(5.0,1.0,0.0,1.0)
	elif(key == GLUT_KEY_F2):
		glRotate(-5.0,1.0,0.0,1.0)

def display():
	#Menampilkan objek dan sumbu kartesius
	global eyeX, eyeY, eyeZ, is2D
	change()
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	if(is2D):
		gluLookAt(eyeX, eyeY, eyeZ, eyeX, eyeY, -1.0, 0.0, 1.0,  0.0);
		displayCartesian2D()
		displayObject()
		gluLookAt(0, 0, 0, 0, 0, -1.0, 0.0, 1.0,  0.0);
	else:
		gluLookAt(eyeX, eyeY, eyeZ, eyeX, eyeY, -1.0, 0.0, 1.0,  0.0);
		displayCartesian3D()
		displayObject()
		gluLookAt(0, 0, 0, 0, 0, -1.0, 0.0, 1.0,  0.0);
	eyeX = 0
	eyeY = 0
	eyeZ = 0
	glutSwapBuffers()
	glutPostRedisplay()
	return

def transformationInput():
	#Menampilkan tampilan saat menerima input
	print("Masukkan transformasi yang diinginkan")
	print("Ketik help untuk melihat command yang ada")
	print(">>> ", end='', flush=True)

def commandList():
	#Menampilkan command yang dapat dilakukan
	if(is2D):
		print("translate <dx> <dy>: Melakukan translasi objek dengan menggeser nilai x sebesar dx dan menggeser nilai y sebesar dy.")
		print("dilate <k>: Melakukan dilatasi objek dengan faktor scaling k.")
		print("rotate <deg> <a> <b>: Melakukan rotasi objek secara berlawanan arah jarum jam sebesar deg derajat terhadap titik a,b")
		print("reflect <param>: Melakukan pencerminan objek. Nilai param adalah salah satu dari nilainilai berikut: x, y, y=x, y=-x, atau (a,b). Nilai (a,b) adalah titik untuk melakukan pencerminan terhadap.")
		print("shear <param> <k>: Melakukan operasi shear pada objek. Nilai param dapat berupa x (terhadap sumbu x) atau y (terhadap sumbu y). Nilai k adalah faktor shear.")
		print("stretch <param> <k>: Melakukan operasi stretch pada objek. Nilai param dapat berupa x (terhadap sumbu x) atau y (terhadap sumbu y). Nilai k adalah faktor stretch.")
		print("Melakukan transformasi linier pada objek dengan matriks transformasi [[a,b],[c,d]]")
		print("reset: Mengembalikan objek pada kondisi awal objek didefinisikan.")
		print("exit: Keluar dari program.")

def openGLDisplay():
	#Menampilkan tampilan openGL
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(600,600)
	glutInitWindowPosition(0,0)
	glutCreateWindow(window_name)
	glutDisplayFunc(display)
	glutKeyboardFunc(keyPressed)
	transformationInput()
	glutSpecialFunc(specialKey)
	glutMainLoop()
	return

def outputInstructions():
	##Menampilkan instruksi sebelum permainan
	print("Selamat datang di simulasi transformari geometri")
	print("Untuk berpindah-pindah di ruang kartesian, silakan menekan arrow keys pada keyboard")

def main():
	#Main program
	outputInstructions()
	inputDimensionChoice()
	if(is2D):
		input2D()
	else:
		input3D()
	openGLDisplay()

if __name__=='__main__':
	main()
