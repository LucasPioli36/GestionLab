-- Día 2: acceso del dueño y alta aislada por negocio.
-- Se ejecuta después de 202609210001_initial_schema.sql.

create or replace function public.is_business_member(target_business_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.business_members
    where business_id = target_business_id
      and user_id = auth.uid()
  );
$$;

create or replace function public.create_business(business_name text, business_timezone text default 'America/Montevideo')
returns public.businesses
language plpgsql
security definer
set search_path = public
as $$
declare
  new_business public.businesses;
begin
  if auth.uid() is null then
    raise exception 'Debes iniciar sesión para crear un negocio.';
  end if;

  insert into public.businesses (name, timezone)
  values (trim(business_name), business_timezone)
  returning * into new_business;

  insert into public.business_members (business_id, user_id, role)
  values (new_business.id, auth.uid(), 'owner');

  return new_business;
end;
$$;

revoke all on function public.is_business_member(uuid) from public;
grant execute on function public.is_business_member(uuid) to authenticated;
revoke all on function public.create_business(text, text) from public;
grant execute on function public.create_business(text, text) to authenticated;

create policy "members can read their businesses"
  on public.businesses for select to authenticated
  using (public.is_business_member(id));

create policy "users can read their own memberships"
  on public.business_members for select to authenticated
  using (user_id = auth.uid());

create policy "members can manage professionals"
  on public.professionals for all to authenticated
  using (public.is_business_member(business_id))
  with check (public.is_business_member(business_id));

create policy "members can manage services"
  on public.services for all to authenticated
  using (public.is_business_member(business_id))
  with check (public.is_business_member(business_id));

create policy "members can manage clients"
  on public.clients for all to authenticated
  using (public.is_business_member(business_id))
  with check (public.is_business_member(business_id));

create policy "members can manage reservations"
  on public.reservations for all to authenticated
  using (public.is_business_member(business_id))
  with check (public.is_business_member(business_id));

create policy "members can read reservation events"
  on public.reservation_events for select to authenticated
  using (public.is_business_member(business_id));
