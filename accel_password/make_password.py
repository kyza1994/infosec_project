import sys
import numpy as np
from pykalman import KalmanFilter

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

    #to write in file "password"
    lines = []

    kf = KalmanFilter(transition_matrices=np.array([[1.15, 1], [0, 1]]), transition_covariance=0.01 * np.eye(2))
    states_pred = kf.em(x).smooth(x)[0]
    filtered_x = states_pred[:, 0]
    lines.append(' '.join(list(map(str, filtered_x))) + "\n")

    kf = KalmanFilter(transition_matrices=np.array([[1.1, 0.5], [0, 1]]), transition_covariance=0.01 * np.eye(2))
    states_pred = kf.em(y).smooth(y)[0]
    filtered_y = states_pred[:, 0]
    lines.append(' '.join(list(map(str, filtered_y))) + "\n")

    file = open("password", "w")
    file.writelines(lines)
    file.close()
