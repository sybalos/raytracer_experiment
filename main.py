import glm

# Image

imageWidth = 256
imageHeight = 256

imageString = "P3\n{} {}\n255\n".format(imageWidth, imageHeight)
for i in reversed(range(imageHeight-1)):
    for j in range(imageWidth):
        r = float(i) / (imageWidth-1)
        g = float(j) / (imageHeight-1)
        b = 0.25

        ir = int(255.999 * r)
        ig = int(255.999 * g)
        ib = int(255.999 * b)

        imageString += "{} {} {} \n".format(ir,ig,ib)

file = open("result.ppm", "w")
file.write(imageString)
file.close()

