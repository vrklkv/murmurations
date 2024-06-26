import dataclasses as dat
import numpy.linalg as npl
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
tfin=1000
p=20
w=250
r=5
n=1.3
p_new=p/n
col3=(255,146,24)
col2=(0,0,0)
col1=(255,255,255)
images=[]
im=Image.new('RGB',(w,w),col1)
images.append(im)


@dat.dataclass
class point():
    glav: bool = 0
    x_prev: float = 0
    y_prev: float = 0
    x: float = 0
    y: float = 0
    vx: float = 0
    vy: float = 0
    alpha1: float=0
    alpha2: float=0
    alpha3: float=0
    alpha4: float=0


b0 = point(1,0,0,w/2+0,w/2+0,1,2,0.5,1.0,0.6,0.4)
b1 = point(0,0,0,w/2+2*p_new,w/2+1*p_new,0,1,0.5,0.0,0.1,0.9)
b2 = point(0,0,0,w/2-1*p_new,w/2+2*p_new,1/np.sqrt(2),1/np.sqrt(2),0.5,0.0,0.1,0.9)
b=[b0,b1,b2]
t=0
while(t<tfin):
  t=t+1
  xc=np.array([b[0].x,b[0].y])
  vc=np.array([b[0].vx,b[0].vy])
  im=Image.new('RGB',(w,w),col1)
  draw=ImageDraw.Draw(im)
  draw.rectangle((0,0,w-1,w-1),fill=col1,outline=col2)
  if(((xc+b[0].alpha1*vc)[0]>w-1-p_new) or ((xc+b[0].alpha1*vc)[0]<p_new)):
    vc[0]=-vc[0]
  if(((xc+b[0].alpha1*vc)[1]>w-1-p_new) or ((xc+b[0].alpha1*vc)[1]<p_new)):
    vc[1]=-vc[1]
  b[0].x_prev=b[0].x
  b[0].y_prev=b[0].y
  prev=np.array([b[0].x_prev,b[0].y_prev])
  b[0].x=(xc+b[0].alpha1*vc)[0]
  b[0].y=(xc+b[0].alpha1*vc)[1]
  b[0].vx=(b[0].alpha2*vc+b[0].alpha3*(xc-prev)*(npl.norm(xc-prev,ord=2)>p)+b[0].alpha4*(-xc+prev)*(npl.norm(xc-prev,ord=2)<p))[0]
  b[0].vy=(b[0].alpha2*vc+b[0].alpha3*(xc-prev)*(npl.norm(xc-prev,ord=2)>p)+b[0].alpha4*(-xc+prev)*(npl.norm(xc-prev,ord=2)<p))[1]
  draw.ellipse(((xc[0]-r)%(w-1),(xc[1]-r)%(w-1),(xc[0]+r)%(w-1),(xc[1]+r)%(w-1)),fill=col3)
  for k in range(1,len(b)):
    b[k].x_prev=b[k].x
    b[k].y_prev=b[k].y
    prev=np.array([b[k].x_prev,b[k].y_prev])
    b[k].x=b[k].x_prev+b[k].alpha1*b[k].vx
    b[k].y=b[k].y_prev+b[k].alpha1*b[k].vy
    b[k].vx=b[k].alpha2*b[k].vx+b[k].alpha3*(xc-prev)[0]*(npl.norm(xc-prev,ord=2)>p)+b[k].alpha4*(-xc+prev)[0]*(npl.norm(xc-prev,ord=2)<p)
    b[k].vy=b[k].alpha2*b[k].vy+b[k].alpha3*(xc-prev)[1]*(npl.norm(xc-prev,ord=2)>p)+b[k].alpha4*(-xc+prev)[1]*(npl.norm(xc-prev,ord=2)<p)
    for j in range(0,k):
      #if(not(i==j)):
      xk=np.array([b[k].x,b[k].y])
      vk=np.array([b[k].vx,b[k].vy])
      xj=np.array([b[j].x,b[j].y])
      vj=np.array([b[j].vx,b[j].vy])
      if(npl.norm((xk+b[k].alpha1*vk)-(xj+b[j].alpha1*vj),ord=2)<p_new):
        tcrit=(p_new-npl.norm((xk+b[k].alpha1*vk)-(xj+b[j].alpha1*vj),ord=2))/npl.norm(vk,ord=2)
        b[k].x_prev=b[k].x+b[k].vx*tcrit
        b[k].x=b[k].x_prev-b[k].vx*(1-tcrit)
        b[k].y_prev=b[k].y+b[k].vy*tcrit
        b[k].y=b[k].y_prev-b[k].vy*(1-tcrit)
        b[k].vx=-b[k].vx
        b[k].vy=-b[k].vy
    if((b[k].x+b[k].alpha1*b[k].vx>w-1-p_new) or (b[k].x+b[k].alpha1*b[k].vx<p_new)):
      tcrit=((w-1-p_new-b[k].x)/b[k].vx)*(b[k].x+b[k].alpha1*b[k].vx>w-1-p_new)+((b[k].x-p_new)/b[k].vx)*(b[k].x+b[k].alpha1*b[k].vx<p_new)
      b[k].x_prev=b[k].x+b[k].vx*tcrit
      b[k].x=b[k].x_prev-b[k].vx*(1-tcrit)
      b[k].vx=-b[k].vx
    if((b[k].y+b[k].alpha1*b[k].vy>w-1-p_new) or (b[k].y+b[k].alpha1*b[k].vy<p_new)):
      tcrit=((w-1-p_new-b[k].y)/b[k].vy)*(b[k].y+b[k].alpha1*b[k].vy>w-1-p_new)+((b[k].y-p_new)/b[k].vy)*(b[k].y+b[k].alpha1*b[k].vy<p_new)
      b[k].y_prev=b[k].y+b[k].vy*tcrit
      b[k].y=b[k].y_prev-b[k].vy*(1-tcrit)
      b[k].vy=-b[k].vy
    draw.ellipse((b[k].x-r,b[k].y-r,b[k].x+r,b[k].y+r),fill=col2)
  images.append(im)
images[0].save('pillow_imagedraw.gif',save_all=True,append_images=images[1:],optimize=False,duration=40,loop=0)
