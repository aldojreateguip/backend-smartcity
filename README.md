# SMART CITY PROJECT MPM - MAYNAS

Este proyecto consiste en un sistema de seguimiento de compactadoras en la ciudad de Iquitos. Su propósito principal es facilitar el monitoreo de las compactadoras encargadas de la recolección de basura, permitiendo visualizar su ubicación en tiempo real y asignar rutas de recojo de manera eficiente.

Principales características y funcionalidades:

- Visualización de la ubicación en tiempo real de las compactadoras en un mapa interactivo.
- Registro y gestión de compactadoras, incluyendo información relevante como número de identificación, modelo, estado, etc.
- Asignación automática de rutas de recojo de basura basadas en algoritmos de optimización.
- Generación de informes y estadísticas relacionadas con el seguimiento y desempeño de las compactadoras.

Este proyecto se desarrollará utilizando el framework Django de Python, aprovechando su potencial para la creación de aplicaciones web robustas y escalables.

## Tabla de contenidos

- [Instalación](#instalación)

## Instalación

Sigue estos pasos para instalar y configurar el entorno de desarrollo de tu proyecto:


1. Clona el repositorio de GitHub:
```bash

git clone https://github.com/juan-huamani/backend-smartcity.git

```
2. Crea y activa un entorno virtual (opcional, pero se recomienda)

- Instalar 

```bash

pip install virtualenv 

```
- Crear entorno virtual 

```bash 

virtualenv venv 

```
- Activar entorno virtual 

```bash 

source venv/Scripts/activate 

```

3. Instala las dependencias del proyecto (Asegurarse de que el entorno virtual este activado)
```bash

pip install -r requirements.txt

```
4. Realiza las migraciones de la base de datos
```bash

python manage.py migrate

```
5. Inicia el servidor de desarrollo de Django
```bash

python manage.py runserver

```
