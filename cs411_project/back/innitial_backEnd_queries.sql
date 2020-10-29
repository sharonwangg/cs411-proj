create database book_club;
use book_club;

create table books(
book_id int,
author varchar(100),
book_title varchar(100),
genre varchar(100),
primary key(book_id));



create table user(
username varchar(10),
primary key (username)
);

insert into login values('batman','batman123','batman@gmail.com','43');
insert into login values('robin','robin123','robin@gmail.com','34');

create table login(
username varchar(10),
password varchar(50),
email varchar(50),
age int,
check(age>=5 and age<=85 and email like  '%_@__%.__%'),
primary key(username)
);



create table Reads_(
username varchar(50),
book_id int,
page_number int,
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE  ON UPDATE CASCADE,
primary key(username,book_id));


create table Likes(
username varchar(50),
book_id int,
likes_dislikes varchar(20),
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE  ON UPDATE CASCADE,
primary key(username,book_id));


select * from books;






create table post(
username varchar(10),
post_id int not null,
text1 varchar(250),
dateTime datetime,
book_id int not null,
FOREIGN KEY(username) REFERENCES user(username) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
primary key(post_id)
);


Select username, text1,
dateTime,
book_id from post
where text1 like (%s%);

Select username, text1,
dateTime,
book_id from post
where username like (%s%);


INSERT INTO `post` (`username`,`post_id`,`text1`, `dateTime`,`book_id`) VALUES (%s, %s, %s, %s, %s)


select * from post

update post set text1='new_text'
where username='username'


delete from post 
where post_id='post_id'


