import re ## permite usar expresiones regulares para validar información
from entidad import EntidadSistema ## clase abstracta base del sistema, de aquí hereda el cliente
from excepciones import ClienteInvalidoError ## excepción personalizada para datos de clientes
from logger import registrar_evento ## registra los eventos en el archivo de logs del proyecto

 ## clase cliente que hereda de EntidadSistema
class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ."""
## permite almacenar  información que se requiere del cliente.
    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)

        self.__nombre = self._validar_nombre(nombre)
        self.__documento = self._validar_documento(documento)
        self.__correo = self._validar_correo(correo)
        self.__telefono = self._validar_telefono(telefono)

        registrar_evento(f"Cliente registrado: {self.__nombre}")

    # valida y organiza la infomación que se suministra

    @staticmethod
    def _validar_nombre(nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.", nombre)

        if len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.", nombre)

        return nombre.strip().title()

## validación del documento
    @staticmethod
    def _validar_documento(documento):
        documento = str(documento).strip()

        if not documento.isdigit():
            raise ClienteInvalidoError("El documento debe contener solamente números.", documento)

        if not 6 <= len(documento) <= 12:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 dígitos.", documento)

        return documento

## validación del correo electronico
    @staticmethod
    def _validar_correo(correo):
        if not isinstance(correo, str):
            raise ClienteInvalidoError("El correo debe ser texto.", correo)

        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.match(patron, correo.strip()):
            raise ClienteInvalidoError("El correo electrónico no es válido.", correo)

        return correo.strip().lower()
## validación del numero teléfonico
    @staticmethod
    def _validar_telefono(telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise ClienteInvalidoError("El teléfono debe contener entre 7 y 15 dígitos.", telefono)
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
        registrar_evento(f"Correo actualizado para cliente {self.__documento}")
    @telefono.setter
    def telefono(self, nuevo_telefono):
        self.__telefono = self._validar_telefono(nuevo_telefono)
        registrar_evento(f"Teléfono actualizado para cliente {self.__documento}")
## revisa que todos los datos del cliente sigan siendo válidos, es obligatorio por la clase EntidadSistema
    def validar(self):
        self._validar_nombre(self.__nombre)
        self._validar_documento(self.__documento)
        self._validar_correo(self.__correo)
        self._validar_telefono(self.__telefono)
        return True
## devuelve el resumen del cliente en texto, también es obligatorio por la clase EntidadSistema
    def mostrar_informacion(self):
        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )
## este metodo devuelve toda la infomación del cliente en un diccionario
    def obtener_informacion(self):
        return {
            "identificador": self.identificador,
            "nombre": self.__nombre,
            "documento": self.__documento,
            "correo": self.__correo,
            "telefono": self.__telefono
        }
    def __str__(self):
        return self.mostrar_informacion()
