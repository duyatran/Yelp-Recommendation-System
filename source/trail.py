import matplotlib.pyplot as plt
plt.switch_backend('agg')
fig = plt.figure(figsize=(10,4), dpi = 300)
ax = fig.add_subplot(111)
ax.plot([1,2], [1,2])
fig.savefig("trail.png", format = "png", dpi = 300)