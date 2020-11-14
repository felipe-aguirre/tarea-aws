import boto3
from menu import *
import re
AUTH_PATTERN = re.compile("(.+?)=(.*)")
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
def checker(textDetections, base):
    palabras = base.lower().strip().split()
    if len(palabras) == 0:
        return False
    for word in textDetections:
        if word['DetectedText'].lower() in palabras and word['Confidence']>97:
            palabras.remove(word['DetectedText'].lower())
    if len(palabras) == 0:
        return True
    return False

def detect_text(selection, credenciales):
    if len(credenciales) == 3:
        client = boto3.client(
            'rekognition',
            aws_access_key_id=credenciales['aws_access_key_id'],
            aws_secret_access_key=credenciales['aws_secret_access_key'],
            aws_session_token=credenciales['aws_session_token']
        )
    else:
        client = boto3.client(
            'rekognition',
            aws_access_key_id=credenciales['aws_access_key_id'],
            aws_secret_access_key=credenciales['aws_secret_access_key'],
        )
    try:
        response=client.detect_text(Image={'S3Object':{'Bucket':selection['bucket'],'Name':selection['photo']}})
    except Exception as error:
        # InvalidS3ObjectException: nombre del objeto png
        print("ERROR - No se pudo acceder al objeto en S3, posibles causas:")
        print("\t - Nombre de bucket y/o imagen incorrecto.")
        print("\t - Datos de autenticación en el archivo credentials incorrectos o expirados.")
        print("\t - Error en permisos de acceso.")
        print("\t - Error en la conexión.")
        print("Revise el archivo debug.log para más detalles.")
        logger.debug(error)
        return "" 
    logger.debug("Conexión a S3 válida")    
    textDetections = response['TextDetections']
    logger.debug("Respuesta obtenida de AWS rekognition:")
    for linea in textDetections:
        logger.debug(linea)
    logger.debug("Ejecución Checker texto base en imagen")
    revisor = checker(textDetections,selection['base'])
    return revisor

# UI
def main():
    logger.debug("START apertura archivo credenciales.")
    try:
        ARCHIVO = open('credentials', encoding="utf-8")
    except FileNotFoundError as fnfError:
        logger.debug("Error fatal - Archivo credentials no existe, revise README")
        print("Error fatal - Archivo credentials no existe, revise README")
        print("Deteniendo script.")
        return 
    except Exception as error:
        logger.debug(error)
        print("Error fatal al abrir archivo credentials, revisar debug.log")
        print("Deteniendo script")
        return 
    logger.debug("Archivo credentials encontrado.")
    logger.debug("END apertura archivo credenciales.")
    
    logger.debug("START revisión validez formato credenciales")
    credenciales = dict()
    for linea in ARCHIVO:
        matcher = re.search(AUTH_PATTERN, linea)
        if matcher:
            logger.debug("Se encontró valor para parámetro {}".format(matcher.group(1)))
            credenciales[matcher.group(1)] = matcher.group(2)
    if ['aws_access_key_id','aws_secret_access_key'] == sorted(credenciales.keys()):
        logger.debug("WARNING - credentials sin session_token")
        print("Advertencia - Su archivo credentials no contiene el session_token\nLa sesión no funcionará si está intentando usar credenciales temporales.")
    elif ['aws_access_key_id','aws_secret_access_key', 'aws_session_token'] == sorted(credenciales.keys()):
        logger.debug('Formato válido de aws_access_key_id, aws_secret_access_key y aws_session_token')
    else:
        logger.debug("ERROR - Datos de sesión AWS con formato inválido, revise el archivo credentials")
        print("Error en la autenticación en AWS, revise debug.log")
        return
    
    logger.debug("END revisión validez credenciales")
    logger.debug("START ejecución Interfaz")


    # OK Verificar que no está vacio
    # OK Verificar que existe el bucket y la foto
    # Habilitar loop por si hay mas de una foto
    # Datos de prueba actuales
    defaultData = {
        'bucket': 'testsoftware1',
        'photo': 'text.png',
        'base': "It's monday but keep smiling"
    }
    # verificar que default data sean string y que tenga las llaves correspondientes
    
    logger.debug("Default bucket: "+defaultData['bucket'])
    logger.debug("Default photo: "+defaultData['photo'])
    logger.debug("Default base: "+defaultData['base'])
    selection = menu(defaultData)
    logger.debug("Usuario eligió analizar:")
    while selection != 'EXIT':
        if len(selection['base'] != 0):
            print(detect_text(selection,credenciales))
        else:
            print("La palabra base no puede estar vacía - revise los valores preestablecidos en el código")
            logger.debug("ERROR - valor actual de defaultData['base'] no puede ser un string vacío")
        selection = review(defaultData)
        logger.debug("Usuario eligió analizar"+selection)
    logger.debug("Usuario decidió salir mediante el comando EXIT.")
    logger.debug("FIN DEL PROGRAMA")

main()
