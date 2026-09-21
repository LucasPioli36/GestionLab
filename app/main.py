import json
import os
from datetime import datetime
from enum import StrEnum

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class ReservationStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    EXPIRED = "expired"


ALLOWED_TRANSITIONS = {
    ReservationStatus.PENDING: {ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED, ReservationStatus.EXPIRED},
    ReservationStatus.CONFIRMED: {ReservationStatus.CANCELLED, ReservationStatus.COMPLETED, ReservationStatus.NO_SHOW},
    ReservationStatus.CANCELLED: set(),
    ReservationStatus.COMPLETED: set(),
    ReservationStatus.NO_SHOW: set(),
    ReservationStatus.EXPIRED: set(),
}


def can_transition(current: ReservationStatus, target: ReservationStatus) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def overlaps(starts_at: datetime, ends_at: datetime, other_starts_at: datetime, other_ends_at: datetime) -> bool:
    if starts_at >= ends_at or other_starts_at >= other_ends_at:
        raise ValueError("La hora de finalización debe ser posterior a la de inicio.")
    return starts_at < other_ends_at and other_starts_at < ends_at


class HealthResponse(BaseModel):
    status: str
    service: str


class PublicAppConfig(BaseModel):
    auth_enabled: bool
    supabase_url: str | None = None
    supabase_anon_key: str | None = None


def public_app_config() -> PublicAppConfig:
    """Expose only the values designed for browser use.

    The Supabase anonymous key is a public client key; the service-role key is
    intentionally never read or returned by this application.
    """
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    return PublicAppConfig(
        auth_enabled=bool(url and anon_key and "your-project" not in url and anon_key != "replace-me"),
        supabase_url=url,
        supabase_anon_key=anon_key,
    )


app = FastAPI(title="Agenda MVP", version="0.1.0")


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="agenda-mvp")


@app.get("/", tags=["system"])
def root() -> HTMLResponse:
    return HTMLResponse(content=LANDING_PAGE)


@app.get("/app-config", response_model=PublicAppConfig, tags=["system"])
def app_config() -> PublicAppConfig:
    return public_app_config()


