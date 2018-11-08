try:
    from PIL import Image, ExifTags
    errored = False
except ImportError:
    errored = True
    print("You need to install Pillow\npip3 install pillow")

from glob import glob
import os, sys


ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
HELP_DIALOG = "please specify the folder containing images and optionally the new height and width eg.\npython3 make_ratio your_image_folder_name 200 300"


""" 
printing a progress bar 
from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
"""
def printProgressBar ( iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█' ):
    percent = ( "{0:." + str( decimals ) + "f}" ).format( 100 * ( iteration / float( total ) ) )
    filledLength = int( length * iteration // total )
    bar = fill * filledLength + '-' * ( length - filledLength )
    print( '\r%s |%s| %s%% %s' % ( prefix, bar, percent, suffix ), end = '\r' )

    if iteration == total: 
        print()


""" resize an image, preserving aspect ratio and keeping it centerred """
def resizer(img, w, h):
    offset_x, offset_y = 0, 0
    if img.width / img.height > w / h:
        new_width = w*img.height//h
        offset_x = (img.width - new_width)//2
    else:
        new_height = h*img.width//w
        offset_y = (img.height - new_height)//2
    img = img.crop( ( offset_x, offset_y, img.width - offset_x, img.height - offset_y) )
    img = img.resize( (w, h), Image.ANTIALIAS)
    return img


""" rotate by 90 degrees any images that have Orientation 5, 6, 7, or 8 """
def correct_rotation(img):
    try:
        exif=dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
        if "UserComment" in exif:
            del exif["UserComment"]
        if "MakerNote" in exif:
            del exif["MakerNote"]

        if exif['Orientation']:
            if exif['Orientation'] > 4:
                img = img.rotate(-90, expand=True)
    except AttributeError as e:
        pass
    return img

""" crop and resize the images to 400 by 600 """
def make_ratios(folder, w=400, h=600):
    new_folder = folder + "_resized"
    os.mkdir(os.getcwd() + "/" + new_folder)
    images = []
    for extension in ALLOWED_EXTENSIONS:
        images += glob(folder + "/*" + extension)

    x = 1
    for image in images:
        i = Image.open(image)
        i = correct_rotation(i)
        i = resizer(i, w, h)
        new_filename = new_folder + "/" + image.split("/")[-1]
        i.save(new_filename)
        printProgressBar(x, len(images), prefix = 'Progress:', suffix = "", length = 50)
        x += 1

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(HELP_DIALOG)
    elif not errored:
        if len(sys.argv) == 4:
            make_ratios(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        else:
            make_ratios(sys.argv[1])

# TODO: facial detection mode, center cropped image around detected face