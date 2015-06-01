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
