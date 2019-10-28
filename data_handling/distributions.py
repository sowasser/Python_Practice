from scipy.stats import gamma
import matplotlib.pyplot as plt


speed_dist = gamma.rvs(size=10, a=2)
vision_dist = gamma.rvs(size=10, a=10)
sep_dist = gamma.rvs(size=10, a=2)


# Graph distributions
plt.style.use("dark_background")
fig = plt.figure(figsize=(6, 9))

ax1 = fig.add_subplot(3, 1, 1)
plt.title("Speed Distribution")

ax2 = fig.add_subplot(3, 1, 2)
plt.title("Vision Distribution")

ax3 = fig.add_subplot(3, 1, 3)
plt.title("Separation Distribution")


ax1.hist(speed_dist)
ax2.hist(vision_dist)
ax3.hist(sep_dist)

plt.show()

