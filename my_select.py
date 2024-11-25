import sqlite3
import faker
from tabulate import tabulate


USER_ID = 3
STATUS_NAME = 'new'
TASK_ID = 1
OLD_FULLNAME = 'Mark Davis'


fake_data = faker.Faker()
USER_NAME = fake_data.name()
USER_EMAIL = fake_data.unique.email()
EMAIL_PATTERN = USER_EMAIL[USER_EMAIL.index('@'):]

def execute_query(choise: str) -> list:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        match choise:

            case 'user_id':
                cur.execute("""
                    SELECT t.id, t.title, t.description, s.name 
                    FROM tasks AS t
                    LEFT JOIN status AS s ON t.status_id = s.id
                    WHERE user_id = ?;""", (USER_ID,))
                return tabulate(cur.fetchall(), headers=['ID',f"{USER_ID} USER'S TASKS",'DESCRIPTION','STATUS'], tablefmt='fancy_grid')
            
            case 'status_name':
                cur.execute("""
                    SELECT t.id, t.title, t.description, u.fullname
                    FROM tasks AS t
                    LEFT JOIN users AS u ON t.user_id = u.id
                    WHERE t.status_id IN (SELECT id FROM status WHERE name = ?)""", (STATUS_NAME,))
                return tabulate(cur.fetchall(), headers=['ID',f"TASKS WITH STATUS {STATUS_NAME}",'DESCRIPTION','OWNER'], tablefmt='fancy_grid')
            
            case 'change_status':
                cur.execute("""
                    SELECT t.id, t.title, s.name 
                    FROM tasks AS t
                    LEFT JOIN status AS s ON t.status_id = s.id
                    WHERE t.id = ?;""", (TASK_ID,))
                data_list = cur.fetchall()
                cur.execute("""
                    UPDATE status
                    SET name = ?
                    WHERE id IN (SELECT status_id FROM tasks WHERE id = ?);""", (STATUS_NAME,TASK_ID))
                cur.execute("""
                    SELECT s.name 
                    FROM status AS s
                    WHERE s.id IN (SELECT status_id FROM tasks WHERE id = ?);""", (TASK_ID,))
                new_data = cur.fetchall()
                data_list = [o + n for o, n in zip(data_list, new_data)]
                return tabulate(data_list, headers=['ID',"TASK",'OLD STATUS','NEW STATUS'], tablefmt='fancy_grid')
            
            case 'user_no_tasks':
                cur.execute("""
                    SELECT u.id, u.fullname, u.email 
                    FROM users AS u
                    WHERE u.id NOT IN (SELECT user_id FROM tasks);""")
                return tabulate(cur.fetchall(), headers=['ID',"USERS WITH NO TASKS",'EMAIL'], tablefmt='fancy_grid')
            
            case 'add_user':
                cur.execute("""
                    INSERT INTO users (fullname, email)
                    VALUES (?,?);""",(USER_NAME,USER_EMAIL))
                cur.execute("""
                    SELECT u.id, u.fullname, u.email 
                    FROM users AS u
                    ORDER BY u.id DESC
                    LIMIT 1;""")
                return tabulate(cur.fetchall(), headers=['ID',"LAST ADDED USER",'EMAIL'], tablefmt='fancy_grid')
            
            case 'not_completed_tasks':
                cur.execute("""
                    SELECT t.id, t.title, t.description, u.fullname, s.name
                    FROM tasks AS t
                    LEFT JOIN users AS u ON t.user_id = u.id
                    LEFT JOIN status AS s ON t.status_id = s.id
                    WHERE t.status_id NOT IN (SELECT id FROM status WHERE name = ?)""", ('completed',))
                return tabulate(cur.fetchall(), headers=['ID',"NOT COMLETED TASKS",'DESCRIPTION','OWNER','STATUS'], tablefmt='fancy_grid')
            
            case 'delete_task':
                cur.execute("""
                    SELECT t.id, t.title, u.fullname, s.name
                    FROM tasks AS t
                    LEFT JOIN users AS u ON t.user_id = u.id
                    LEFT JOIN status AS s ON t.status_id = s.id
                    WHERE t.id = ?;""", (TASK_ID,))
                data_list = cur.fetchall()
                cur.execute("""
                    DELETE FROM tasks
                    WHERE id = ?;""",(TASK_ID,))
                return tabulate(data_list, headers=['ID',"DELETED TASK",'OWNER','STATUS'], tablefmt='fancy_grid')
            
            case 'email_pattern':
                cur.execute("""
                    SELECT u.id, u.fullname, u.email 
                    FROM users AS u
                    WHERE u.email LIKE ?;""",(f'%{EMAIL_PATTERN}%',))
                return tabulate(cur.fetchall(), headers=['ID',"USER'S NAME",f'EMAIL WITH {EMAIL_PATTERN}'], tablefmt='fancy_grid')
            
            case 'update_fullname':
                cur.execute("""
                    SELECT u.id, u.fullname, u.email 
                    FROM users AS u
                    WHERE u.fullname = ?;""",(OLD_FULLNAME,))
                old_data = cur.fetchall()
                cur.execute("""
                    UPDATE users
                    SET fullname = ?
                    WHERE fullname = ?;""",(USER_NAME,OLD_FULLNAME))
                cur.execute("""
                    SELECT u.id, u.fullname, u.email 
                    FROM users AS u
                    WHERE u.fullname = ?;""",(USER_NAME,))
                new_data = cur.fetchall()
                data_list = [(old_data[0], old_data[1], new_data[1], old_data[2]) for old_data, new_data in zip(old_data, new_data)]
                return tabulate(data_list, headers=['ID',"OLD USER'S NAME","NEW USER'S NAME",'EMAIL'], tablefmt='fancy_grid')
            
            case 'count_tasks':
                cur.execute("""
                    SELECT COUNT(id), name
                    FROM status
                    GROUP BY name;""")
                return tabulate(cur.fetchall(), headers=['COUNT',"STATUS"], tablefmt='fancy_grid')
            
            case 'email_pattern_tasks':
                cur.execute("""
                    SELECT t.id, t.title, s.name,  u.fullname,  u.email
                    FROM tasks AS t
                    LEFT JOIN users AS u ON t.user_id = u.id
                    LEFT JOIN status AS s ON t.status_id = s.id
                    WHERE t.user_id IN (SELECT id FROM users WHERE email LIKE ?);""",(f'%{EMAIL_PATTERN}%',))
                return tabulate(cur.fetchall(), headers=['ID',f"TASKS OWNERS WITH {EMAIL_PATTERN}",'STATUS','OWNER','EMAIL'], tablefmt='fancy_grid')
            
            case 'empty_description':
                cur.execute("""
                    SELECT t.id, t.title, s.name,  u.fullname
                    FROM tasks AS t
                    LEFT JOIN users AS u ON t.user_id = u.id
                    LEFT JOIN status AS s ON t.status_id = s.id
                    WHERE t.description IS NULL OR t.description = '' ;""")
                return tabulate(cur.fetchall(), headers=['ID',"TASKS WITH NO DESCRIPTIONS ",'STATUS','OWNER'], tablefmt='fancy_grid')
            
            case 'users_in_progress':
                cur.execute("""
                    SELECT t.id, t.title, u.fullname
                    FROM tasks AS t
                    INNER JOIN users AS u ON t.user_id = u.id
                    WHERE t.status_id IN (SELECT id FROM status WHERE name = 'in progress');""")
                return tabulate(cur.fetchall(), headers=['ID',"TASKS WITH STATUS IN PROGRES",'OWNER'], tablefmt='fancy_grid')
            
            case 'users_tasks_count':
                cur.execute("""
                    SELECT COUNT(t.user_id), u.fullname 
                    FROM users AS u
                    LEFT JOIN tasks AS t ON t.user_id = u.id
                    GROUP BY u.fullname;""")
                return tabulate(cur.fetchall(), headers=['COUNT OF TASKS',"OWNER"], tablefmt='fancy_grid')
                

print(execute_query('user_id'))
