import os
import io

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from PIL import Image

def get_file_name_without_extension(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def watermarkToApply(origin_pdf, watermark, image_binary, output_file_path):
    pdf_writer = PdfFileWriter()
    
    for page_num in range(origin_pdf.getNumPages()):
        page = origin_pdf.getPage(page_num)
        packet = io.BytesIO()
        
        page_width, page_height = page.mediaBox.getWidth(), page.mediaBox.getHeight()
        x_offset = (page_width - image_binary.width) / 2 
        y_offset = (page_height - image_binary.height) / 2 
        x, y = float(x_offset), float(y_offset)
        
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        rgba_image = Image.new("RGBA", image_binary.size, (255, 255, 255, 0))
        rgba_image.paste(image_binary, (0, 0), image_binary)
        can.drawInlineImage(rgba_image, x, y, width=image_binary.width, height=image_binary.height)
        can.save()
        
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        page.merge_page(new_pdf.getPage(0))
        pdf_writer.addPage(page)
    
    with open(output_file_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

def watermarkAuto():
    pdf_folder = 'pdf'
    assets_folder = 'imgs'
    output_folder = 'novo-pdf'

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    watermark_files = [f for f in os.listdir(assets_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for pdf_file in pdf_files: 
        pdf_path = os.path.join(pdf_folder, pdf_file)
        pdf_name = get_file_name_without_extension(pdf_path)

        for watermark_file in watermark_files:
            watermark_path = os.path.join(assets_folder, watermark_file)
            watermark_name = get_file_name_without_extension(watermark_path)

            with Image.open(watermark_path) as watermark_image, open(pdf_path, "rb") as pdf_file:
                origin_pdf = PdfFileReader(pdf_file)
                output_file_path = os.path.join(output_folder, f"{pdf_name}_{watermark_name}.pdf")
                watermarkToApply(origin_pdf, watermark_path, watermark_image, output_file_path)

if __name__ == "__main__":
    watermarkAuto()
