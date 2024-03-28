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

-- CALL check_status('service_name')
CREATE OR REPLACE PROCEDURE __blackneedles__.check_status (service_name varchar)
    RETURNS string
    LANGUAGE sql
    as $$
BEGIN
    RETURN (SELECT SYSTEM$GET_SERVICE_STATUS(:service_name, '0') AS STATUS);
END;
$$
;


-- CALL get_service_spec('service_name')
CREATE OR REPLACE PROCEDURE __blackneedles__.describe_service (service_name varchar)
    RETURNS TABLE ()
    LANGUAGE sql
    as $$
DECLARE
    res RESULTSET;
BEGIN
    res := (DESCRIBE SERVICE identifier(:service_name));
    RETURN TABLE(res);
END;
$$
;
