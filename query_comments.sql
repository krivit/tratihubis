-- All Trac ticket comments to convert from a Trac 0.11 / PostgreSQL DB
select    ticket,  to_timestamp(time), author,    newvalue from    ticket_change where    field = 'comment'    and newvalue <> '' order    by ticket, time
