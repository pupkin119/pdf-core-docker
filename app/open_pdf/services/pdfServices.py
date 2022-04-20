from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image
from django.conf import settings
from fpdf import FPDF

from ..api_models.pdfRequestModels import ManualPdfModel
from ..constants.img_constants import sertTeamplateName
from ..utils.transformers import transform_name

montserratBoldFont = str(settings.MEDIA_ROOT) + "open-sans/Montserrat-Bold.ttf"
montserratRegularFont = str(settings.MEDIA_ROOT) + "open-sans/Montserrat-Regular.ttf"


def generate_pdfs_imgs(image_dir: str, manual_pdfs_list: list[ManualPdfModel]) -> None:
    for i, manualParams in enumerate(manual_pdfs_list):
        draw = Drawing()
        with Image(filename=str(settings.MEDIA_ROOT) + '/imgs/' + sertTeamplateName) as image:
            draw.font = montserratBoldFont

            draw.font_size = 25 * 4
            draw.fill_color = Color('#333333')

            name = transform_name(manualParams.name, 21)
            course = transform_name(manualParams.course, 21)

            draw.text(205, 1418 + 30, name)
            draw.text(205, 1888 + 30, course)
            draw.font = montserratRegularFont
            draw.font_size = 8 * 5
            draw.text(339 + 30, 3040, manualParams.town)

            draw(image)
            print(image_dir)
            image.save(filename=image_dir + "/img_" + str(i) + '.jpg')


def generate_pdfs(pdfs_dir: str, image_dir: str, manual_pdfs_list: list[ManualPdfModel]) -> None:
    pdf_filename = pdfs_dir + "/certificates.pdf"

    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(0)

    for i, manualParams in enumerate(manual_pdfs_list):
        #     im2 = PILImage.open("imgs/" + str(rand_uuid) + "/img_" + str(i) + ".jpg")
        # for image in imagelist:
        pdf.add_page()
        pdf.image(image_dir + "/img_" + str(i) + ".jpg", w=200)
    pdf.output(pdf_filename, "F")
