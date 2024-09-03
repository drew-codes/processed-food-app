import os
from dotenv import load_dotenv

load_dotenv() 

def get_grocer_base_url(): 
  return os.environ['GROCER_URL_BASE']