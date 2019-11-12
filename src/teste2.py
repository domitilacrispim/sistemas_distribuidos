import os
from threading import Thread
from time import sleep
from random import randint

class Th_cliente(Thread):

 def __init__ (self, num):
   Thread.__init__(self)
   self.num = num
   self.passaro=["arara", "rabanada", "agapornis", "sabia", "pombo", "passaro_nadave"]
 def run(self):
  os.system("python3.7 client.py "+str(self.passaro[randint(0,5)])+ " 2")

class Th(Thread):

 def __init__ (self, num):
   Thread.__init__(self)
   self.num = num
 def run(self):
  os.system("python3.7 server.py 2")


b=Th(0)
b.start()
a=[]
sleep(4)
for i in range(10):
 a.append(Th_cliente(i))
 a[i].start()

