import os
import io

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from PIL import Image

def watermarkToApply(origin_pdf, watermark, imageBinary, output_file_path):
    # Inicializa o escritor do novo arquivo PDF
    pdf_writer = PdfFileWriter()
    # Itera sobre cada página do PDF original
    for page_num in range(origin_pdf.getNumPages()):
        # Obtém a página original do arquivo PDF na posição page_num
        page = origin_pdf.getPage(page_num)
        # Cria um objeto de buffer de bytes na memória 
        packet = io.BytesIO()
        # Obtém as dimensões da página
        page_width, page_height = page.mediaBox.getWidth(), page.mediaBox.getHeight()
        # Calcula as coordenadas para centralizar a imagem na horizontal e vertical
        x_offset = (page_width - imageBinary.width) / 2 
        y_offset = (page_height - imageBinary.height) / 2 
        x = float(x_offset)
        y = float(y_offset)
        # Esse objeto será usado para desenhar a imagem da marca d'água na nova página associado ao buffer de bytes
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        # Desenha a imagem da marca d'água no centro da página
        can.drawImage(watermark, x, y, width=imageBinary.width, height=imageBinary.height)
        # Salva as alterações feitas no objeto de desenho
        can.save()
        # Move o cursor para o início do buffer de bytes, preparando-o para ser lido
        packet.seek(0)
        # Cria um novo objeto PdfFileReader usando o buffer de bytes contendo a nova página com a marca d'água.
        new_pdf = PdfFileReader(packet)
         # Mescla a página original do PDF com a nova página que contém a marca d'água. A função merge_page combina os conteúdos das duas páginas.
        page.merge_page(new_pdf.getPage(0))
        # Adiciona a página mesclada ao objeto pdf_writer, que será usado para criar o novo arquivo PDF final.
        pdf_writer.addPage(page)
    # Abre e fecha o bloco
    with open(output_file_path, "wb") as output_pdf:
        # Salva o novo arquivo PDF
        pdf_writer.write(output_pdf)


def watermarkAuto():
    # Diretórios
    pdf_folder = 'pdf'
    assets_folder = 'imgs'
    output_folder = 'novo-pdf'
    # Lista de arquivos PDFs e Imagens
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    watermark_files = [f for f in os.listdir(assets_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    # Loop através de cada arquivo PDFs e Imagens
    for pdf_file in pdf_files: 
        # Pega o caminho do PDF que recebe a marca d'água
        pdf_path = os.path.join(pdf_folder, pdf_file)
        # Pega o nome do PDF
        pdf_name = os.path.basename(pdf_path).split('.')[0]
        # Itera imagem sobre cada página do PDF original
        for watermark_file in watermark_files:
            # Pega o caminho da imagem que será a marca d'água
            watermark_path = os.path.join(assets_folder, watermark_file)
            # Pega o nome da imagem
            watermark_name = os.path.basename(watermark_path).split('.')[0]
            # Abre o arquivo da imagem e o PDF em modo de ler binário
            watermark_image = Image.open(watermark_path)
            origin_pdf = PdfFileReader(open(pdf_path, "rb"))
            # Gera o nome do novo arquivo PDF com base no nome do PDF original e da imagem da marca d'água
            output_file_path = os.path.join(output_folder, f"{pdf_name}_{watermark_name}.pdf")
            # Função que aplica a marca d'água e gera o novo arquivo PDF
            watermarkToApply(origin_pdf, watermark_path, watermark_image, output_file_path)

if __name__ == "__main__":
    watermarkAuto()
   