# Author: Egor Kuznetsov

import sys
from numpy.linalg import norm
import numpy as np
from pykalman import KalmanFilter
from sklearn.metrics.pairwise import manhattan_distances

threshold = 0.45

#Computes Dynamic Time Warping (DTW) of two sequences.
def dtw(x, y, dist):
    d = 15
    r, c = len(x), len(y)
    D0 = np.zeros((r + 1, c + 1))
    D0[0, 1:] = np.inf
    D0[1:, 0] = np.inf
    D1 = D0[1:, 1:]
    for i in range(r):
        for j in range(c):
            if float(r)/c * j - d < i and float(r)/c * j + d > i:
                D1[i, j] = dist(x[i], y[j])
            else:
                D1[i, j] = np.inf
    for i in range(r):
        for j in range(c):
            D1[i, j] += min(D0[i, j], D0[i, j+1], D0[i+1, j])
    return D1[-1, -1] / sum(D1.shape)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error input. Type <name of programm> <name of file with password>")
    else:
        try:
            file = open(sys.argv[1], "r")
        except IOError:
            print("ERROR file")
        x, y, z = [], [], []
        for line in file:
            accelerations = line.split()
            accelerations = list(map(float, accelerations))
            x.append(accelerations[0])
            y.append(accelerations[1])
            z.append(accelerations[2])
        file.close()

        kf = KalmanFilter(transition_matrices=np.array([[1.15, 1], [0, 1]]), transition_covariance=0.01 * np.eye(2))
        states_pred = kf.em(x).smooth(x)[0]
        filtered_x = states_pred[:, 0]

        kf = KalmanFilter(transition_matrices=np.array([[1.1, 0.5], [0, 1]]), transition_covariance=0.01 * np.eye(2))
        states_pred = kf.em(y).smooth(y)[0]
        filtered_y = states_pred[:, 0]

        file = open("password", "r")
        password_x = file.readline().split()
        password_x = list(map(float, password_x))
        password_y = file.readline().split()
        password_y = list(map(float, password_y))
        file.close()

        dist_x = dtw(password_x, filtered_x, dist=lambda x, y: norm(x - y, ord=None))
        dist_y = dtw(password_y, filtered_y, dist=lambda x, y: norm(x - y, ord=None))#norm(x - y, ord=None))

        print(dist_x, dist_y, dist_x + dist_y)
        if dist_x + dist_y <= threshold:
            print("Correct password")
        else:
            print("Wrong password")
