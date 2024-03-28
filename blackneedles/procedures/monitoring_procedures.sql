CREATE SCHEMA IF NOT EXISTS __blackneedles__;


-- CALL list_sevices('database_name')
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


-- CALL get_service_status(['service_name1', 'service_name2'])
CREATE OR REPLACE PROCEDURE __blackneedles__.list_services (database_name array)
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

