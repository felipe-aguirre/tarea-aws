import boto3
from data import auth

def checker(text,base):
    palabras = base.lower().strip().split()
    promedio = list()
    for word in text:
        if word['DetectedText'].lower() in palabras and word['Confidence']>97:
            palabras.remove(word['DetectedText'].lower())
            promedio.append(word['Confidence'])
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

    bucket='testsoftware1'
    photo='text.png'
    base=""
    print(detect_text(photo,bucket,base))

main()
