from abc import ABC, abstractmethod
from excepciones import ParametroInvalidoError


# Clase abstracta que sirve de molde para Cliente, Servicio y Reserva, no se usa sola
class EntidadSistema(ABC):

    def __init__(self, identificador):
        # Toda entidad necesita un identificador, así que lo validamos antes de guardarlo
        self._identificador = self.validar_texto(identificador, "identificador")

    # Deja consultar el identificador desde afuera, pero no cambiarlo (encapsulación)
    @property
    def identificador(self):
        return self._identificador

    # Revisa que un texto no esté vacío y le quita los espacios de más; las clases hijas la pueden reutilizar
    @staticmethod
    def validar_texto(valor, nombre_campo):
        if valor is None or str(valor).strip() == "":
            raise ParametroInvalidoError(f"El campo {nombre_campo} no puede estar vacío", valor)
        return str(valor).strip()

    # Método obligatorio: cada clase hija debe revisar que sus propios datos sean correctos
    @abstractmethod
    def validar(self):
        pass

    # Método obligatorio: cada clase hija decide cómo mostrar su información
    @abstractmethod
    def mostrar_informacion(self):
        pass

    # Hace que al imprimir un objeto se muestre su información en vez de un código raro
    def __str__(self):
        return self.mostrar_informacion()


# Esta parte solo se ejecuta al correr este archivo directamente, sirve para probarlo
if __name__ == "__main__":
    # Comprobamos que no se pueda crear un objeto de una clase abstracta
    try:
        entidad = EntidadSistema("001")
    except TypeError as e:
        print("Correcto, no se puede crear una entidad abstracta:", e)

    # Comprobamos que la validación detecte un texto que solo tiene espacios
    try:
        EntidadSistema.validar_texto("   ", "nombre")
    except ParametroInvalidoError as e:
        print("Correcto, se detectó el error:", e)