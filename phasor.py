'''
phasor.py
Copyright (c) 2020 @RR_Inyo

Released under the MIT license.
https://opensource.org/licenses/mit-license.php
'''

# Drawing a phasor diagram of grid-tie VSC
from cmath import *
from turtle import *
import kandinsky as kd

# Drawing function
def drawvector(A,names,unit):
  xorig=-80
  yorig=0
  unitsize=160
  col=['blue','orange','green','brown','red','grey','purple']
  
  # Reset the turtle
  reset()
  hideturtle()
  penup()
  goto(xorig,yorig)
  kd.draw_string('O',xorig+160,-yorig+120)
  pendown()
  
  # Drawing
  for i, a in enumerate(A):
    setheading(phase(a)*180/pi)
    color(col[i % 7])
    forward(abs(a)/unit*unitsize/2)
    x, y = position()
    kd.draw_string(names[i],int(x)+160,-int(y)+120-8)
    forward(abs(a)/unit*unitsize/2)
  
  penup()
  
# Calculation function
def phasor(P,Q,Upccpu=1.0,f=50):
  # Message
  print('Phasor calc for grid-tie VSC')
  print('Copyright (c) 2020 @RR_Inyo')
  print('Version 0.1.0')
  print('----------')
  
  # Constants
  Upccnom=6600
  Usecnom=440
  Snom=100e3
  fnom=50
  Inom=Snom/Usecnom/sqrt(3)
  Zbase=Usecnom**2/Snom
  Z=[\
    (0.01+0.12j*f/fnom)*Zbase,\
    (0.005+0.07j*f/fnom)*Zbase
  ]
  Names_Z=[\
    'Transformer',\
    'Filter',\
  ]
  Names_U=[\
    'Usec',\
    'Ut',\
    'Uf',\
    'Uc',\
    'I'
  ]
  unit_plot=Usecnom
  
  # PCC voltage
  Upcc=Upccnom*Upccpu
  Usec=Usecnom*Upccpu
  print('Upcc=',Upcc,'V')
  print('Usec=',Usec,'V')
  print('----------')
  
  # Powers
  S=abs(P+Q*1j)
  print('P=',P,'W')
  print('Q=',Q,'var')
  print('S=',S,'VA')
  print('----------')
  
  # Current
  I=(P+Q*1j)/Usec/sqrt(3)
  print('I=',I,'A')
  print('|I|=',abs(I),'A')
  print('arg I=',phase(I)*180/pi,'deg')
  print('-----------')
  
  # Voltage drops
  Uz=[]
  U=[Usec]
  for i, z in enumerate(Z):
    Utmp=z*I*sqrt(3)
    Uz.append(Utmp)
    U.append(U[-1]-Utmp)
    print('After',Names_Z[i])
    print('U=',U[i+1],'V')
    print('|U|=',abs(U[i+1]),'V')
    print('----------')
  
  # Call the drawing function
  Uplot=[]
  Uplot.append(Usec)
  Uplot.extend([-i for i in Uz])
  Uplot.append(-U[-1])
  Uplot.append(I*Usecnom/Inom/2)
  drawvector(Uplot,Names_U,unit_plot)
