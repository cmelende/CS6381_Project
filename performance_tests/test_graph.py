import matplotlib.pyplot as plt
import csv

y = []
x = []

i = 0
with open('10.0.0.1-10.0.0.3.log','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        y.append(float(row[4]))
        x.append(i)
        i+=1

print([x for x in zip(x,y)])
plt.plot(x,y, label='pub-sub data, sub01')
plt.xlabel('x')
plt.ylabel('y')
plt.title('pub-sub performance - sub01')
#plt.legend()
plt.show()