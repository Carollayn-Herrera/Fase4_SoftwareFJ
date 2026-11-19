from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from logger import registrar_evento, registrar_error


# Listas donde se guardan los clientes, servicios y reservas que se van creando
clientes = []
servicios = []
reservas = []


# Ejecuta una operación y, si falla, muestra el error sin que el programa se detenga
def ejecutar_operacion(numero, descripcion, accion):
    print(f"\nOperación {numero}: {descripcion}")
    try:
        resultado = accion()
    except ErrorSoftwareFJ as e:
        # Errores que nosotros mismos previmos, como datos inválidos o servicios no disponibles
        print(f"   Error controlado: {e}")
        registrar_error(f"Falló la operación {numero}", e)
    except Exception as e:
        # Cualquier otro error inesperado también se registra para que el sistema siga funcionando
        print(f"   Error inesperado: {e}")
        registrar_error(f"Error inesperado en la operación {numero}", e)
    else:
        # Solo se muestra si la operación salió bien
        print(f"   Operación exitosa: {resultado}")
    finally:
        # Se guarda en el log que la operación terminó, haya salido bien o mal
        registrar_evento(f"Fin de la operación {numero}: {descripcion}")


# Cada función de aquí abajo es una de las operaciones que se simulan
def registrar_cliente_valido():
    cliente = Cliente("C001", "ana gómez", "1023456789", "ana.gomez@gmail.com", "3001234567")
    clientes.append(cliente)
    return cliente


def registrar_cliente_invalido():
    # El correo no tiene @, así que el cliente no se debería poder registrar
    cliente = Cliente("C002", "Luis Pérez", "80123456", "luisperez.com", "3109876543")
    clientes.append(cliente)
    return cliente


def crear_servicios():
    sala = ReservaSala("S01", "Sala de reuniones", 50000, 10)
    equipo = AlquilerEquipo("E01", "Proyector", 30000, "Video beam")
    asesoria = AsesoriaEspecializada("A01", "Asesoría en Python", 80000, "Programación")
    servicios.extend([sala, equipo, asesoria])
    return f"se crearon {len(servicios)} servicios"


def crear_servicio_invalido():
    # Un precio negativo no tiene sentido, entonces el servicio se rechaza
    servicio = ReservaSala("S02", "Sala pequeña", -20000, 4)
    servicios.append(servicio)
    return servicio


def reserva_exitosa():
    # Ana reserva la sala por 2 horas, se confirma y se calcula el total con el IVA del 19 %
    reserva = Reserva("R001", clientes[0], servicios[0], 2)
    reserva.confirmar()
    reserva.procesar(impuesto=0.19)
    reservas.append(reserva)
    return reserva


def reserva_con_descuento():
    # Ana pide una asesoría de 3 horas virtual con un 10 % de descuento
    servicios[2].validar_parametros(modalidad="virtual")
    reserva = Reserva("R002", clientes[0], servicios[2], 3)
    reserva.confirmar()
    reserva.procesar(impuesto=0.19, descuento=0.10)
    reservas.append(reserva)
    return reserva


def reserva_servicio_no_disponible():
    # Ponemos el proyector como no disponible para ver qué pasa al intentar reservarlo
    servicios[1].cambiar_disponibilidad(False)
    reserva = Reserva("R003", clientes[0], servicios[1], 4)
    reservas.append(reserva)
    reserva.confirmar()
    return reserva


def reserva_duracion_invalida():
    # Una reserva con horas negativas no se puede crear
    reserva = Reserva("R004", clientes[0], servicios[0], -3)
    reservas.append(reserva)
    return reserva


def sala_sobre_capacidad():
    # La sala es para 10 personas y se intenta reservar para 15
    servicios[0].validar_parametros(personas=15)
    return "la sala sí tiene capacidad"


def cancelar_dos_veces():
    # Se cancela una reserva y luego se intenta cancelar otra vez, lo cual no está permitido
    reserva = Reserva("R005", clientes[0], servicios[0], 1)
    reservas.append(reserva)
    reserva.cancelar()
    reserva.cancelar()
    return reserva


# Aquí arranca el programa y se ejecutan las 10 operaciones en orden
if __name__ == "__main__":
    print("=== Sistema de gestión Software FJ ===")
    registrar_evento("Inicio de la simulación del sistema")

    ejecutar_operacion(1, "Registrar un cliente con datos correctos", registrar_cliente_valido)
    ejecutar_operacion(2, "Registrar un cliente con correo inválido", registrar_cliente_invalido)
    ejecutar_operacion(3, "Crear los tres tipos de servicio", crear_servicios)
    ejecutar_operacion(4, "Crear un servicio con precio negativo", crear_servicio_invalido)
    ejecutar_operacion(5, "Reservar la sala, confirmar y procesar", reserva_exitosa)
    ejecutar_operacion(6, "Reservar una asesoría con descuento", reserva_con_descuento)
    ejecutar_operacion(7, "Reservar un equipo que no está disponible", reserva_servicio_no_disponible)
    ejecutar_operacion(8, "Crear una reserva con duración negativa", reserva_duracion_invalida)
    ejecutar_operacion(9, "Reservar la sala para más personas de las permitidas", sala_sobre_capacidad)
    ejecutar_operacion(10, "Cancelar dos veces la misma reserva", cancelar_dos_veces)

    # Resumen final de lo que quedó guardado en el sistema
    print("\n=== Resumen ===")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios disponibles: {len(servicios)}")
    print(f"Reservas creadas: {len(reservas)}")
    for reserva in reservas:
        print(f" - {reserva}")

    registrar_evento("Fin de la simulación del sistema")
    print("\nLos detalles de cada operación quedaron guardados en registro_eventos.log")