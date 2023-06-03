import numpy as np
import matplotlib.pyplot as plt
import random

x_size = 8
y_size = 5

A = np.ones((x_size, y_size))
A[0, 1] = -1
A[0, 2] = -1
A[0, 3] = -1
A[0, 4] = -1
A[1, 1] = -1
A[1, 2] = -1
A[1, 4] = -1
A[2, 1] = -1
A[2, 3] = -1
A[2, 4] = -1
A[3, 1] = -1
A[3, 4] = -1
A[4, 2] = -1
A[4, 3] = -1
A[4, 4] = -1
A[5, 2] = -1
A[6, 4] = -1
A[6, 4] = -1
A[7, 4] = -1

for i in range(0, x_size-1):
    if A[i, y_size-1] == 1:
        plt.plot(A[i, 1], A[i, 2], 'ko:')
    else:
        plt.plot(A[i, 1], A[i, 2], 'r+:')

plt.axis([-2, 2, -2, 2])

# TODO: generate empty vectors based on size
W = [0, 0, 0, 0]
Wk = [0, 0, 0, 0]

print(W)

change = 1

while change == 1:
    change = 0

    for i in range(0, x_size-1):
        # TODO: select random row
        S = A[i, 0] * W[0] + A[i, 1] * W[1] + A[i, 2] * W[2] + A[i, 3] * W[3]
        sig = 0

        if S > 0:
            sig = 1
        else:
            sig = -1

        if (sig > 0 and A[i, y_size-1] == 1) or (sig < 0 and A[i, y_size-1] == -1):
            W = W
        else:
            change = 1
            if S != 0:
                for j in range(0, y_size-1):
                    W[j] = W[j] + 0.5 * (A[i, y_size-1] - sig) * A[i, j]

        if S == 0:
            change = 1
            for j in range(0, 3):
                W[j] = W[j] + A[i, 3] * A[i, j]
        print(W)

k = -2
XX = np.zeros(401)
YY = np.zeros(401)

for i in range(0, 401):
    XX[i] = k
    YY[i] = -((W[1] / W[2]) * k) - (W[0] * 1) / W[2]
    k = k + 0.01

plt.plot(XX, YY)

plt.show()

# Get user input
u1 = float(input("Enter u1: "))
u2 = float(input("Enter u2: "))
u3 = float(input("Enter u3: "))

# Calculate sum of inputs * weights
S = 1 * W[0] + u1 * W[1] + u2 * W[2] + u3 * W[3]


def f(s):
    if s > 0:
        return 1
    if s == 0:
        return 0
    else:
        return -1


# Calculate output
print(f(S))
