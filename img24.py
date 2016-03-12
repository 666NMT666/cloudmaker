from PIL import Image

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
		
	def blendImage(self, img):
		for y in range(self.height):
			for x in range(self.width):
				self.setPixelAdd(x,y,img.getPixel(x,y))

	def getPILImage(self):
		return Image.frombuffer('RGB',(self.width,self.height),bytes(self.buffer),"raw",'RGB',0,1)
	
	def loadPILImage(self, fname):
		img=Image.open(fname)
		(self.width,self.height)=img.size
		self.buffer=bytearray(img.convert('RGB').tostring())
	
	def save(self,fname):
		self.getPILImage().save(fname)


if __name__ == '__main__':
	for i in range(8):
		img1 = CImage24(fname="saved/saved"+str(i)+".png")
		img2 = CImage24(fname="images/smile"+str(i)+".png")
		for y in range(img1.height):
			for x in range(img1.width):
				img1.setPixelAdd(x,y,img2.getPixel(x,y))
		img1.save("saved"+str(i)+".png")
