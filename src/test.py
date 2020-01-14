from PIL import Image

pic = Image.open("test.png").convert("LA")

xx = 150
yy = 50

pic = pic.resize((xx,yy), Image.ANTIALIAS)

pic.save("output.png")

with open("test.txt", "w")as f:
	for y in range(yy):
		text = ""
		for x in range(xx):
			print(x,y)
			value = pic.getpixel((x,y))
			print(value)
			if value[0] > 100:
				text = text + " "
			else:
				text = text + "#"
		f.write(text + "\n")