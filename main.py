"""Simulación de 12 operaciones: válidas e inválidas. El programa nunca se detiene."""
from software_fj.sistema import SistemaFJ
from software_fj.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main() -> None:
    fj = SistemaFJ()

    print("\n1. Cliente válido")
    ana = fj.registrar_cliente(nombre="Ana Gómez", documento="1043567890",
                               correo="ana@correo.com", telefono="3001234567")
    print("\n2. Cliente inválido (correo mal formado)")
    fj.registrar_cliente(nombre="Luis Pérez", documento="1020304050",
                         correo="luis-sin-arroba", telefono="3109876543")
    print("\n3. Cliente inválido (parámetro faltante)")
    fj.registrar_cliente(nombre="Marta Ruiz", documento="55667788")
    print("\n4. Segundo cliente válido")
    carlos = fj.registrar_cliente(nombre="Carlos Díaz", documento="900800700",
                                  correo="carlos@correo.com", telefono="3151112233")

    print("\n5. Servicio válido: sala")
    sala = fj.registrar_servicio(ReservaSala, nombre="Sala Ejecutiva",
                                 tarifa_hora=80_000, capacidad=25)
    print("\n6. Servicio inválido (tarifa negativa)")
    fj.registrar_servicio(AlquilerEquipo, nombre="Proyector", tarifa_hora=-5, equipo="Epson")
    equipo = fj.registrar_servicio(AlquilerEquipo, nombre="Alquiler Portátil",
                                   tarifa_hora=15_000, equipo="Laptop")
    asesoria = fj.registrar_servicio(AsesoriaEspecializada, nombre="Asesoría Cloud",
                                     tarifa_hora=120_000, nivel="senior")

    print("\n7. Reserva exitosa (sala, 3 h) con confirmación y procesamiento")
    r1 = fj.crear_reserva(ana, sala, 3)
    fj.confirmar_reserva(r1)
    fj.procesar_reserva(r1)

    print("\n8. Reserva fallida (duración inválida: 20 h)")
    fj.crear_reserva(carlos, sala, 20)

    print("\n9. Procesar sin confirmar (operación no permitida, excepción encadenada)")
    r2 = fj.crear_reserva(carlos, equipo, 10)
    fj.procesar_reserva(r2)

    print("\n10. Reserva con descuento del 10 %")
    r3 = fj.crear_reserva(ana, asesoria, 2)
    fj.confirmar_reserva(r3)
    fj.procesar_reserva(r3, descuento=0.10)

    print("\n11. Servicio no disponible")
    equipo.disponible = False
    fj.crear_reserva(ana, equipo, 5)

    print("\n12. Cancelar una reserva ya procesada (no permitido)")
    fj.cancelar_reserva(r1)

    print("\n--- RESUMEN ---")
    for objeto in fj.clientes + fj.servicios + fj.reservas:
        print(" ", objeto.describir())
    print("\nEl programa terminó sin interrupciones. Revisa logs/software_fj.log")


if __name__ == "__main__":
    main()
