from PIL import Image
from os import listdir

def get_images():
    files = listdir('.')
    images = []
    for f in files:
        if ".png" in f:
            images.append(f)
    return images

images = get_images()

crops = []
for i in images:
    img = Image.open(i)
    SCINT_top = 187
    SCINT_left = 409
    SCINT_bottom = 218
    SCINT_right = 520
    box = (SCINT_left, SCINT_top, SCINT_right, SCINT_bottom)
    area = img.crop(box)
    area.save(i+'.cropped.ppm','ppm')
    crops.append(i+'.cropped.ppm')

    IFC_NIM_top = 446
    IFC_NIM_left = 746
    IFC_NIM_bottom = 460
    IFC_NIM_right = 844

    box = (IFC_NIM_left, IFC_NIM_top, IFC_NIM_right, IFC_NIM_bottom)
    area = img.crop(box)

    area.save(i+'.cropped2.ppm','ppm')
    crops.append(i+'.cropped2.ppm')

from subprocess import call
for i in crops:
    call(["gocr", i])
