import base64


def base64ToJGP(base64Image, name):
    imageLen = len(base64Image)
    image = base64Image[22:imageLen]
    imgdata = base64.b64decode(image)
    filename = '/static/images/'+name+'.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
        return filename
    return 'failed the image convertion'
    