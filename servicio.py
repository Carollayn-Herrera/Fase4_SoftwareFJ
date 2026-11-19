##Importación de herramientas para la creación de la clase abstracta y registro de evento
from abc import abstractmethod
from entidad import EntidadSistema ## clase abstracta base del sistema, de aquí hereda el servicio
from excepciones import ParametroInvalidoError ## excepción personalizada para datos que no son válidos
from logger import registrar_evento ## registra los eventos en el archivo de logs del proyecto
## clase general que modela los servicios de Software
class Servicio(EntidadSistema):
    """Clase abstracta que representa un servicio de Software FJ."""
## parametros a recibir
    def __init__(self, codigo, nombre, precio_base):
        if not codigo or not isinstance(codigo, str):
            raise ParametroInvalidoError("El código del servicio es obligatorio.", codigo)
        if not nombre or not isinstance(nombre, str):
            raise ParametroInvalidoError("El nombre del servicio es obligatorio.", nombre)
        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)):
            raise ParametroInvalidoError("El precio debe ser numérico.", precio_base)
        if precio_base <= 0:
            raise ParametroInvalidoError("El precio debe ser mayor que cero.", precio_base)
        super().__init__(codigo.strip().upper()) ## el código se usa como identificador de la entidad
## verificación y almacenamiendo de datos .
        self._codigo = codigo.strip().upper()
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = True
        registrar_evento(f"Servicio creado: {self._nombre}")
    @property
    def codigo(self):
        return self._codigo
    @property
    def nombre(self):
        return self._nombre
    @property
    def precio_base(self):
        return self._precio_base
    @property
    def disponible(self):
        return self._disponible
    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise ParametroInvalidoError("La disponibilidad debe ser True o False.", estado)
        self._disponible = estado
        registrar_evento(f"Disponibilidad de {self._nombre} actualizada: {estado}")
##Método para establecerlas funciones que deben implementar los servicios
    @abstractmethod
    def calcular_costo(self, duracion):
        pass
    @abstractmethod
    def describir_servicio(self):
        pass
    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass
## revisa que los datos generales del servicio sigan siendo válidos, es obligatorio por EntidadSistema
    def validar(self):
        if not self._nombre:
            raise ParametroInvalidoError("El nombre del servicio es obligatorio.", self._nombre)
        if self._precio_base <= 0:
            raise ParametroInvalidoError("El precio debe ser mayor que cero.", self._precio_base)
        return True
## muestra la descripción del servicio, también es obligatorio por EntidadSistema
    def mostrar_informacion(self):
        return self.describir_servicio()
## función de calculo donde incluye el 19% del impuesto
    def calcular_costo_con_impuestos(self, duracion, impuesto=0.19):
        """Variante del cálculo con impuesto configurable."""
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ParametroInvalidoError("El impuesto debe ser numérico.", impuesto)
        if not 0 <= impuesto <= 1:
            raise ParametroInvalidoError("El impuesto debe estar entre 0 y 1.", impuesto)
        costo = self.calcular_costo(duracion)
        return round(costo * (1 + impuesto), 2)
## funcion que permite calcular el descuento incluyendo el % del impuesto
    def calcular_costo_con_descuento(
        self, duracion, descuento=0, impuesto=0.19
    ):
        """Variante del cálculo con descuento e impuesto."""
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ParametroInvalidoError("El descuento debe ser numérico.", descuento)
        if not 0 <= descuento <= 1:
            raise ParametroInvalidoError("El descuento debe estar entre 0 y 1.", descuento)
        costo = self.calcular_costo(duracion)
        costo_descuento = costo * (1 - descuento)
        return round(costo_descuento * (1 + impuesto), 2)
    def __str__(self):
        return (
            f"{self._nombre} | Código: {self._codigo} | "
            f"Precio base: ${self._precio_base:,.2f}"
        )
## clase heredada de servicio, y representa el calculo de personas que van a reeservar
class ReservaSala(Servicio):
    """Servicio especializado en reservas de salas."""
    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise ParametroInvalidoError("La capacidad debe ser un número entero.", capacidad)
        if capacidad <= 0:
            raise ParametroInvalidoError("La capacidad debe ser mayor que cero.", capacidad)
        self.__capacidad = capacidad

    def validar_parametros(self, **kwargs):
        personas = kwargs.get("personas")

        if isinstance(personas, bool) or not isinstance(personas, int):
            raise ParametroInvalidoError("Debe indicar un número entero de personas.", personas)
        if personas <= 0 or personas > self.__capacidad:
            raise ParametroInvalidoError("La cantidad de personas supera la capacidad.", personas)
        return True
    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ParametroInvalidoError("La duración debe ser numérica.", duracion)
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor que cero.", duracion)
        return round(self.precio_base * duracion, 2)
    def describir_servicio(self):
        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad máxima: {self.__capacidad} personas. "
            f"Tarifa por hora: ${self.precio_base:,.2f}"
        )
## clase heredada de servicio, permite administrar el alquiler de los equipos
class AlquilerEquipo(Servicio):
    """Servicio especializado en alquiler de equipos."""

    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ParametroInvalidoError("Debe especificar el tipo de equipo.", tipo_equipo)
        self.__tipo_equipo = tipo_equipo.strip()
    def validar_parametros(self, **kwargs):
        cantidad = kwargs.get("cantidad")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ParametroInvalidoError("La cantidad debe ser un número entero.", cantidad)
        if cantidad <= 0:
            raise ParametroInvalidoError("La cantidad debe ser mayor que cero.", cantidad)
        return True
    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ParametroInvalidoError("La duración debe ser numérica.", duracion)
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor que cero.", duracion)
        return round(self.precio_base * duracion, 2)
    def describir_servicio(self):
        return (
            f"Alquiler de equipo: {self.nombre}. "
            f"Tipo: {self.__tipo_equipo}. "
            f"Tarifa por hora: ${self.precio_base:,.2f}"
        )
## clase heredada de sevicios, donde se indica el tipo de asesoria
class AsesoriaEspecializada(Servicio):
    """Servicio especializado en asesorías profesionales."""
    def __init__(self, codigo, nombre, precio_base, especialidad):
        super().__init__(codigo, nombre, precio_base)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ParametroInvalidoError("Debe indicar una especialidad.", especialidad)
        self.__especialidad = especialidad.strip()
    def validar_parametros(self, **kwargs):
        modalidad = kwargs.get("modalidad")
        modalidades_validas = ["virtual", "presencial"]
        if not isinstance(modalidad, str):
            raise ParametroInvalidoError("Debe especificar la modalidad.", modalidad)

        if modalidad.lower() not in modalidades_validas:
            raise ParametroInvalidoError("Modalidad no válida.", modalidad)
        return True
    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ParametroInvalidoError("La duración debe ser numérica.", duracion)
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor que cero.", duracion)
        return round(self.precio_base * duracion * 1.15, 2)
    def describir_servicio(self):
        return (
            f"Asesoría especializada: {self.nombre}. "
            f"Especialidad: {self.__especialidad}. "
            f"Tarifa por hora: ${self.precio_base * 1.15:,.2f}"
        )