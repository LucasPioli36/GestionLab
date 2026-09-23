# Agenda MVP

Base del MVP para negocios de uñas y peluquerías. Incluye la definición funcional del Día 1, un esquema inicial para Supabase/PostgreSQL, una aplicación FastAPI mínima y datos de demostración.

## Roadmap

El plan completo de implementación está disponible en [ROADMAP_MVP_10_DIAS.md](ROADMAP_MVP_10_DIAS.md).

## Ejecutar localmente

1. Crear un entorno virtual con Python 3.12.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Copiar `.env.example` a `.env` y completar las variables de Supabase si se quiere conectar una base real.
4. Ejecutar `uvicorn app.main:app --reload`.
5. Abrir `http://127.0.0.1:8000/health`.

## Contenido del Día 1

- `docs/day-1-scope.md`: pantallas, reglas de reserva y decisiones de alcance.
- `docs/data-model.md`: entidades, relaciones y estados de reserva.
- `supabase/migrations/`: migración SQL inicial y datos de demostración.
- `app/`: servicio FastAPI inicial, listo para crecer en los próximos días.
- `tests/`: pruebas del dominio de reservas.

## Próximo paso

Crear un proyecto de Supabase, ejecutar las migraciones en orden y configurar las variables de entorno. El despliegue queda preparado mediante `railway.toml`, pero requiere vincular una cuenta y un proyecto de Railway.
