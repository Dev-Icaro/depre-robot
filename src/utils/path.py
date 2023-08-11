import os, sys

def get_current_path():
   if getattr(sys, 'frozen', False):
      return os.path.abspath(sys.executable)
   else:
      return os.path.abspath(os.path.dirname(__file__))
   

def get_pdfs_folder_path():
   working_path = os.path.abspath(os.getcwd())
   pdf_folder = os.path.join(working_path, 'pdfs')

   return pdf_folder