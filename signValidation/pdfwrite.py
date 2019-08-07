import fitz

class pdfwrite:
	def __init__(self, pdfName, imageName, saveName):
		self.pdfName = pdfName
		self.imageName = imageName
		self.saveName = saveName

	def processing(self):
		doc = fitz.open(self.pdfName)
		page = doc[0]
		rect = fitz.Rect(95,727,205,760)
		pix = fitz.Pixmap(self.imageName)
		page.insertImage(rect, pixmap = pix, overlay = True)
		doc.save(self.saveName)
		doc.close()

#obj = pdfwrite("aof.pdf", "0233727630.png", "newpdf.pdf")
#obj.processing()