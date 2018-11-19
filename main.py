import OpenGL
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from transformation import *

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
isEnd = False
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

def displayCartesian():
	#Menampilkan sumbu x, y, dan z
	#X Axis
	glPushAttrib(GL_ENABLE_BIT)
	glLineStipple(1, 0xAAAA)
	glEnable(GL_LINE_STIPPLE)
	glColor3f(1.0, 0, 0)
	glBegin(GL_LINES)
	glVertex3fv((-500,0,0))
	glVertex3fv((0,0,0))
	glEnd()
	glPopAttrib()

	glBegin(GL_LINES)
	glVertex3fv((0,0,0))
	glVertex3fv((500,0,0))
	glEnd()

	#Y Axis
	glPushAttrib(GL_ENABLE_BIT)
	glLineStipple(1, 0xAAAA)
	glEnable(GL_LINE_STIPPLE)
	glColor3f(0, 1.0, 0)
	glBegin(GL_LINES)
	glVertex3fv((0,-500,0))
	glVertex3fv((0,0,0))
	glEnd()
	glPopAttrib()

	glBegin(GL_LINES)
	glVertex3fv((0,0,0))
	glVertex3fv((0,500,0))
	glEnd()

	#Z Axis
	glPushAttrib(GL_ENABLE_BIT)
	glLineStipple(1, 0xAAAA)
	glEnable(GL_LINE_STIPPLE)
	glColor3f(0, 0, 1.0)
	glBegin(GL_LINES)
	glVertex3fv((0,0,-500))
	glVertex3fv((0,0,0))
	glEnd()
	glPopAttrib()

	glBegin(GL_LINES)
	glVertex3fv((0,0,0))
	glVertex3fv((0,0,500))
	glEnd()

def input2D():
	#Meminta input untuk objek 2D
	global shape
	N = int(input("Masukkan nilai N\n"))
	if(N > 0):
		print("Masukkan " + str(N) + " buah titik 2 dimensi")
		valid = False
		while(not valid):
			try:
				x, y = map(float, input().split())
				valid = True
			except:
				print("Harap memasukkan 2 buah angka dipisahkan oleh spasi")
		vertices = Matriks([[x/10],[y/10]])
		edges = []
		for i in range(N-1):
			valid = False
			while(not valid):
				try:
					x, y = map(float, input().split())
					valid = True
				except:
					print("Harap memasukkan 2 buah angka dipisahkan oleh spasi")
			vertices.AddColumn([[x/10],[y/10]])
			edges.insert(len(edges),[i,(i+1)%N])
		shape = Object2D(vertices, edges)
	else:
		shape = Object2D(Matriks([[0],[0]]),[])

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
		if(q[0][0] == "rotate"):
			shape.rotate(q[0][1],q[0][2],q[0][3])
		else:
			shape.vertices += q[0][0]
		if(q[0][-1] == 0):
			q.pop(0)

def processCommand(command):
	#Menjalankan command yang telah diberikan
	global q,is3D,isEnd
	if(q):
		print("Sedang terjadi transformasi, silakan tunggu transformasi selesai")
		return
	parsedCommand = command.split(' ')
	func = parsedCommand[0].lower()
	iteration = 500
	try:
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
			if is3D:
				c = float(parsedCommand[4])
				temp.rotate(degree,a,b,c)
			else:
				q.append(["rotate", degree/iteration,a,b,iteration])
		elif(func == "reflect"):
			param = parsedCommand[1]
			temp.reflect(param)
		elif(func == "shear"):
			param = parsedCommand[1]
			k = float(parsedCommand[2])
			if is3D:
				k2 = float(parsedCommand[3])
				temp.shear(param,k,k2)
			else:
				temp.shear(param,k)
		elif(func == "stretch"):
			param = parsedCommand[1]
			k = float(parsedCommand[2])
			if is3D:
				k2 = float(parsedCommand[3])
				temp.stretch(param,k,k2)
			else:
				temp.stretch(param,k)
		elif(func == "custom"):
			a = float(parsedCommand[1])
			b = float(parsedCommand[2])
			c = float(parsedCommand[3])
			d = float(parsedCommand[4])
			if is3D:
				e = float(parsedCommand[5])
				f = float(parsedCommand[6])
				g = float(parsedCommand[7])
				h = float(parsedCommand[8])
				i = float(parsedCommand[9])
				temp.custom(a,b,c,d,e,f,g,h,i)
			else:
				temp.custom(a,b,c,d)
		elif(func == "help"):
			commandList()
			return
		elif(func == "reset"):
			temp.reset()
		elif(func == "exit"):
			glutLeaveMainLoop()
			isEnd = True
			return
		else:
			print("Command tidak valid, silakan ulangi")
			return

		if(func != "rotate"):
			temp.vertices -= shape.vertices
			temp.vertices.M /= iteration
			q.append([temp.vertices,iteration])
	except:
		print("Terdapat parameter yang salah, silakan ulangi")

