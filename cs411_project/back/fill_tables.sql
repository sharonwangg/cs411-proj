#fills tables with dummy data for testing

insert into login values('batman','batman123','batman@gmail.com','43');
insert into login values('robin','robin123','robin@gmail.com','34');

insert into user values('batman');
insert into user values('robin');

insert into books values(12, 'Harper Lee', 'To Kill a Mockingbird', 'fiction');
insert into books values(31, 'J. R. R. Tolkien', 'The Lord of the Rings', 'fantasy');
insert into books values(43, 'Paulo Coelho', 'The Alchemist', 'fantasy');
insert into books values(52, 'J. K Rowling', "Harry Potter and the Philosopher's Stone", 'fantasty');
insert into books values(53, 'J. K Rowling', "Harry Potter and the Chamber of Secrets", 'fantasty');
insert into books values(54, 'J. K Rowling', "Harry Potter and the Prisoner of Azkaban", 'fantasty');
insert into books values(55, 'J. K Rowling', "Harry Potter and the Goblet of Fire", 'fantasty');
insert into books values(56, 'J. K Rowling', "Harry Potter and the Order of the Phoenix", 'fantasty');
insert into books values(57, 'J. K Rowling', "Harry Potter and the Half-Blood Prince", 'fantasty');
insert into books values(58, 'J. K Rowling', "Harry Potter and the Deathly Hallows", 'fantasty');

insert into post (username, text1, book_id) values ('batman', 'Boo Radley is my favorite character', 12);
insert into post (username, text1, book_id) values ('robin', 'I enjoyed chapter 7', 12);
insert into post (username, text1, book_id) values ('batman',  'I liked the use of metaphor in chapter 8', 12);
insert into post (username, text1, book_id) values ('batman', 'There was too much imagery in chapter 2', 12);
insert into post (username, text1, book_id) values ('robin', 'I disliked chapter 5', 12);

#complex queries for demo
use book_club;
(SELECT count(*), book_id FROM post WHERE username = 'batman' GROUP BY book_id) UNION (SELECT count(*), book_id FROM post WHERE username = 'robin' GROUP BY book_id);
SELECT count(*), b.book_title FROM books b NATURAL JOIN Reads_ r WHERE b.author LIKE "%Rowling%" AND r.page_number >= 50 GROUP BY b.book_title; 