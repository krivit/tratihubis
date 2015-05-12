-- All trac attachments to link to from a Trac 0.11 / PostgreSQL DB
select    id,     filename,     to_timestamp(time),    author from    attachment order    by id asc
