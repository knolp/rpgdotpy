from PIL import Image

pic = Image.open("test.png")

xx = 25
yy = 25

pic = pic.resize((xx,yy), Image.ANTIALIAS).convert("RGBA")

pic.save("output.png")
pixels = pic.load()
values = []
new = []
mod = 100


for y in range(yy):
	for x in range(xx):
		value = pic.getpixel((x,y))
		values.append(value)
		red = value[0] - (value[0] % mod)
		green = value[1] - (value[1] % mod)
		blue = value[2] - (value[2] % mod)
		pixels[x,y] = (red, green, blue, value[3])

pic.save("output2.png")