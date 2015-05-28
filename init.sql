create table rooftops (
    id serial primary key,
    shape geometry not null,
    sunlight real
);

