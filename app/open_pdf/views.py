import pathlib
import uuid

import numpy as np
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from typing import Dict

from .api_models.pdfRequestModels import ManualPdfModel

# Vector = list[float]
# ManualPdf = list[ManualPdfModel]
from .models import PdfSchedule
from django.conf import settings

from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

from .services.pdfServices import generate_pdfs_imgs, generate_pdfs

MEDIA_ROOT = str(settings.MEDIA_ROOT)


@csrf_exempt
def manual_pdf(request: WSGIRequest):
    request_json = json.loads(request.body)
    print(request_json)
    # request_json = request_json[0]
    # f = ManualPdfModel(name='sfsd',course="badwj",town="skfsdf")
    # ManualPdfRequest = ManualPdfModel.from_json(json.dumps(request_json))
    # ManualPdfRequest = ManualPdfModel.from_json(json.dumps(request_json))

    ManualPdfs = ManualPdfModel.schema().load(request_json, many=True)

    imagesDirUuid = uuid.uuid4()

    request_json = json.loads(request.body)
    manualPdfs = ManualPdfModel.schema().load(request_json, many=True)

    # pdfSchedule = PdfSchedule()
    #
    # pdfSchedule.count = len(manualPdfs)
    # pdfSchedule.dirName = imagesDirUuid
    # pdfSchedule.save()

    pathlib.Path(MEDIA_ROOT + '/imgs/' + str(imagesDirUuid)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(MEDIA_ROOT + '/pdfs/' + str(imagesDirUuid)).mkdir(parents=True, exist_ok=True)

    generate_pdfs_imgs(MEDIA_ROOT + '/imgs/' + str(imagesDirUuid), manualPdfs)

    generate_pdfs(MEDIA_ROOT + '/pdfs/' + str(imagesDirUuid),
                  MEDIA_ROOT + '/imgs/' + str(imagesDirUuid),
                  manualPdfs)
    resp = json.dumps({"url": settings.MEDIA_URL + 'pdfs/' + str(imagesDirUuid) + "/certificates.pdf"})
    return HttpResponse(resp, content_type='application/json')


@csrf_exempt
def manual_pdf111(request):
    if request.is_ajax() and request.POST:
        try:
            # page_images = []
            imagesDirUuid = uuid.uuid4()

            request_json = json.loads(request.body)
            manualPdfs = ManualPdfModel.schema().load(request_json, many=True)

            pdfSchedule = PdfSchedule()

            pdfSchedule.count = len(manualPdfs)
            pdfSchedule.dirName = imagesDirUuid
            pdfSchedule.save()

            pathlib.Path(MEDIA_ROOT + 'imgs/' + str(imagesDirUuid)).mkdir(parents=True, exist_ok=True)
            pathlib.Path(MEDIA_ROOT + 'pdfs/' + str(imagesDirUuid)).mkdir(parents=True, exist_ok=True)

            for i in np.arange(len(courses)):
                draw = Drawing()
                with Image(filename='imgs/sertf20.jpg') as image:
                    draw.font = 'open-sans/Montserrat/Montserrat-Bold.ttf'
                    # 19 = 25
                    # draw.font_size = 186
                    draw.font_size = 25 * 4
                    draw.fill_color = Color('#333333')
                    # name = transform_name(names[i])
                    name = transform_name(names[i], 21)
                    course = transform_name(courses[i], 21)
                    # draw.text(340, 2385, name)
                    # draw.text(340, 3173, courses[i])
                    draw.text(205, 1418 + 30, name)
                    draw.text(205, 1888 + 30, course)
                    draw.font = 'open-sans/Montserrat/Montserrat-Regular.ttf'
                    draw.font_size = 8 * 5
                    # draw.text(684, 5105, town)
                    draw.text(339 + 30, 3040, town)

                    # draw.viewbox(340, 2385, 340 + 2300, 2385 + 400)
                    draw(image)

                    image.save(filename='imgs/' + str(rand_uuid) + '/img_' + str(i) + '.jpg')

            # im1 = PILImage.open("imgs/" + str(rand_uuid) + "/img_0.jpg")

            # for i in np.arange(1, len(names)):
            #     im2 = PILImage.open("imgs/"+str(rand_uuid)+"/img_" + str(i) +".jpg")
            #     page_images.append(im2)

            # shutil.rmtree('imgs/' + str(rand_uuid))

            pdf1_filename = "pdfs/" + str(rand_uuid) + "/cutway.pdf"

            # im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True, append_images=page_images)
            pdf = FPDF('P', 'mm', 'A4')
            pdf.set_auto_page_break(0)

            for i in np.arange(0, len(names)):
                #     im2 = PILImage.open("imgs/" + str(rand_uuid) + "/img_" + str(i) + ".jpg")
                # for image in imagelist:
                pdf.add_page()
                pdf.image("imgs/" + str(rand_uuid) + "/img_" + str(i) + ".jpg", w=200)
            pdf.output(pdf1_filename, "F")

            scheduler.enqueue_in(timedelta(days=1), delete_later_pdf, str(rand_uuid))
            # scheduler.enqueue_in(timedelta(minutes=1), delete_later_pdf, str(rand_uuid))

            data = json.dumps({'success': str(rand_uuid), 'error': None, 'description': None})

            return HttpResponse(data, content_type='application/json')

        except Exception as e:
            data = json.dumps({'success': None, 'error': True, 'description': "Произошла ошибка \n" + str(e)})
            return HttpResponse(data, content_type='application/json')

#
# @csrf_exempt
# def manual_pdf(request):
#     if request.is_ajax() and request.POST:
#         try:
#             names = request.POST.getlist("names[]")
#             courses = request.POST.getlist("courses[]")
#             town = request.POST['town']
#
#             page_images = []
#             rand_uuid = uuid.uuid4()
#
#             # s = Sertificates.objects.first()
#             # s.payment = s.payment + len(courses)
#             # s.save()
#
#             pathlib.Path('imgs/' + str(rand_uuid)).mkdir(parents=True, exist_ok=True)
#             pathlib.Path('pdfs/' + str(rand_uuid)).mkdir(parents=True, exist_ok=True)
#             for i in np.arange(len(courses)):
#                 draw = Drawing()
#                 with Image(filename='imgs/sertf20.jpg') as image:
#                     draw.font = 'open-sans/Montserrat/Montserrat-Bold.ttf'
#                     # 19 = 25
#                     # draw.font_size = 186
#                     draw.font_size = 25 * 4
#                     draw.fill_color = Color('#333333')
#                     # name = transform_name(names[i])
#                     name = transform_nameV2(names[i], 21)
#                     course = transform_nameV2(courses[i], 21)
#                     # draw.text(340, 2385, name)
#                     # draw.text(340, 3173, courses[i])
#                     draw.text(205, 1418 + 30, name)
#                     draw.text(205, 1888 + 30, course)
#                     draw.font = 'open-sans/Montserrat/Montserrat-Regular.ttf'
#                     draw.font_size = 8 * 5
#                     # draw.text(684, 5105, town)
#                     draw.text(339 + 30, 3040, town)
#
#                     # draw.viewbox(340, 2385, 340 + 2300, 2385 + 400)
#                     draw(image)
#
#                     image.save(filename='imgs/' + str(rand_uuid) + '/img_' + str(i) + '.jpg')
#
#             # im1 = PILImage.open("imgs/" + str(rand_uuid) + "/img_0.jpg")
#
#             # for i in np.arange(1, len(names)):
#             #     im2 = PILImage.open("imgs/"+str(rand_uuid)+"/img_" + str(i) +".jpg")
#             #     page_images.append(im2)
#
#             # shutil.rmtree('imgs/' + str(rand_uuid))
#
#             pdf1_filename = "pdfs/" + str(rand_uuid) + "/cutway.pdf"
#
#             # im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True, append_images=page_images)
#             pdf = FPDF('P', 'mm', 'A4')
#             pdf.set_auto_page_break(0)
#
#             for i in np.arange(0, len(names)):
#                 #     im2 = PILImage.open("imgs/" + str(rand_uuid) + "/img_" + str(i) + ".jpg")
#                 # for image in imagelist:
#                 pdf.add_page()
#                 pdf.image("imgs/" + str(rand_uuid) + "/img_" + str(i) + ".jpg", w=200)
#             pdf.output(pdf1_filename, "F")
#
#             scheduler.enqueue_in(timedelta(days=1), delete_later_pdf, str(rand_uuid))
#             # scheduler.enqueue_in(timedelta(minutes=1), delete_later_pdf, str(rand_uuid))
#
#             data = json.dumps({'success': str(rand_uuid), 'error': None, 'description': None})
#
#             return HttpResponse(data, content_type='application/json')
#
#         except Exception as e:
#             data = json.dumps({'success': None, 'error': True, 'description': "Произошла ошибка \n" + str(e)})
#             return HttpResponse(data, content_type='application/json')
