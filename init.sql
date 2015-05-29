/* The main table. Stores all the rooftops. */
create table rooftops (
    id serial primary key,
    shape geometry not null,
    sunlight real
);

