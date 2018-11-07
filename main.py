# Receive point
# Create display
# Create point
# Receive Operation
# Update display

import OpenGL
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import transformation

vertices = []
edges = []
is2D = False
is3D = False
window_name = 'cartesian'
angle = 0.0
lx = 0.0
lz = -1.0
x = 0.0
z = 5.0

def displayObject2D():
	#Menampilkan object saat ini
    glColor3f(random.random(),random.random(),random.random())
    glBegin(GL_POLYGON)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def displayObject3D():
	return

def displayCartesian2D():
	#Menampilkan sumbu x dan y
	glColor3f(0.0, 0.0, 0.0)
	glBegin(GL_LINES)
	glVertex3fv((-1,0,0))
	glVertex3fv((1,0,0))
	glEnd()
	glBegin(GL_LINES)
	glVertex3fv((0,-1,0))
	glVertex3fv((0,1,0))
	glEnd()

def displayCartesian3D():
	return


def input2D():
	is2D = True
	N = int(raw_input("Masukkan nilai N\n"))
	print "Masukkan " + str(N) + " buah titik 2 dimensi"
	for i in range(N):
		print i
		x, y = map(float, raw_input().split())
		z = 0
		arr = [x/25,y/25,z]
		print arr
		vertices.insert(len(vertices), arr)
		edges.insert(len(edges),[i,(i+1)%N])

def input3D():
	is3D = True
	return

def main():
    input2D()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutCreateWindow(window_name)
    glutDisplayFunc(display)

    #glutReshapeFunc(changeSize)
    glutMainLoop()
    return

def display():
	glClearColor(1.0, 1.0, 1.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glPushMatrix()
	if(is2D):
		gluLookAt(0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0,  0.0);
		displayCartesian2D()
		displayObject2D()
	else:
		displayCartesian3D()
		displayObject3D()

	glPopMatrix()
	glutSwapBuffers()
	return

def changeSize(w, h):
	if(h == 0):
		h = 1
	ratio = 1.0* w / h
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glViewport(0, 0, w, h)
	gluPerspective(45,ratio,1,1000)
	glMatrixMode(GL_MODELVIEW)

main()