from datetime import datetime

# Nombre del archivo de texto donde se van guardando los eventos y errores
ARCHIVO_LOG = "registro_eventos.log"


# Agrega una línea al archivo con la fecha y hora, el tipo de registro y el mensaje
def _escribir_linea(tipo, mensaje):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual en formato legible
    try:
        # Se abre en modo "a" para agregar al final sin borrar lo que ya estaba escrito
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"{fecha} - {tipo} - {mensaje}\n")
    except OSError as e:
        # Si el archivo no se puede escribir, solo avisamos para que el programa no se detenga
        print(f"No se pudo escribir en el log: {e}")


# Registra algo que salió bien, por ejemplo cuando se crea un cliente o se confirma una reserva
def registrar_evento(mensaje):
    _escribir_linea("EVENTO", mensaje)


# Registra un error y, si recibimos la excepción, también guarda qué tipo de error fue
def registrar_error(mensaje, error=None):
    if error is not None:
        mensaje = f"{mensaje} | {type(error).__name__}: {error}"
    _escribir_linea("ERROR", mensaje)


# Esta parte solo se ejecuta al correr este archivo directamente, sirve para probarlo
if __name__ == "__main__":
    registrar_evento("Prueba de evento")
    registrar_error("Prueba de error", ValueError("valor incorrecto"))
    print("Revisa el archivo registro_eventos.log")