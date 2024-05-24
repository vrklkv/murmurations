import numpy.linalg as npl
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.animation as anim
from PIL import Image, ImageDraw
tfin=1000
p=20
w=250
r=5
x=[[np.array([w/2+1,w/2+1,1])],[np.array([w/2+1,w/2+0,0])],[np.array([w/2-1,w/2+0,0])]] #массив историй перемещений каждого чувака. Координаты трёхмерные
v=[[np.array([1,2,0])],[np.array([0,1,0])],[np.array([1,1,0])]]
col3=(255,146,24)
col2=(0,0,0)
col1=(255,255,255)
images=[]
im=Image.new('RGB',(w,w),col1)
images.append(im)
alpha=[np.array([0.5,1.0,3.0,1.7]),np.array([0.5,0.0,1.3,2.0]),np.array([0.5,0.0,1.2,2.1])]
while(len(x[0])<tfin):
  xc=x[0][-1]
  vc=v[0][-1]
  im=Image.new('RGB',(w,w),col1)
  draw=ImageDraw.Draw(im)
  draw.rectangle((0,0,w-1,w-1),fill=col1,outline=col2) #размеры коробки меньше размеров экрана на 1
  if(((xc+alpha[0][0]*vc)[0]>w-1-r) or ((xc+alpha[0][0]*vc)[0]<r)):
    vc[0]=-vc[0]
  if(((xc+alpha[0][0]*vc)[1]>w-1-r) or ((xc+alpha[0][0]*vc)[1]<r)):
    vc[1]=-vc[1]
  if(((xc+alpha[0][0]*vc)[2]>w-1-r) or ((xc+alpha[0][0]*vc)[2]<r)):
    vc[2]=-vc[2]
  x[0].append(xc+alpha[0][0]*vc)
  v[0].append(alpha[0][1]*vc+alpha[0][2]*(xc-x[0][-2])*(npl.norm(xc-x[0][-2],ord=2)>p)+alpha[k][3]*(-xc+x[0][-2])*(npl.norm(xc-x[0][-2],ord=2)<p))
  draw.ellipse(((xc[0]-r)%(w-1),(xc[1]-r)%(w-1),(xc[0]+r)%(w-1),(xc[1]+r)%(w-1)),fill=col3)
  for k in range(1,len(x)):
    x[k].append(x[k][-1]+alpha[k][0]*v[k][-1])
    v[k].append(alpha[k][1]*v[k][-1]+alpha[k][2]*(xc-x[k][-2])*(npl.norm(xc-x[k][-2],ord=2)>p)+alpha[k][3]*(-xc+x[k][-2])*(npl.norm(xc-x[k][-2],ord=2)<p))
    #print(k,':',x[k][-1],' ',v[k][-1],'\n')
    #print(k,':',x[k][-1][0],' ',x[k][-1][1],'\n')
    #...> w-1-r и ... <r - чтобы чуваки не втыкались носом в границу
    if(((x[k][-1]+alpha[k][0]*v[k][-1])[0]>w-1-r) or ((x[k][-1]+alpha[k][0]*v[k][-1])[0]<r)):
      v[k][-1][0]=-v[k][-1][0] #при столкновении меняется на противоположную соответствующая компонента скорости (работает для всех трех измерений)
    if(((x[k][-1]+alpha[k][0]*v[k][-1])[1]>w-1-r) or ((x[k][-1]+alpha[k][0]*v[k][-1])[1]<r)):
      v[k][-1][1]=-v[k][-1][1]
    if(((x[k][-1]+alpha[k][0]*v[k][-1])[2]>w-1-r) or ((x[k][-1]+alpha[k][0]*v[k][-1])[2]<r)):
      v[k][-1][2]=-v[k][-1][2]
    draw.ellipse((x[k][-1][0]-r,x[k][-1][1]-r,x[k][-1][0]+r,x[k][-1][1]+r),fill=col2)
  images.append(im)
images[0].save('pillow_imagedraw.gif',save_all=True,append_images=images[1:],optimize=False,duration=40,loop=0)
