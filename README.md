# Django Drifter Project

## Overview

The Drifter project provides custom Django management commands to
manage database migrations. It includes commands to revert and redo
migrations for a specified app or the entire project.

These commands are most useful during development and so cannot be
run in production (`DEBUG = False`).

## Features

- **Revert Migration**: Reverts one or more migrations, optionally for a specified app.
- **Redo Migration**: Reverts and re-applies the last migration, optionally for a specified app.
- **Reset Database**: Drops all tables and runs all migrations.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/kennethlove/django-dtrifter.git
   cd django-drifter
   ```

2. Install the required dependencies:
   ```sh
   pip install .
   ```
   
3. Add `migrator` to the `INSTALLED_APPS` setting in your Django project's `settings.py` file:
   ```python
   INSTALLED_APPS = [
       ...,
       "drifter",
   ]
   ```

## Usage

### Revert Migration

The `revert_migration` command reverts the last migration for a specified app.

```sh
python manage.py revert_migration [app_name] [--num N]
```

- `app_name`: The name of the app whose migration you want to revert.
- `--num N`: (Optional) The number of migrations to revert. Defaults to 1.

### Redo Migration

The `redo_migration` command undoes and redoes the last migration for a specified app.

```sh
python manage.py redo_migration [--app app_name]
```

- `--app app_name`: (Optional) The name of the app whose migration you want to redo.
 
### Reset Database

The `reset_database` command drops all tables and runs all migrations.

```sh
python manage.py reset_database [--yes]
```

- `--yes`: (Optional) Skips the confirmation prompt.

## Running Tests

Before running the tests, start a local Postgres database:

```shell
docker run --name drifter-postgres -e POSTGRES_USER=django -e POSTGRES_PASSWORD=django -p 5432:5432 -d polls
```

To run the tests, use the following command:

```sh
pytest
```

## Example

### Revert Migration Example

```sh
python manage.py revert_migration polls --num 2
```

This command reverts the last two migrations for the `polls` app.

### Redo Migration Example

```sh
python manage.py redo_migration --app polls
```

This command redoes the last migration for the `polls` app.

### Reset Database Example

```sh
python manage.py reset_database
```

This command drops all tables and runs all migrations.

## Contributing

Contributions are more than welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more details.