#chat implemented using reference videos: 
#https://youtu.be/pvUUidK1zuw
#https://youtu.be/uJC8A_7VZOA


from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient, DESCENDING


client = MongoClient("mongodb+srv://admin:admin@cluster0.1cjsr.mongodb.net/chat?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")
messages_collection = chat_db.get_collection("messages")
audio_collection =chat_db.get_collection("book_audio_book")

def get_all_room(username):
    li =list(room_members_collection.find({'_id.username': username},{'room_name':1,'_id':0}))
    return li[0]

def delete_chat(room_id,room_name):
    print(room_name)
    rooms_collection.remove({'_id': ObjectId(room_id)})
    room_members_collection.remove({'room_name':room_name})
    messages_collection.remove({'room_id':room_id})



def get_book_link(book_name):
    return audio_collection.find_one({'book_name':book_name})


def insert_audio(book,audio_book):
    audio_id = audio_collection.insert_one(
        {'book_name': book, 'audio_link': audio_book, 'created_at': datetime.now()}).inserted_id

def get_id(name):
    return rooms_collection.find_one({'name': name},{'_id': 1})

def save_user(username, email, password):
    users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})


def save_room(room_name, created_by,book_name):
    room_id = rooms_collection.insert_one(
        {'name': room_name, 'created_by': created_by, 'created_at': datetime.now(),'book_name':book_name}).inserted_id
    add_room_member(room_id, room_name, created_by, created_by, is_room_admin=True)
    return room_id


def update_room(room_id, room_name):
    rooms_collection.update_one({'_id': ObjectId(room_id)}, {'$set': {'name': room_name}})
    room_members_collection.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})


def get_room(room_id):
    return rooms_collection.find_one({'_id': ObjectId(room_id)})


def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    room_members_collection.insert_one(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
         'added_at': datetime.now(), 'is_room_admin': is_room_admin})


def add_room_members(room_id, room_name, usernames, added_by):
    room_members_collection.insert_many(
        [{'_id': {'room_id': ObjectId(room_id), 'username': username}, 'room_name': room_name, 'added_by': added_by,
          'added_at': datetime.now(), 'is_room_admin': False} for username in usernames])


def remove_room_members(room_id, usernames):
    room_members_collection.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})


def get_room_members(room_id):
    return list(room_members_collection.find({'_id.room_id': ObjectId(room_id)}))


def get_rooms_for_user(username):
    return list(room_members_collection.find({'_id.username': username}))


def is_room_member(room_id, username):
    return room_members_collection.count_documents({'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    return room_members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}, 'is_room_admin': True})


def save_message(room_id, text, sender):
    messages_collection.insert_one({'room_id': room_id, 'text': text, 'sender': sender, 'created_at': datetime.now()})



def get_messages(room_id):
    messages = list(
        messages_collection.find({'room_id': str(room_id)}).sort('created_at', DESCENDING))
    for message in messages:
        message['created_at'] = message['created_at'].strftime("%d %b, %H:%M")
    return messages[::-1]
