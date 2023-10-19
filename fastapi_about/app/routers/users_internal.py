from fastapi import Depends, FastAPI, Request, Response, HTTPException, Header
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from functools import wraps

import uuid

from fastapi import APIRouter
router = APIRouter()

api_base_url = '/dmtool/fastapi_about/internal/about/'

from typing import List
from typing import Annotated

from db import get_session

#from models.models import Song, SongCreate
from models.users import User, UserCreate
from models.users import User_permission, User_permissionCreate
from models.users import User_api_key, User_api_keyCreate, User_api_keyUpdate

from datetime import datetime
#1980-01-01 00:00:00.000
unceased_datetime_str = '01/01/1980 00:00:00'
unceased_datetime_object = datetime.strptime(unceased_datetime_str, '%d/%m/%Y %H:%M:%S')

import rsa

# Users

## Fields
#authlib_id
#authlib_provider
#created_at
#modified_at
#ceased_at

## who are you

@router.get(api_base_url + "whoareyou_request")
async def whoareyou(request: Request):
    my_header = request.headers
    return {"message": my_header}

'''
@router.get(api_base_url + "whoareyou_response")
async def whoareyou(response: Response):
    my_header = response.headers
    return {"message": my_header}


@router.get(api_base_url + "whoareyou_response")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    my_header = response.headers
    return {"message": my_header}

'''

'''
def decor(f):
    async def _fn():
        starttime = time.time()
        await f()
        print(
            "child function run time is ",
            (time.time() - starttime) * 1000,
            "ms",
        )

    return _fn

https://www.sitepoint.com/understanding-python-decorators/

def multiply_numbers(func):
    def multiply_two_numbers(num1, num2):
        print("we're multiplying two number {} and {}".format(num1, num2))
        return func(num1, num2)
        
    return multiply_two_numbers

@multiply_numbers
def multiply_two_given_numbers(num1, num2):
    return f'{num1} * {num2} = {num1 * num2}'
    
print(multiply_two_given_numbers(3, 4))
 >>>
we're multiplying two number 3 and 4
3 * 4 = 12

--------------------------------------


def decorator_func(decorated_func):
    def wrapper_func(*args, **kwargs):
        print(f'there are {len(args)} positional arguments and {len(kwargs)} keyword arguments')
        return decorated_func(*args, **kwargs)
        
    return wrapper_func

@decorator_func
def names_and_age(age1, age2, name1='Ben', name2='Harry'):
    return f'{name1} is {age1} yrs old and {name2} is {age2} yrs old'
    
print(names_and_age(12, 15, name1="Lily", name2="Ola"))
>>>
There are 2 positional arguments and 2 keyword arguments
Lily is 12 yrs old and Ola is 15 yrs old


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper


@app.post("/")
@auth_required # Custom decorator
async def root(payload: SampleModel):
    return {"message": "Hello World", "payload": payload}

The main caveat of this method is that you can't access the request object in the wrapper and I assume it is your primary intention.

If you need to access the request, you must add the argument to the router function as,

from fastapi import Request


@app.post("/")
@auth_required  # Custom decorator
async def root(request: Request, payload: SampleModel):
    return {"message": "Hello World", "payload": payload}

'''

'''

async def check_api_key():
        print("hello from decorator")
        ## check api key existence
        #dmtool_user_int = int(dmtool_userid)
        statement = select(User_api_key).where(User_api_key.user_id == dmtool_userid).where(User_api_key.api_key == dmtool_apikey) ## and User_api_key.ceased_at==unceased_datetime_object)
        # print("statement >>>>>>>>>>>>>>>>" , str(statement))
        #try:
        user_api_keys = await session.exec(statement)
        user_api_key = user_api_keys.one()
        return check_api_key
        #except:
        #    raise HTTPException(status_code=404, detail="Unauthorised Request")

'''

'''
def check_api_key_outer(f):
    @fastapi_wraps(f)
    async def check_api_key():
        print("hello from decorator")
        ## check api key existence
        #dmtool_user_int = int(dmtool_userid)
        statement = select(User_api_key).where(User_api_key.user_id == dmtool_userid).where(User_api_key.api_key == dmtool_apikey) ## and User_api_key.ceased_at==unceased_datetime_object)
        # print("statement >>>>>>>>>>>>>>>>" , str(statement))
        #try:
        user_api_keys = await session.exec(statement)
        user_api_key = user_api_keys.one()
        return check_api_key
        #except:
        #    raise HTTPException(status_code=404, detail="Unauthorised Request")
'''

