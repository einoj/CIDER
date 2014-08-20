from PIL import Image
from os import listdir, remove
from subprocess import check_output, call
from guiselection import SelectImage
from sys import argv

if len(argv) != 2:
    print "This program takes one argument. An integer of how many boxes of data should be taken from the image."
    print "Ex. \"python cider.py 4\""
    exit()
try:
    num_boxes = int(argv[1])
except ValueError:
    print argv[1] + " is not an integer!"
    exit()

#find all .png files in dataimages directory
def get_images():
    files = listdir("./dataimages")
    images = []
    for f in files:
        if ".png" in f:
            f = "./dataimages/"+f
            images.append(f)
    return images

# get the bounds of the data to be extracted from the images
# this opens up the first image and lets the user select an area with their mouse
def get_crop_boxes(num_boxes, image):
    boxes = []
    for i in range(num_boxes):
        s = SelectImage(image)
        area = s.cropSelection()
        boxes.append(area)
    return boxes


def crop_images(images, boxes):
    print "Cropping images..."
    crops = []
    for i in images:
        # int included in filename to differentieate between the num_boxes
        boxnum = 0
        for box in boxes:
            #open image to be cropped using PIL
            img = Image.open(i)
            #crop the area
            area = img.crop(box)
            area.save(i+".cropped"+str(boxnum)+".ppm","ppm")
            crops.append(i+".cropped"+str(boxnum)+".ppm")
            boxnum += 1
    return crops

images = get_images()
crop_boxes = get_crop_boxes(num_boxes, images[0])
crops = crop_images(images, crop_boxes)
datafile = open("data.csv", "w")
counter = 0

print "Extracting data from images..."
for i in crops:
    counter += 1
    #-C "0123456789" tells gocr that the images contains only numbers
    #This is needed because it would read 0 as O
    data = (check_output(["gocr", "-C", "0123456789", i]))
    datafile.write(data.rstrip()+", ")
    if counter == num_boxes:
        #i is the file name, i.split(".")[1].split("/")[2] gets the date from the filename
        datafile.write(i.split(".")[1].split("/")[2] + "\n")
        counter = 0
    #cleanup
    remove(i)

datafile.close()
print "Done!"
