# Beginnings

https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_8_3

# Hope to expose server to web

https://madvirus.hashnode.dev/securing-your-fastapi-with-api-key-authentication-a-step-by-step-guide

https://joshdimella.com/blog/adding-api-key-auth-to-fast-api

# Use aerich in application

You can use aerich out of cli by use Command class.

from aerich import Command

command = Command(tortoise_config=config, app='models')
await command.init()
await command.migrate('test')
