"""Clase abstracta Entidad y clase Cliente (encapsulación + validaciones)."""
import re
from abc import ABC, abstractmethod

from .excepciones import ClienteInvalidoError, ParametroFaltanteError


class Entidad(ABC):
    """Abstracción de cualquier entidad general del sistema."""

    _contador = 0  # contador compartido para generar identificadores

    def __init__(self) -> None:
        Entidad._contador += 1
        self._id = Entidad._contador  # atributo encapsulado

    @property
    def id(self) -> int:
        """Identificador único (solo lectura)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma."""


class Cliente(Entidad):
    """Cliente de Software FJ con datos personales encapsulados."""

    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__()
        if nombre is None or documento is None or correo is None or telefono is None:
            raise ParametroFaltanteError(
                "Nombre, documento, correo y teléfono son obligatorios."
            )
        # Se usan los setters para validar desde la creación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self.__nombre = valor.strip().title()

    # ---- documento ----
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor) -> None:
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 dígitos.")
        self.__documento = valor

    # ---- correo ----
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor.strip().lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor) -> None:
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener exactamente 10 dígitos.")
        self.__telefono = valor

    def describir(self) -> str:
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.correo} | Tel: {self.telefono}")
