### HOW TO SET UP

## Requirements

1. PostgreSQL as s DB

## Init DB

1. First of all create a DB called skeleton

Run the command in `psql` CLI
```bash
create user skeleton with password 'skeleton';
create database skeleton with owner=skeleton;
```

2. Run yoyo migration:
```bash
yoyo apply --database postgresql://skeleton:skeleton@localhost/skeleton  service/core/migrations/
```

## Development

**Do not drop database to reaply SQL initial script!**

Use:
```bash
select 'drop table if exists "' || tablename || '";' 
from pg_tables
where schemaname = 'public'; -- or any other schema
```

It will give you much more flexibility.
As a result you will get multiple commands to execute to drop just tables.
After that just apply migration again.

OR just use truncate during testing...
