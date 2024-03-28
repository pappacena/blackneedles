CREATE SCHEMA IF NOT EXISTS __blackneedles__;

CREATE OR REPLACE PROCEDURE __blackneedles__.list_services (database_name string)
    RETURNS TABLE ()
    LANGUAGE sql
    as $$
DECLARE
    res RESULTSET;
BEGIN
    res := (SHOW SERVICES IN DATABASE identifier(:database_name));
    RETURN TABLE(res);
END;
$$
;