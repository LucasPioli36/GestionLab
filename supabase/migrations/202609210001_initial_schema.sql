create extension if not exists btree_gist;

create type public.member_role as enum ('owner', 'staff');
create type public.reservation_status as enum ('pending', 'confirmed', 'cancelled', 'completed', 'no_show', 'expired');

create table public.businesses (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(trim(name)) between 2 and 120),
  timezone text not null default 'America/Montevideo',
  created_at timestamptz not null default now()
);

create table public.business_members (
  business_id uuid not null references public.businesses(id) on delete cascade,
  user_id uuid not null,
  role public.member_role not null default 'staff',
  created_at timestamptz not null default now(),
  primary key (business_id, user_id)
);

create table public.professionals (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  display_name text not null check (char_length(trim(display_name)) between 2 and 100),
  active boolean not null default true,
  created_at timestamptz not null default now(),
  unique (id, business_id)
);

create table public.services (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  name text not null check (char_length(trim(name)) between 2 and 120),
  duration_minutes integer not null check (duration_minutes between 5 and 720),
  price_cents integer not null check (price_cents >= 0),
  active boolean not null default true,
  created_at timestamptz not null default now(),
  unique (id, business_id)
);

create table public.clients (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  full_name text not null check (char_length(trim(full_name)) between 2 and 160),
  phone text not null check (char_length(trim(phone)) between 6 and 32),
  created_at timestamptz not null default now(),
  unique (business_id, phone), unique (id, business_id)
);

create table public.reservations (
  id uuid primary key default gen_random_uuid(),
  business_id uuid not null references public.businesses(id) on delete cascade,
  professional_id uuid not null,
  service_id uuid not null,
  client_id uuid not null,
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  status public.reservation_status not null default 'pending',
  public_request_key uuid,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (ends_at > starts_at),
  foreign key (professional_id, business_id) references public.professionals (id, business_id),
  foreign key (service_id, business_id) references public.services (id, business_id),
  foreign key (client_id, business_id) references public.clients (id, business_id)
);

create unique index reservations_public_request_key_unique on public.reservations (business_id, public_request_key) where public_request_key is not null;
alter table public.reservations add constraint reservations_no_active_professional_overlap
  exclude using gist (professional_id with =, tstzrange(starts_at, ends_at, '[)') with &&)
  where (status in ('pending', 'confirmed'));

create table public.reservation_events (
  id uuid primary key default gen_random_uuid(),
  reservation_id uuid not null references public.reservations(id) on delete cascade,
  business_id uuid not null references public.businesses(id) on delete cascade,
  previous_status public.reservation_status,
  next_status public.reservation_status not null,
  actor_user_id uuid,
  note text,
  created_at timestamptz not null default now()
);

create index reservations_business_starts_at_idx on public.reservations (business_id, starts_at);
create index reservation_events_reservation_id_idx on public.reservation_events (reservation_id, created_at);

alter table public.businesses enable row level security;
alter table public.business_members enable row level security;
alter table public.professionals enable row level security;
alter table public.services enable row level security;
alter table public.clients enable row level security;
alter table public.reservations enable row level security;
alter table public.reservation_events enable row level security;
