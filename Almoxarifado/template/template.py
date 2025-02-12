import subprocess
from Site_django import settings
import pathlib 
caminho = str(pathlib.Path(__file__).parents[0])
from decouple import config
def excel_to_pdf_libreoffice(input_excel, output_pdf):
  """
  Converte um arquivo Excel para PDF usando LibreOffice.
  :param input_excel: Caminho do arquivo Excel de entrada.
  :param output_pdf: Caminho do arquivo PDF de saída.
  """
  
  command = [
      config('LIBRE_ROOT'), "--headless", "--convert-to", "pdf", "--outdir",
      output_pdf, f'{settings.BASE_DIR}/{input_excel}'
  ]
  subprocess.run(command)
  