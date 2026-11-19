##Importación de herramientas para la creación de la clase abstracta y registro de evento
import logging
from abc import ABC, abstractmethod
logger = logging.getLogger("SoftwareFJ")
## clase general que modela los servicios de Software
class Servicio(ABC):
    """Clase abstracta que representa un servicio de Software FJ."""
## parametros a recibir 
    def __init__(self, codigo, nombre, precio_base):
        if not codigo or not isinstance(codigo, str):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("El código del servicio es obligatorio.")
        if not nombre or not isinstance(nombre, str):
            raise ClienteInvalidoError("El nombre del servicio es obligatorio.")
        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)):
            raise ClienteInvalidoError("El precio debe ser numérico.")
        if precio_base <= 0:
            raise ClienteInvalidoError("El precio debe ser mayor que cero.")
## verificación y almacenamiendo de datos .
        self._codigo = codigo.strip().upper()
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = True
        logger.info("Servicio creado: %s", self._nombre)
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
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("La disponibilidad debe ser True o False.")
        self._disponible = estado
        logger.info(
            "Disponibilidad de %s actualizada: %s",
            self._nombre, estado
        )
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
## función de calculo donde incluye el 19% del impuesto
    def calcular_costo_con_impuestos(self, duracion, impuesto=0.19):
        """Variante del cálculo con impuesto configurable."""
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("El impuesto debe ser numérico.")
        if not 0 <= impuesto <= 1:
            raise ClienteInvalidoError("El impuesto debe estar entre 0 y 1.")
        costo = self.calcular_costo(duracion)
        return round(costo * (1 + impuesto), 2)
## funcion que permite calcular el descuento incluyendo el % del impuesto
    def calcular_costo_con_descuento(
        self, duracion, descuento=0, impuesto=0.19
    ):
        """Variante del cálculo con descuento e impuesto."""
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("El descuento debe ser numérico.")
        if not 0 <= descuento <= 1:
            raise ClienteInvalidoError("El descuento debe estar entre 0 y 1.")
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
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("La capacidad debe ser un número entero.")
        if capacidad <= 0:
            raise ClienteInvalidoError("La capacidad debe ser mayor que cero.")
        self.__capacidad = capacidad

    def validar_parametros(self, **kwargs):
        personas = kwargs.get("personas")

        if isinstance(personas, bool) or not isinstance(personas, int):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("Debe indicar un número entero de personas.")
        if personas <= 0 or personas > self.__capacidad:
            raise ClienteInvalidoError("La cantidad de personas supera la capacidad.")
        return True
    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("La duración debe ser numérica.")
        if duracion <= 0:
            raise ClienteInvalidoError("La duración debe ser mayor que cero.")
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
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("Debe especificar el tipo de equipo.")
        self.__tipo_equipo = tipo_equipo.strip()
    def validar_parametros(self, **kwargs):
        cantidad = kwargs.get("cantidad")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("La cantidad debe ser un número entero.")
        if cantidad <= 0:
            raise ClienteInvalidoError("La cantidad debe ser mayor que cero.")
        return True
    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ClienteInvalidoError("La duración debe ser numérica.")
        if duracion <= 0:
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("La duración debe ser mayor que cero.")
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
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("Debe indicar una especialidad.")
        self.__especialidad = especialidad.strip()
    def validar_parametros(self, **kwargs):
        modalidad = kwargs.get("modalidad")
        modalidades_validas = ["virtual", "presencial"]
        if not isinstance(modalidad, str):
            def ClienteInvalidoError(arg1):
                ...
            raise ClienteInvalidoError("Debe especificar la modalidad.")

        if modalidad.lower() not in modalidades_validas:
            raise ClienteInvalidoError("Modalidad no válida.")
        return True
    def calcular_costo(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ClienteInvalidoError("La duración debe ser numérica.")
        if duracion <= 0:
            def ClienteInvalidoError(arg1):                ...

            raise ClienteInvalidoError("La duración debe ser mayor que cero.")
        return round(self.precio_base * duracion * 1.15, 2)
    def describir_servicio(self):
        return (
            f"Asesoría especializada: {self.nombre}. "
            f"Especialidad: {self.__especialidad}. "
            f"Tarifa por hora: ${self.precio_base * 1.15:,.2f}"
        )
