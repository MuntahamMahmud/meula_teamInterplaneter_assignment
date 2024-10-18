#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QTextEdit, QGridLayout,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt,QThread
import sys

class ControlUnit:
    def __init__(self):
        rospy.init_node('controlunit', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)
    


class GUIApp(QWidget,ControlUnit):
    def __init__(self):
        super().__init__()
        
       
        self.meula = 10
        self.init_ui()

    def init_ui(self):
      
        
        self.layout_hori=QHBoxLayout()

       
        self.grid_layout = QGridLayout()
        self.front_button = QPushButton("FRONT")
        self.back_button = QPushButton("BACK")
        self.right_button = QPushButton("RIGHT")
        self.left_button = QPushButton("LEFT")

        
        self.front_button.clicked.connect(self.move_forward)
        self.back_button.clicked.connect(self.move_backward)
        self.right_button.clicked.connect(self.turn_right)
        self.left_button.clicked.connect(self.turn_left)

        
        self.grid_layout.addWidget(self.front_button, 0, 1)
        self.grid_layout.addWidget(self.back_button, 2, 1)
        self.grid_layout.addWidget(self.right_button, 1, 2)
        self.grid_layout.addWidget(self.left_button, 1, 0)

        self.layout_hori.addLayout(self.grid_layout)
        self.layoutV=QVBoxLayout()

        
        self.meula_label = QLabel(f"Remaining Meula: {self.meula}")
        self.layoutV.addWidget(self.meula_label)
        
        
        self.increase_meula_button = QPushButton("Increase Meulas")
        self.increase_meula_button.clicked.connect(self.increase_meulas)
        self.layoutV.addWidget(self.increase_meula_button)
        
        #spacer
        self.spacer = QSpacerItem(20, 130, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layoutV.addItem(self.spacer)


        
        self.meula_label1 = QLabel("MESSAGES:")
        self.layoutV.addWidget(self.meula_label1)
        self.msg_box = QTextEdit()
        self.msg_box.setPlaceholderText("Messages will appear here...")
        self.msg_box.setReadOnly(True)
        self.msg_box.setFixedSize(300, 50)
        self.layoutV.addWidget(self.msg_box)
        self.layout_hori.addLayout(self.layoutV)

        
        self.setLayout(self.layout_hori)

    def move_forward(self):
        
        if self.meula>0:

            self.meula=self.meula-1
            self.update_meula_display()
            self.msg_box.append("Bot is Moving Forward")
            

            start_time = rospy.get_time()
            velocity=Twist()
            while rospy.get_time() - start_time < 1:
                velocity.linear.x=0.2

                self.pub.publish(velocity)  
                self.rate.sleep()           

        
            velocity.linear.x = 0.0
            self.pub.publish(velocity)
        else: 
            self.show_error() 


    def move_backward(self):
        if self.meula>0:
            self.meula=self.meula-1
            self.update_meula_display()
            self.msg_box.append("Bot is Backward")
            start_time = rospy.get_time()
            velocity=Twist()

            while rospy.get_time() - start_time < 1:
                velocity.linear.x=-0.2

                self.pub.publish(velocity)  
                self.rate.sleep()           

        
            velocity.linear.x = 0.0
            self.pub.publish(velocity) 
        else:
            self.show_error()

    def turn_right(self):
        if self.meula>=2:
            self.meula=self.meula-2
            self.msg_box.append("Bot is Rightward")
            self.update_meula_display()
            start_time = rospy.get_time()
            velocity=Twist()

            while rospy.get_time() - start_time < 1:
                velocity.angular.z=-0.2

                self.pub.publish(velocity)  
                self.rate.sleep()           

        
            velocity.angular.z = 0.0
            self.pub.publish(velocity) 
        else :
            self.show_error()
    def turn_left(self):
         
         if self.meula>=2:
            self.meula=self.meula-2
            self.msg_box.append("Bot is Leftward")
            self.update_meula_display()
            start_time = rospy.get_time()
            velocity=Twist()

            while rospy.get_time() - start_time < 1:
                velocity.angular.z=0.2

                self.pub.publish(velocity)  
                self.rate.sleep()           

        
            velocity.angular.z = 0.0
            self.pub.publish(velocity)
         else:
            self.show_error()

    def increase_meulas(self):
        self.meula=self.meula+2
        self.msg_box.append("Bot is Moving 360 ")
        self.update_meula_display()
        velocity=Twist()
        velocity.angular.z=0.4

        end_time = rospy.get_time() + 15.7
        while rospy.get_time() < end_time:
            self.pub.publish(velocity)
            self.rate.sleep()

        # Stop the robot
        velocity.angular.z = 0.0
        self.pub.publish(velocity)



    def update_meula_display(self):
        self.meula_label.setText(f"Remaining Meula: {self.meula}")

    def show_error(self):
        self.msg_box.append("Error: Not enough meula")
class ROSControlThread(QThread):
    def run(self):
        rospy.loginfo("COntrol unit is running")
        rospy.spin()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUIApp()
    window.show()

    
    ros_thread=ROSControlThread()
    ros_thread.start()

    sys.exit(app.exec())
