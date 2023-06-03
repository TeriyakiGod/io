import numpy as np
import matplotlib.pyplot as plt
import math

A = np.zeros((4, 4))
A[0, 0] = 1
A[0, 1] = 0
A[0, 2] = 0
A[0, 3] = 0
A[1, 0] = 1
A[1, 1] = 0
A[1, 2] = 1
A[1, 3] = 1
A[2, 0] = 1
A[2, 1] = 1
A[2, 2] = 0
A[2, 3] = 1
A[3, 0] = 1
A[3, 1] = 1
A[3, 2] = 1
A[3, 3] = 0

count = 0
steps = 50000

ERR = np.zeros(steps // 100 + 1)

# Plotting the classification area
for i in range(0, 4):
    if A[i, 3] == 1:
        plt.plot(A[i, 1], A[i, 2], 'ko:')
    else:
        plt.plot(A[i, 1], A[i, 2], 'r+:')
plt.axis([-0.5, 1.5, -0.5, 1.5])

W = np.zeros(9)
S = np.zeros(3)
U = np.zeros(3)
F = np.zeros(3)
d = np.zeros(3)

# Random initialization of initial weights
for i in range(0, 9):
    W[i] = np.random.rand() - 0.5

ro = 0.2
iteration = 0


def neural_network_output(u1, u2):
    S_temp = np.zeros(3)
    U_temp = np.zeros(3)
    # Forward propagation - hidden layer
    S_temp[0] = W[0] + W[1] * u1 + W[2] * u2
    S_temp[1] = W[3] + W[4] * u1 + W[5] * u2

    U_temp[0] = 1 / (1 + math.exp(-S_temp[0]))
    U_temp[1] = 1 / (1 + math.exp(-S_temp[1]))

    # Forward propagation - output layer
    S_temp[2] = W[6] + W[7] * U_temp[0] + W[8] * U_temp[1]
    U_temp[2] = 1 / (1 + math.exp(-S_temp[2]))

    # Round the output to the nearest integer
    result = (U_temp[2])

    return result


while iteration < steps:
    iteration = iteration + 1

    # Randomly selecting a training vector
    i = np.random.randint(4)

    # Forward propagation - hidden layer
    S[0] = W[0] * A[i, 0] + W[1] * A[i, 1] + W[2] * A[i, 2]
    S[1] = W[3] * A[i, 0] + W[4] * A[i, 1] + W[5] * A[i, 2]

    U[0] = 1 / (1 + math.exp(-S[0]))
    U[1] = 1 / (1 + math.exp(-S[1]))

    # Forward propagation - output layer
    S[2] = W[6] * A[i, 0] + W[7] * U[0] + W[8] * U[1]
    U[2] = 1 / (1 + math.exp(-S[2]))

    # Backpropagation - output layer
    F[2] = U[2] * (1 - U[2])
    d[2] = (A[i, 3] - U[2]) * F[2]

    # Backpropagation - hidden layer
    F[0] = U[0] * (1 - U[0])
    d[0] = W[7] * d[2] * F[0]

    F[1] = U[1] * (1 - U[1])
    d[1] = W[8] * d[2] * F[1]

    # Calculating the error
    if iteration % 100 == 0:
        s = 0
        for j in range(0, 3):
            s += abs(A[j, 3] - neural_network_output(A[j, 1], A[j, 2]))
        ERR[iteration // 100] = s

    # Updating weights - output layer
    W[6] = W[6] + ro * d[2] * A[i, 0]
    W[7] = W[7] + ro * d[2] * U[0]
    W[8] = W[8] + ro * d[2] * U[1]

    # Updating weights - hidden layer
    W[0] = W[0] + ro * d[0] * A[i, 0]
    W[1] = W[1] + ro * d[0] * A[i, 1]
    W[2] = W[2] + ro * d[0] * A[i, 2]

    W[3] = W[3] + ro * d[1] * A[i, 0]
    W[4] = W[4] + ro * d[1] * A[i, 1]
    W[5] = W[5] + ro * d[1] * A[i, 2]

# Plotting the obtained separation lines (neuron 1)
XX = np.zeros(401)
YY = np.zeros(401)
k = 0
for i in np.arange(-2, 2.01, 0.01):
    XX[k] = i
    YY[k] = -((W[1] / W[2]) * i) - (W[0] * 1) / W[2]
    k = k + 1
plt.plot(XX, YY)

# Plotting the obtained separation lines (neuron 2)
k = 0
for i in np.arange(-2, 2.01, 0.01):
    XX[k] = i
    YY[k] = -((W[4] / W[5]) * i) - (W[3] * 1) / W[5]
    k = k + 1
plt.plot(XX, YY)
plt.axis([-0.5, 1.5, -0.5, 1.5])

plt.show()


def plot_error(ERR):
    iterations = range(100, len(ERR) * 100 + 1, 100)
    plt.plot(iterations, ERR)
    plt.xlabel('Iteration')
    plt.ylabel('Error')
    plt.show()


plot_error(ERR)

loop = 1
while loop == 1:
    # Get u1 and u2 input from user
    u1 = float(input("Enter u1: "))
    if u1 == -10:
        loop = 0
        break
    u2 = float(input("Enter u2: "))
    if u2 == -10:
        loop = 0
        break
    res = round(neural_network_output(u1, u2))
    print("Output: ", res)
