#! /usr/bin/env python

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'waiter.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal,Qt,pyqtSlot
import time
import Queue

# ROS related Imports
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2


# GUI related Code
class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):
		self.function(*self.args, **self.kwargs)
# GUI Related Code ends

# Navigated related Code starts
speed = Twist()
goal = Point() 

linear=0.6
angular=0.6

x = 0.0
y = 0.0 
theta = 0.0

# odometry callback function
def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

# Navigated related Code ends



class Ui_MainWindow(object): 

	def __init__(self):
		self.threadpool = QtCore.QThreadPool()
		self.threadpool.setMaxThreadCount(1)
		self.q = Queue.Queue(maxsize=20)
		self.worker = None
		# go_on is a variable that helps in breaking out of loops while stopping threads
		# go_on=True means to stop the worker thread
		self.go_on = False 
		self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
		self.return_to_home=False


	# task is just a sample long running function to debug gui without running ROS 
	def task(self,x,y):

		for i in range(10):
			if self.go_on:
				break

			time.sleep(0.5)
			print(linear ," at ",i,"th second and x-y ",x,y)
			print(angular ," at ",i,"th second")

	# Buttons and sliders signal connections below

	def linear_change(self,value):
		global linear
		linear=2*float(value)/100
		self.lcdNumber.display(linear)

	def angular_change(self,value):
		global angular
		angular = 2*float(value)/100
		self.lcdNumber_2.display(angular)
	
	def btn_home_click(self):
		self.label.setText("Returning To Home")
		self.btn_emer_pressed()
		time.sleep(0.5)
		self.go_on=False
		self.worker=Worker(self.go_to,-0.66,0.64)
		self.threadpool.start(self.worker)
	
	def btn_1_click(self):
		self.btn_emer_pressed()
		return_to_home=True
		table_num=1
		time.sleep(0.5)
		self.go_on=False
		self.worker=Worker(self.move_to,return_to_home,table_num,-0.35,0)
		self.threadpool.start(self.worker)
	
	def btn_2_click(self):
		self.btn_emer_pressed()
		return_to_home=True
		table_num=2
		time.sleep(0.5)
		self.go_on=False
		self.worker=Worker(self.move_to,return_to_home,table_num,-0.66,-0.64)
		self.threadpool.start(self.worker)
	
	def btn_3_click(self):
		self.btn_emer_pressed()
		return_to_home=True
		table_num=3
		time.sleep(0.5)
		self.go_on=False
		self.worker=Worker(self.move_to,return_to_home,table_num,0.33,-0.64)
		self.threadpool.start(self.worker)
	
	def btn_4_click(self):
		self.btn_emer_pressed()
		return_to_home=True
		table_num=4
		time.sleep(0.5)
		self.go_on=False
		self.worker=Worker(self.move_to,return_to_home,table_num,0.66,0.015)
		self.threadpool.start(self.worker)

	def btn_5_click(self):
		self.btn_emer_pressed()
		return_to_home=True
		table_num=5
		time.sleep(0.5)
		self.go_on=False
		self.worker=Worker(self.move_to,return_to_home,table_num,0.33,0.66)
		self.threadpool.start(self.worker)
	
	def btn_emer_pressed(self):
		self.go_on=True
		with self.q.mutex:
			self.q.queue.clear()
			# print("Threads killed")
		global speed
		speed.linear.x = 0.0
		speed.angular.z = 0.0
		self.pub.publish(speed)
	# Signal functions above


	# Funtion to move back and forth from table to kitchen
	def move_to(self,return_to_home,table_num,des_x,des_y):
		label_caption="Taking Order to Table Number "+str(table_num)

		self.label.setText(label_caption)
		self.go_to(des_x,des_y)
		
		if return_to_home :
			global x
			global y
			if self.go_on:
				return
			if abs(des_x-x)<= 0.08 or abs(des_y-y)<= 0.08:
				print("Order Delivered")
			rospy.sleep(2)
			self.label.setText("Returning to Kitchen")
			self.go_to(-0.66,0.64)
			if self.go_on:
				return
			print("Ready For Next Order")
			self.label.setText("Hello Chef!")


	# Function to Navigate to destination
	def go_to(self,des_x,des_y):
		# Function that accepts goal co-ordinates and handles movement 
		
		global slide_linear
		global slide_angular
		global goal
		global speed
		global x
		global y 

		# print("Inside GoTo ")
		# print("x- ",x," y- ",y)

		goal.x=des_x
		goal.y=des_y

		inc_x = goal.x -x
		inc_y = goal.y -y
		
		angle_to_goal = atan2(inc_y, inc_x)

		r= rospy.Rate(5)
		# print("outside move loop x- error ",goal.x-x, " y-error ",goal.y-y)

		# Move while Position error is less than 0.1
		while abs(goal.x-x)>= 0.08 or abs(goal.y-y)>= 0.08:
			# direction 
			global speed

			# print("inside move loop x- error ",abs(goal.x-x), " y-error ",abs(goal.y-y))

			inc_x = goal.x -x
			inc_y = goal.y -y
			angle_to_goal = atan2(inc_y, inc_x)

			# print("difference in theta ", abs(angle_to_goal - theta))
			while abs(angle_to_goal - theta) > 0.1:
				if self.go_on:
					break
				global speed
				speed.linear.x = 0.0
				speed.angular.z = angular
				
				self.pub.publish(speed)
				r.sleep()
			
			# after this thread killed
			if self.go_on:
				break
			# move forward
			speed.linear.x = linear
			speed.angular.z = 0

			self.pub.publish(speed)

			r.sleep()
		# stop after reaching the destination
		speed.linear.x=0
		speed.angular.z = 0

		self.pub.publish(speed)
		# print("Finished")
		rospy.sleep(0.5)
	# Navigation function ends

	def setupUi(self, MainWindow):

		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(814, 664)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setStyleSheet("background-color : #E0E0E0")
		self.centralwidget.setObjectName("centralwidget")
		self.slider_turn = QtWidgets.QSlider(self.centralwidget)
		self.slider_turn.setGeometry(QtCore.QRect(430, 530, 291, 41))
		self.slider_turn.setProperty("value", 20)
		self.slider_turn.setOrientation(QtCore.Qt.Horizontal)
		self.slider_turn.setObjectName("slider_turn")
		self.slider_forward = QtWidgets.QSlider(self.centralwidget)
		self.slider_forward.setGeometry(QtCore.QRect(720, 140, 71, 321))
		self.slider_forward.setStatusTip("")
		self.slider_forward.setAutoFillBackground(False)
		self.slider_forward.setSingleStep(1)
		self.slider_forward.setProperty("value", 20)
		self.slider_forward.setOrientation(QtCore.Qt.Vertical)
		self.slider_forward.setInvertedAppearance(False)
		self.slider_forward.setObjectName("slider_forward")
		self.btn_5 = QtWidgets.QPushButton(self.centralwidget)
		self.btn_5.setStyleSheet("background-color : #ADADAD")
		self.btn_5.setFont(QtGui.QFont('Ubuntu', 15))
		self.btn_5.setGeometry(QtCore.QRect(160, 380, 89, 80))
		self.btn_5.setMinimumSize(QtCore.QSize(80, 80))
		self.btn_5.setMaximumSize(QtCore.QSize(100, 16777215))
		self.btn_5.setObjectName("btn_5")
		self.btn_1 = QtWidgets.QPushButton(self.centralwidget)
		self.btn_1.setStyleSheet("background-color : #ADADAD")
		self.btn_1.setFont(QtGui.QFont('Ubuntu', 15))
		self.btn_1.setGeometry(QtCore.QRect(80, 150, 89, 80))
		self.btn_1.setMinimumSize(QtCore.QSize(80, 80))
		self.btn_1.setObjectName("btn_1")
		self.btn_2 = QtWidgets.QPushButton(self.centralwidget)
		self.btn_2.setFont(QtGui.QFont('Ubuntu', 15))
		self.btn_2.setStyleSheet("background-color : #ADADAD")
		self.btn_2.setGeometry(QtCore.QRect(240, 150, 89, 80))
		self.btn_2.setMinimumSize(QtCore.QSize(80, 80))
		self.btn_2.setObjectName("btn_2")
		self.btn_3 = QtWidgets.QPushButton(self.centralwidget)
		self.btn_3.setFont(QtGui.QFont('Ubuntu', 15))
		self.btn_3.setStyleSheet("background-color : #ADADAD")
		self.btn_3.setGeometry(QtCore.QRect(50, 270, 89, 80))
		self.btn_3.setMinimumSize(QtCore.QSize(80, 80))
		self.btn_3.setObjectName("btn_3")
		self.btn_4 = QtWidgets.QPushButton(self.centralwidget)
		self.btn_4.setFont(QtGui.QFont('Ubuntu', 15))
		self.btn_4.setStyleSheet("background-color : #ADADAD")
		self.btn_4.setGeometry(QtCore.QRect(270, 270, 89, 80))
		self.btn_4.setMinimumSize(QtCore.QSize(80, 80))
		self.btn_4.setObjectName("btn_4")
		self.btn_home = QtWidgets.QPushButton(self.centralwidget)
		self.btn_home.setStyleSheet("background-color : #35FF69")
		self.btn_home.setGeometry(QtCore.QRect(490, 350, 171, 60))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
		self.btn_home.setSizePolicy(sizePolicy)
		self.btn_home.setMinimumSize(QtCore.QSize(100, 60))
		self.btn_home.setObjectName("btn_home")
		self.btn_emer = QtWidgets.QPushButton(self.centralwidget)
		self.btn_emer.setStyleSheet("background-color : #EC0B43")
		self.btn_emer.setGeometry(QtCore.QRect(530, 190, 90, 80))
		self.btn_emer.setMinimumSize(QtCore.QSize(90, 80))
		self.btn_emer.setMaximumSize(QtCore.QSize(90, 16777215))
		self.btn_emer.setObjectName("btn_emer")
		self.line = QtWidgets.QFrame(self.centralwidget)
		self.line.setGeometry(QtCore.QRect(10, 610, 781, 21))
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")
		self.line_2 = QtWidgets.QFrame(self.centralwidget)
		self.line_2.setGeometry(QtCore.QRect(380, 80, 20, 511))
		self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
		self.lcdNumber.setStyleSheet("background-color : #14213D")
		self.lcdNumber.setGeometry(QtCore.QRect(710, 90, 91, 41))
		self.lcdNumber.setObjectName("lcdNumber")
		self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
		self.lcdNumber_2.setStyleSheet("background-color : #14213D")
		self.lcdNumber_2.setGeometry(QtCore.QRect(530, 480, 91, 41))
		self.lcdNumber_2.setObjectName("lcdNumber_2")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(20, 500, 321, 51))
		self.label.setObjectName("label")
		self.label.setFont(QtGui.QFont('Ubuntu', 13))
		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(520, 570, 131, 21))
		self.label_2.setObjectName("label_2")
		self.label_3 = QtWidgets.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(720, 470, 67, 41))
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setObjectName("label_3")
		self.label_4 = QtWidgets.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(170, 290, 67, 41))
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		self.label_4.setObjectName("label_4")
		self.label_5 = QtWidgets.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(300, 10, 211, 51))
		font = QtGui.QFont()
		font.setPointSize(20)
		font.setItalic(True)
		self.label_5.setFont(font)
		self.label_5.setObjectName("label_5")
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.btn_1.clicked.connect(self.btn_1_click)
		self.btn_2.clicked.connect(self.btn_2_click)
		self.btn_3.clicked.connect(self.btn_3_click)
		self.btn_4.clicked.connect(self.btn_4_click)
		self.btn_5.clicked.connect(self.btn_5_click)
		self.btn_home.clicked.connect(self.btn_home_click)
		self.btn_emer.clicked.connect(self.btn_emer_pressed)
		global linear
		global angular
		angular=2*float(self.slider_turn.value())/100
		linear=2*float(self.slider_forward.value())/100
		self.lcdNumber.display(linear)
		self.lcdNumber_2.display(angular)

		self.slider_forward.valueChanged['int'].connect(self.linear_change)
		self.slider_turn.valueChanged['int'].connect(self.angular_change)

		# lcd_number is linear speed lcd2 is angular

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.slider_forward.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
		self.btn_5.setText(_translate("MainWindow", "5"))
		self.btn_1.setText(_translate("MainWindow", "1"))
		self.btn_2.setText(_translate("MainWindow", "2"))
		self.btn_3.setText(_translate("MainWindow", "3"))
		self.btn_4.setText(_translate("MainWindow", "4"))
		self.btn_home.setText(_translate("MainWindow", "Return To Kitchen"))
		self.btn_emer.setText(_translate("MainWindow", "Emergency \n"
		" Stop"))
		self.label.setText(_translate("MainWindow", "Status of robot"))
		self.label_2.setText(_translate("MainWindow", "Set Turning Speed "))
		self.label_3.setText(_translate("MainWindow", "Forward  \n"
		"Speed"))
		self.label_4.setText(_translate("MainWindow", "Dining \n"
		" Area"))
		self.label_5.setText(_translate("MainWindow", "RIGBETELS CAFE"))


if __name__ == "__main__":
	import sys
	rospy.init_node('Waiter')

	sub = rospy.Subscriber("/odom", Odometry, newOdom)

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)

	MainWindow.show()
	sys.exit(app.exec_())

