import json
from PIL import Image, ExifTags
from docx import Document
import docx
from PyPDF2 import PdfFileReader

image_format = ["jpg","png","jpeg"]
docx_format = ['docx', 'doc']

# Processing Meta Deta Of The File
def create_input_meta_data(request):
    meta_data={}
    file=request.FILES['document']
    extention=file.name.split('.')[::-1][0]
    meta_data['file_name']=file.name
    meta_data['extention']=extention
    meta_data['file_size']=str(file.size/1000)+" Kbs"
    meta_data['mime_type']=file.content_type
    meta_data['content_extra_type']=file.content_type_extra
    meta_data['charset']=file.charset

    details={}

    # If image
    if(extention in image_format):
        img = Image.open(file)
        img_exif = img.getexif()

        if img_exif is not None:
            img_exif_dict = dict(img_exif)

            for key, val in img_exif_dict.items():
                if key in ExifTags.TAGS:
                    details[str(ExifTags.TAGS[key])]=str(repr(val))
                    # ExifVersion:b'0230'
                    # ...
                    # FocalLength:(2300, 100)
                    # ColorSpace:1
                    # FocalLengthIn35mmFilm:35
                    # ...
                    # Model:'X-T2'
                    # Make:'FUJIFILM'
                    # ...
                    # DateTime:'2019:12:01 21:30:07'
                    # ...
            details['mode']=img.mode
            details['size']=str(img.size[0])+'x'+str(img.size[1])
            details['height']=img.size[0]
            details['width']=img.size[1]

    # If docx
    elif(extention in docx_format):
        document = Document(file)
        core_properties = document.core_properties
        details['author']=core_properties.author
        details['category']=core_properties.category
        details['comments']=core_properties.comments
        details['content_status']=core_properties.content_status
        details['created']=str(core_properties.created)
        details['identifier']=core_properties.identifier
        details['keywords']=core_properties.keywords
        details['language']=core_properties.language
        details['last_modified_by']=str(core_properties.last_modified_by)
        details['last_printed']=str(core_properties.last_printed)
        details['modified']=str(core_properties.modified)
        details['revision']=core_properties.revision
        details['subject']=core_properties.subject
        details['title']=core_properties.title
        details['version']=core_properties.version

    # If PDF
    elif(extention == "pdf"):
        pdf = PdfFileReader(file)
        info = pdf.getDocumentInfo()

        details['author']=info.author
        details['creator']=info.creator
        details['producer']=info.producer
        details['producer']=info.producer
        details['subject']=info.subject
        details['title']=info.title
        details['pages']=pdf.getNumPages()

    #print(json.dumps(details, indent=4))
    meta_data['details']=details
    return meta_data
