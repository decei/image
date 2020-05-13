from PIL import Image
im = Image.open('IMG_0909.jpeg')
pixelMap = im.load()

img = Image.new(im.mode, im.size)
pixelsNew = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if 205 in pixelMap[i,j]:
            pixelsNew[i,j] = (0, 0, 0)
        else:
            pixelsNew[i,j] = pixelMap[i,j]

img.show()       
img.save("image6.jpeg")
img.close()

ig = im.copy()
ig.save("ig.jpeg")
im.close()