def keyPressed(key, x, y):
	#Menampilkan output pada terminal saat OpenGL telah dijalankan
	global currentCommand
	if(ord(key) == 13): #Newline
		print(end='\n',flush=True)
		processCommand(currentCommand)
		currentCommand = ""
		if(not isEnd):
			transformationInput()
		return
	elif(ord(key) == 8): #Backspace
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
	
	displayCartesian()
	gluLookAt(eyeX, eyeY, eyeZ, eyeX, eyeY, -1.0, 0.0, 1.0,  0.0);
	displayObject()
	gluLookAt(0, 0, 0, 0, 0, -1.0, 0.0, 1.0,  0.0);
	gluLookAt(eyeX, eyeY, eyeZ, eyeX, eyeY, -1.0, 0.0, 1.0,  0.0);
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
		print("reflect <param>: Melakukan pencerminan objek. Nilai param adalah salah satu dari nilai-nilai berikut: x, y, y=x, y=-x, atau (a,b). Nilai (a,b) adalah titik untuk melakukan pencerminan terhadap.")
		print("shear <param> <k>: Melakukan operasi shear pada objek. Nilai param dapat berupa x (terhadap sumbu x) atau y (terhadap sumbu y). Nilai k adalah faktor shear.")
		print("stretch <param> <k>: Melakukan operasi stretch pada objek. Nilai param dapat berupa x (terhadap sumbu x) atau y (terhadap sumbu y). Nilai k adalah faktor stretch.")
		print("Melakukan transformasi linier pada objek dengan matriks transformasi [[a,b],[c,d]]")
		print("reset: Mengembalikan objek pada kondisi awal objek didefinisikan.")
		print("exit: Keluar dari program.")
	else:
		print("translate <dx> <dy> <dz>: Melakukan translasi objek dengan menggeser nilai x sebesar dx, menggeser nilai y sebesar dy, dan menggeser nilai z sebesar dz.")
		print("dilate <k>: Melakukan dilatasi objek dengan faktor scaling k.")
		print("rotate <deg> <a> <b> <c>: Melakukan rotasi objek terhadap sumbu x y atau z dengan parameter a = 1 jika terhadap sumbu x, b = 1 jika terhadap sumbu y, dan c = 1 jika terhadap sumbu z")
		print("reflect <param>: Melakukan pencerminan objek. Nilai param adalah salah satu dari nilai-nilai berikut: xy, xz, yz, atau titik origin (0,0,0).")
		print("shear <param> <k1> <k2>: Melakukan operasi shear pada objek. Nilai param dapat berupa x (terhadap sumbu x), y (terhadap sumbu y), atau z (terhadap sumbu z). Nilai k1 dan k2 adalah faktor shear terhadap sumbu bukan param.")
		print("stretch <param> <k1> <k2>: Melakukan operasi stretch pada objek. Nilai param dapat berupa x (terhadap sumbu x), y (terhadap sumbu y), atau z (terhadap sumbu z). Nilai k1 dan k2 adalah faktor stretch terhadap sumbu bukan param.")
		print("Melakukan transformasi linier pada objek dengan matriks transformasi [[a,b,c],[d,e,f],[g,h,i]]")
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
