# MVP de gestión de pequeños negocios — Roadmap de 10 días

Fecha: 21 de septiembre de 2026.

## Objetivo

Construir un MVP usable por 3–5 negocios de uñas y peluquerías para gestionar reservas, agenda, caja e historial de clientes. Priorizar acceso sencillo, uso desde el celular y costos bajos.

El plazo supone trabajo diario dedicado y decisiones rápidas sobre el piloto. Al día 10 debe existir un piloto operativo; la reducción de ausencias y el valor comercial se validarán con uso real durante las dos semanas posteriores.

## Alcance inicial

- Una sucursal por negocio.
- Turnos individuales y uno o varios profesionales.
- Servicios con precio y duración.
- Horarios semanales, descansos y bloqueos.
- Reservas públicas sin cuenta de cliente.
- Agenda, confirmaciones, cancelaciones, reprogramaciones y asistencia.
- Señas, cobros, gastos y arqueo de caja.
- Historial de clientes, fidelidad y cumplimiento.
- Indicadores básicos de reservas, ausencias y cobros.

Fuera del MVP: gimnasios con cupos, membresías, clases grupales o recurrentes, múltiples sucursales, aplicaciones móviles nativas, WhatsApp automatizado, pasarela de pagos y facturación fiscal.

## Stack y arquitectura

| Componente | Elección |
|---|---|
| Backend | Python + FastAPI |
| Interfaz | Jinja2 + HTMX, diseñada primero para celular |
| Base de datos | PostgreSQL de Supabase |
| Autenticación del dueño | Supabase Auth con Google |
| Alternativa de acceso | Código por email, sujeto a configurar proveedor SMTP |
| Hosting | Un servicio Python en Railway |
| Métricas y cumplimiento | Consultas SQL y reglas explícitas |

Mantener una sola aplicación y una base compartida. Todos los datos operativos deben pertenecer a un negocio, con permisos y políticas de acceso que impidan acceso cruzado. Las reservas públicas pasan por el servidor con validación y límites de solicitudes. Las claves privilegiadas nunca se exponen al navegador.

Entidades iniciales: negocios, miembros y permisos, profesionales, servicios, disponibilidad, clientes, reservas, pagos, movimientos de caja, cierres de caja y registro de cambios relevantes.

## Experiencia de acceso

### Dueño

1. Continuar con Google.
2. Crear negocio y definir zona horaria.
3. Cargar servicios, precios, profesionales y horarios.
4. Compartir enlace público de reservas.

Mantener la sesión para evitar accesos repetidos. Incorporar código por email como alternativa si el proveedor de correo queda configurado dentro del plazo.

### Cliente

1. Abrir enlace desde Instagram o WhatsApp.
2. Elegir servicio, profesional o cualquiera disponible y horario.
3. Ingresar nombre y teléfono.
4. Solicitar reserva y ver su estado e instrucciones.

El negocio confirma el primer contacto por WhatsApp. Un teléfono escrito no acredita identidad ni permite consultar historiales. Los enlaces privados tienen permisos limitados, vencimiento y acceso únicamente a la reserva correspondiente.

## Roadmap

### Día 1 — Base y alcance

- [x] Definir pantallas y reglas de reserva.
- [x] Diseñar el modelo de datos y estados de las reservas.
- [x] Crear proyecto, migraciones y entorno de prueba.
- [x] Desplegar la aplicación inicial.
- [ ] Contactar los negocios piloto.

**Resultado verificable:** aplicación desplegada con un negocio de demostración.

### Día 2 — Acceso y alta

- [ ] Implementar login con Google y sesión persistente.
- [ ] Construir alta guiada del negocio.
- [ ] Configurar zona horaria y permisos.
- [ ] Aplicar aislamiento entre negocios desde el inicio.

**Resultado verificable:** el dueño entra y crea su negocio sin contraseña.

### Día 3 — Servicios y horarios

- [ ] Crear y editar servicios con precio y duración.
- [ ] Configurar profesionales.
- [ ] Definir jornada semanal y descansos.
- [ ] Permitir bloqueos de horarios.
- [ ] Calcular disponibilidad según duración y profesional.

**Resultado verificable:** el dueño configura su semana y ve disponibilidad correcta.

### Día 4 — Reserva pública

- [ ] Construir el flujo servicio → profesional → horario → datos de contacto.
- [ ] Validar disponibilidad en el servidor al guardar.
- [ ] Impedir superposiciones desde la base de datos, incluso con solicitudes simultáneas.
- [ ] Evitar duplicados por reenvío de la misma solicitud.
- [ ] Mostrar estado de reserva e instrucciones claras.

**Resultado verificable:** un cliente solicita un turno desde el celular sin crear cuenta.

### Día 5 — Agenda operativa

- [ ] Crear vista diaria y semanal.
- [ ] Permitir reservas manuales desde el panel.
- [ ] Confirmar, cancelar y reprogramar turnos.
- [ ] Marcar asistencia o ausencia.
- [ ] Incorporar botones de WhatsApp con mensajes prearmados.
- [ ] Crear enlaces privados para gestionar reservas.

**Resultado verificable:** un negocio puede gestionar una jornada completa.

### Día 6 — Señas y cobros

- [ ] Registrar señas por transferencia y validación manual.
- [ ] Configurar vencimiento de reservas pendientes de seña.
- [ ] Mostrar saldo restante.
- [ ] Registrar cobros por efectivo, transferencia y tarjeta.
- [ ] Evitar doble contabilización de señas y cobros.

**Resultado verificable:** una reserva pasa de pendiente a confirmada y luego a pagada sin duplicar cobros.

### Día 7 — Caja y arqueo

