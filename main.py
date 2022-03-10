from fileinput import close
from random import random, sample
from tkinter import CENTER
from typeInfo import *
from ray import Ray
from vector import *

# Image

aspectRatio = 16.0 / 9.0
imageWidth = 400
imageHeight = int(imageWidth / aspectRatio)
samplePerPixel = 100


# Camera
class Camera:
    def __init__(self):
        self.aspectRatio = 16.0 / 9.0
        self.viewportHeight = 2.0
        self.viewportWidth = self.aspectRatio * self.viewportHeight
        self.focalLength = 1.0

        self.origin = Point3(0,0,0)
        self.horizontal = Vec3(self.viewportWidth,0,0)
        self.vertical = Vec3(0,self.viewportHeight,0)
        self.lowerLeftCorner = self.origin - self.horizontal/2 - self.vertical/2 - Vec3(0,0,self.focalLength)
    
    def getRay(self, u,v):
        return Ray(self.origin, self.lowerLeftCorner + u*self.horizontal + v*self.vertical - self.origin)


camera = Camera()

# Utils
def randomRange(min,max):
    return min + (max-min) * random.random()
# Render

class HitRecord:
    def __init__(self):
        self.p = Point3()
        self.normal = Vec3()
        self.t = 0
        self.frontFace = False

    def setFaceNormal(self, ray, outwardNormal):
        self.frontFace = glm.dot(ray.direction, outwardNormal) < 0
        self.normal = outwardNormal if self.frontFace else -outwardNormal

class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def hit(self, ray, tMin, tMax):
        oc = ray.origin - self.center
        a = lenSquared(ray.direction)
        half_b = glm.dot(oc, ray.direction)
        c = lenSquared(oc) - self.radius * self.radius

        discriminant = half_b * half_b - a*c
        if discriminant < 0: return False,None
        sqrtd = glm.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root < tMin or tMax < root:
            root = (-half_b + sqrtd) / a
            if root < tMin or tMax < root:
                return False, None

        record = HitRecord()
        record.t = root
        record.p = ray.at(record.t)
        outwardNormal = (record.p - self.center) / self.radius
        record.setFaceNormal(ray, outwardNormal)

        return True, record

class HittableList:
    def __init__(self):
        self.objects = []

    def hit(self, ray, tMin, tMax):
        hitRec = None
        hitAnything = False
        closest = tMax

        for object in self.objects:
            hitResult = object.hit(ray, tMin, closest) 
            if hitResult[0]:
                hitAnything = True
                closest = hitResult[1].t
                hitRec = hitResult[1]
        
        return hitAnything, hitRec

# World
world = HittableList()
sphere1 = Sphere(Point3(0,0,-1), 0.5)
sphere2 = Sphere(Point3(0,-100.5,-1), 100)
world.objects.append(sphere1)
world.objects.append(sphere2)

def hitSphere(center, radius, ray):
    oc = ray.origin - center
    a = lenSquared(ray.direction)
    half_b = glm.dot(oc, ray.direction)
    c = lenSquared(oc) - radius*radius
    
    discriminant = half_b*half_b - a*c

    if discriminant < 0:
        return -1.0
    else:
        return (-half_b - glm.sqrt(discriminant)) / a

def writeColor(outputString, color):
    ir = int(255.999 * color.r)
    ig = int(255.999 * color.g)
    ib = int(255.999 * color.b)
    outputString += "{} {} {} \n".format(ir,ig,ib)
    return outputString

def writeColorScaled(outputString, color, samplePerPixel):
    r = color.r
    g = color.g
    b = color.b
    
    #Divide color by the number of samples
    scale = 1.0 / samplePerPixel
    r *= scale
    g *= scale
    b *= scale

    # Write the translated [0,255] of each component
    ir = int(256 * glm.clamp(r,0.0,0.999))
    ig = int(256 * glm.clamp(g,0.0,0.999))
    ib = int(256 * glm.clamp(b,0.0,0.999))
    outputString += "{} {} {} \n".format(ir,ig,ib)
    return outputString


def rayColor(ray, _world):
    hitResult = _world.hit(ray, 0, float('inf'))
    if hitResult[0]:
        return 0.5 * (hitResult[1].normal + Color(1,1,1))

    unitDirection = glm.normalize(ray.direction)
    t = 0.5 * (unitDirection.y + 1.0)
    return (1.0-t) * Color(1.0,1.0,1.0) + t * Color(0.5,0.7,1.0)

imageString = "P3\n{} {}\n255\n".format(imageWidth, imageHeight)
for j in reversed(range(imageHeight-1)):
    print("\rScanlines remaining: {} ", j)
    for i in range(imageWidth):
        pixelColor = Color(0,0,0)
        for s in range(samplePerPixel):
            u = (i + random()) / (imageWidth - 1)
            v = (j + random()) / (imageHeight - 1)
            ray = camera.getRay(u,v)
            pixelColor += rayColor(ray,world)
        imageString = writeColorScaled(imageString, pixelColor, samplePerPixel)
print("\nDone\n")

file = open("result.ppm", "w")
file.write(imageString)
file.close()

