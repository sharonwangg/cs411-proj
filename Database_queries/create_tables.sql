#drop database book_club;
CREATE DATABASE book_club;
USE book_club;

CREATE TABLE books(
book_id int,
author varchar(100),
book_title varchar(100),
genre varchar(100),
PRIMARY KEY(book_id)
);

CREATE TABLE user(
username varchar(10),
PRIMARY KEY(username),
FOREIGN KEY(username) REFERENCES login(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE login(
username varchar(10),
password varchar(50),
email varchar(50),
age int,
check(age>=5 and age<=85 and email like  '%_@__%.__%'),
PRIMARY KEY(username)
);

CREATE TABLE Reads_(
username varchar(10),
book_id int,
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE  ON UPDATE CASCADE,
PRIMARY KEY(username,book_id)
);

CREATE TABLE Likes(
username varchar(10),
book_id int,
likes_dislikes varchar(20),
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE  ON UPDATE CASCADE,
PRIMARY KEY(username,book_id)
);

CREATE TABLE Event_(
event_id int not null AUTO_INCREMENT, 
dateTime varchar (50),
event_name varchar (50),
event_description varchar(250),
location varchar(100),
book_id int,
host1 varchar(10),
PRIMARY KEY(event_id),
FOREIGN KEY(host1) REFERENCES user(username) ON DELETE SET NULL ON UPDATE CASCADE,
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);	

CREATE TABLE post(
username varchar(10),
post_id int not null AUTO_INCREMENT,
text1 varchar(250),
dateTime datetime default NOW(),
book_id int,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY(post_id, book_id)
);

CREATE TABLE club(
username varchar(10),
club_id int not null,
is_admin BOOLEAN default 0,
PRIMARY KEY(username, club_id),
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE SET NULL ON UPDATE CASCADE,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE
);
