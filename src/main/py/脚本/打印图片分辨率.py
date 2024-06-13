import cv2

def jpeg_res(filename):
    with open(filename,'rb') as img_file:
        # height of image (in 2 bytes) is at 164th position
        img_file.seek(163)
        # read the 2 bytes
        a = img_file.read(2)
        # calculate height
        height = (a[0] << 8) + a[1]
        # next 2 bytes is width
        a = img_file.read(2)
        # calculate width
        width = (a[0] << 8) + a[1]
        print("The resolution of the image is",width,"x",height)

def getImageVar(imgPath):
    image = cv2.imread(imgPath)

    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar


if __name__ == '__main__':
    path = '/Users/jinmu/Downloads/1.png'
    jpeg_res(path)
    print(getImageVar(path))