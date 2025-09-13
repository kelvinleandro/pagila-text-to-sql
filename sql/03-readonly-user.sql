-- Create a read-only user
CREATE USER llm_user WITH PASSWORD 'llm_pwd';

-- Grant read-only access to all tables in the public schema
GRANT CONNECT ON DATABASE pagila TO llm_user;
GRANT USAGE ON SCHEMA public TO llm_user;

-- Grant SELECT privileges on all tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO llm_user;

-- Ensure future tables also grant SELECT
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO llm_user;