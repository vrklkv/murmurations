import numpy.linalg as npl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from PIL import Image, ImageDraw
tfin=50
p=1
w=500
r=1
x=[[np.array([w/2+1,w/2+1,1])],[np.array([w/2+1,w/2+0,0])]] #массив историй перемещений каждого элемента. Координаты трёхмерные
v=[[np.array([1,0,0])],[np.array([0,1,0])]]
col2=(0,0,0)
col1=(255,255,255)
images=[]
im=Image.new('RGB',(w,w),col1)
images.append(im)
alpha=[np.array([0.5,1.2,1,1]),np.array([1,1.3,1,1])]
while(len(x[0])<tfin):
  xc=x[0][-1]
  im=Image.new('RGB',(w,w),col1)
  draw=ImageDraw.Draw(im)
  for k in range(len(x)):
    x[k].append(x[k][-1]+alpha[k][0]*v[k][-1])
    v[k].append(alpha[k][1]*v[k][-1]+alpha[k][2]*(xc-x[k][-2])*(npl.norm(xc-x[k][-2],ord=2)>p)+alpha[k][3]*(-xc+x[k][-2])*(npl.norm(xc-x[k][-2],ord=2)<p))
    #print(k,':',x[k][-1],' ',v[k][-1],'\n')
    #print(k,':',x[k][-1][0],' ',x[k][-1][1],'\n')
    draw.ellipse((x[k][-1][0]-r,x[k][-1][1]-r,x[k][-1][0]+r,x[k][-1][1]+r),fill=col2)
  images.append(im)
images[0].save('pillow_imagedraw.gif',save_all=True,append_images=images[1:],optimize=False,duration=40,loop=0)
