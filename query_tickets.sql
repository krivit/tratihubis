-- All Trac tickets to convert from a Trac 0.11 / PostgreSQL DB
select    id,    type,    owner,    reporter,    milestone,    status,    resolution,    summary,    description,    to_timestamp(time),    to_timestamp(changetime),    component, priority, keywords, cc from    ticket order    by id
