# coding=utf-8
from io import BytesIO
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

__author__ = 'kolyakoikelov'

RUSSIAN_ENGLISH_SYMBOLS = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ш': 'sh',
    'щ': 'sh',
    'ь': '\'',
    'ы': 'y',
    'ъ': '\'',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'ч': 'ch',
    'ө': 'o',
    'ң': 'n',
    'ү': 'u',
}


def transform(path):
    def wrapped(instance, filename):

        filename = filename.lower()
        for key in RUSSIAN_ENGLISH_SYMBOLS:
            if key in filename:
                filename = filename.replace(key, RUSSIAN_ENGLISH_SYMBOLS[key])
        return os.path.join(path, filename)

    return ''


def convert_cyrillic_to_latin(text):
    symbols = {
        u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd',
        u'е': 'e', u'ё': 'e', u'ж': 'j', u'з': 'z', u'и': 'i', u'й': 'y',
        u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o',
        u'п': 'p', u'р': 'r', u'с': 's', u'т': 't', u'у': 'u',
        u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch', u'ш': 'sh',
        u'щ': 'sch', u'ь': 'y', u'ы': 'y', u'ъ': 'y', u'э': 'e', u'ю': 'yu',
        u'я': 'ya',
    }

    for k, v in symbols.items():
        text = text.replace(k, v)

    return text


def create_thumbnail_image(main_image, thumb_image, thumbnail_size):
    if not main_image:
        return

    if main_image.name.endswith(".jpg") or main_image.name.endswith(".jpeg"):
        pil_type = 'jpeg'
        file_extension = 'jpg'
        image_type = 'image/jpeg'

    elif main_image.name.endswith(".png"):
        pil_type = 'png'
        file_extension = 'png'
        image_type = 'image/png'
    elif main_image.name.endswith(".gif"):
        pil_type = 'gif'
        file_extension = 'gif'
        image_type = 'image/gif'
    else:
        pil_type = 'jpeg'
        file_extension = 'jpg'
        image_type = 'image/jpeg'

    image = Image.open(BytesIO(main_image.read()))
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    output = BytesIO()
    image.save(output, pil_type)
    output.seek(0)
    thumbnail_image = SimpleUploadedFile(os.path.split(main_image.name)[-1], output.read(), content_type=image_type)
    thumb_image.save(
        '%s_thumbnail.%s' % (convert_cyrillic_to_latin(os.path.splitext(main_image.name)[0]), file_extension),
        thumbnail_image, save=False)
    main_image.seek(0)


def image_upload_to(instance, filename):
    filename_parts = filename.split('.')

    if len(filename_parts) > 0:
        ext = filename_parts[1]
        name = convert_cyrillic_to_latin(filename_parts[0].lower())

        filename = "%s.%s" % (name, ext)

    return os.path.join(instance.upload_to_path, filename)