- [ ] Registrar apertura de caja.
- [ ] Registrar ingresos, gastos y retiros.
- [ ] Separar movimientos por medio de pago.
- [ ] Registrar efectivo contado al cierre.
- [ ] Calcular diferencia entre efectivo esperado y contado.

**Fórmula:** efectivo esperado = apertura + cobros en efectivo − salidas en efectivo.

**Resultado verificable:** el dueño puede cerrar el día y detectar diferencias.

### Día 8 — Clientes y métricas

- [ ] Mostrar historial de visitas, cancelaciones y ausencias.
- [ ] Mostrar fidelidad mediante cantidad de visitas y fecha de la última.
- [ ] Calcular cumplimiento con reglas explícitas.
- [ ] Permitir corregir registros y conservar autoría de cambios.
- [ ] Mostrar reservas, ausencias y cobros con período definido.

**Resultado verificable:** cada indicador tiene una explicación y coincide con los registros.

### Día 9 — Prueba real y ajustes

- [ ] Probar el circuito completo con 1–2 negocios.
- [ ] Revisar experiencia desde celular.
- [ ] Verificar aislamiento y permisos.
- [ ] Probar reservas simultáneas, cancelaciones y reprogramaciones.
- [ ] Verificar señas, cobros y cierres de caja.
- [ ] Crear backup y comprobar restauración.
- [ ] Corregir errores que impidan operar.

**Resultado verificable:** los negocios completan reserva → asistencia → cobro → cierre.

### Día 10 — Lanzamiento del piloto

- [ ] Incorporar 3–5 negocios.
- [ ] Cargar sus servicios, profesionales y horarios.
- [ ] Entregar guía breve de uso.
- [ ] Activar seguimiento de errores y consumo de infraestructura.
- [ ] Compartir los enlaces públicos de reserva.
- [ ] Definir canal para recibir problemas y comentarios.

**Resultado verificable:** piloto activo con enlaces compartidos por los negocios.

## Historial y score de cumplimiento

Presentarlo como confianza para reservar basada en hechos, no como verificación de identidad ni valoración subjetiva de la calidad de una persona.

Separar:

- **Fidelidad:** cantidad de visitas y fecha de la última.
- **Cumplimiento:** asistencias, cancelaciones tardías y ausencias.

Fórmula inicial propuesta:

```text
Cumplimiento = 100 × asistencias / (asistencias + ausencias + cancelaciones tardías)
```

Reglas:

- Considerar los últimos 180 días.
- Mostrar “Sin historial suficiente” con menos de cinco eventos relevantes, incluido denominador cero.
- Excluir cancelaciones del negocio y cancelaciones del cliente dentro del plazo permitido.
- Definir el plazo de cancelación por negocio y comunicarlo al reservar.
- Mantener historial separado por negocio.
- Permitir correcciones con registro de quién realizó el cambio.
- No bloquear clientes automáticamente por el puntaje.

El dueño puede usar el historial para solicitar confirmación o seña. Ningún puntaje garantiza que no haya ausencias.

## Criterios de aceptación para lanzar

- [ ] Dos clientes no pueden reservar al mismo profesional en horarios superpuestos.
- [ ] Un negocio no puede consultar ni modificar datos de otro.
- [ ] Cancelar o reprogramar libera correctamente la disponibilidad.
- [ ] Las reservas pendientes vencidas liberan el horario según la política definida.
- [ ] Las señas descuentan el saldo y los cobros se contabilizan una sola vez.
- [ ] El arqueo distingue efectivo de transferencias y tarjetas.
- [ ] Los enlaces privados solo permiten gestionar la reserva correspondiente.
- [ ] Existe una copia de seguridad y se comprobó su restauración.
- [ ] El flujo principal funciona desde celular.

## Costos y control de alcance

Objetivo presupuestario inicial: USD 5–15 mensuales de infraestructura para un piloto pequeño, más dominio y correo si corresponde. Es una estimación que debe contrastarse con tarifas y consumo al desplegar, no una tarifa garantizada.

- Empezar con Supabase Free si sus límites resultan suficientes y preparar backups propios para el piloto.
- Usar un único servicio Python y medir consumo.
- Mantener WhatsApp manual, señas por transferencia y confirmación del dueño.
- Evitar infraestructura de microservicios y servicios de IA para el score.

Si aparece un atraso, recortar primero la vista semanal, el puntaje numérico y métricas secundarias. Conservar agenda diaria, historial factual, reservas, cobros y arqueo. El aislamiento de datos y la prevención de turnos duplicados son condiciones de lanzamiento.

## Validación posterior: dos semanas

Medir:

- Tiempo necesario para completar una reserva.
- Reservas completadas frente a intentos iniciados.
- Ausencias sobre turnos que correspondía atender.
- Días de uso del panel por negocio.
- Comentarios sobre fricciones y tareas que todavía se realizan por fuera.
- Disposición a pagar un precio concreto.

Criterio inicial de validación: al menos tres negocios usan el producto de forma sostenida y dos aceptan continuar pagando un precio concreto. Registrar una referencia inicial de ausencias cuando exista; no atribuir una mejora al sistema sin datos suficientes.

## Primer paso de implementación

Comenzar por el día 1: estructura del proyecto, modelo de datos, migraciones y negocio de demostración. Priorizar el circuito completo **reservar → asistir → cobrar → cerrar caja** antes de ampliar funcionalidades.

## Referencias técnicas

- [FastAPI: plantillas](https://fastapi.tiangolo.com/advanced/templates/)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Supabase: configuración SMTP](https://supabase.com/docs/guides/auth/auth-smtp)
- [Precios de Supabase](https://supabase.com/pricing)
- [Precios de Railway](https://railway.com/pricing)

