import statistics as stat
from sklearn.cluster import KMeans
import requests
import pprint
import urllib.request as urllib
import zipfile
import pymysql.cursors
import json
import hashlib
import flask
from flask import Flask, render_template, request,url_for, redirect,session
import pymysql.cursors
from datetime import datetime
import numpy as np
import math
from db import save_room,add_room_members

#Advanced funtion 1 - places users in book clubs based on their preferences for books existing in the database

def create_user(username,password,email,age):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')

    value=''

    print(username)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `user` (`username`) VALUES (%s)"
            cursor.execute(sql, (username))
            #password_hash= hashlib.md5(password).hexdigest()
            sql = "INSERT INTO `login` (`username`,`password`,`email`,`age`) VALUES (%s,%s,%s,%s)"
            value=cursor.execute(sql, (username,password,email,age))
        connection.commit()
    finally:
        connection.close()
        print(value)
        return value





def get_book_ids():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='m8y7b6v5',
                                db='book_club')

    # select book_ids from Books table
    book_ids = []
    try:
        with connection.cursor() as cur:
            sql = "SELECT book_id FROM `Books`"
            cur.execute(sql)
            book_ids = cur.fetchall()
        connection.commit()
    finally:
        connection.close()

    # fix tuple problem
    fixed_book_ids = []
    for book_id in book_ids:
        fixed_book_ids.append(book_id[0])

    return fixed_book_ids


def get_usernames():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='m8y7b6v5',
                                db='book_club')

    # select usernames from user table
    usernames = []
    try:
        with connection.cursor() as cur:
            sql = "SELECT username FROM `user`"
            cur.execute(sql)
            usernames = cur.fetchall()
        connection.commit()
    finally:
        connection.close()

    # fix tuple problem
    fixed_usernames = []
    for username in usernames:
        fixed_usernames.append(username[0])

    return fixed_usernames


# get rows from `Likes`
def get_likes_data():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='m8y7b6v5',
                                db='book_club')

    likes_rows = []

    try:
        with connection.cursor() as cur:
            sql = "SELECT * FROM `Likes`"
            cur.execute(sql)
            likes_rows = cur.fetchall()
        connection.commit()
    finally:
        connection.close()

    return likes_rows


def get_username_to_id(usernames):
    username_to_id = {}
    id = 0
    for username in usernames:
        username_to_id[username] = id
        id += 1
    return username_to_id


def get_book_id_to_new_book_id(book_ids):
    book_id_to_new_book_id = {}
    id = 0
    for book_id in book_ids:
        book_id_to_new_book_id[book_id] = id
        id += 1
    return book_id_to_new_book_id


# for each user, an array where each element represents a book
# (-1 - dislike, 0 - nothing, 1 - like)
def get_user_preferences(book_id_to_new_book_id, likes_rows, username_to_id):
    preferences = np.zeros(shape=(len(usernames), len(list(book_id_to_new_book_id))))

    for likes_row in likes_rows:
        username = likes_row[0]
        book_id = likes_row[1]
        like_dislike = likes_row[2]
        to_insert = -1
        if like_dislike == "Like":
            to_insert = 1
        preferences[username_to_id[username], book_id_to_new_book_id[book_id]] = to_insert

    return preferences


def identify_min_cluster_outside_tol(clusters, ideal_group_size, tol):
    min_cluster = None
    min_cluster_id = None
    for cluster_id, user_ids in clusters.items():
        if user_ids.size < (ideal_group_size - tol):
            if min_cluster is None or user_ids.size < min_cluster.size:
                min_cluster = user_ids
                min_cluster_id = cluster_id
    return min_cluster, min_cluster_id


def identify_max_cluster(clusters):
    max_cluster = None
    max_cluster_id = None
    for cluster_id, user_ids in clusters.items():
        if max_cluster is None or user_ids.size > max_cluster.size:
            max_cluster = user_ids
            max_cluster_id = cluster_id
    return max_cluster, max_cluster_id


