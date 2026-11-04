# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto de la Fase 4 – Programación (213023), UNAD. Python 3.8+, sin bases de datos ni librerías externas.

## Ejecución
```bash
python main.py
```
Genera `logs/software_fj.log` con todos los eventos y errores.

## Estructura
| Archivo | Contenido |
|---|---|
| `software_fj/excepciones.py` | Excepciones personalizadas (jerarquía desde `SoftwareFJError`) |
| `software_fj/entidades.py` | Clase abstracta `Entidad` y `Cliente` (encapsulación + validaciones) |
| `software_fj/servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `software_fj/reserva.py` | `Reserva`: confirmar, cancelar, procesar (try/except/else/finally + `raise ... from`) |
| `software_fj/sistema.py` | `SistemaFJ`: listas internas y ejecución segura de operaciones |
| `software_fj/registro.py` | Configuración del archivo de logs |
| `main.py` | Simulación de 12 operaciones válidas e inválidas |

## Conceptos POO aplicados
Abstracción, herencia, polimorfismo (`calcular_costo`, `describir`, `validar_parametros`), encapsulación (atributos privados y `property`), sobrecarga de métodos (`calcular_costo_total` con parámetros opcionales), manejo avanzado de excepciones y logging.

## Integrantes
- (Agregar nombres del grupo)
