#-*- coding: utf-8 -*-
import re
from django.db.models.fields.files import ImageFieldFile,ImageField
import os
from django.conf import settings

class TImageFieldFile(ImageFieldFile):
    def delete(self, save=True):
        #remove all existing thumbnails
        filehead, filetail = os.path.split(self.name)
        basename, format = os.path.splitext(filetail)
        miniatures_dir = os.path.join(self.storage.location,filehead,settings.THUMBNAILS_SUBDIR)
        pattern = re.compile(r'^%s_(\d+x\d+)c?%s$' % (basename, format))
        for file in os.listdir(miniatures_dir):
            m = re.match(pattern, file)
            if m is not None:
                self.storage.delete(os.path.join(filehead,settings.THUMBNAILS_SUBDIR,file))

        super(self.__class__, self).delete(save)

class TImageField(ImageField):
    attr_class = TImageFieldFile

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^thumbnails\.fields\.TImageField"])
except ImportError:
	pass
