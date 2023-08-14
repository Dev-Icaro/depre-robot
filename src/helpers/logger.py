from utils.path import get_current_path
from datetime import datetime
import os

def log(message):
  log_file_path = os.path.join(get_current_path(), 'log.txt')

  with open(log_file_path, 'w') as log_file:
    current_hour = datetime.now().time()
    log_message = f"{current_hour.strftime('%H:%M:%S')}: {message}"

    log_file.write(log_message)