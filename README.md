# Blackneedles

Blackneedles a simple and easy to use python library and command line tool to manage and bring observability to Snowflake Snowpark Container Services and Snowflake Native Apps.

The name comes from the Black Needles Peak (Pico das Agulhas Negras), the highest mountain in the state of Rio de Janeiro, Brazil, and only place in the state where one can see snowflakes.

## Installation

```bash
pip install blackneedles
```

## Usage

To use either the library or the command line tool, you need to have a Snowflake configurations at `~/.snowsql/config` or set the environment variables `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`.

If you want to connect to Snowflake Container Services, you must set `SNOWFLAKE_DATABASE` to your database name.When using it on Native App, you must set `SNOWFLAKE_DATABASE` to the native app name.

In either way, you must install the support procedures and functions in your database or native app. You can do that by running the following command:

```bash
SNOWFLAKE_DATABASE=your_database_or_native_app blackneedles install
```

This will install the necessary procedures and functions in a `__blacknedlles__` schema. To remove everything, you just need to drop this schema from the database.

If you are installing this in a Native App, you must also grant the necessary privileges to the role that will be using the library. You can do that by running the following command:

```bash
SNOWFLAKE_DATABASE=your_database_or_native_app blackneedles install --grant <your_application_role>
```