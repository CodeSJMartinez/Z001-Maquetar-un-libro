import markdown2
import pdfkit
import json
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

# Ruta del ejecutable wkhtmltopdf
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Verificar si la ruta es válida
try:
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
except OSError as e:
    print(f"Error: wkhtmltopdf no encontrado en la ruta especificada: {path_to_wkhtmltopdf}")
    raise e

# Función para convertir Markdown a HTML
def convert_md_to_html(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            md_content = file.read()
        html_content = markdown2.markdown(md_content)
        return html_content
    except FileNotFoundError as e:
        print(f"Error: El archivo {input_file} no fue encontrado.")
        raise e

# Función para crear el documento HTML completo usando una plantilla
def create_html_document(content, template_file='templates/base.html'):
    try:
        with open(template_file, 'r', encoding='utf-8') as file:
            template = file.read()
        document = template.replace("{{ content }}", content)
        return document
    except FileNotFoundError as e:
        print(f"Error: La plantilla {template_file} no fue encontrada.")
        raise e

# Función para generar un PDF a partir del contenido HTML
def generate_pdf(html_content, output_file='output.pdf', options=None):
    if options is None:
        options = {
            'page-size': 'Letter',  # Se puede ajustar según las necesidades
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
    try:
        pdfkit.from_string(html_content, output_file, options=options, configuration=config)
    except OSError as e:
        print(f"Error al generar el PDF: {e}")
        raise e

# Función para crear una cubierta simple usando PIL
def create_cover(cover_file='assets/cover.png', size=(1650, 2550), finish='matte'):
    try:
        cover = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(cover)
        
        # Cargar la fuente
        try:
            title_font = ImageFont.truetype("arial.ttf", 80)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            print("Error: La fuente 'arial.ttf' no fue encontrada. Usando fuente predeterminada.")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Agregar texto a la cubierta
        draw.text((100, 100), "El Viaje del Héroe", font=title_font, fill="black")
        draw.text((100, 250), "Por Juan Pérez", font=subtitle_font, fill="black")
        
        # Aplicar efectos según el acabado
        if finish == 'matte':
            # Aplicar algún efecto adicional si es necesario
            pass

        cover.save(cover_file)
    except UnidentifiedImageError as e:
        print(f"Error al crear la cubierta: {e}")
        raise e

def main():
    try:
        # Leer configuraciones
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config_data = json.load(config_file)

        # Convertir Markdown a HTML
        html_content = convert_md_to_html('input.md')
        
        # Crear el documento HTML completo con la plantilla
        html_document = create_html_document(html_content)
        
        # Generar el PDF
        generate_pdf(html_document, output_file='output.pdf', options={
            'page-size': config_data.get('size', 'A4'),  # Tamaño de la página
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        })
        
        # Crear la cubierta (opcional)
        create_cover(finish=config_data.get('cover_finish', 'matte'))
    
    except json.JSONDecodeError as e:
        print(f"Error: El archivo config.json no es válido. {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()

