import time
import hashlib
import PIL
import numpy
import qrcode
import cv2

def get_id(length):
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    return hash.hexdigest()[:length]

def rand_filename(extention,name_length = 4):
    name = get_id(name_length) + extention
    return name

def make_qrcode(text):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=4,
    border=3,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    img = numpy.array(qr_img.convert('RGB'))
    img = img[:, :, ::-1].copy() 
    return img

def save_frame(img,location):
    cv2.imwrite( location, img)

def qr_overlay(image,qr):
    # I want to put logo on top-left corner, So I create a ROI
    qr_rows,qr_cols,channels = qr.shape
    img_rows,img_cols,img_channels = image.shape

    image[img_rows-qr_rows:img_rows, 0:qr_cols] = qr

    return image

def main():
    print("use within app")



if __name__ == "__main__":
    main()