LANDING_PAGE = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>GestionLab — Tu agenda, en orden</title>
    <style>
      :root { color-scheme: light; --ink:#18222e; --muted:#697386; --brand:#5b4ce5; --brand-soft:#eeecff; --line:#e5e7eb; --bg:#fbfbfe; }
      * { box-sizing: border-box; } body { margin:0; min-height:100vh; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:radial-gradient(circle at 90% 5%, #e4dfff 0, transparent 24rem), var(--bg); }
      main { width:min(100% - 2rem, 68rem); margin:auto; padding:2.4rem 0 4rem; } .brand { display:flex; align-items:center; gap:.7rem; font-weight:800; letter-spacing:-.04em; } .mark { display:grid; place-items:center; width:2rem; height:2rem; color:white; background:var(--brand); border-radius:.65rem; box-shadow:0 8px 22px #5b4ce540; }
      .hero { display:grid; grid-template-columns:1.15fr .85fr; gap:3rem; align-items:center; padding:5.5rem 0 2rem; } h1 { margin:0 0 1.15rem; max-width:12ch; font-size:clamp(2.65rem, 7vw, 5.3rem); line-height:.98; letter-spacing:-.07em; } .lead { max-width:34rem; color:var(--muted); font-size:1.1rem; line-height:1.6; } .eyebrow { display:inline-block; margin-bottom:1rem; padding:.4rem .7rem; color:#4735bd; background:var(--brand-soft); border-radius:999px; font-size:.84rem; font-weight:700; }
      .card { padding:1.65rem; background:#fff; border:1px solid var(--line); border-radius:1.3rem; box-shadow:0 20px 45px #1b24300d; } h2 { margin:.1rem 0 .5rem; font-size:1.45rem; letter-spacing:-.04em; } .card p { color:var(--muted); line-height:1.5; } button { width:100%; margin-top:1rem; padding:.82rem 1rem; border:0; border-radius:.7rem; background:var(--brand); color:white; font:inherit; font-weight:700; cursor:pointer; } button:hover { background:#493bc9; } button:disabled { cursor:not-allowed; background:#aaa6d8; } form { display:grid; gap:.85rem; margin-top:1.25rem; } label { display:grid; gap:.35rem; font-size:.9rem; font-weight:650; } input, select { padding:.74rem .8rem; color:var(--ink); background:white; border:1px solid #cfd4dd; border-radius:.65rem; font:inherit; } .hidden { display:none; } .notice { min-height:1.4rem; margin:.9rem 0 0; color:var(--muted); font-size:.9rem; line-height:1.45; } .error { color:#b42318; } .success { color:#067647; } .steps { display:grid; grid-template-columns:repeat(3, 1fr); gap:1rem; margin-top:3.5rem; } .step { padding:1rem 0; border-top:2px solid var(--line); color:var(--muted); } .step strong { display:block; margin:.7rem 0 .25rem; color:var(--ink); } .num { color:var(--brand); font-weight:800; }
      @media (max-width: 700px) { main { padding-top:1.5rem; } .hero { grid-template-columns:1fr; gap:2rem; padding-top:3.5rem; } .steps { grid-template-columns:1fr; margin-top:2.5rem; } }
    </style>
  </head>
  <body>
    <main>
      <div class="brand"><span class="mark">G</span> GestionLab</div>
      <section class="hero">
        <div>
          <span class="eyebrow">Agenda simple para tu negocio</span>
          <h1>Menos mensajes. Más tiempo para atender.</h1>
          <p class="lead">Organizá reservas, clientes y tu jornada desde un solo lugar. Empezá creando el espacio de tu negocio.</p>
        </div>
        <section class="card" aria-live="polite">
          <div id="signed-out">
            <h2>Empezá con tu cuenta</h2>
            <p>Entrá con Google para crear y administrar tu negocio.</p>
            <button id="google-login" type="button">Continuar con Google</button>
          </div>
          <div id="signed-in" class="hidden">
            <h2>Creá tu negocio</h2>
            <p id="welcome"></p>
            <form id="business-form">
              <label>Nombre del negocio <input id="business-name" name="business-name" minlength="2" maxlength="120" required placeholder="Ej.: Estudio Valentina" /></label>
              <label>Zona horaria <select id="timezone" name="timezone"><option value="America/Montevideo">Montevideo (GMT-3)</option><option value="America/Argentina/Buenos_Aires">Buenos Aires (GMT-3)</option><option value="America/Santiago">Santiago (GMT-4)</option></select></label>
              <button type="submit">Crear mi negocio</button>
            </form>
          </div>
          <p id="notice" class="notice"></p>
        </section>
      </section>
      <section class="steps" aria-label="Cómo funciona">
        <div class="step"><span class="num">01</span><strong>Ingresás con Google</strong>Tu cuenta es la llave de tu negocio.</div>
        <div class="step"><span class="num">02</span><strong>Creás tu espacio</strong>Elegís el nombre y la zona horaria.</div>
        <div class="step"><span class="num">03</span><strong>Configurás tu agenda</strong>Luego sumás servicios, profesionales y horarios.</div>
      </section>
    </main>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script>
      const signedOut = document.querySelector('#signed-out');
      const signedIn = document.querySelector('#signed-in');
      const notice = document.querySelector('#notice');
      const loginButton = document.querySelector('#google-login');
      const form = document.querySelector('#business-form');
      let supabase;
      const showNotice = (message, type = '') => { notice.textContent = message; notice.className = `notice ${type}`; };
      const showSession = (session) => {
        signedOut.classList.add('hidden'); signedIn.classList.remove('hidden');
        document.querySelector('#welcome').textContent = `Hola${session.user.email ? `, ${session.user.email}` : ''}. Este será tu primer paso.`;
      };
      (async () => {
        const config = await fetch('/app-config').then((response) => response.json());
        if (!config.auth_enabled) {
          loginButton.disabled = true;
          showNotice('El acceso con Google se está configurando. Volvé a intentar en unos minutos.');
          return;
        }
        supabase = window.supabase.createClient(config.supabase_url, config.supabase_anon_key);
        const { data: { session } } = await supabase.auth.getSession();
        if (session) showSession(session);
        loginButton.addEventListener('click', async () => {
          const { error } = await supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: window.location.origin } });
          if (error) showNotice(error.message, 'error');
        });
        form.addEventListener('submit', async (event) => {
          event.preventDefault();
          const name = document.querySelector('#business-name').value.trim();
          const timezone = document.querySelector('#timezone').value;
          const { error } = await supabase.rpc('create_business', { business_name: name, business_timezone: timezone });
          if (error) { showNotice(error.message, 'error'); return; }
          form.reset(); showNotice('¡Listo! Tu negocio fue creado. El próximo paso será definir tus servicios y horarios.', 'success');
        });
      })().catch(() => showNotice('No pudimos iniciar la configuración. Actualizá la página e intentá de nuevo.', 'error'));
    </script>
  </body>
</html>"""
