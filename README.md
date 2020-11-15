# Tarea AWS

Aplicación hecha en Python para detectar texto en fotografías usando los servicios de AWS Rekognition e imágenes almacenadas en un bucket en AWS S3.

La aplicación requiere poseer una cuenta en AWS y acceso a las credenciales de terminal, ya sea permanentes o temporales, que incluyen un token de sesión.

- Autor: Felipe Aguirre
- 13 de Noviembre 2020
---

## Requisitos

- Tener instalado [python 3.x](https://www.python.org/download/releases/3.0/) en su sistema operativo
- Instalar la dependencia [boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) mediante el comando
`pip install boto3`

---

## Contenido

- `main.py` Archivo ejecutable principal:
  - **main():** Ejecución de la estructura principal del programa, incluyendo la interacción con la consola
  - **detect_text(photo, bucket, base):** Consulta a AWS rekognition por el texto que se encuentre en una imagen, subida previamente a un bucket de S3, tal como se detalla en las instrucciones.
  - **checker(text, base): ** Revisa si
- `menu.py` - Archivo auxiliar para implementar el CLI en python.
- `./images` - Carpeta que contiene las imágenes usadas en el testing. Una copia de cada imagen se encuentra en un bucket de S3.
- `debug.log` - Ofrece un registro del funcionamiento del aplicativo.
- `credentials` - Archivo de credenciales (no incluido en el repositorio). Ver sección instrucciones

---

## Supuestos

Dado a que el requerimiento exacto es `Verificar si en el texto de imagen de prueba está presente el texto de imagen de control.` se hacen los siguientes supuestos:

- Para efectos del programa y la incertidumbre que existe en el orden en que AWS rekognition lee la imagen, dependiendo de la orientación, se asume que no es requisito que la palabra *base* se encuentre en el mismo orden en la imagen. 
  - Ejemplo: la Imagen de prueba [ok-extra-between.jpg](images/ok-extra-between.jpg) si se considera válida al detectar `It's monday but keep smiling`
- Del mismo modo, se asume que cada palabra del texto base puede aparecer más de una vez en la imagen.
  - Ejemplo: La imágen de prueba [ok-repeated.jpeg](images/ok-repeated.jpeg) si se considera válida al detectar `It's monday but keep smiling`
- No es necesario que exclusivamente el texto de prueba se encuentre en la imagen:
  - Ejemplo: La imágen de prueba [ok-extra.png](images/ok-extra.png) si se considera válida al detectar `It's monday but keep smiling`



---



## Instrucciones

- Crear un archivo en la carpeta raiz llamado `credentials`. Debe contener los datos de sesión de su cuenta AWS en el formato que utiliza [la documentación oficial de AWS](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

  Ejemplo:

  `credentials`

  ```bash
  [default]
  aws_access_key_id=ASIAQCLK7UK3FZAITIGD
  aws_secret_access_key=NnPowMZaLjkl7iLuFwlsd4OgWIbkILPTdLYOcHIJ
  aws_session_token=FwoGZXIvYXdzEJU5W0CLPAYhT9dVITaTSCQBvT0wVag4/9yztwAalrlyYAT/Mjce1BrZwJMu2yu+1JrdMTLwLauu4Coe+Jfqfz3oqvXQUOr6Nuz9n6wmV+YKfYLEkMQRoaq7VR1HdeLoVKUJKOVJT5oHFihpSg9UX364SfiODxUefXaDxP2AYJH82Km6i4Ayep5toyV9zgG94gjM0CPDZyns/oNj0kNr0vZ3OEUZeirYSg6lyDF9g9bCUzGo9MXwn9AIC6yeGJYzS7jRyRwjN0/oJPDF6Cx2j+o97oineCijCycb9BTItQ5e6ym6JdWBNmDc/EYwwB58QfQMGDHSmZZX7+xY2B8Q6ZTfGfmczkkyaJJUp
  ```

  ​	Nota: Los datos mostrados en el ejemplo no son válidos, debe usar los entregados en su cuenta AWS.

- Crear un bucket en S3 y subir en él las imágenes a probar

- Ejecutar el archivo `main.py`

  - Durante la ejecución se le pedirá si desea usar datos preestablecidos o datos nuevos para el nombre del bucket, la imágen y el texto respectivamente.
  - Si desea modificar los datos preestablecidos, cambie los valores de las variables `BUCKET`, `PHOTO` y `BASE` de las líneas 7, 9 y 11 del archivo `main.py`respectivamente.

```python
EXTRACTO DE main.py
...
# Datos Iniciales:
# Bucket: Nombre de Bucket en que se ubican las imágenes
BUCKET = 'testsoftware1'
# Photo: Nombre de la imagen incluida en el Bucket anterior, debe contener la extensión
PHOTO = 'base.png'
# Base: Texto que se desea encontrar en la imágen
BASE = "It's monday but keep smiling"
...
```

