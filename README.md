# Z001-Maquetar-un-libro

Este código es un pequeño programa que toma un archivo de texto en formato Markdown y lo convierte en un documento PDF, completo con una cubierta de libro opcional. Usa varias bibliotecas de Python para leer archivos, manipular texto e imágenes, y generar el PDF final. Cada función tiene un propósito específico en el proceso, y el flujo está controlado por la función principal main, que coordina todas las operaciones.

### 1. **Importaciones y Configuración Inicial**
   ```python
   import markdown2
   import pdfkit
   import json
   from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
   ```
   **Explicación:** Aquí, el código importa algunas bibliotecas:
   - `markdown2`: Convierte texto escrito en Markdown (un formato de texto simple) a HTML.
   - `pdfkit`: Convierte HTML a PDF.
   - `json`: Permite leer y manipular archivos JSON, que son archivos de texto que almacenan datos en forma de clave-valor.
   - `PIL (Python Imaging Library)`: Trabaja con imágenes. En particular, se usa para crear y modificar imágenes.

   ```python
   path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
   ```
   **Explicación:** Se define una variable `path_to_wkhtmltopdf` con la ruta donde está instalado `wkhtmltopdf`, un programa necesario para convertir HTML en PDF.

   ```python
   try:
       config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
   except OSError as e:
       print(f"Error: wkhtmltopdf no encontrado en la ruta especificada: {path_to_wkhtmltopdf}")
       raise e
   ```
   **Explicación:** Este bloque de código intenta configurar `pdfkit` usando la ruta especificada. Si la ruta es incorrecta o el programa no se encuentra, se muestra un mensaje de error y se detiene la ejecución.

### 2. **Funciones para Convertir Markdown y Crear Documentos HTML**
   ```python
   def convert_md_to_html(input_file):
       try:
           with open(input_file, 'r', encoding='utf-8') as file:
               md_content = file.read()
           html_content = markdown2.markdown(md_content)
           return html_content
       except FileNotFoundError as e:
           print(f"Error: El archivo {input_file} no fue encontrado.")
           raise e
   ```
   **Explicación:** Esta función toma un archivo de texto en formato Markdown y lo convierte a HTML.
   - Abre el archivo `input_file`.
   - Lee su contenido.
   - Usa `markdown2` para convertir el texto de Markdown a HTML.
   - Devuelve el HTML generado.

   ```python
   def create_html_document(content, template_file='templates/base.html'):
       try:
           with open(template_file, 'r', encoding='utf-8') as file:
               template = file.read()
           document = template.replace("{{ content }}", content)
           return document
       except FileNotFoundError as e:
           print(f"Error: La plantilla {template_file} no fue encontrada.")
           raise e
   ```
   **Explicación:** Esta función toma el contenido HTML generado y lo inserta en una plantilla HTML más grande.
   - Abre un archivo de plantilla (una base HTML que tiene un diseño predefinido).
   - Busca el lugar donde se espera el contenido (`{{ content }}`) y lo reemplaza con el HTML generado.
   - Devuelve el documento HTML completo.

### 3. **Generar un PDF**
   ```python
   def generate_pdf(html_content, output_file='output.pdf', options=None):
       if options is None:
           options = {
               'page-size': 'Letter',
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
   ```
   **Explicación:** Esta función convierte el contenido HTML en un archivo PDF.
   - Define opciones como el tamaño de la página y los márgenes.
   - Usa `pdfkit` para crear el PDF.
   - Si algo falla, muestra un mensaje de error.

### 4. **Crear una Cubierta de Libro**
   ```python
   def create_cover(cover_file='assets/cover.png', size=(1650, 2550), finish='matte'):
       try:
           cover = Image.new('RGB', size, color='white')
           draw = ImageDraw.Draw(cover)
           
           try:
               title_font = ImageFont.truetype("arial.ttf", 80)
               subtitle_font = ImageFont.truetype("arial.ttf", 40)
           except IOError:
               print("Error: La fuente 'arial.ttf' no fue encontrada. Usando fuente predeterminada.")
               title_font = ImageFont.load_default()
               subtitle_font = ImageFont.load_default()

           draw.text((100, 100), "El Viaje del Héroe", font=title_font, fill="black")
           draw.text((100, 250), "Por Juan Pérez", font=subtitle_font, fill="black")
           
           if finish == 'matte':
               pass

           cover.save(cover_file)
       except UnidentifiedImageError as e:
           print(f"Error al crear la cubierta: {e}")
           raise e
   ```
   **Explicación:** Esta función crea una imagen que sirve como la cubierta de un libro.
   - Define el tamaño y color de la imagen.
   - Intenta cargar las fuentes necesarias para el título y subtítulo. Si no las encuentra, usa fuentes predeterminadas.
   - Dibuja el texto en la imagen.
   - Guarda la imagen como un archivo `cover.png`.

### 5. **Función Principal**
   ```python
   def main():
       try:
           with open('config.json', 'r', encoding='utf-8') as config_file:
               config_data = json.load(config_file)

           html_content = convert_md_to_html('input.md')
           
           html_document = create_html_document(html_content)
           
           generate_pdf(html_document, output_file='output.pdf', options={
               'page-size': config_data.get('size', 'A4'),
               'margin-top': '0.75in',
               'margin-right': '0.75in',
               'margin-bottom': '0.75in',
               'margin-left': '0.75in',
               'encoding': "UTF-8"
           })
           
           create_cover(finish=config_data.get('cover_finish', 'matte'))
       
       except json.JSONDecodeError as e:
           print(f"Error: El archivo config.json no es válido. {e}")
       except Exception as e:
           print(f"Ocurrió un error: {e}")
   ```
   **Explicación:** Esta es la función principal que coordina todo.
   - Lee configuraciones de un archivo JSON.
   - Convierte un archivo Markdown a HTML.
   - Crea un documento HTML completo usando una plantilla.
   - Genera un PDF a partir del HTML.
   - Opcionalmente, crea una imagen para la cubierta del libro.

   ```python
   if __name__ == "__main__":
       main()
   ```
   **Explicación:** Esta línea se asegura de que la función `main` se ejecute cuando el archivo es ejecutado directamente.



