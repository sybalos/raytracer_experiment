
from typeInfo import *

from ray import Ray

imageWidth = 256
imageHeight = 256
imageString = "P3\n{} {}\n255\n".format(imageWidth, imageHeight)

def writeColor(outputString, color):
    ir = int(255.999 * color.r)
    ig = int(255.999 * color.g)
    ib = int(255.999 * color.b)
    outputString += "{} {} {} \n".format(ir,ig,ib)
    return outputString

for j in reversed(range(imageHeight-1)):
    print("\rScanlines remaining: {} ", j)
    for i in range(imageWidth):
        color = Color(float(i) / (imageWidth - 1), float(j) / (imageHeight - 1), 0.25 )
        imageString = writeColor(imageString, color)
print("\nDone\n")


file = open("result.ppm", "w")
file.write(imageString)
file.close()

