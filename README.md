# Sistema de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto de la Fase 4 - Componente práctico del curso de Programación (213023_141) de la UNAD.

El sistema gestiona los clientes, servicios y reservas de la empresa Software FJ, que ofrece reserva de salas, alquiler de equipos y asesorías especializadas. Está hecho en Python con programación orientada a objetos, sin bases de datos: la información se maneja con objetos y listas, y los errores y eventos se guardan en un archivo de logs.

## Archivos del proyecto

| Archivo | Qué contiene |
|---|---|
| `excepciones.py` | Excepciones personalizadas del sistema |
| `logger.py` | Registro de eventos y errores en el archivo `registro_eventos.log` |
| `entidad.py` | Clase abstracta `EntidadSistema`, base de las demás clases |
| `cliente.py` | Clase `Cliente` con validaciones de sus datos |
| `servicios.py` | Clase abstracta `Servicio` y los servicios especializados |
| `reserva.py` | Clase `Reserva`: confirmación, cancelación y procesamiento |
| `main.py` | Programa principal con las operaciones simuladas |

## Cómo ejecutarlo

1. Tener instalado Python 3.10 o superior.
2. Descargar o clonar este repositorio.
3. Abrir una terminal en la carpeta del proyecto y ejecutar:

    python main.py

No necesita instalar librerías adicionales.

## Integrantes

- Carollayn Herrera Ramirez: excepciones, registro de logs, clase abstracta general y README
- (Compañero 2): cliente y servicios
- (Compañero 3): reserva y programa principal