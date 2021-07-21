import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('test.csv', delimiter=' ')
df2 = pd.read_csv('test2.csv', delimiter=' ')

print(df)

axn = plt.gca()
x = df['time']
axn.scatter(x=x, y=df['x'], c='red')
axn.scatter(x=x, y=df['y'], c='blue')
axn.scatter(x=x, y=df['z'], c='green')
ax2 = axn.twinx()

x = df2['time']
ax2.scatter(x=x, y=df2['x'], c='black')
ax2.scatter(x=x, y=df2['y'], c='black')
ax2.scatter(x=x, y=df2['z'], c='black')

ax3 = axn.twinx()



x = df['time']
ax3.scatter(x=x, y=df2['x'], c='black')
ax3.scatter(x=x, y=df2['y'], c='black')
ax3.scatter(x=x, y=df2['z'], c='black')


plt.show()
axn = df.plot.scatter(x='time', y='x')
df.plot.scatter(x='time', y='y', ax=axn)
df.plot.scatter(x='time', y='z', ax=axn)
axn = axn.twinx()
axn = df2.plot.scatter(x='time', y='x', ax=axn)
df2.plot.scatter(x='time', y='y', ax=axn)
df2.plot.scatter(x='time', y='z', ax=axn)

plt.show()
