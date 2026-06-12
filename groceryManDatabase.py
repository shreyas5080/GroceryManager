import psycopg2


def get_connection():
    connection = psycopg2.connect(host='localhost', port=5432,
                                  database='groceryManagement-db', user='postgres', password='successiskey')

    return connection


def delete(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM groceryitems WHERE itemname= %s ''', (name,))
    connection.commit()
    connection.close()


def insert(groceryName, quantity, user_email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO groceryitems(itemname, quantity, user_email) VALUES(%s, %s, %s)''',
                   (groceryName, quantity, user_email))

    connection.commit()
    connection.close()


def get_results(user_email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''select g.itemname 
    from groceryitems g join users u on 
    g.user_email = u.user_email
    where u.user_email = %s''', (user_email,))
    results = cursor.fetchall()

    connection.commit()
    connection.close()

    return results


def insert_in_users(fname, lname, email, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO users(user_fname, user_lname, user_email, user_password) VALUES(%s, %s, %s, %s)''',
                   (fname, lname, email, password))

    connection.commit()
    connection.close()


def get_email(user_email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT user_email FROM users WHERE user_email= %s''',
                   (user_email,))
    my_results = cursor.fetchone()
    connection.commit()
    connection.close()

    return my_results


def get_password(user_email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT user_password FROM users WHERE user_email= %s''',
                   (user_email,))
    pass_results = cursor.fetchone()

    connection.commit()
    connection.close()

    return pass_results


def get_name(user_email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT user_lname, user_fname FROM users WHERE user_email= %s''',
                   (user_email,))
    name_results = cursor.fetchall()

    their_name = name_results[0]
    result_name = ' '.join(their_name)

    connection.commit()
    connection.close()

    return result_name


def get_user():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()

    connection.commit()
    connection.close()

    return users


def delete_person(user_email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM users WHERE user_email = %s''', (user_email,))

    connection.commit()
    connection.close()
