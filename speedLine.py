from PIL import Image
import array, random, math

class CImage24(object):		
	def __init__(self,width=0,height=0,fname=0):
		if fname==0:
			self.width=width
			self.height=height
			self.buffer=[0 for i in range(width*height*3)]
		else:
			self.loadPILImage(fname)
		
	def getPixel(self,x,y):
		if x>=self.width or y>=self.height or y<0 or x<0: return (0,0,0)
		return (self.buffer[x*3+y*self.width*3+0],self.buffer[x*3+y*self.width*3+1],self.buffer[x*3+y*self.width*3+2])
	
	def setPixel(self,x,y,color):
		if x>=self.width or y>=self.height or y<0 or x<0: return
		for i in range(3):
			self.buffer[x*3+y*self.width*3+i]=color[i]
	
	def setPixelAdd(self,x,y,color):
		if x>=self.width or y>=self.height or y<0 or x<0: return
		for i in range(3):
			tmp=color[i]+self.buffer[x*3+y*self.width*3+i]
			if tmp > 255: tmp = 255
			self.buffer[x*3+y*self.width*3+i]=tmp

	def setPixelMul(self,x,y,color):
		if x>=self.width or y>=self.height or y<0 or x<0: return
		for i in range(3):
			tmp=(color[i]*self.buffer[x*3+y*self.width*3+i])//256
			self.buffer[x*3+y*self.width*3+i]=tmp

	def brend(self, img):
		w = min(self.width,img.width)
		h = min(self.height,img.height)
		for y in range(h):
			for x in range(w):
				self.setPixelAdd(x,y,img.getPixel(x,y))

	def reverse(self):
		for y in range(self.height):
			for x in range(self.width):
				tmp=self.getPixel(x,y)
				self.setPixel(x,y,(255-tmp[0],255-tmp[1],255-tmp[2]))

	def getPILImage(self):
		return Image.frombuffer('RGB',(self.width,self.height),bytes(self.buffer),"raw",'RGB',0,1)
	
	def loadPILImage(self, fname):
		img=Image.open(fname)
		(self.width,self.height)=img.size
		self.buffer=bytearray(img.convert('RGB').tostring())
	
	def save(self,fname):
		self.getPILImage().save(fname)


class CImageMaker(object):
	def setImage(self,img):
		self.img = img
	
	def getImage(self):
		return self.img

	def save(self, fname):
		self.img.save(fname)

	def brend(self, imgMaker):
		self.img.brend(imgMaker.img)

class CDistribution(CImageMaker):
	def __init__(self,w,h):
		self.width=w
		self.height=h
		self.img=CImage24(w,h)
	
	def _Simple(self, x, y, const=1.0):
		return int(255 / ( 1.0+ const*math.sqrt(x*x+y*y)))

	def render(self, func, const=1.0):
		for j in range(self.height):
			for i in range(self.width):
				c = func(self.width//2 - i,self.height//2 - j, const)
				self.img.setPixelAdd( i, j, (c,c,c))

class CSpeedLine(CImageMaker):
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
	
	def render(self,func):
		for j in range(self.size):
			for i in range(self.size):
				c = func(self.size//2 - i,self.size//2 - j)
				self.img.setPixelAdd( i, j, (c,c,c))


if __name__ == '__main__':
	SIZE=2**7
	for i in range(8):
		sl=CSpeedLine(SIZE,1)
		sl.render(sl._OverSampling)
		dis=CDistribution(SIZE, SIZE)
		dis.render(dis._Simple, 0.01115+0.01*random.random())
		dis.brend(sl)
		dis.img.reverse()
		dis.save("../_saved_dis_speedline_nonOS_MUL"+str(SIZE)+"_"+str(i+1)+".bmp")
