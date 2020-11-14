import boto3
from data import auth

# Logger
import logging
logger = logging.getLogger('Tarea AWS')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Revisor: Check si la imagen tiene la frase base
def checker(text,base):
    palabras = base.lower().strip().split()
    if len(palabras == 0):
        return False
    for word in text:
        if word['DetectedText'].lower() in palabras and word['Confidence']>97:
            palabras.remove(word['DetectedText'].lower())
    if len(palabras) == 0:
        return True
    return False

def detect_text(photo, bucket,base):
    
    client = boto3.client(
        'rekognition',
        aws_access_key_id=auth[0],
        aws_secret_access_key=auth[1],
        aws_session_token=auth[2]
    )

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    revisor = checker(textDetections,base)
    return revisor

# UI
def main():
    logger.debug("Inicio ejecución")

    # Verificar que es string
    # Verificar que no está vacio
    # Verificar que existe el bucket y la foto
    # Habilitar loop por si hay mas de una foto
    
    # Datos de prueba actuales 
    bucket='testsoftware1'
    photo='text.png'
    base="It's monday but keep smiling"
    logger.debug("Default bucket: "+bucket)
    logger.debug("Default photo: "+photo)
    logger.debug("Default base: "+base)
    print("Bienvenido al script de AWS rekognition")
    print(detect_text(photo,bucket,base))

main()
