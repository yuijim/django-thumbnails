Django Thumbnails
=================

Django Thumbnails started as modified [thumbnail filter from
django snippets](http://djangosnippets.org/snippets/1718/). It evolved
to contain custom ImageField ([South](http://south.aeracode.org/)-aware) 
and tabular inline admin template.

In addition app utilizes
[code](http://github.com/thsutton/django-application-settings)
that allows application set its own default settings. 

Usage
-----

Django Thumbnails comes with two default settings:
    THUMBNAILS_SIZE = "128x128"
    THUMBNAILS_SUBDIR = "thumbnails"
    
`THUMBNAILS_SIZE` contains default width x height values. Only positive
integers are allowed.
`THUMBNAILS_SUBDIR` specifies default subdir, when the thumbnails are
stored. It is always relative to the directory containing original file. 

### Filters

Load filters in template using:
    {% load thumbnail %}
    
To create normal thumbnails (width & height doesn't exceed specified
dimentions, but whole image is resized proportionally) use one of the
following:
    <img src="{{ object.image|thumbnail }}" />
    <img src="{{ object.image|thumbnail:"240x240" }}" />
Argument of the filter specifies desired width x height.

To create cropped thumbnail (width & height are exactly as specified - 
not counting rounding errors) use:
    <img src="{{ object.image|thumbnail_crop }}" />
    <img src="{{ object.image|thumbnail_crop:"240x240" }}" />

### TImageField

Use of the thumbnail filters is the most effective when coupled with
`TImageField`. `TImageField` is normal django `ImageField` except for
the fact that it is thumbnails-aware - when the original image file is
being deleted, thumbnails files are deleted too.

### Admin

To take full advantage of thumbnails filters one may want to use custom
tabular inline template for models containing image fields. To do so
specify `template` parameter in the `TabularInline` admin class:
    class PhotoInline(admin.TabularInline):
        model = Photo
        template = 'thumbnails/tabular.html'
