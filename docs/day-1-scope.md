# Día 1 Base y alcance

## Alcance cerrado para el piloto

El piloto atiende negocios de uñas y peluquerías con una única sucursal. Cada reserva corresponde a un único cliente, servicio y profesional, con un horario de inicio y fin. No contempla cupos, clases grupales, membresías, facturación fiscal, cobros en línea ni múltiples sucursales.

La aplicación se implementa como un único servicio FastAPI. En producción usa PostgreSQL de Supabase; el servidor controla las reservas públicas y las credenciales privilegiadas no llegan al navegador.

## Pantallas del MVP

| Persona | Pantalla | Objetivo | Día |
|---|---|---|---|
| Dueño | Acceso | Entrar con Google y mantener sesión | 2 |
| Dueño | Alta inicial | Crear negocio, zona horaria, servicios, profesionales y horarios | 2–3 |
| Dueño | Agenda diaria | Gestionar reservas y asistencia | 5 |
| Dueño | Caja | Registrar apertura, cobros, gastos y cierre | 6–7 |
| Dueño | Clientes | Consultar historial factual y cumplimiento | 8 |
| Cliente | Reserva pública | Elegir servicio, profesional, horario y datos de contacto | 4 |
| Cliente | Gestión privada | Consultar o cancelar únicamente su reserva | 5 |

## Reglas de reserva

1. Una reserva pertenece a un único negocio, profesional, servicio y cliente.
2. El horario termina después de empezar y se almacena en UTC. Cada negocio conserva su zona horaria IANA para mostrarlo localmente.
3. Un profesional no puede tener dos reservas activas superpuestas. La regla se impone en PostgreSQL mediante una restricción de exclusión; no depende de la interfaz.
4. Los estados activos son `pending` y `confirmed`. Los estados `cancelled`, `completed`, `no_show` y `expired` liberan el horario.
5. Una reserva pendiente puede confirmarse, cancelarse o vencer. Una confirmada puede cancelarse, marcarse como completada o como ausencia. Los estados finales no cambian.
6. La petición pública debe incluir una clave de idempotencia. Reintentos con la misma clave devuelven la misma reserva en vez de crear otra.
7. El teléfono sirve para contacto; no es una identidad autenticada ni autoriza acceso al historial.

## Modelo de datos

- `businesses` y `business_members`: negocio, zona horaria y permisos.
- `professionals` y `services`: oferta y duración.
- `clients`, `reservations` y `reservation_events`: operación y trazabilidad.

Todas las tablas operativas usan `business_id`. La migración habilita RLS y las políticas se completarán junto con el acceso del dueño en el Día 2.

## Criterio de salida

La aplicación puede iniciar y responder en `/health`; el esquema y los datos de demo se pueden aplicar a una base PostgreSQL vacía. El despliegue y el contacto con pilotos requieren las cuentas externas y no se consideran completos hasta verificarlos.
