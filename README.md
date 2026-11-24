# Mesa de Partes Digital

Aplicación de escritorio en Python basada en el prototipo de la Municipalidad de Los Olivos. Permite registrar expedientes, consultarlos y obtener su cargo de recepción.

## Inicio rápido

1. Extrae el ZIP completo en una carpeta.
2. Abre PowerShell en la carpeta que contiene main.py.
3. Ejecuta **py main.py**. Si tu instalación usa el comando python, ejecuta **python main.py**.

Necesitas Python 3.9 o posterior con Tkinter (incluido en la instalación estándar de Windows). La aplicación usa componentes de la biblioteca estándar y funciona localmente. Puedes comprobar Tkinter con **py -m tkinter**.

## Uso

- **Nuevo expediente** abre el formulario. Al guardar, el programa asigna el código, guarda el registro y muestra el cargo para copiarlo.
- **Expedientes** permite buscar por código, DNI, remitente o asunto, filtrar por área y cambiar el orden. Selecciona una fila y pulsa **Ver expediente** para consultar todos sus campos.
- **Importar TXT** permite seleccionar el archivo data/expedientes.txt del programa anterior. Importa los datos válidos y conserva el registro existente si el código coincide. El resumen indica cuántas filas fueron importadas, repetidas, conflictivas o inválidas.
- **Ctrl+N** abre un nuevo registro. **Ctrl+F** lleva el foco al buscador. **Esc** cierra un diálogo o limpia la búsqueda cuando el buscador tiene el foco.

El primer inicio crea data/mesa_partes.sqlite3 junto al programa. La base arranca vacía y las fechas de recepción usan la hora de Lima. Puedes usar una base de prueba aparte con **py main.py --base prueba.sqlite3**. Para respaldar los datos, cierra la aplicación y copia el archivo de la base.

## Código

| Archivo | Responsabilidad |
| --- | --- |
| main.py | Inicio de la aplicación y selección de la base |
| modelos.py | Expediente, validación y cargo de recepción |
| repositorio.py | Persistencia SQLite, correlativos e importación |
| interfaz.py | Pantallas y controles de escritorio |
| test_repositorio.py | Pruebas de validación, persistencia, importación y registros simultáneos |

Ejecuta las pruebas desde esta carpeta con **py -m unittest -v**.