def balance_clusters(clusters, min_cluster, min_cluster_id, min_cluster_center, max_cluster, preference_matrix):
    min_distance = None
    possible_transfer = None
    possible_transfer_index = None
    for i, user_id in enumerate(max_cluster):
        user_preferences = preference_matrix[user_id]
        distance = math.sqrt(sum([(a - b)**2 for a, b in zip(min_cluster_center, user_preferences)]))
        if min_distance is None or distance < min_distance:
            min_distance = distance
            possible_transfer = user_id
            possible_transfer_index = i
    clusters[min_cluster_id] = np.append(min_cluster, possible_transfer)
    clusters[max_cluster_id] = np.delete(max_cluster, possible_transfer_index)


def get_group_id_of_new_user(clf, clusters, username, likes, dislikes, book_id_to_new_book_id):
    '''
    clf (KMeans.fit object)
    clusters (dict from group_id to list of usernames)
    username (str)
    likes (list of liked book_ids)
    dislikes (list of disliked book_ids)
    book_id_to_new_book_id (dict from original to adjusted book_ids)
    '''
    preference = np.zeros(shape=(1, len(list(book_id_to_new_book_id))))
    for liked_book_id in likes:
        preference[0, book_id_to_new_book_id[liked_book_id]] = 1
    for disliked_book_id in dislikes:
        preference[0, book_id_to_new_book_id[disliked_book_id]] = -1

    min_distance = None
    assigned_group_id = None
    for group_id in clusters.keys():
        cluster_center = clf.cluster_centers_[group_id]
        distance = math.sqrt(sum([(a - b)**2 for a, b in zip(cluster_center, preference[0])]))
        if min_distance is None or distance < min_distance:
            min_distance = distance
            assigned_group_id = group_id

    clusters[assigned_group_id].append(username)

    return assigned_group_id


def insert_clusters(clustered_users):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='m8y7b6v5',
                                db='book_club')
    
    try:
        with connection.cursor() as cur:
            for gid, usernames in clustered_users.items():
                for username in usernames:
                    sql = "INSERT INTO `club` (`username`, `club_id`) VALUES (%s, %s)"
                    cur.execute(sql, (username, str(gid)))
        connection.commit()
    finally:
        connection.close()

def group_new_user(new_user, clubid):
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='m8y7b6v5',
                                db='book_club')
    try:
        with connection.cursor() as cur:
            sql = "INSERT INTO `club` (`username`, `club_id`) VALUES (%s, %s)"
            cur.execute(sql, (new_user, clubid))
        connection.commit()
    finally:
        connection.close()


def assign_room(clusters):
    for i in clusters.keys():
        room_id=save_room(i, 'system',i)
        add_room_members(room_id, i, clusters[i], 'system')
    #save_room(room_name,created_by,book_name)
    #room_id = save_room(room_name, session['username'],book_name)
    #add_room_members(room_id, room_name, usernames, session['username'])



usernames = get_usernames()
username_to_id = get_username_to_id(usernames)
book_id_to_new_book_id = get_book_id_to_new_book_id(get_book_ids())
preference_matrix = get_user_preferences(book_id_to_new_book_id, get_likes_data(), username_to_id)
ideal_group_size = 5
clf = KMeans(n_clusters=int(len(usernames) / ideal_group_size), random_state=411).fit(preference_matrix)
clusters = {i: np.where(clf.labels_ == i)[0] for i in range(clf.n_clusters)}



while True:
    min_cluster, min_cluster_id = identify_min_cluster_outside_tol(clusters, ideal_group_size, 0)
    if min_cluster is None:
        break
    max_cluster, max_cluster_id = identify_max_cluster(clusters)
    min_cluster_center = clf.cluster_centers_[min_cluster_id]
    balance_clusters(clusters, min_cluster, min_cluster_id, min_cluster_center, max_cluster, preference_matrix)

# assign usernames to each cluster
for group_id, user_ids in clusters.items():
    usernames = []
    for user_id in user_ids:
        usernames.append(list(username_to_id)[user_id])
    clusters[group_id] = usernames   

#assign chat room:
assign_room(clusters)
config=open('config.txt','w+')
config.write(str(clf)+'\n')
config.write(str(clusters))
config.close()
#insert_clusters(clusters)

#add new user
#create_user('sharonwaFng','swang123','swang@gmail.com','20')
#gid = get_group_id_of_new_user(clf, clusters, 'sharonwang', [375, 376], [388, 393], book_id_to_new_book_id)
#group_new_user('sharonwang',gid)




