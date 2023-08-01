# Started from

https://github.com/testdrivenio/fastapi-tortoise-aerich

# Modified to use Podman and it does not work!

    podman exec container_fastapi_aerich_1 aerich init-db
    BASE_DIR
    /app
    aerich db >>> mysql://pythonuser:pythonuser@0.0.0.0:3306/dev
    Inited models already, or delete migrations/models and try again.
    Traceback (most recent call last):
      File "/env/bin/aerich", line 8, in <module>
        sys.exit(main())
      File "/env/lib/python3.10/site-packages/aerich/cli.py", line 265, in main
        cli()
      File "/env/lib/python3.10/site-packages/click/core.py", line 1157, in __call__
        return self.main(*args, **kwargs)
      File "/env/lib/python3.10/site-packages/click/core.py", line 1078, in main
        rv = self.invoke(ctx)
      File "/env/lib/python3.10/site-packages/click/core.py", line 1688, in invoke
        return _process_result(sub_ctx.command.invoke(sub_ctx))
      File "/env/lib/python3.10/site-packages/click/core.py", line 1434, in invoke
        return ctx.invoke(self.callback, **ctx.params)
      File "/env/lib/python3.10/site-packages/click/core.py", line 783, in invoke
        return __callback(*args, **kwargs)
      File "/env/lib/python3.10/site-packages/click/decorators.py", line 33, in new_func
        return f(get_current_context(), *args, **kwargs)
      File "/env/lib/python3.10/site-packages/aerich/cli.py", line 34, in wrapper
        loop.run_until_complete(Tortoise.close_connections())
      File "/usr/local/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
        return future.result()
      File "/env/lib/python3.10/site-packages/tortoise/__init__.py", line 615, in close_connections
        await connections.close_all()
      File "/env/lib/python3.10/site-packages/tortoise/connection.py", line 188, in close_all
        tasks = [conn.close() for conn in self.all()]
      File "/env/lib/python3.10/site-packages/tortoise/connection.py", line 177, in all
        return [self.get(alias) for alias in self.db_config]
      File "/env/lib/python3.10/site-packages/tortoise/connection.py", line 48, in db_config
        raise ConfigurationError(
    tortoise.exceptions.ConfigurationError: DB configuration not initialised. Make sure to call Tortoise.init with a valid configuration before attempting to create connections.

# FastAPI + Tortoise-ORM + Aerich

Quick example of FastAPI with Tortoise and Aerich (for migration support).

## Quick Start

Build the image and spin up the `web` (FastAPI + Uvicorn) and `web-db` (Postgres) containers:

```sh
$ docker-compose up -d --build
```

Ensure [http://localhost:8002/ping](http://localhost:8002/ping) works:

```json
{
    "ping": "pong!"
}
```

Init Aerich:

```sh
$ docker-compose exec web aerich init -t db.TORTOISE_ORM
```

Create the first migration and apply it to the database:

```sh
$ docker-compose exec web aerich init-db
```

## Create Migration

Make a change to the model. Then, run:

```
$ docker-compose exec web aerich migrate
$ docker-compose exec web aerich upgrade
```

## Postgres

Want to access the database via psql?

```sh
$ docker-compose exec web-db psql -U postgres
```

Then, you can connect to the database and run SQL queries. For example:

```sh
# \c web
# select * from event;
```
