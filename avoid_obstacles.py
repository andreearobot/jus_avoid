#!/usr/bin/env python
# BEGIN ALL

import rospy
from std_msgs.msg import Int32

# Maestro channel assignment
izq = 4
dcho = 5
# Threshold distance: below, change rotation wheel
min_dist= 23.1 # Corresponding to an output of 250 from Sharp sensor

# SPEED CONTROL
zero= 6000 # STOPPED
speed= 600 # REFERENCE SPEED
desv=       -0.13*speed
spin= 300 # ROTATION SPEED
desv_spin=  -0.13*spin

# BEGIN CALLBACK
def scan_callback(msg):
        global g_sharp_ahead
        g_sharp_ahead = msg.data
 # END CALLBACK

g_sharp_ahead = 50 #Anything to start, no obstacle in front
speed_L= 0
speed_R= 0

# Times of motion and pause to stabilise reading of the sharp sensor
cycle = 0.5 # Used for rospy.Rate, 'fwFactor' times driving forward if no obstacle is found
fwFactor= 100
turning = 1
stopped= 0.5	

def avoid():
	# Node initialization
	rospy.init_node('control', anonymous=False)
 	rospy.on_shutdown(self.shutdown)

	############################################
	# BEGIN SUBSCRIBER: Sharp sensor
	read_sharp = rospy.Subscriber('sharp_data', Int32, scan_callback)
	# END SUBSCRIBER
	############################################
	# BEGIN PUB: left and right servos speed set
	write_left = rospy.Publisher('speed_left', Int32,queue_size=10)
	write_right = rospy.Publisher('speed_right', Int32,queue_size=10)
	# END PUB
	############################################

	driving_forward = True
	state_change = False # Detects when some motor needs to change its direction of rotation
	#Maximum time for JUS to turn to other direction
	state_change_time = rospy.Time.now() + rospy.Duration(fwFactor*cycle)

	# BEGIN LOOP
	rate = rospy.Rate(1/cycle)


	while not rospy.is_shutdown():
		# CHECK IF IT IS NEEDED TO CHANGE THE STATE BETWEEN AHEAD/TURNING
		if driving_forward:
		        if (g_sharp_ahead < min_dist or rospy.Time.now() > state_change_time):
		                driving_forward = False
		                state_change_time = rospy.Time.now() + rospy.Duration(turning)
		                #Detects in which iteration some motor has to change its direction
		                if not state_change:
		                        state_change = True
		else: # we're not driving_forward
		        if rospy.Time.now() > state_change_time:
		                driving_forward = True # we're done spinning, time to go forward!
		                state_change_time = rospy.Time.now() + rospy.Duration(fwFactor*cycle)
	
		#SEND MOTION COMMANDS
		if state_change:
		        # Stop the motors and wait some time before commanding them to move again
		        speed_L= 0 #zero # 0
		        speed_R= 0 #zero # 0
		        write_left.publish(speed_L)
		        write_right.publish(speed_R)
		rospy.sleep(stopped)
		state_change = False

		if driving_forward:
		        # GO AHEAD since there is no obstacle
		        speed_L= + (speed-desv) #-1
		        speed_R= - (speed-desv) # 1
		else:
		        # TURN 'clockwise' since there is an obstacle
		        speed_L= + (spin-desv_spin) # -1
		        speed_R= + (spin-desv_spin) #-1

		write_left.publish(speed_L + zero)
		write_right.publish(speed_R + zero)
		print "Distance = ", g_sharp_ahead
		print "LEFT motor speed=   ", speed_L
		print "RIGHT motor speed= ", speed_R
		rate. sleep()

def shutdown(self):
        rospy.loginfo("Stop")
	write_left.publish(0)
	write_right.publish(0)
        rospy.sleep(1)
 
if _name_ == '_main_':
    try:
        avoid()
    except:
        rospy.loginfo("node terminated.")

# END LOOP
# END ALL