# User CRUD

## get one user with email


@router.get(api_base_url + "user/{email_in}", response_model=User)
async def get_user_by_email(email_in: str, session: AsyncSession = Depends(get_session),
                            dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(User).where(User.email == email_in)
    user = "user unknown"
    try:
        users = await session.exec(statement)
        user = users.one()
    except:
        if user ==  "user unknown":
            user = User(authlib_id="google",
                    authlib_provider="google",
                    email=email_in)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            try:
                users = await session.exec(statement)
                user = users.one()
            except:
                user = "user unknown"
    
    return user


@router.get(api_base_url + "users",response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):

    ## check api key existence
    #dmtool_user_int = int(dmtool_userid)
    statement = select(User_api_key).where(User_api_key.user_id == dmtool_userid).where(User_api_key.api_key == dmtool_apikey).where(User_api_key.ceased_at==unceased_datetime_object)
    # print("statement >>>>>>>>>>>>>>>>" , str(statement))
    try:
        user_api_keys = await session.exec(statement)
        user_api_key = user_api_keys.one()
   
        #    #a = 1
        #if check_api_key(dmtool_userid,dmtool_apikey) == True:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return [User(id=user.id,
                        authlib_id=user.authlib_id,
                        authlib_provider=user.authlib_provider,
                        email=user.email,
                        created_at=user.created_at,
                        modified_at=user.modified_at,
                        ceased_at=user.ceased_at) for user in users]
        #else:
        #    raise HTTPException(status_code=404, detail="Unauthorised Request")
    except:
        raise HTTPException(status_code=404, detail="Unauthorised Request")


