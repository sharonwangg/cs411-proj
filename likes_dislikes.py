import xlrd
import pymysql.cursors

#generates sql insert statements for likes and dislikes data from google form responses
wb = xlrd.open_workbook('Likes and Dislikes Data.xlsx')
sheet = wb.sheet_by_index(0)
a = open("likes.txt", "w")
ins1 = "INSERT INTO user VALUES('"
ins2 = "INSERT INTO login VALUES('"
mid = "','"
ins3 = "INSERT INTO Likes VALUES('"


for i in range(1,sheet.nrows,2):
    a.write(ins1 + sheet.cell_value(i,2) + "');\n")
for i in range(1,sheet.nrows,2):
    a.write(ins2 + sheet.cell_value(i,2) + mid + sheet.cell_value(i,3) + mid + sheet.cell_value(i,4) + mid + str(sheet.cell_value(i,0)) + "');\n")

def search_book(value):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='m8y7b6v5',
                                 db='book_club')
    returni=0
    rows = []
    try:
        with connection.cursor() as cur:
            cur.execute('Select book_id from books where book_title like %s limit 1', ("%" + value + "%"))
            rows = cur.fetchall()
            if len(rows) != 0:
                returni = rows[0]
    finally:
        connection.close()
        return returni


for i in range (1, sheet.nrows,2):
    for j in range (5, sheet.ncols):
        bookid = search_book(sheet.cell_value(i,j))
        if bookid != (0,) and bookid != 0:
            a.write(ins3 + sheet.cell_value(i,2) + mid + str(bookid[0]) + mid + "Like');\n")
        bookid = search_book(sheet.cell_value(i+1,j))
        if bookid != (0,) and bookid != 0:
            a.write(ins3 + sheet.cell_value(i,2) + mid + str(bookid[0]) + mid + "Disike');\n")

