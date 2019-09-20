# RunSQL - A Pandoc filter to execute SQL queries

A pandoc filter to execute and collect the results of SQL queries.

## Syntax

Regular queries where you expect it to return a table should be formatted as
such:

```sql
~~~runsql
SELECT * FROM table;
~~~
```

If wish to update, delete or perform other operations that does not return a
table, you need to specify that there are no results.

```sql
~~~runsql
no_result: True
---
DELETE FROM table;
~~~
```

## Usage

If `runsql.py` is in the same folder:

```bash
pandoc --filter ./runsql.py test.md -o test.pdf
```

If `runsql.py` is installed to a directory in `$PATH`:

```bash
pandoc --filter runsql.py test.md -o test.pdf
```

## Configuration

The filter fetches it's configuration from the environment through:

- `MYSQL_HOST`: Hostname to the SQL server (default `localhost`)
- `MYSQL_USER`: Username of the SQL user (default `root`)
- `MYSQL_PASSWORD`: Password of the SQL user (default `secret`)
- `MYSQL_DATABASE`: Database to perform queries to (default `trlog`)

## Example

See `test.md` and the generated `test.pdf` files for an example.
