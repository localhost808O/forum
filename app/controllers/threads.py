from venv import create
from aiohttp import web

from jsonschema import validate
from json import dumps
from utils.access_key import jwt_expired, get_jwt_dec
import jwt

from db import db
from models.thread import Thread
from models.message import Message
from models.profile import Profile
from models.user import User

from utils.secret_key import secret_key

schema = {
    "type" : "object",
    "properties" : {
        "jwt" : {"type" : "string"},
        "name" : {"type" : "string"},
    },
}
routes = web.RouteTableDef()

@routes.post('/api/threads/')
async def create_thread(request):
    # парсим json, валидируем 
    json_input = await request.json()
    error = validate(json_input, schema)
    if error: 
        web.Response(text=error)
    jwt_dec = get_jwt_dec(json_input['jwt']) 
    if not jwt_dec:
        error = dumps({"error":"wrong token"})
        return web.Response(text=error)
    # проверка досутпа jwt
    if jwt_expired(jwt_dec):
        error = dumps({"error":"expired token"})
        return web.Response(text=error) 
    user_id = jwt_dec['user_id']
    # получаем автора по user_id
    author = await Profile.select('id').where(Profile.user_id==user_id).gino.scalar()
    # создаём новый тред с заданным именем и сохраняем в бд
    thread = await Thread.create(name=json_input['name'], author=author)
    json = dumps({'thread': thread.id })
    return web.Response(text=json)

@routes.get('/api/threads/{id}/')
async def get_thread_by_id(request):
    id = int(request.match_info['id'])
    # найти в базе данных нужный тред
    thread = await Thread.get(id)
    # найти все сообщения, которые связаны с этим тредом
    messages = await Message.query.where(Message.thread_id == id).gino.all()
    print(messages)
    last_message = messages[-1]
    print(last_message)
    last_message_author = await Profile.get(last_message.author_id)
    print(last_message_author)

    # собрать все данные в ответный json
    json = dumps({
        "thread": {
            "id": thread.id,
            "name": thread.name,
            "last_message": {
                "id": last_message.id,
                "body": last_message.body,
                "publication_time" : last_message.publication_time,
                "author": {
                    "name": last_message_author.name,
                    "registration_time" : last_message_author.registration_time,
                }
            }
        }
    })
    return web.Response(text=json)

@routes.get('/api/threads/')
async def get_threads(request):
    #получить информацию обо всех тредах
    threads = await db.all(Thread.query)
    # собрать все данные в ответный json
    # для этого создадим массив имен и айдишников
    obj = []
    for _ in range(len(threads)):
        obj.append({"id":threads[_].id, "name":threads[_].name})
    json = dumps({"threads": obj})
    return web.Response(text=json)

