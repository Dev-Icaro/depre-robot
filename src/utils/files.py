import os 

def change_file_extension(file_name, new_extension):
  base_name = os.path.splitext(file_name)[0]

  return f"{base_name}.{new_extension}"



