import psycopg2

conn = psycopg2.connect(database='netology_db', user='postgres', password='3662075')


def create_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        surname VARCHAR(20) NOT NULL,
        mail VARCHAR(45) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        num VARCHAR(15) UNIQUE,
        client_id int REFERENCES client(client_id)
        );
    """)


def add_client(first_name, last_name, email):
    cur.execute("""
            INSERT INTO client(name, surname, mail)
            VALUES(%s, %s, %s) RETURNING client_id;
            """, (first_name, last_name, email))


# conn.commit()
def id_clint(email):
    cur.execute("""
                SELECT * FROM client
                WHERE mail = %s
                ;
                """, (email,))
    client_id = cur.fetchone()[0]
    return client_id


def id_num(num):
    cur.execute("""
                SELECT * FROM phone
                WHERE num = %s
                ;
                """, (num,))
    id = cur.fetchone()[0]
    return id


def add_phone(email, ph):
    cur.execute("""
                INSERT INTO phone(num, client_id)
                VALUES(%s, %s);
                """, (ph, id_clint(email)))


def change_client(table, column, info, curent):
    if table == 'phone':
        cur.execute("""
                    UPDATE phone SET num=%s WHERE id=%s
                    """, (info, id_num(curent)))
    elif table == 'client':
        if column == 'name':
            cur.execute("""
                        UPDATE client SET name=%s WHERE client_id=%s
                        """, (info, id_clint(curent)))
        elif column == 'surname':
            cur.execute("""
                        UPDATE client SET surname=%s WHERE client_id=%s
                        """, (info, id_clint(curent)))
        elif column == 'mail':
            cur.execute("""
                        UPDATE client SET mail=%s WHERE client_id=%s
                        """, (info, id_clint(curent)))


def delete_phone(phone):
    cur.execute("""
                DELETE FROM phone WHERE num=%s
                """, (phone,))


def delete_client(mail):
    cur.execute("""
                DELETE FROM client WHERE client_id=%s
                """, (id_clint(mail),))


def find_client():
    curent = input('Поиск по "client" или "phone":')
    if curent == 'client':
        print(id_clint(input('введите email:')))
    elif curent == 'phone':
        print(id_num(input('введите номер телефона:')))


with conn.cursor() as cur:
    cur.execute(""" DROP TABLE phone; DROP TABLE client""")
    create_db()
    add_client(first_name='Джонни', last_name='Депп', email='JonniDepp@netology.ru')
    add_phone('JonniDepp@netology.ru', '+78945662132')
    change_client('client', 'mail', 'BredPitt@yandex.ru', 'JonniDepp@netology.ru')
    find_client()
    delete_phone('+78945662132') #закомитьте эти функции, что бы не удалились данные
    delete_client('BredPitt@yandex.ru') #закомитьте эти функции, что бы не удалились данные
    conn.commit()
    conn.close()
