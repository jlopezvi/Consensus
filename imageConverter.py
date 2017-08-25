import base64
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def base64ToJGP(base64Image, name):
	base64Image += "=" * ((4 - len(base64Image) % 4) % 4)
	imageLen = len(base64Image)
	image = base64Image[22:imageLen]
	imgdata = base64.b64decode(image)
	path = '/static/images'+name+'.jpg'
	fullpath = basedir + path
	with open(fullpath, 'wb') as f:
		f.write(imgdata)
		return path
	return 'failed the image convertion'