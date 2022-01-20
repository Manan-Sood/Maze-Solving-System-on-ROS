#!/usr/bin/env python3

import sys
import rospy

from path_planning.msg import direction, map_detail
from MapClass import Map

flag = True 
arr=[[[]]]
map_arr = [[]]
nd = ""

class PlannerNode:    
    def __init__(self):
        self.direction_publisher = rospy.Publisher("/direction", direction, queue_size=10)
        # This is the publisher which will publish the direction for the bot to move
        # A general format for publishing has been given below

        self.walls_subscriber = rospy.Subscriber("/walls", map_detail, self.wall_callback)
        # This is the subscriber that will listen for the details about the map that the bot will aquire
        # This data will be send to the wall_callback function where it should be handled

        rospy.sleep(5) # a delay of some time to let the setup of the subscriber and publisher be completed
        # Since we know that the first step the bot will take will be down, we can simply do it here
        temp_val = direction() # make an object of the message type of the publisher
        temp_val.direction = 'down' # assign value to the object. Refer the custom direction.msg in the msg directory
        self.direction_publisher.publish(temp_val) # publish the object

    
    def wall_callback(self, map_detail):
        global flag
        global arr
        global map_arr
        global nd
        map1 = map_detail
        if map1.current_x == map1.end_x and map1.current_y == map1.end_y:
            pass
        else:
            if flag:
                map1 = map_detail
                arr = [[[0]*7 for k in range(map1.width)] for i in range(map1.height)]
                map_arr = [[0]*map1.width for i in range(map1.height)]
                # preprocessing the array.
                for i in range(map1.height):
                    for j in range(map1.width):
                        for k in range(7):
                            arr[i][j][k]=0
                arr[0][0][0]=arr[0][0][2]=arr[0][0][3]=arr[0][0][4]=1
                arr[0][0][5] = arr[0][0][6] = 0
                arr[1][0][5] = arr[1][0][6] = 0
                for i in range(map1.height):
                    for j in range(map1.width):
                        map_arr[i][j] = abs(map1.end_x - i) + abs(map1.end_y -j)
                flag = False
            # this function will be called everytime the map sends data regarding the map on the '/walls' upic
            # you will recieve the data in the form of the map_detail variable which is an object of custom message type map_detail.msg from the msg directory
            print(map_detail)
            wall = map1.current_value
            a = [0,0,0,0]
            if wall>=8:
                wall-=8
                a[0] = 1
            if wall>=4:
                wall-=4
                a[2]=1
            if wall>=2:
                wall-=2
                a[3]=1
            if wall>=1:
                a[1]=1
                wall-=1
            for i  in range(4):
                arr[map1.current_x][map1.current_y][i] = a[i]
            arr[map1.current_x][map1.current_y][4] = 1
            step = [[int(1000000),""],[int(1000000),""],[int(1000000),""],[int(1000000),""]]
            size=0
            if map1.current_x>0:
                if not arr[map1.current_x-1][map1.current_y][4] and not arr[map1.current_x][map1.current_y][0]:
                    step[0][0] = int(map_arr[map1.current_x-1][map1.current_y])
                    step[size][1] = "up"
                    size =size+1
            if map1.current_y>0:
                if not arr[map1.current_x][map1.current_y-1][4] and not arr[map1.current_x][map1.current_y][2]:
                    step[size][0]=int(map_arr[map1.current_x][map1.current_y-1])
                    step[size][1]="left"
                    size = size+1
            if map1.current_x<map1.height-1:
                if not arr[map1.current_x+1][map1.current_y][4] and not arr[map1.current_x][map1.current_y][1]:
                    step[size][0]=int(map_arr[int(map1.current_x)+1][map1.current_y])
                    step[size][1] = "down"
                    size = size + 1
            if map1.current_y<map1.width-1:
                if not arr[map1.current_x][map1.current_y+1][4] and not arr[map1.current_x][map1.current_y][3]:
                    step[size][0]=int(map_arr[map1.current_x][map1.current_y+1])
                    step[size][1] = "right"
                    size = size+1
            step.sort()
            if not step[0][0]==1000000:
                nd = step[0][1]
                if nd == "up":
                    arr[map1.current_x-1][map1.current_y][5] = map1.current_x
                    arr[map1.current_x-1][map1.current_y][6] = map1.current_y
                elif nd == "down":
                    arr[map1.current_x+1][map1.current_y][5] = map1.current_x
                    arr[map1.current_x+1][map1.current_y][6] = map1.current_y
                elif nd == "right":
                    arr[map1.current_x][map1.current_y+1][5] = map1.current_x
                    arr[map1.current_x][map1.current_y+1][6] = map1.current_y
                elif nd == "left":
                    arr[map1.current_x][map1.current_y-1][5] = map1.current_x
                    arr[map1.current_x][map1.current_y-1][6] = map1.current_y
            else:
                if map1.current_x>arr[map1.current_x][map1.current_y][5] and not arr[map1.current_x][map1.current_y][0]:
                    nd = "up"
                elif map1.current_x<arr[map1.current_x][map1.current_y][5] and not arr[map1.current_x][map1.current_y][1]:
                    nd = "down"
                elif map1.current_y>arr[map1.current_x][map1.current_y][6] and not arr[map1.current_x][map1.current_y][2]:
                    nd = "left"
                elif map1.current_y<arr[map1.current_x][map1.current_y][6] and not arr[map1.current_x][map1.current_y][3]:
                    nd = "right"
            temp_val = direction() # make an object of the message type of the publisher
            temp_val.direction = nd # assign value to the object. Refer the custom direction.msg in the msg directory
            self.direction_publisher.publish(temp_val) # publish the object
        
        
        
if __name__ == '__main__':
    rospy.init_node('planner_node')
    PlannerNode()
    rospy.spin()
