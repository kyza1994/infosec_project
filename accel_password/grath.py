__author__ = 'Егор'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.integrate import simps
import math
from pykalman import KalmanFilter
import mlpy

file = open("square.TXT", "r")
dt = 0.01
velocity_x, velocity_y, velocity_z = [], [], []
acceleration_x, acceleration_y, acceleration_z = [], [], []
distance_x, distance_y, distance_z = [], [], []
i = 0
for line in file:
    accels = line.split()
    accels = list(map(float, accels))
    acceleration_x.append(accels[0])
    acceleration_y.append(accels[1])
    acceleration_z.append(accels[2])


sum_acc_x, sum_acc_y, sum_acc_z = 0, 0, 0
num = 10
'''
for i in range(num):
    sum_acc_x += acceleration_x.pop(0)
    sum_acc_y += acceleration_y.pop(0)
    sum_acc_z += acceleration_z.pop(0)
average_x = sum_acc_x/num
average_y = sum_acc_y/num
average_z = sum_acc_z/num

for i in range(len(acceleration_x)):
    acceleration_x[i] -= average_x
    acceleration_y[i] -= average_y
    acceleration_z[i] -= average_z
'''
'''
n = 3
accel_x = []
accel_y = []
accel_z = []
for i in range(2, len(acceleration_x), n):
    accel_x.append((acceleration_x[i-2] + acceleration_x[i-1] + acceleration_x[i]) / n)
    accel_y.append((acceleration_y[i-2] + acceleration_y[i-1] + acceleration_y[i]) / n)
    accel_z.append((acceleration_z[i-2] + acceleration_z[i-1] + acceleration_z[i]) / n)
'''
'''
for i in range(len(acceleration_x)):
    if abs(acceleration_x[i]) < 2:
        acceleration_x[i] = 0
    if abs(acceleration_y[i]) < 2:
        acceleration_y[i] = 0
    if abs(acceleration_z[i]) < 2:
        acceleration_z[i] = 0
'''
t = np.arange(0, (len(acceleration_x))*dt, dt)

kf = KalmanFilter(transition_matrices=np.array([[1.15, 1], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
states_pred = kf.em(acceleration_x).smooth(acceleration_x)[0]

plt.figure(1)
obs_scatter = plt.plot(t[0:len(acceleration_x)], acceleration_x, color='b',
                         label='observations x')
acceleration_x = states_pred[:, 0]
position_line = plt.plot(t[0:len(states_pred[:, 0])], states_pred[:, 0],
                        linestyle='-', color='r',
                        label='filtered x')
plt.legend(loc='lower right')
plt.xlabel('time')
plt.grid()

#dist, cost, path = mlpy.dtw_subsequence(acceleration_x, states_pred[:, 0], dist_only=False)
lines = [' '.join(list(map(str, states_pred[:, 0]))) + "\n"]

kf = KalmanFilter(transition_matrices=np.array([[1.1, 0.5], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
states_pred = kf.em(acceleration_y).smooth(acceleration_y)[0]

plt.figure(2)
obs_scatter = plt.plot(t[0:len(acceleration_y)], acceleration_y, color='b',
                         label='observations y')
acceleration_y = states_pred[:, 0]
position_line = plt.plot(t[0:len(states_pred[:, 0])], states_pred[:, 0],
                        linestyle='-', color='r',
                        label='filtered y')
plt.legend(loc='lower right')
plt.xlabel('time')
plt.grid()

lines.append(' '.join(list((map(str,states_pred[:, 0])))) + "\n")

file = open("filtered_square_ver3.txt", "w")
file.writelines(lines)

'''
kf = KalmanFilter(transition_matrices=np.array([[1.6, 0.5], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))
states_pred = kf.em(acceleration_z).smooth(acceleration_z)[0]

plt.figure(3)
obs_scatter = plt.plot(t[0:200], acceleration_z[0:200], color='b',
                         label='observations z')
#acceleration_z = states_pred[:, 0]
#position_line = plt.plot(t, states_pred[:, 0],
#                        linestyle='-', color='r',
#                        label='filtered z')
plt.legend(loc='lower right')
plt.xlabel('time')
plt.grid()



'''
velocity_x.append(0)
velocity_y.append(0)
velocity_z.append(0)

distance_x.append(0)
distance_y.append(0)
distance_z.append(0)
'''
for i in range(1, len(acceleration_x)):
    velocity_x.append(velocity_x[i-1] + simps([acceleration_x[i-1], acceleration_x[i]], [0, dt]))
    velocity_y.append(velocity_y[i-1] + simps([acceleration_y[i-1], acceleration_y[i]], [0, dt]))
    velocity_z.append(velocity_z[i-1] + simps([acceleration_z[i-1], acceleration_z[i]], [0, dt]))

for i in range(1, len(velocity_x)):
    distance_x.append(distance_x[i-1] + simps([velocity_x[i-1], velocity_x[i]], [0, dt]))
    distance_y.append(distance_y[i-1] + simps([velocity_y[i-1], velocity_y[i]], [0, dt]))
    distance_z.append(distance_z[i-1] + simps([velocity_z[i-1], velocity_z[i]], [0, dt]))

t = np.arange(0, (len(velocity_x))*dt, dt)
#t1 = np.arange(dt, (len(accel_x))*n*dt, n*dt)
distance_x = np.array(distance_x)
distance_y = np.array(distance_y)
distance_z = np.array(distance_z)
'''
'''
plt.figure(2)
plt.plot(t, acceleration_x, 'r-', label = "x")
#plt.plot(t, acceleration_y, 'g-', label = "y")
#plt.plot(t, acceleration_z, 'b-', label = "z")
plt.legend()
plt.title("Acceleration")
plt.grid()

print(len(t1), len(accel_x))
plt.figure(2)
plt.plot(t1, accel_x, 'r-', label = "x")
plt.plot(t1, accel_y, 'g-', label = "y")
plt.plot(t1, accel_z, 'b-', label = "z")
plt.legend()
plt.title("Acceleration")
plt.grid()
'''
'''
plt.figure(4)
plt.plot(t, velocity_x, 'r-', label = "x")
plt.plot(t, velocity_y, 'g-', label = "y")
plt.plot(t, velocity_z, 'b-', label = "z")
plt.legend()
plt.title("Velocity")
plt.grid()

plt.figure(5)
plt.plot(t, distance_x, 'r-', label = "x")
plt.plot(t, distance_y, 'g-', label = "y")
plt.plot(t, distance_z, 'b-', label = "z")
plt.legend()
plt.title("Distance")
plt.grid()

fig = plt.figure(6)
ax = fig.add_subplot(111, projection='3d')
ax.plot(distance_x, distance_y, distance_z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

'''
plt.show()