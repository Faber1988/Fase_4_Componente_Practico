"""Gestor principal: administra las listas internas (sin base de datos)."""
from .entidades import Cliente
from .excepciones import SoftwareFJError
from .registro import obtener_logger
from .reserva import Reserva

log = obtener_logger()


class SistemaFJ:
    def __init__(self) -> None:
        self.clientes, self.servicios, self.reservas = [], [], []

    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación; si falla, registra el error y sigue."""
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as e:
            causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
            log.error("%s -> %s: %s%s", descripcion, type(e).__name__, e, causa)
            print(f"  [ERROR CONTROLADO] {type(e).__name__}: {e}{causa}")
            return None
        except Exception as e:  # error inesperado: el sistema no se detiene
            log.critical("%s -> Error inesperado %s: %s", descripcion, type(e).__name__, e)
            print(f"  [ERROR INESPERADO] {type(e).__name__}: {e}")
            return None
        log.info("%s -> OK", descripcion)
        print(f"  [OK] {descripcion}")
        return resultado

    def registrar_cliente(self, **datos):
        def crear():
            cliente = Cliente(**datos)
            self.clientes.append(cliente)
            return cliente
        return self._ejecutar("Registro de cliente", crear)

    def registrar_servicio(self, clase, **datos):
        def crear():
            servicio = clase(**datos)
            self.servicios.append(servicio)
            return servicio
        return self._ejecutar(f"Creación de servicio {clase.__name__}", crear)

    def crear_reserva(self, cliente, servicio, horas):
        def crear():
            reserva = Reserva(cliente, servicio, horas)
            self.reservas.append(reserva)
            return reserva
        return self._ejecutar("Creación de reserva", crear)

    def confirmar_reserva(self, reserva):
        return self._ejecutar("Confirmación de reserva", reserva.confirmar)

    def cancelar_reserva(self, reserva):
        return self._ejecutar("Cancelación de reserva", reserva.cancelar)

    def procesar_reserva(self, reserva, **kwargs):
        return self._ejecutar("Procesamiento de reserva", reserva.procesar, **kwargs)
