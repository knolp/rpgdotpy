from PIL import Image
import sys
import os

if len(sys.argv) == 1:
	print("Need to specify gif-file")

im = Image.open(sys.argv[1])
save_name = sys.argv[1].split(".")[0]
print(f"{sys.argv[1]} contained {im.n_frames} frames.")
counter = 0
while True:
	try:
		im.seek(counter)
		temp = im.convert("L")
		temp = temp.resize((150,49))
		temp.save(f"animations/tmp/img_{counter}.png")
	except EOFError:
		break
	counter += 1


images = [Image.open(f"animations/tmp/img_{counter}.png") for counter in range(0,im.n_frames)]
f = open(f"animations/{save_name}.txt", "w")
for i in range(len(images)):
	gray = images[i].convert('L')
	for x in range(49):
		for y in range(150):
			value = gray.getpixel((y,x))
			if value < 200:
				gray.putpixel((y,x), 255)
				f.write("#")
			else:
				gray.putpixel((y,x), 0)
				f.write(" ")

		f.write("\n")
	#for item in dir(gray):
	#	print(item)
	#bw = gray.point(lambda x: 0 if x<128 else 255, '1')
	images[i] = gray
	#images[i] = images[i].convert("l")
	#pass
f.close()
images[0].save(f"animations/tmp/gifs/{save_name}.gif", save_all=True, append_images=images[1:], loop=0)
for item in os.listdir("animations/tmp"):
	if item.startswith("img_"):
		os.remove(os.path.join("animations/tmp/", item))
