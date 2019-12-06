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