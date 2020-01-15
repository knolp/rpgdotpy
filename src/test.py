from PIL import Image

pic = Image.open("test.png")

xx = 150
yy = 50

pic = pic.resize((xx,yy), Image.ANTIALIAS)

pic.save("output.png")
pixels = pic.load()
print(type)
values = []
new = []


for y in range(yy):
	for x in range(xx):
		value = pic.getpixel((x,y))
		values.append(value)
		temp = value[0] - (value[0] % 10)
		new.append(temp)
		pixels[x,y] = (temp, 255, 100)

pic.save("output2.png")

print(len(set(values)))
print(len(set(new)))

for item in set(new):
	print(item)