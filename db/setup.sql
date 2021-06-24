-- noinspection SqlNoDataSourceInspectionForFile

\set ON_ERROR_STOP on

-- Procedure that updates the changed_at column
CREATE OR REPLACE FUNCTION update_modified_at()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.modified_at = NOW();
  RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TYPE enum_post_status AS ENUM
(
  'published',
  'hidden'
);

CREATE TABLE users
(
  user_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  username VARCHAR(64) NOT NULL,
  email VARCHAR(120) NOT NULL,
  password_hash VARCHAR(128) NOT NULL,
  last_seen TIMESTAMP WITH TIME ZONE,
  token VARCHAR(32),
  token_expiration TIMESTAMP WITH TIME ZONE
);
CREATE UNIQUE INDEX users_username_idx ON users (username);
CREATE UNIQUE INDEX users_email_idx ON users (email);
CREATE UNIQUE INDEX users_token_idx ON users (token);
CREATE TRIGGER update_user_modified_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE PROCEDURE update_modified_at();

CREATE TABLE posts
(
  post_id SERIAL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  modified_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  status enum_post_status NOT NULL DEFAULT 'hidden',
  published_at TIMESTAMP WITH TIME ZONE,
  subject TEXT NOT NULL,
  body TEXT,
  user_id INTEGER REFERENCES users(user_id)
);
CREATE TRIGGER update_post_modified_at
  BEFORE UPDATE ON posts
  FOR EACH ROW EXECUTE PROCEDURE update_modified_at();

INSERT INTO 
  posts (status, published_at, subject, body)
VALUES
  ('published', NOW(), 'This is post number one', 'This is the body of post number one'),
  ('published', NOW(), 'This is post number two', 'This is the body of post number two'),
  ('published', NOW(), 'This is post number three', 'This is the body of post number three'),
  ('hidden', NULL, 'This is post number four', 'This is the body of post number four, this is hidden'),
  ('published', NOW(), 'This is post number five', 'This is the body of post number five'),
  ('published', NOW(), 'This is post number six', 'This is the body of post number six'),
  ('published', NOW(), 'This is post number seven', 'This is the body of post number seven');
