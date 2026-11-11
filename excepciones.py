# Excepciones personalizadas del sistema Software FJ


# Excepción base, de aquí heredan todas las demás
class ErrorSoftwareFJ(Exception):
    def __init__(self, mensaje="Ocurrió un error en el sistema", dato=None):
        self.mensaje = mensaje
        self.dato = dato  # Guardamos el valor que causó el error para mostrarlo después
        super().__init__(self.mensaje)  # Le pasamos el mensaje a la clase Exception de Python

    # Arma el texto que se ve cuando se imprime el error, agregando el dato si lo hay
    def __str__(self):
        if self.dato is not None:
            return f"{self.mensaje} (dato recibido: {self.dato})"
        return self.mensaje


# Se lanza cuando un cliente tiene datos incorrectos, como un correo mal escrito
class ClienteInvalidoError(ErrorSoftwareFJ):
    pass


# Se lanza cuando falta un dato obligatorio o viene con un valor que no sirve
class ParametroInvalidoError(ErrorSoftwareFJ):
    pass


# Se lanza cuando se intenta usar un servicio que no está disponible en ese momento
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    pass


# Se lanza cuando una reserva no se puede crear, confirmar o cancelar
class ReservaInvalidaError(ErrorSoftwareFJ):
    pass


# Se lanza cuando se intenta hacer algo que el sistema no permite, como cancelar dos veces
class OperacionNoPermitidaError(ErrorSoftwareFJ):
    pass


# Se lanza cuando un cálculo de costo da un resultado imposible, como un valor negativo
class CalculoInconsistenteError(ErrorSoftwareFJ):
    pass