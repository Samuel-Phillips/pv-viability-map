/* The role that sunlight will log in as. */
create role sunlight with password 'H3YCOOLK1D1STH1SYOU' login;
/* The main table. Stores all the rooftops. */
create table rooftops (
    id serial primary key,
    shape geometry not null,
    building_area real,
    useable_build_area real,
    percent_usable real,
    kwhs real,
    system_size_kw real,
    savings integer
);
grant all privileges on table rooftops to sunlight;
