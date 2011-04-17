#-*- coding: utf-8 -*-
import re
from django.db.models.fields.files import ImageFieldFile,ImageField
import os
from django.conf import settings
from django.db.models import signals

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

    def contribute_to_class(self, cls, name):
        super(ImageField, self).contribute_to_class(cls, name)
        signals.post_delete.connect(self.delete_file, sender=cls)
        
    def delete_file(self, instance, sender, **kwargs): 
        file = getattr(instance, self.attname) 
        # If no other object of this type references the file, 
        # and it's not the default value for future objects, 
        # delete it from the backend. 
        if file and file.name != self.default and \
            not sender._default_manager.filter(**{self.name: file.name}): 
                file.delete(save=False) 
        elif file: 
            # Otherwise, just close the file, so it doesn't tie up resources. 
            file.close() 

try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^thumbnails\.fields\.TImageField"])
except ImportError:
	pass
