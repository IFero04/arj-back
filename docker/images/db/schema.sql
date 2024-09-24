CREATE DATABASE arj;
\c arj;

-- Create user for the API with password from environment variable
CREATE USER api WITH PASSWORD 'api';

-- Create necessary extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
