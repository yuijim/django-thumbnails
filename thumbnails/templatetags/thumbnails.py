# -*- coding:utf-8 -*-
from thumbnails.utils import create_thumbnail
from django.template import Library
from django.conf import settings

register = Library()

@register.filter
def thumbnail(file, size=settings.THUMBNAILS_SIZE):
    return create_thumbnail(file, size)

@register.filter
def thumbnail_crop(file, size=settings.THUMBNAILS_SIZE):
	return create_thumbnail(file, size, crop=True)
