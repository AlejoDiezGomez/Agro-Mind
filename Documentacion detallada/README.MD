# Estado Actual del Proyecto

## Parte Contable (versión 9.1):
A través de un menú creado con Kivy, podemos acceder a dos funcionalidades principales: un libro de cuentas y un libro diario.

### Libro de Cuentas:
En este libro, el usuario puede crear cuentas que serán usadas posteriormente para la registración en el libro diario.

### Libro Diario:
En este apartado, el usuario puede elegir en un menú desplegable las cuentas creadas previamente en el libro de cuentas. Además, se puede registrar si es parte de un débito o un haber, junto con una descripción. También se pueden eliminar registros utilizando el ID correspondiente.

### Salida de Archivos:
El sistema genera dos archivos CSV:
1. Uno con la información de las cuentas registradas en el libro de cuentas (columnas: `Cuenta`, `Detalle`).
2. Otro archivo CSV generado diariamente, que registra la información del libro diario (columnas: `ID`, `Fecha`, `Cuenta`, `Débito`, `Crédito`, `Descripción`). Se genera un archivo nuevo por cada día en que se ejecute el programa.

## Tecnologías Utilizadas

A continuación se presenta una lista de las tecnologías y bibliotecas utilizadas en este proyecto:

### 1. **Kivy**
   - **`kivy.app.App`**: Para crear aplicaciones móviles o de escritorio con interfaces gráficas.
   - **`kivy.uix.screenmanager.ScreenManager`**: Para gestionar múltiples pantallas dentro de la aplicación.
   - **`kivy.uix.screenmanager.Screen`**: Para definir las diferentes pantallas de la aplicación.
   - **`kivy.uix.boxlayout.BoxLayout`**: Para organizar widgets en un diseño de caja, apilando elementos verticalmente u horizontalmente.
   - **`kivy.uix.button.Button`**: Para crear botones interactivos.
   - **`kivy.uix.textinput.TextInput`**: Para crear campos de entrada de texto.
   - **`kivy.uix.label.Label`**: Para mostrar etiquetas de texto.
   - **`kivy.uix.spinner.Spinner`**: Para crear menús desplegables.
   - **`kivy.uix.gridlayout.GridLayout`**: Para organizar widgets en una cuadrícula.
   - **`kivy.uix.anchorlayout.AnchorLayout`**: Para anclar widgets a un lugar específico en la interfaz.
   - **`kivy.uix.scrollview.ScrollView`**: Para agregar funcionalidad de desplazamiento a los widgets que contienen más contenido del que cabe en la pantalla.
   - **`kivy.core.window.Window`**: Para controlar aspectos de la ventana de la aplicación, como el color de fondo.

### 2. **Pandas**
   - **`pandas as pd`**: Para manipular y gestionar datos tabulares (DataFrames), como leer y escribir archivos CSV y realizar agregaciones de datos.

### 3. **OS (Módulo estándar de Python)**
   - **`os.path.exists`**: Para verificar la existencia de archivos en el sistema de archivos.
   - **`os.path`**: Para manipular rutas de archivos.

### 4. **Datetime (Módulo estándar de Python)**
   - **`datetime.now()`**: Para obtener la fecha y hora actual y formatearla según sea necesario.

## Base de Datos (desarrollo actual):
En esta parte, se está desarrollando una base de datos en SQL para almacenar los datos provenientes de los archivos CSV. También se definirá el ciclo de vida de los datos y su tratamiento.
## Proceso de ETL para uno de los dataframe 
### Ciclo Tentativo:
1. **Creación de los CSV** por la parte contable.
2. **Verificación de los datos**: Ordenamiento, manejo de errores y modificaciones en Python.
3. **Carga de los datos** en la base de datos SQL.