@router.post(api_base_url + "user")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    user = User(authlib_id=user.authlib_id,
                authlib_provider=user.authlib_provider,
                email=user.email,
                created_at=user.created_at,
                modified_at=user.modified_at,
                ceased_at=user.ceased_at)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete(api_base_url + "user/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(User).where(User.id == user_id)
    results = await session.exec(statement)
    user = results.one()
    await session.delete(user)
    await session.commit()
    return {"deleted": user}

# User_permission CRUD
## User_permission, User_permissionCreate

# Fields
# id
# user_id
# authorised
# created_at
# modified_at
# ceased_at

@router.get(api_base_url + "user_permission", response_model=list[User])
async def get_user_permission(session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(User_permission))
    user_permissions = result.scalars().all()
    return [User_permission(
        id = user_permission.id,
        user_id = user_permission.user_id,
        authorised = user_permission.authorised,
        created_at = user_permission.created_at,
        modified_at = user_permission.modified_at,
        ceased_at = user_permission.ceased_at
    ) for user_permission in user_permissions]


@router.post(api_base_url + "user_permission")
async def add_user_permission(user_permission: User_permissionCreate, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    user_permission = User_permission(user_id = user_permission.user_id,
        authorised = user_permission.authorised,
        created_at = user_permission.created_at,
        modified_at = user_permission.modified_at,
        ceased_at = user_permission.ceased_at)
    session.add(user_permission)
    await session.commit()
    await session.refresh(user_permission)
    return user_permission

@router.delete(api_base_url + "user_permission/{user_permission_id}")
async def delete_user_permission(user_permission_id: int, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(User_permission).where(User_permission.id == user_permission_id)
    results = await session.exec(statement)
    user_permission = results.one()
    await session.delete(user_permission)
    await session.commit()
    return {"deleted": user_permission}


# User_api_key
## User_api_key, User_api_keyCreate
# Fields
# id
# user_id
# secret_key
# public_key
# created_at
# modified_at
# ceased_at

@router.get(api_base_url + "user_api_keys", response_model=list[User_api_key])
async def get_user_api_keys(session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    result = await session.execute(select(User_api_key))
    user_api_keys = result.scalars().all()
    return [User_api_key(id = user_api_key.id,
                        user_id = user_api_key.user_id,
                        api_key= user_api_key.api_key,
                        encrypted_api_key= user_api_key.encrypted_api_key,
                        private_key = user_api_key.private_key,
                        public_key = user_api_key.public_key,
                        created_at = user_api_key.created_at,
                        modified_at = user_api_key.modified_at,
                        ceased_at = user_api_key.ceased_at
                        ) for user_api_key in user_api_keys]

## get one api key for user

@router.get(api_base_url + "user_api_key/{user_id}", response_model=User_api_key)
async def get_user_api_key(user_id: int, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(User_api_key).where(User_api_key.user_id == user_id)
    user_api_keys = await session.exec(statement)
    user_api_key = user_api_keys.one()
    return user_api_key

## add one api key for user

@router.post(api_base_url + "user_api_key")
async def add_user_api_key(user_api_key: User_api_keyCreate, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    #public_key_gen, private_key_gen = rsa.newkeys(512)
    #print('public_key_gen  >>>' ,public_key_gen)
    #print('private_key_gen  >>>' ,private_key_gen)
    api_key_str = str(uuid.uuid1())
    encrypted_api_key_str = str(uuid.uuid1())
    public_key_gen_str = str(uuid.uuid1())
    private_key_gen_str = str(uuid.uuid1())              
    #encrypted_api_key = rsa.encrypt(api_key_str.encode(),public_key_gen)
    user_api_key = User_api_key(user_id = user_api_key.user_id,
                        api_key = api_key_str,
                        encrypted_api_key = encrypted_api_key_str,
                        public_key = public_key_gen_str,
                        private_key = private_key_gen_str,
                        created_at = datetime.utcnow(),
                        modified_at = datetime.utcnow(),
                        ceased_at = user_api_key.ceased_at)
    session.add(user_api_key)
    await session.commit()
    await session.refresh(user_api_key)
    return user_api_key

## delete one api key

@router.delete(api_base_url + "user_api_key/{user_api_key_id}")
async def delete_user_api_key(user_api_key_id: int, session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None):
    statement = select(User_api_key).where(User_api_key.id == user_api_key_id)
    results = await session.exec(statement)
    user_api_key = results.one()
    await session.delete(user_api_key)
    await session.commit()
    return {"deleted": user_api_key}

'''

## cease record

@router.put(api_base_url + "user_api_key/{user_api_key_id}", response_model=User_api_key)
async def update_user_api_key(user_api_key_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(User_api_key).where(User_api_key.id == user_api_key_id)
    results = session.exec(statement)
    user_api_key = results.one()
    await session.delete(user_api_key)
    await session.commit()
    user_api_key = User_api_key(user_id = user_api_key.user_id,
                        api_key= user_api_key.api_key,
                        encrypted_api_key= user_api_key.encrypted_api_key,
                        private_key = user_api_key.private_key,
                        public_key = user_api_key.public_key,
                        created_at = user_api_key.created_at,
                        modified_at = user_api_key.modified_at,
                        ceased_at = datetime.utcnow())
    session.add(user_api_key)
    await session.commit()
    await session.refresh(user_api_key)
    return user_api_key

@router.get(api_base_url + "users",
            response_model=list[User]
            )
async def get_users(session: AsyncSession = Depends(get_session),
                    dmtool_userid: Annotated[int | None, Header()] = None,
                    dmtool_apikey: Annotated[str | None, Header()] = None):

'''




## update and cease record

@router.post(api_base_url + "user_api_key/{user_api_key_id}", response_model=User_api_key)
async def cease_api_key(user_api_key_id: int, session: AsyncSession = Depends(get_session),
                        dmtool_userid: Annotated[int | None, Header()] = None):

    #statement = select(User_api_key).where(User_api_key.user_id == dmtool_userid).where(User_api_key.api_key == dmtool_apikey).where(User_api_key.ceased_at==unceased_datetime_object)
    # print("statement >>>>>>>>>>>>>>>>" , str(statement))
    #try:
    #user_api_keys = await session.exec(statement)
    #user_api_key = user_api_keys.one()
    
    statement = select(User_api_key).where(User_api_key.id == user_api_key_id).where(User_api_key.user_id == dmtool_userid).where(User_api_key.ceased_at==unceased_datetime_object)
    results = await session.exec(statement)
    user_api = results.one()
    user_api.ceased_at =  datetime.utcnow()
    session.add(user_api)
    await session.commit()
    await session.refresh(user_api)
    return user_api
    #except:
    #    raise HTTPException(status_code=404, detail="Unauthorised Request")
