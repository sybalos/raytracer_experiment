from typeInfo import *
from ray import Ray

# Image

aspectRatio = 16.0 / 9.0
imageWidth = 400
imageHeight = int(imageWidth / aspectRatio)

# Camera

viewportHeight = 2.0
viewportWidth = aspectRatio * viewportHeight
focalLength = 1.0

origin = Point3(0,0,0)
horizontal = Vec3(viewportWidth, 0, 0)
vertical = Vec3(0,viewportHeight, 0)
lowerLeftCorner = origin - horizontal/2 - vertical/2 - Vec3(0,0,focalLength)

# Render

def hitSphere(center, radius, ray):
    oc = ray.origin - center
    a = glm.dot(ray.direction, ray.direction)
    b = 2.0 * glm.dot(oc, ray.direction)
    c = glm.dot(oc,oc) - radius * radius
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return -1.0
    else:
        return (-b - glm.sqrt(discriminant)) / (2.0*a)

def writeColor(outputString, color):
    ir = int(255.999 * color.r)
    ig = int(255.999 * color.g)
    ib = int(255.999 * color.b)
    outputString += "{} {} {} \n".format(ir,ig,ib)
    return outputString

def rayColor(ray):
    t = hitSphere(Point3(0,0,-1), 0.5, ray)
    if t > 0.0:
        N = Vec3(glm.normalize(ray.at(t) - Vec3(0,0,-1)))
        return 0.5*Color(N.x + 1, N.y + 1, N.z + 1)

    unitDirection = glm.normalize(ray.direction)
    t = 0.5 * (unitDirection.y + 1.0)
    return (1.0-t) * Color(1.0,1.0,1.0) + t * Color(0.5,0.7,1.0)

imageString = "P3\n{} {}\n255\n".format(imageWidth, imageHeight)
for j in reversed(range(imageHeight-1)):
    print("\rScanlines remaining: {} ", j)
    for i in range(imageWidth):
        u = float(i) / (imageWidth - 1)
        v = float(j) / (imageHeight - 1)
        r = Ray(origin, lowerLeftCorner + u * horizontal + v*vertical - origin)
        color = rayColor(r)
        imageString = writeColor(imageString, color)
print("\nDone\n")

#rayColor(Ray(Color(0,0,0), Vec3(0,0,0)))

file = open("result.ppm", "w")
file.write(imageString)
file.close()

