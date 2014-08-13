from PIL import Image
from os import listdir, remove
from subprocess import check_output, call


#find all .png files in working directory
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
    #This selection is of 4 data values in the image
    #The 2 scintilators and 2 copies of the coincidence
    img = Image.open(i)
    SCINT_top = 187
    SCINT_left = 409
    SCINT_bottom = 218
    SCINT_right = 520
    box = (SCINT_left, SCINT_top, SCINT_right, SCINT_bottom)
    area = img.crop(box)
    area.save(i+'.cropped.ppm','ppm')
    #crop the area
    crops.append(i+'.cropped.ppm')

    #The area in the image that contains the
    #XION data
    IFC_NIM_top = 446
    IFC_NIM_left = 746
    IFC_NIM_bottom = 460
    IFC_NIM_right = 844

    box = (IFC_NIM_left, IFC_NIM_top, IFC_NIM_right, IFC_NIM_bottom)
    #crop the area
    area = img.crop(box)

    area.save(i+'.cropped2.ppm','ppm')
    crops.append(i+'.cropped2.ppm')

cropped1 = True
datafile = open("data.csv", "w")
for i in crops:
    #-C "0123456789" tells gocr that the images contains only numbers
    #This is needed because it would read 0 as O
    data = (check_output(["gocr", "-C", "0123456789", i]))
    splitdata = data.split()
    if cropped1:
        for j in splitdata: 
            datafile.write(j+", ")
        cropped1 = not cropped1
    else:
        try:
            #split(".")[0] removes everthing after the . thus leaving only the date-time
            datafile.write(splitdata[0] + ", " + i.split(".")[0] +"\n")
        except IndexError:
            datafile.write("something wrong in " + i.split(".")[0] +"\n")
            print "something wrong in " + i.split(".")[0] +"\n"
        cropped1 = not cropped1
    #cleanup
    remove(i)

datafile.close()
