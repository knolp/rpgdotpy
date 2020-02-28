from PIL import Image

pic = Image.open("bord.jpg")

anchors = [35,60,120,180,240,300]

def convert_light(n):
	if n < 40:
		return 0
	elif n > 240:
		return 255
	else:
		return 127

xx = 1000
yy = 1000
pic = pic.resize((xx,yy), Image.ANTIALIAS).convert("HSV")
ret_list = []

mod = 16
tilesize = 5
iterations_x = int(xx / tilesize)
iterations_y = int(yy / tilesize)



for x in range(xx):
	for y in range(yy):
		value = pic.getpixel((x,y))
		closest = min([abs(value[0] - x) for x in anchors])
		sat = abs(value[1] - 270)
		if sat > 230:
			sat = 230
		pic.putpixel((x,y),(closest, sat ,value[2]))


#for i in range(iterations_x):
#	for j in range(iterations_y):
#		region_values = []
#		for x in range(i * tilesize, (i * tilesize) + tilesize):
#			for y in range(j * tilesize, (j * tilesize) + tilesize):
#				region_values.append(pic.getpixel((x,y)))
#		
#		#Get max and put pixels
#		most = max(region_values, key=region_values.count)
#
#		for x in range(i * tilesize, (i * tilesize) + tilesize):
#			for y in range(j * tilesize, (j * tilesize) + tilesize):
#				pic.putpixel((x,y), most)







	#print(pic.getpixel((x,y)))
	#value = pic.getpixel((50, x))[0]
	#if value not in ret_list:
		#ret_list.append(value)


pic.convert('RGB').save("output2.png", "PNG", optimize=True)