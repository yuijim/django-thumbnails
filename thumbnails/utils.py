#-*- coding: utf-8 -*-
import os
import Image
from django.conf import settings

def get_thumbnail_filename(filepath, size, crop=False):
    if isinstance( size, tuple ):
        size = '%dx%d' % size[:2]
    filehead, filetail = os.path.split(filepath)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + ( 'c' if crop else '') + format

    return miniature

# modified snippet from djangosnippets.org
def create_thumbnail(file, size=settings.THUMBNAILS_SIZE, miniature_subdir=settings.THUMBNAILS_SUBDIR, crop=False):
    if isinstance( size, tuple ):
        x, y = size[:2]
    elif isinstance( size, basestring ):
        x, y = [float(x) for x in size.split('x')]
    #getting miniature name
    miniature = get_thumbnail_filename(file.path, size, crop)
    #getting miniature url
    filehead, filetail = os.path.split(file.url)
    filehead = os.path.join(filehead,miniature_subdir)
    miniature_url = filehead + '/' + miniature
    #getting miniature filename
    filehead2, filetail2 = os.path.split(file.path)
    filehead2 = os.path.join(filehead2,miniature_subdir)
    miniature_filename = os.path.join(filehead2, miniature)
    if os.path.exists(miniature_filename) and os.path.getmtime(file.path)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if miniature subdir does ot exist, create it
    subdir, fn = os.path.split(file.path)
    p = os.path.join(subdir,miniature_subdir)
    if not os.path.exists(p):
        os.mkdir(p)
        i = open(os.path.join(p,"index.html"),"w")
        i.close()
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(file.path)
        if crop:
            cx,cy = image.size
            s = min(cx/x,cy/y)
            nx,ny = int(s*x),int(s*y)
            ox,oy = int((cx-nx)/2),int((cy-ny)/2)
            box = (ox,oy,ox+nx,oy+ny)
            image = image.crop(box)
        image.thumbnail([int(x), int(y)], Image.ANTIALIAS)
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url
