import numpy.linalg as npl
import numpy as np
kfin=10
p=1
x=[[np.array([1,1,1])]] #массив историй перемещений каждого элемента. Координаты трёхмерные
v=[[np.array([1,0,0])]]
k=0
alpha=[np.array([1,2,1,1])]
while(len(x[0])<kfin):
  for k in range(len(x)):
    xc=x[0][-1]
    x[k].append(x[k][-1]+alpha[k][0]*v[k][-1])
    v[k].append(alpha[k][1]*v[k][-1]+alpha[k][2]*(xc-x[k][-2])*(npl.norm(xc-x[k][-2],ord=2)>p)+alpha[k][3]*(-xc+x[k][-2])*(npl.norm(xc-x[k][-2],ord=2)<p))
    print(x[k][-1],' ',v[k][-1],'\n')