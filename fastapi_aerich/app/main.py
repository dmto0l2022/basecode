
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_crudrouter.core.tortoise import TortoiseCRUDRouter
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields, Tortoise

#TORTOISE_ORM = {
#    "connections": {"default": 'mysql://pythonuser:pythonuser@container_mariadb:3306/dev'},
#    "apps": {
#        "models": {
#            "models": ["models", "aerich.models"],
#            "default_connection": "default",
#        },
#    },
#}

TORTOISE_ORM = {
    "connections": {"default": 'mysql://pythonuser:pythonuser@0.0.0.0:3306/dev'},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# Create Database Tables
async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

app = FastAPI()
register_tortoise(app, config=TORTOISE_ORM)


# Tortoise ORM Model
class TestModel(Model):
    test = fields.IntField(null=False, description=f"Test value")
    ts = fields.IntField(null=False, description=f"Epoch time")


# Pydantic schema
TestSchema = pydantic_model_creator(TestModel, name=f"{TestModel.__name__}Schema")
TestSchemaCreate = pydantic_model_creator(TestModel, name=f"{TestModel.__name__}SchemaCreate", exclude_readonly=True)

# Make your FastAPI Router from your Pydantic schema and Tortoise Model
router = TortoiseCRUDRouter(
    schema=TestSchema,
    create_schema=TestSchemaCreate,
    db_model=TestModel,
    prefix="test"
)

# Add it to your app
app.include_router(router)
