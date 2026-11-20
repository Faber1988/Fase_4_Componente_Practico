"""Clase Reserva: integra cliente, servicio, duración y estado."""
from .entidades import Cliente, Entidad
from .excepciones import (OperacionNoPermitidaError, ReservaInvalidaError,
                          ServicioNoDisponibleError, SoftwareFJError)
from .registro import obtener_logger
from .servicios import Servicio

log = obtener_logger()


class Reserva(Entidad):
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: float) -> None:
        super().__init__()
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un cliente y un servicio válidos.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible.")
        servicio.validar_parametros(horas)  # falla si la duración no es válida
        self._cliente, self._servicio, self._horas = cliente, servicio, horas
        self._estado = "PENDIENTE"
        self._costo = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self) -> None:
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"Solo se confirman reservas PENDIENTES (actual: {self._estado}).")
        self._estado = "CONFIRMADA"
        log.info("Reserva #%s confirmada", self.id)

    def cancelar(self) -> None:
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}.")
        self._estado = "CANCELADA"
        log.info("Reserva #%s cancelada", self.id)

    def procesar(self, descuento: float = 0.0) -> float:
        """Procesa la reserva con try/except/else/finally y encadenamiento."""
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    "La reserva debe estar CONFIRMADA para procesarse.")
            total = self._servicio.calcular_costo_total(self._horas, descuento=descuento)
        except SoftwareFJError as error:
            log.error("Fallo al procesar reserva #%s: %s", self.id, error)
            # encadenamiento: la causa original se conserva con 'from'
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva #{self.id}.") from error
        else:  # solo se ejecuta si NO hubo excepción
            self._estado, self._costo = "PROCESADA", total
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{total:,.2f}")
            return total
        finally:  # siempre se ejecuta
            log.info("Fin del intento de procesamiento de reserva #%s", self.id)

    def describir(self) -> str:
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado}")
