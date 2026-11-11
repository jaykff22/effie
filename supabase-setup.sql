-- IELTS Notes: per-user learning progress
-- Run once in Supabase Dashboard → SQL Editor → New query.
create table if not exists public.learning_progress (
  user_id uuid not null references auth.users(id) on delete cascade,
  resource_id text not null,
  completed boolean not null default false,
  updated_at timestamptz not null default now(),
  primary key (user_id, resource_id)
);

alter table public.learning_progress enable row level security;

create policy "Users can read their own progress"
  on public.learning_progress for select to authenticated
  using ((select auth.uid()) = user_id);

create policy "Users can insert their own progress"
  on public.learning_progress for insert to authenticated
  with check ((select auth.uid()) = user_id);

create policy "Users can update their own progress"
  on public.learning_progress for update to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

create policy "Users can delete their own progress"
  on public.learning_progress for delete to authenticated
  using ((select auth.uid()) = user_id);
