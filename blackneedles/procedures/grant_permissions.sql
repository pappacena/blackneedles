GRANT USAGE ON PROCEDURE __blackneedles__.list_services (string) TO {grant_target};
GRANT USAGE ON PROCEDURE __blackneedles__.check_status (varchar) TO {grant_target};
GRANT USAGE ON PROCEDURE __blackneedles__.describe_service (varchar) TO {grant_target};
GRANT USAGE ON PROCEDURE __blackneedles__.alter_service (varchar, varchar) TO {grant_target};
GRANT USAGE ON PROCEDURE __blackneedles__.get_service_logs (varchar, varchar, varchar) TO {grant_target};