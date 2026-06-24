CREATE DATABASE IF NOT EXISTS sandbox;

CREATE TABLE IF NOT EXISTS sandbox.countries (
    id LONG,
    country STRING,
    capital STRING
) USING DELTA;
