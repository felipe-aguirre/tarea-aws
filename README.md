# Tarea AWS

- Autor: Felipe Aguirre
- 13 de Noviembre 2020
---

## Requisitos

- Tener instalado [python 3.x](https://www.python.org/download/releases/3.0/) en su sistema operativo
- Instalar la dependencia [boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) mediante el comando
`pip install boto3`

---

## Contenido

- Archivo `main.py`que contiene las funciones
  - **main():** Ejecución de la estructura principal del programa, incluyendo la interacción con la consola
  - **detect_text(photo, bucket, base):** Consulta a AWS rekognition por el texto que se encuentre en una imagen, subida previamente a un bucket de S3, tal como se detalla en las instrucciones.
  - **checker(text, base): ** Revisa si

---

## Supuestos

Dado a que el requerimiento exacto es `Verificar si en el texto de imagen de prueba está presente el texto de imagen de control.` se hacen los siguientes supuestos:

- Para efectos del programa y la incertidumbre que existe en el orden en que AWS rekognition lee la imagen, dependiendo de la orientación, se asume que no es requisito que la palabra *base* se encuentre en el mismo orden que en la imagen. 
- Del mismo modo, se asume que cada palabra del texto base puede aparecer más de una vez en la imagen.



---



## Instrucciones

- Editar el archivo `test_cases.py`: Modificar la lista `cases`de la linea `15` por una lista de tuplas con los pares de parámetros de prueba

  ```python
  cases = [("Sol", "Luna"), ("Dia", "NOCHE"), (3,"test"), ("Buenas", 5), (6,8)]
  # Reemplazar por la lista de tuplas que se deseen probar
  ```

- Ubicar los archivios `function,py`y `test_cases.py`en el mismo directorio

- Ejecutar `test_cases.py`con el intérprete Python

- Se generará un LOG en el mismo directorio base, llamado `debug.log`que contiene el detalle de las pruebas realizadas

---

## Supuestos

- El programa está diseñado para recibir solo 2 argumentos, es decir, la tupla de cada prueba solo puede contener 2 elementos.

