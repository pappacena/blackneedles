CREATE SCHEMA IF NOT EXISTS __blackneedles__;


-- CALL __blackneedles__.list_sevices('database_name')
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

-- CALL __blackneedles__.check_status('service_name')
CREATE OR REPLACE PROCEDURE __blackneedles__.check_status (service_name varchar)
    RETURNS string
    LANGUAGE sql
    as $$
BEGIN
    RETURN (SELECT SYSTEM$GET_SERVICE_STATUS(:service_name, '0') AS STATUS);
END;
$$
;


-- CALL __blackneedles__.describe_service('service_name')
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


-- CALL __blackneedles__.alter_service('service_name', 'suspended')
CREATE OR REPLACE PROCEDURE __blackneedles__.alter_service (service_name varchar, action varchar)
    RETURNS string
    LANGUAGE sql
    as $$
BEGIN
    LET alter_service_statement string := 'ALTER SERVICE ' || service_name || ' ' || action || ' ;';
    EXECUTE IMMEDIATE alter_service_statement;
    RETURN alter_service_statement;
END;
$$
;


-- CALL __blackneedles__.list_compute_pool(database_name)
CREATE OR REPLACE PROCEDURE __blackneedles__.list_compute_pool ()
    RETURNS TABLE ()
    LANGUAGE sql
    as $$
DECLARE
    res RESULTSET;
BEGIN
    res := (SHOW COMPUTE POOLS);
    RETURN TABLE(res);
END;
$$
;
