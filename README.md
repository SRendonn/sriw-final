## Configuración rápida

1. Crear entorno virtual

```
py -3 -m venv venv

# Linux/macOS
venv/bin/activate

# Windows
venv\Scripts\activate
```

2. Instalar dependencias desde **requirements.txt**

```
pip install -r requirements.txt
```

3. Correr aplicación de flask

```
# Linux/macOS
export FLASK_APP=app.py
export FLASK_ENV=development

# Windows Powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

flask run
```

## Documentación

### Introducción

Si queremos crear nuestro propio equipo de FIFA, ¿Cómo podríamos obtener los mejores jugadores en sus respectivas posiciones?

Planteamos una aplicación para poder resolver esta necesidad ya que muchas veces queremos mejorar nuestro equipo pero para saber que jugador es ótpimo para nuestra plantilla necesitamos hacer una búsqueda exahustiva, con nuestra aplicaión esta búsqueda se minimizará para obtener el mejor jugador y de forma mucho más rápida. Esta aplicación ofrece un sistema de recomendación que ayuda a decidir que jugadores son más óptimos para una plantilla de jugadores. El sistema de recomendación usa predicción individual y predicción por colaboración para recomendar hasta 3 jugadores que sean solicitados en cierta posición de juego (Delantero, Mediocampista, Defensa y Portero). Para ello se deben ingresar 5 jugadores pre seleccionados con su respectivo puntaje para poder tener una predicción más sólida y más efectiva. El puntaje es la valoración cualitativa que el usuario le da al jugador. Luego de enviar el formulario, usando el sistema de recomendación se obtendrá el mejor jugador que encaje con los mencionados puntajes. 

### Ontología

La lista de jugadores se obtuvo de nuestra propia ontología [FCF](https://github.com/SRendonn/sriw-final/blob/main/FCF.owl)

### Manual de uso de la aplicación

Como se menciona al principio la aplicación inicia cuando se ingresa a la ruta ```/``` Allí aparecerá un panel con un formulario en donde se podrán seleccionar 5 jugadores.

  <img src="https://user-images.githubusercontent.com/80493825/152716733-3f00ab47-57ec-4e11-abfd-ced04ea805d5.png" width="75%" alt="_"/>

Cada jugador tiene un puntaje asocado el cual será asignado por el usuario dependiendo de su noción sobre el juego y la calificación que éste le puede dar a su plantilla. Luego debajo de los 5 jugdores seleccionados se muestra un campo para poder seleccionar la posición del jugador que queramos recomendar


  <img src="https://user-images.githubusercontent.com/80493825/152716822-f34647ef-31a1-4dad-894a-4e010f61fe8d.png" width="75%" alt="_"/>

Una vez completado el formulario y al darle clic al el botón "Recomendar" se redirigirá al usuario a la ruta ```/recommend-player``` en dónde aparecerá el jugador más óptimo como recomendación y una detallada descripción en la cual se muestra la posición en la que juega, el equipo en el que juega, la liga en la que juega, los jugadores que también juegan en su mismo equipo, en su misma liga y de su misma nacionalidad, el lugar de nacimiento y su pie dominante.

  <img src="https://user-images.githubusercontent.com/80493825/152721484-0e9736a4-61e9-4608-9200-5aebf3607f7e.png" width="75%" alt="_"/>

### Desarrollo de la aplicación

Para el desarrollo e implementación de la aplicación se usó Flask, un framework para crear aplicacones web usando Python. El diseño se hizo con Bulma, un framework de componentes visual para frontend. En el backend se implementó el módulo rdflib para realizar las consultas a la ontología y los módulos numpy y pandas para optimizar las operaciones matriciales del recomendador. 

Al momento de hacer la petición ```GET /``` la aplicación obtiene todos los jugadores y todas las posiciones de la ontología para luego mostrarlos en la vista.

  <img src="https://user-images.githubusercontent.com/80493825/152718920-0267fca6-a79b-49be-8258-b6923119d9d7.png" alt="_"/>

Una vez se rellena el formulario y se envía, la aplicación redirige a la ruta ```POST /recommend-player``` donde obtenemos la mejor recomendación en base a la función:

  <img src="https://user-images.githubusercontent.com/80493825/152719801-48253279-113c-4718-8246-47044e6a9734.png" alt="_"/>

Primero se obtiene el perfil normalizado del usuario, después se obtienen los perfiles normalizados de los otros usuarios (dummies) y se hace la recomendación individual para cada dummy. Despues se hace una suma ponderada de las recomendaciones individuales por las distancias de cada dummy al usuario, obtieniendo así una recomendación total ponderada califcando a cada jugador para finalmente extraer el jugador con mejor puntaje.
