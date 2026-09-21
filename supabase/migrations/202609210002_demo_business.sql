insert into public.businesses (id, name, timezone)
values ('11111111-1111-1111-1111-111111111111', 'Studio Demo', 'America/Montevideo');

insert into public.professionals (id, business_id, display_name)
values ('22222222-2222-2222-2222-222222222222', '11111111-1111-1111-1111-111111111111', 'Sofía');

insert into public.services (id, business_id, name, duration_minutes, price_cents)
values
  ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111', 'Manicura', 60, 120000),
  ('44444444-4444-4444-4444-444444444444', '11111111-1111-1111-1111-111111111111', 'Corte de cabello', 45, 95000);
