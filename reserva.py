from entidad import EntidadSistema
from excepciones import (ReservaInvalidaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, CalculoInconsistenteError)
from logger import registrar_evento, registrar_error


# Esta clase representa una reserva: junta al cliente con el servicio que pidió y por cuántas horas
class Reserva(EntidadSistema):

    # Estos son los estados por los que puede pasar una reserva
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)  # La clase padre se encarga de revisar el identificador
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = Reserva.PENDIENTE  # Cuando se crea, la reserva queda pendiente hasta que se confirme
        self._costo_total = 0  # Arranca en cero porque el valor se calcula al procesarla
        self.validar()  # Antes de dar la reserva por creada, revisamos que los datos estén bien
        registrar_evento(f"Reserva {self.identificador} creada para {self._cliente.nombre}")

    # Con estas propiedades se pueden ver los datos de la reserva, pero no cambiarlos desde afuera
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # Revisa que la reserva tenga un cliente, un servicio y una cantidad de horas válida
    def validar(self):
        if self._cliente is None or self._servicio is None:
            raise ReservaInvalidaError("La reserva debe tener un cliente y un servicio")
        # Las horas deben ser un número y además mayor que cero, no se puede reservar 0 o -1 horas
        if not isinstance(self._duracion, (int, float)) or self._duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser un número mayor que cero", self._duracion)
        return True

    # Confirma la reserva, siempre y cuando esté pendiente y el servicio se pueda usar
    def confirmar(self):
        try:
            # Si la reserva ya fue confirmada, cancelada o procesada, no se puede volver a confirmar
            if self._estado != Reserva.PENDIENTE:
                raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado {self._estado}")
            # Tampoco se puede confirmar si el servicio no está disponible en ese momento
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio {self._servicio.nombre} no está disponible")
        except (OperacionNoPermitidaError, ServicioNoDisponibleError) as e:
            registrar_error(f"No se pudo confirmar la reserva {self.identificador}", e)
            raise  # Dejamos el error en el log y lo pasamos para que el programa principal lo maneje
        else:
            # Si llegamos aquí es porque no hubo ningún problema, así que la reserva queda confirmada
            self._estado = Reserva.CONFIRMADA
            registrar_evento(f"Reserva {self.identificador} confirmada")
        finally:
            # Esto se guarda en el log siempre, salga bien o mal la confirmación
            registrar_evento(f"Terminó el intento de confirmar la reserva {self.identificador}")

    # Cancela la reserva, pero solo si no se había cancelado o procesado antes
    def cancelar(self):
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):
            error = OperacionNoPermitidaError(f"La reserva {self.identificador} ya está {self._estado.lower()}")
            registrar_error("Intento de cancelación no permitido", error)
            raise error
        self._estado = Reserva.CANCELADA
        registrar_evento(f"Reserva {self.identificador} cancelada")

    # Calcula cuánto hay que pagar y deja la reserva como procesada, solo si ya estaba confirmada
    def procesar(self, impuesto=0, descuento=0):
        if self._estado != Reserva.CONFIRMADA:
            error = OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas", self._estado)
            registrar_error(f"No se pudo procesar la reserva {self.identificador}", error)
            raise error
        try:
            # Le pedimos al servicio que calcule su precio, porque cada tipo de servicio cobra distinto
            costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
            # Si el valor da cero o negativo, algo quedó mal en el cálculo
            if costo <= 0:
                raise ValueError(f"el costo calculado fue {costo}")
        except (ValueError, TypeError) as e:
            registrar_error(f"Error al calcular el costo de la reserva {self.identificador}", e)
            # Lanzamos nuestro propio error, pero conectado al original para saber qué lo causó
            raise CalculoInconsistenteError("No se pudo calcular el costo de la reserva") from e
        else:
            # Si el cálculo salió bien, guardamos el valor y la reserva queda procesada
            self._costo_total = costo
            self._estado = Reserva.PROCESADA
            registrar_evento(f"Reserva {self.identificador} procesada por ${costo:,.0f}")
            return costo

    # Arma un resumen de la reserva con todos sus datos para mostrarlo en pantalla
    def mostrar_informacion(self):
        return (f"Reserva {self.identificador} | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} h | "
                f"Estado: {self._estado} | Total: ${self._costo_total:,.0f}")


# Esta parte solo se ejecuta si corremos este archivo directamente, la usamos para probarlo
if __name__ == "__main__":

    # Clases de prueba sencillas para probar mientras tenemos listos cliente.py y servicios.py
    class ClientePrueba:
        def __init__(self, nombre):
            self.nombre = nombre

    class ServicioPrueba:
        def __init__(self, nombre, precio_base, disponible=True):
            self.nombre = nombre
            self.precio_base = precio_base
            self.disponible = disponible

        # Calcula el precio por horas y le suma el impuesto o le resta el descuento
        def calcular_costo(self, duracion, impuesto=0, descuento=0):
            subtotal = self.precio_base * duracion
            return subtotal + subtotal * impuesto - subtotal * descuento

    ana = ClientePrueba("Ana Gómez")
    sala = ServicioPrueba("Sala de reuniones", 50000)
    proyector = ServicioPrueba("Alquiler de proyector", 30000, disponible=False)

    # Caso 1: una reserva que sale bien de principio a fin
    r1 = Reserva("R001", ana, sala, 2)
    r1.confirmar()
    r1.procesar(impuesto=0.19)
    print(r1)

    # Caso 2: se intenta reservar un servicio que no está disponible
    try:
        Reserva("R002", ana, proyector, 3).confirmar()
    except ServicioNoDisponibleError as e:
        print("Error controlado:", e)

    # Caso 3: se intenta reservar con una cantidad de horas negativa
    try:
        Reserva("R003", ana, sala, -1)
    except ReservaInvalidaError as e:
        print("Error controlado:", e)

    # Caso 4: se intenta cancelar dos veces la misma reserva
    r4 = Reserva("R004", ana, sala, 1)
    r4.cancelar()
    try:
        r4.cancelar()
    except OperacionNoPermitidaError as e:
        print("Error controlado:", e)

    # Caso 5: un descuento exagerado hace que el precio dé negativo y se muestra la causa del error
    r5 = Reserva("R005", ana, sala, 1)
    r5.confirmar()
    try:
        r5.procesar(descuento=1.5)
    except CalculoInconsistenteError as e:
        print("Error controlado:", e, "| Causa original:", e.__cause__)