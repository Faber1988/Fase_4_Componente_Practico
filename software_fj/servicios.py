"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod

from .entidades import Entidad
from .excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                          ServicioInvalidoError)

IVA = 0.19  # impuesto por defecto


class Servicio(Entidad):
    """Abstracción de un servicio ofrecido por Software FJ."""

    def __init__(self, nombre: str, tarifa_hora: float) -> None:
        super().__init__()
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El servicio requiere un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número positivo.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    # ---- métodos abstractos (se sobrescriben en cada servicio) ----
    @abstractmethod
    def calcular_costo(self, horas: float) -> float:
        """Costo base antes de impuestos y descuentos."""

    @abstractmethod
    def validar_parametros(self, horas: float) -> None:
        """Valida los parámetros propios de cada servicio."""

    # ---- sobrecarga simulada: una sola firma con parámetros opcionales ----
    def calcular_costo_total(self, horas: float, impuesto: float = IVA,
                             descuento: float = 0.0) -> float:
        """Variantes de cálculo:
        - calcular_costo_total(h)                    -> con IVA 19 %
        - calcular_costo_total(h, impuesto=0.0)      -> sin impuesto
        - calcular_costo_total(h, descuento=0.10)    -> con IVA y 10 % de descuento
        """
        self.validar_parametros(horas)
        if not 0 <= descuento < 1 or impuesto < 0:
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango.")
        base = self.calcular_costo(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo total calculado no es positivo.")
        return round(total, 2)

    def describir(self) -> str:
        return f"Servicio #{self.id}: {self.nombre} | ${self.tarifa_hora:,.0f}/hora"


class ReservaSala(Servicio):
    """Reserva de salas: el costo crece con la capacidad."""

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int) -> None:
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ServicioInvalidoError("La capacidad debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 12:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 12 horas.")

    def calcular_costo(self, horas: float) -> float:
        recargo = 1.10 if self._capacidad > 20 else 1.0  # salas grandes +10 %
        return self.tarifa_hora * horas * recargo

    def describir(self) -> str:
        return f"{super().describir()} | Sala para {self._capacidad} personas"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: incluye un depósito fijo de garantía."""

    DEPOSITO = 50_000

    def __init__(self, nombre: str, tarifa_hora: float, equipo: str) -> None:
        super().__init__(nombre, tarifa_hora)
        if not equipo or not str(equipo).strip():
            raise ServicioInvalidoError("Debe indicar el equipo a alquilar.")
        self._equipo = equipo.strip()

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas.")

    def calcular_costo(self, horas: float) -> float:
        return self.tarifa_hora * horas + self.DEPOSITO

    def describir(self) -> str:
        return f"{super().describir()} | Equipo: {self._equipo} (depósito ${self.DEPOSITO:,})"


class AsesoriaEspecializada(Servicio):
    """Asesoría: el nivel del experto modifica la tarifa."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre: str, tarifa_hora: float, nivel: str) -> None:
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido {nivel!r}. Opciones: {list(self.NIVELES)}")
        self._nivel = nivel

    def validar_parametros(self, horas: float) -> None:
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 8:
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 8 horas.")

    def calcular_costo(self, horas: float) -> float:
        return self.tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self) -> str:
        return f"{super().describir()} | Asesoría nivel {self._nivel}"
