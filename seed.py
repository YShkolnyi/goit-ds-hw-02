from datetime import datetime
import faker
from random import randint, choice, shuffle
import sqlite3

NUMBER_USERS = 3
NUMBER_TASKS = 10
STATUS_NAMES = ['new','in progress','completed']

def generate_fake_data():
    fake_users = []# тут зберігатимемо користувачів
    fake_emails = []# тут зберігаємо пошту
    fake_tasks = []# тут зберігатимемо завдання
    fake_descriptions = []#тут зберігатимемо опис
    fake_status_id = list(range(1, NUMBER_TASKS+1))
    fake_status_name = []
    fake_user_id = []

    fake_data = faker.Faker()
    shuffle(fake_status_id)

# Створимо набір користувачів і пошт у кількості NUMBER_USERS
    for _ in range(NUMBER_USERS):
        fake_users.append(fake_data.name())
        fake_emails.append(fake_data.unique.email())

# Згенеруємо тепер NUMBER_TASKS кількість завдань, описів і статусів
    for _ in range(NUMBER_TASKS):
        fake_tasks.append(fake_data.sentence(nb_words=3))
        fake_descriptions.append(fake_data.text(max_nb_chars=50))
        fake_user_id.append(choice(range(1,NUMBER_USERS+1)))
        fake_status_name.append(choice(STATUS_NAMES))

    return fake_users,fake_emails,fake_tasks,fake_descriptions,fake_status_id,fake_user_id,fake_status_name

def prepare_data(users,emails,tasks,descriptions,status_id,user_id,status_name):
    for_users = []
    for_status = []
    for_tasks = []

    for i in range(NUMBER_USERS):
        for_users.append((users[i],emails[i]))

    for i in range(NUMBER_TASKS):
        for_status.append((status_name[i],))
        for_tasks.append((tasks[i],descriptions[i],status_id[i],user_id[i]))

    return for_users, for_status, for_tasks

def insert_data_to_db(users, statuses, tasks):
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()

        cur.executemany("INSERT INTO users (fullname, email) VALUES (?, ?);", users)
        cur.executemany("INSERT INTO status (name) VALUES (?);", statuses)
        cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?);", tasks)

        con.commit()

if __name__ == "__main__":
    insert_data_to_db(*prepare_data(*generate_fake_data()))