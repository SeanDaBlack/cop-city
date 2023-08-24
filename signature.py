import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as si
import random

def generate_signature(num_points=7, x_range=(-5, 10), y_range=(-10, 10)):

    # Generate random points
    points = [[random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])] for _ in range(num_points)]

    points += points[:3:-1]
    points = np.array(points)
   
    x = points[:,0]
    y = points[:,1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    return x_i, y_i

#==============================================================================
# Plot
#==============================================================================

# fig = plt.figure()

# ax = fig.add_subplot(231)
# plt.plot(t, x, '-og')
# plt.plot(ipl_t, x_i, 'r')
# plt.xlim([0.0, max(t)])
# plt.title('Splined x(t)')

# ax = fig.add_subplot(232)
# plt.plot(t, y, '-og')
# plt.plot(ipl_t, y_i, 'r')
# plt.xlim([0.0, max(t)])
# plt.title('Splined y(t)')

# ax = fig.add_subplot(233)
# plt.plot(x, y, '-og')
# plt.plot(x_i, y_i, 'r')
# plt.xlim([min(x) - 0.3, max(x) + 0.3])
# plt.ylim([min(y) - 0.3, max(y) + 0.3])
# plt.title('Splined f(x(t), y(t))')

# ax = fig.add_subplot(234)
# for i in range(7):
#     vec = np.zeros(11)
#     vec[i] = 1.0
#     x_list = list(x_tup)
#     x_list[1] = vec.tolist()
#     x_i = si.splev(ipl_t, x_list)
#     plt.plot(ipl_t, x_i)
# plt.xlim([0.0, max(t)])
# plt.title('Basis splines')
# plt.show()