from PIL import Image
from img24 import CImage24
import array, random, math

class CDistribution(object):
	def __init__(self,sz):
		self.size=sz
		self.img=CImage24(sz,sz)
	
	def _Simple(self, x, y):
		return int(255 / ( 1.0+ math.sqrt(x*x+y*y)))
	
	def render(self, func=_Simple):
		for j in range(self.size):
			for i in range(self.size):
				c = func(self.size//2 - i,self.size//2 - j)
				self.img.setPixelAdd( i, j, (c,c,c))

class CSpeedLine(object):
	def __init__(self,sz,mul=1):
		self.size=sz
		self.img=CImage24(sz,sz)
		self.noise=[0 for i in range(sz)]
		rand=[random.randint(0,255) for i in range(sz)]
		if mul<=0: mul=1
		for j in range(sz):
			self.noise[j]=rand[int(j/mul)]
	
	def _Simple(self, x, y):
		a = self.size * math.atan2( x, y) / (2*math.pi) + self.size//2
		if a>=self.size:a=self.size-1
		return self.noise[int(a)]
	
	def _OverSampling(self, x, y):
		c = 0
		for k in range(4):
			for h in range(4):
				a = self.size * math.atan2((x + 0.25*k),(y + 0.25*h)) / (2*math.pi) + self.size//2
				if a>=self.size: a = self.size-1
				c += self.noise[int(a)]
		return int(c/16)
	
	def render(self, func=_Simple):
		for j in range(self.size):
			for i in range(self.size):
				c = func(self.size//2 - i,self.size//2 - j)
				self.img.setPixelAdd( i, j, (c,c,c))
	
	def setImage(self,img):
		self.img = img
	
	def getImage(self):
		return self.img
	


SIZE=2**7
for i in range(1):
	sl=CSpeedLine(SIZE,i*0.5+1)
	sl.render(sl._OverSampling)
	imgOut = sl.img.getPILImage()
	imgOut.save("../_saved_line_nonOS_"+str(SIZE)+"_"+str(i+1)+".bmp")
	
	#dis=CDistribution(SIZE)
	#dis.render(dis._Simple)
	#imgOut=dis.img.getPILImage()
	#imgOut.save("../_saved_dis_nonOS_"+str(SIZE)+"_"+str(i+1)+".bmp")
