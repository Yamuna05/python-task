import mysql.connector
from datetime import date


def add_book():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()

    title = raw_input('Enter Book Title :')
    author = raw_input('Enter Book Author : ')
    publisher = raw_input('Enter Book Publisher : ')
    pages = raw_input('Enter Book Pages : ')
    price = raw_input('Enter Book Price : ')
    edition = raw_input('Enter Book Edition : ')
    copies = int(raw_input('Enter copies : '))
    sql = 'insert into book(title,author,price,pages,publisher,edition,status) values ( "' + \
          title + '","' + author + '",' + price + ',' + pages + ',"' + publisher + '","' + edition + '","available");'
    # sql2 = 'insert into transaction(dot,qty,type) values ("'+str(today)+'",'+qty+',"purchase");'
    # print(sql)
    for _ in range(0, copies):
        cursor.execute(sql)
    conn.close()
    print('\n\nNew Book added successfully')
    wait = raw_input('\n\n\n Press any key to continue....')


def add_member():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()

    name = raw_input('Enter Member Name :')
    clas = raw_input('Enter Member Class & Section : ')
    address = raw_input('Enter Member Address : ')
    phone = raw_input('Enter Member Phone  : ')
    email = raw_input('Enter Member Email  : ')

    sql = 'insert into member(name,class,address,phone,email) values ( "' + \
          name + '","' + clas + '","' + address + '","' + phone + \
          '","' + email + '");'
    # sql2 = 'insert into transaction(dot,qty,type) values ("'+str(today)+'",'+qty+',"purchase");'
    # print(sql)

    cursor.execute(sql)
    conn.close()
    print('\n\nNew Member added successfully')
    wait = raw_input('\n\n\n Press any key to continue....')


def modify_book():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()
    clear()
    print('Modify BOOK Details Screen ')
    print('-' * 120)
    print('\n1. Book Title')
    print('\n2. Book Author')
    print('\n3. Book Publisher')
    print('\n4. Book Pages')
    print('\n5. Book Price')
    print('\n6. Book Edition')
    print('\n\n')
    choice = int(raw_input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'title'
    if choice == 2:
        field = 'author'
    if choice == 3:
        field = 'publisher'
    if choice == 4:
        field = 'pages'
    if choice == 5:
        field = 'price'
    book_id = raw_input('Enter Book ID :')
    value = raw_input('Enter new value :')
    if field == 'pages' or field == 'price':
        sql = 'update book set ' + field + ' = ' + value + ' where id = ' + book_id + ';'
    else:
        sql = 'update book set ' + field + ' = "' + value + '" where id = ' + book_id + ';'
    # print(sql)
    cursor.execute(sql)
    print('\n\n\nBook details Updated.....')
    conn.close()
    wait = raw_input('\n\n\n Press any key to continue....')


def modify_member():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()
    clear()
    print('Modify Memeber Information Screen ')
    print('-' * 120)
    print('\n1. Name')
    print('\n2. Class')
    print('\n3. address')
    print('\n4. Phone')
    print('\n5. Emaile')
    print('\n\n')
    choice = int(raw_input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'name'
    if choice == 2:
        field = 'class'
    if choice == 3:
        field = 'address'
    if choice == 4:
        field = 'phone'
    if choice == 5:
        field = 'email'
    mem_id = raw_input('Enter member ID :')
    value = raw_input('Enter new value :')
    sql = 'update member set ' + field + ' = "' + value + '" where id = ' + mem_id + ';'
    # print(sql)
    cursor.execute(sql)
    print('Member details Updated.....')
    conn.close()
    wait = raw_input('\n\n\n Press any key to continue....')


def issue_book():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()

    clear()
    print('\n BOOK ISSUE SCREEN ')
    print('-' * 120)
    book_id = raw_input('Enter Book  ID : ')
    mem_id = raw_input('Enter Member ID :')

    result = book_status(book_id)
    result1 = mem_issue_status(mem_id)
    # print(result1)
    today = date.today()
    if len(result1) == 0:
        if result == 'available':
            sql = 'insert into transaction(b_id, m_id, doi) values(' + book_id + ',' + mem_id + ',"' + str(
                today) + '");'
            sql_book = 'update book set status="issue" where id =' + book_id + ';'
            cursor.execute(sql)
            cursor.execute(sql_book)
            print('\n\n\n Book issued successfully')
        else:
            print('\n\nBook is not available for ISSUE... Current status :', result1)
    else:
        if len(result1) < 1:
            sql = 'insert into transaction(b_id, m_id, doi) values(' + \
                  book_id + ',' + mem_id + ',"' + str(today) + '");'
            sql_book = 'update book set status="issue" where id =' + book_id + ';'
            # print(len(result))
            cursor.execute(sql)
            cursor.execute(sql_book)
            print('\n\n\n Book issued successfully')
        else:
            print('\n\nMember already have book from the Library')
        # print(result)

    conn.close()
    wait = raw_input('\n\n\n Press any key to continue....')

def return_book():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()
    global fine_per_day
    clear()
    print('\n BOOK RETURN SCREEN ')
    print('-' * 120)
    book_id = raw_input('Enter Book  ID : ')
    mem_id = raw_input('Enter Member ID :')
    today = date.today()
    result = book_issue_status(book_id, mem_id)
    if result == None:
        print('Book was not issued...Check Book Id and Member ID again..')
    else:
        sql = 'update book set status ="available" where id =' + book_id + ';'
        din = (today - result[3]).days
        fine = din * fine_per_day  # fine per data
        sql1 = 'update transaction set dor ="' + str(today) + '" , fine=' + str(
            fine) + ' where b_id=' + book_id + ' and m_id=' + mem_id + ' and dor is NULL;'

        cursor.execute(sql)
        cursor.execute(sql1)
        print('\n\nBook returned successfully')
    conn.close()
    wait = raw_input('\n\n\n Press any key to continue....')


def search_book(field):
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()

    clear()
    print('\n BOOK SEARCH SCREEN ')
    print('-' * 120)
    msg = 'Enter ' + field + ' Value :'
    title = raw_input(msg)
    sql = 'select * from book where ' + field + ' like "%' + title + '%"'
    cursor.execute(sql)
    records = cursor.fetchall()
    clear()
    print('Search Result for :', field, ' :', title)
    print('-' * 120)
    for record in records:
        print(record)
    conn.close()
    wait = raw_input('\n\n\n Press any key to continue....')
def reprot_book_list():
    conn = mysql.connector.connect(
        host='localhost', database='library', user='root', password='')
    cursor = conn.cursor()

    clear()
    print('\n REPORT - BOOK TITLES ')
    print('-' * 120)
    sql = 'select * from book'
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        print(record)
    conn.close()
    wait = raw_input('\n\n\nPress any key to continue.....')
