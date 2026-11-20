"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""


class ParametroFaltanteError(SoftwareFJError):
    """Se omitió un parámetro obligatorio."""


class ClienteInvalidoError(SoftwareFJError):
    """Los datos del cliente no superan las validaciones."""


class ServicioInvalidoError(SoftwareFJError):
    """Los parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se pudo crear o procesar correctamente."""


class OperacionNoPermitidaError(SoftwareFJError):
    """La operación no es válida para el estado actual del objeto."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de costos produjo un resultado inconsistente."""
