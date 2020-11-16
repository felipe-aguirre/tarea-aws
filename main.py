import boto3
import re
AUTH_PATTERN = re.compile("(.+?)=(.*)")

# Datos Iniciales:
# Bucket: Nombre de Bucket en que se ubican las imágenes
BUCKET = 'testsoftware1'
# Photo: Nombre de la imagen incluida en el Bucket anterior, debe contener la extensión
PHOTO = 'base.png'
# Base: Texto que se desea encontrar en la imágen
BASE = "It's monday but keep smiling"



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

# Import funciones auxiliares de UI
from menu import *



# Funcion - Revisor: Check si la imagen tiene la frase base
def checker(textDetections, base):
    palabras = base.lower().strip().split()
    promedio = list()
    if len(palabras) == 0:
        return "Sin texto\nNo se detectó texto alguno en la imágen\n"
    for word in textDetections:
        if word['DetectedText'].lower() in palabras and word['Confidence']>97:
            palabras.remove(word['DetectedText'].lower())
            promedio.append(word['Confidence'])
    if len(palabras) == 0:
        promedio = round(sum(promedio)/len(promedio),2)
        return "Encontrado!\nLa palabra {} fue encontrada en la imágen con un {}% de acierto promedio por palabra.\n".format(base,promedio)
    return "No encontrado\n El texto detectado no corresponde al texto base {}.\n".format(base)

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

# Funcion - Validador: Verifica si el formato de la entrada es correcta
def validador(entrada):
    if type(entrada['bucket']) != str:
        print("Nombre de bucket debe ser un String, verificar script linea 7")
        logger.debug("FATAL ERROR - type of BUCKET not string")
        return False
    if type(entrada['photo']) != str:
        print("Nombre de imágen debe ser un String, verificar script linea 9")
        logger.debug("FATAL ERROR - type of PHOTO not string")
        return False
    if type(entrada['base']) != str:
        print("Texto base debe ser un String, verificar script linea 11")
        logger.debug("FATAL ERROR - type of BASE not string")
        return False
    if len(entrada['bucket']) == 0:
        print("Nombre de bucket no puede ser un texto vacío, verificar script linea 7")
        logger.debug("FATAL ERROR - length of BUCKET 0")
        return False
    if len(entrada['photo']) == 0:
        print("Nombre de imágen no puede ser un texto vacío, verificar script linea 9")
        logger.debug("FATAL ERROR - length of PHOTO 0")
        return False
    if len(entrada['base']) == 0:
        print("Texto base no puede ser un texto vacío, verificar script linea 9")
        logger.debug("FATAL ERROR - length of BUCKET 0")
        return False
    return True
def main():

    # REVISIÓN formato archivo credentials
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
        print("Advertencia - Su archivo credentials no contiene el session_token\nLa aplicación no funcionará si está intentando usar credenciales temporales.")
    elif ['aws_access_key_id','aws_secret_access_key', 'aws_session_token'] == sorted(credenciales.keys()):
        logger.debug('Formato válido de aws_access_key_id, aws_secret_access_key y aws_session_token')
    else:
        logger.debug("ERROR - Datos de sesión AWS con formato inválido, revise el archivo credentials")
        print("Error en la autenticación en AWS, revise debug.log")
        return
    
    logger.debug("END revisión validez credenciales")

    logger.debug("START ejecución Interfaz")
    try:
        defaultData = {
            'bucket': BUCKET,
            'photo': PHOTO,
            'base': BASE
        }
    except Exception as error:
        print("Hubo un error al definir variables preestablecidas, revisar debug.log")
        logger.debug("FATAL ERROR - "+error)

    logger.debug("Default bucket: "+str(defaultData['bucket']))
    logger.debug("Default photo: "+str(defaultData['photo']))
    logger.debug("Default base: "+str(defaultData['base']))
    selection = menu(defaultData)
    logger.debug("Usuario eligió analizar: "+str(selection))
    while selection != 'EXIT':
        if validador(selection):
            print(detect_text(selection,credenciales))
        selection = review(defaultData)
        logger.debug("Usuario eligió analizar: "+str(selection))
    logger.debug("Usuario decidió salir mediante el comando EXIT.")
    logger.debug("FIN DEL PROGRAMA")

main()
