from app import app
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['IMAGE_UPLOAD_PATH'] = "D:/projetos/cadastro de imagens/app/static/images/uploads"