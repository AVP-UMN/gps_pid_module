import rospy
import time
# import GPS
import path_data
import math

'''
This script is PID algorithm to our car
Two error correction is applied:
	1. Correction on Velocity:
		Because maximum velocity is 15mph and for safety, keeping car at 13.5 is best choice
		So, use gyro to detect velocity and do correction.
	2. Correction on angle :
		To keep car running on optimized line, angle between direction of car and direction of optimized line should be zero.
	
	Use stack to pop up points one by one, if passing move to next one 

	Divide the course into 5 phase use the point count in stack to tell car in which area

	Use current direction minus old position collected by loop before to get direction vector
	Then miuns optimized vector:
'''

global point_stack
# phase_1_theta
# phase_2_theta
# phase_3_theta
# phase_4_theta
current_point = point_stack.pop()
point_traveled = 0
opt_path_vec = [current_point[0],current_point[1]]

'''
TODO:
phase_count_1_2
phase_count_2_3
phase_count_3_4
phase_count_4_5
phase_count_final
'''

def get_path_vec(location):
	x1 = location[0]
	y1 = location[1]
	x2 = current_point[0]
	y2 = current_point[1]
	deviation = 0
	real_x = 0
	old_point = [0,0]

	if phase_num == 1:
		deviation = math.abs((y2 - y1) * math.tan(phase_1_theta))
		if y2 < y1:
			deviation *= -1
		real_x = x1 + deviation

		while real_x > x2:
			old_point = current_point
			current_point = point_stack.pop()
			point_traveled += 1
			x2 = current_point[0]
			if point_traveled > phase_count_1_2:
				return None
		return [current_point[0] - old_point[0], current_point[1] - old_point[1]]

	elif phase_num == 2:
		deviation = math.abs((x2 - x1) * math.tan(phase_2_theta))
		if x2 < x1:
			deviation *= -1
		real_y = y1 + deviation

		while real_y > y2:
			current_point = point_stack.pop()
			point_traveled += 1
			y2 = current_point[1]
			if point_traveled > phase_count_2_3:
				return None
		return [current_point[0] - old_point[0], current_point[1] - old_point[1]]

	elif phase_num == 3:
		deviation = math.abs((y2 - y1) * math.tan(phase_3_theta))
		if y2 < y1:
			deviation *= -1
		real_x = x1 + deviation

		while real_x > x2:
			current_point = point_stack.pop()
			point_traveled += 1
			x2 = current_point[0]
			if point_traveled > phase_count_3_4:
				return None 
		return [current_point[0] - old_point[0], current_point[1] - old_point[1]]

	elif phase_num == 4:
		deviation = math.abs((x2 - x1) * math.tan(phase_4_theta))
		if x2 < x1:
			deviation *= -1
		real_y = y1 + deviation

		while real_y > y2:
			current_point = point_stack.pop()
			point_traveled += 1
			y2 = current_point[1]
			if point_traveled > phase_count_4_5:
				return None 
		return [current_point[0] - old_point[0], current_point[1] - old_point[1]]

	elif phase_num == 5:
		deviation = math.abs((y2 - y1) * math.tan(phase_5_theta))
		if y2 < y1:
			deviation *= -1
		real_x = x1 + deviation

		while real_x > x2:
			current_point = point_stack.pop()
			point_traveled += 1
			x2 = current_point[0]
			if point_traveled > phase_count_3_4:
				return None 
		return [current_point[0] - old_point[0], current_point[1] - old_point[1]]
def cal_angle(dir_vec, opt_path_vec):


def main():
	old_position = [0,0]
	err_v_accumulate = 0
	angle_err_accumulate = 0
	dir_vec = []
	opt_path_vec = []
	old_steer_error = 0
	old_v_error = 0
	phase_num = 1
	time.sleep(0.5)
	# Let's rock!
	while finish():
	# Steer Correction 
		# get direction vection in current
		dir_vec = get_position()
		# get vection of optimized path
		opt_path_vec = get_path_vec(dir_vec)
		if opt_path_vec is None:
			phase_num = get_phase(point_traveled)
			continue
		# get angle between direction vection and opt_path vector 
		error_angle = cal_angle(dir_vec, opt_path_vec)
		deviation_vec = [div_vec[0] - opt_path_vec[0], div_vec[1] - opt_path_vec[1]]
		
		# Use pid to calculate exact angle needed to be steered
	  angle_steer = pid_steer(error_angle)
		# Positive for left, - for right.
		if direction(phase_num, deviation_vec):
			# Left Steer
		else:
			# Right Steer

		# update accumulated error to K(i)
		angle_err_accumulate += error_angle

		# update old error to calculate K(d)
		old_steer_error = error_angle 
	
	# Velocity Correction
		
		velocity = get_velocity()

		error_v = get_v_error(point_traveled, velocity)

		theta_speed = pid_v(old_v_error, old_v_error, err_v_accumulate)

		err_v_accumulate = v_err_accumulate + velocity 
		# update old velocity err to calculate K(d)
		old_v_error += error_v

		# frequency of getting position is 0.1 sec
		time.sleep(0.1)

if __name__ = '__main__':
	main()
