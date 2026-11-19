import re ## permite usar expresiones regulares para validar información 
import logging ## registra eventos y errores en archivos de registro 
from abc  import ABC, abstractmethod 
# Creación de las clases abstractas ABC 
# y abstractmethod permite definir métodos que obligatoriamente deben implementar las clases hijas.

logger = logging.getLogger("SoftwareFJ")

class Entidad(ABC):
    """Clase abstracta para las entidades del sistema."""
    def __init__(self, identificador):
        if not identificador:
            raise ValueError("El identificador es obligatorio.")
        self._identificador = identificador
    @property
    def identificador(self):
        return self._identificador
    @abstractmethod
    def obtener_informacion(self):
        """Método que deben implementar las clases derivadas."""
        pass
 ## clase cliente que hereda de la identidad
class Cliente(Entidad):  
    """Representa un cliente de Software FJ."""
## permite almacenar  información que se requiere del cliente.
    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)

        self.__nombre = self._validar_nombre(nombre)
        self.__documento = self._validar_documento(documento)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

        logger.info("Cliente registrado: %s", self.__nombre)

    # valida y organiza la infomación que se suministra 

    @staticmethod
    def _validar_nombre(nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if len(nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

        return nombre.strip().title()
    
## validación del documento 
    @staticmethod
    def _validar_documento(documento):
        documento = str(documento).strip()

        if not documento.isdigit():
            raise ValueError("El documento debe contener solamente números.")

        if not 6 <= len(documento) <= 12:
            raise ValueError("El documento debe tener entre 6 y 12 dígitos.")

        return documento
    
## validación del correo electronico 
    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str):
            raise ValueError("El correo debe ser texto.")

        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.match(patron, correo.strip()):
            raise ValueError("El correo electrónico no es válido.")

        return correo.strip().lower()
## validación del numero teléfonico 
    @staticmethod
    def _validar_telefono(telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise ValueError("El teléfono debe contener entre 7 y 15 dígitos.")
        return telefono
## estas propiedades permiten consultar los atributos privados sin acceder directamente a ellos
    @property
    def nombre(self):
        return self.__nombre
    @property
    def documento(self):
        return self.__documento
    @property
    def correo(self):
        return self.__correo
    @property
    def telefono(self):
        return self.__telefono
 #  permite modificar el correo pero antes valida que el nuevo sea valido
    @correo.setter
    def correo(self, nuevo_correo):
        self.__correo = self._validar_correo(nuevo_correo)
        logger.info("Correo actualizado para cliente %s", self.__documento)
    @telefono.setter
    def telefono(self, nuevo_telefono):
        self.__telefono = self._validar_telefono(nuevo_telefono)
        logger.info("Teléfono actualizado para cliente %s", self.__documento)
## este metodo devuelve toda la infomación del cliente e implementa el metodo abstarcto heredado de identidad 
    def obtener_informacion(self):
        return {
            "identificador": self.identificador,
            "nombre": self.__nombre,
            "documento": self.__documento,
            "correo": self.__correo,
            "telefono": self.__telefono
        }
    def __str__(self):
        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )
