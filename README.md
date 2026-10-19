# Mesa de Partes Digital - Prototipo

**Curso:** Fundamentos de Programación (CIIN1205P)  
**Universidad Privada del Norte**  
**Desafío:** Del archivador al algoritmo, un prototipo para la mesa de partes digital

## Descripción

Prototipo funcional de mesa de partes digital desarrollado en Python 3. Permite:

- Registrar expedientes con validación de datos
- Buscar expedientes por código de identificación
- Ordenar expedientes por código (Bubble Sort)
- Listar todos los registros
- Persistir datos en archivo de texto

## Requisitos

- Python 3.8 o superior

## Cómo ejecutar

```bash
python mesa_partes.py
```

## Estructura del código

| Función | Descripción |
|---------|-------------|
| `validar_dni()` | Valida DNI de 8 dígitos |
| `validar_texto_no_vacio()` | Valida cadenas no vacías |
| `generar_codigo()` | Genera código EXP-AAAA-NNN |
| `registrar_expediente()` | Registro completo con validaciones |
| `buscar_por_codigo()` | Búsqueda lineal |
| `ordenar_por_codigo()` | Bubble Sort sobre arreglos paralelos |
| `listar_expedientes()` | Muestra todos los registros |
| `guardar_en_archivo()` | Persistencia en .txt |
| `cargar_desde_archivo()` | Recuperación de datos |
| `main()` | Menú principal |

## Conceptos aplicados

- Estructuras de control (if, while, for)
- Funciones
- Arreglos (listas paralelas)
- Cadenas de caracteres
- Persistencia con archivos
- Algoritmo de ordenamiento (Bubble Sort)
- Control de versiones con Git

## Cumplimiento normativo

Aporta al cumplimiento de la **Ley N.° 31170** (implementación de mesas de partes digitales y notificaciones electrónicas).

## Equipo

- Integrantes del curso CIIN1205P

## Enlace del repositorio

https://github.com/jefersoneliasgonzalesvargas-netizen/mesa-partes-digital
