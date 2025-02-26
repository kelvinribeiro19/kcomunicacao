-- Create a table for user profiles
create table profiles (
    id uuid references auth.users on delete cascade primary key,
    name text,
    email text unique,
    department text,
    role text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Enable Row Level Security (RLS)
alter table profiles enable row level security;

-- Create policy to allow users to view their own profile
create policy "Users can view own profile"
    on profiles for select
    using ( auth.uid() = id );

-- Create policy to allow users to update their own profile
create policy "Users can update own profile"
    on profiles for update
    using ( auth.uid() = id );

-- Create a secure function to handle new user creation
create function public.handle_new_user() 
returns trigger as $$
begin
    insert into public.profiles (id, email)
    values (new.id, new.email);
    return new;
end;
$$ language plpgsql security definer;

-- Trigger the function every time a user is created
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();
