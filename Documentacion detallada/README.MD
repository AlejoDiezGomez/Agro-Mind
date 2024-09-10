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

## Base de Datos (desarrollo actual):
En esta parte, se está desarrollando una base de datos en SQL para almacenar los datos provenientes de los archivos CSV. También se definirá el ciclo de vida de los datos y su tratamiento.

### Ciclo Tentativo:
1. **Creación de los CSV** por la parte contable.
2. **Verificación de los datos**: Ordenamiento, manejo de errores y modificaciones en Python.
3. **Carga de los datos** en la base de datos SQL.