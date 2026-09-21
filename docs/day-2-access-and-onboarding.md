# Día 2 — Acceso y alta del negocio

## Implementado en el repositorio

- Pantalla pública de bienvenida y alta inicial.
- Inicio de sesión con Google mediante Supabase Auth.
- Creación de negocio por una función SQL con `security definer`: el usuario autenticado queda como `owner` de su propio negocio.
- Políticas RLS que aíslan los datos operativos por `business_id`.

## Configuración pendiente en servicios externos

1. Ejecutar las migraciones SQL en Supabase, en orden (`001`, `002`, `003`).
2. En Supabase, habilitar Google en Authentication → Sign In / Providers.
3. En Google Cloud, crear el cliente OAuth y usar como URL de redirección la que indica Supabase para el proveedor Google.
4. En Render, cargar `SUPABASE_URL` y `SUPABASE_ANON_KEY` desde Supabase → Connect → API Keys.

La clave `SUPABASE_SERVICE_ROLE_KEY` no se utiliza en el navegador ni debe publicarse en el repositorio.
