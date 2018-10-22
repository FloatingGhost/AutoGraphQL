# AutoGQL
### Create a graphql endpoint from any DB

A utility function and inbuilt Flask server for generating a graphQL
schema from an existing SQL database. It uses SQLAlchemy's automap api
to extract tables and relationships and them maps them to a graphQL schema.

Note: the automap api heavily relies on foreign key constraints to figure
out relationships between tables, so make sure your schema is nice and well-built

## Usage

Provide the script with a database connection string and one or many
table names to have as "top-level" types.

```
python3 app.py
usage: app.py [-h] db top_level [top_level ...]

positional arguments:
  db          Database connection string
  top_level   Top level field names
```

`python3 app.py mysql://localhost/misp events`
