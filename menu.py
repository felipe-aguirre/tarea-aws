def review(defaultData):
    while True:
        print("Escriba un número que indique su opción, para salir escriba EXIT:")
        print('\t1 - Datos preestablecidos')
        print('\t2 - Datos nuevos')
        print('\tEXIT')
        eleccion = input("> ")
        if eleccion == '1':
            return defaultData
        elif eleccion == '2':

            newBucket = input("Ingrese nombre de bucket, o presione enter para usar preestablecido: ")
            if len(newBucket)==0:
                newBucket = defaultData['bucket']
            newPhoto = input("Ingrese nombre de Imagen con extensión, o presione enter para usar preestablecido: ")
            if len(newPhoto) == 0:
                newPhoto = defaultData['photo']
            newBase = input("Ingrese texto base, o presione enter para usar preestablecido: ")
            if len(newBase) == 0:
                newBase = defaultData['base']
            return {'bucket': newBucket, 'photo' : newPhoto, 'base':newBase}
        elif eleccion == "EXIT":
            print("Finalizó programa")
            return eleccion
        else:
            print("Error - Eliga una opción correcta")

    
def menu(defaultData):
    print("")
    print("Bienvenido al script de AWS rekognition\n¿Desea usar los datos preestablecidos? \n\nDatos preestablecidos:")
    print("\t- Bucket: "+str(defaultData['bucket']))
    print("\t- Imágen: "+str(defaultData['photo']))
    print("\t- Texto base: "+str(defaultData['base']+"\n"))
    return review(defaultData)
