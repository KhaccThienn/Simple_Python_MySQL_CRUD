import datetime
import mysql.connector
from prettytable import from_db_cursor

def connect_mysql():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = ''
    )

def create_database(db):
    conn = connect_mysql()
    
    cursor = conn.cursor()
    
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db}')
    cursor.execute(f'USE {db}')
    
    print(f'Currently using database {db}')
    
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employee (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        birthday date,
                        phone varchar(100)
                    )
                """)
    
    cursor.close()
    return conn

def create(data, conn):
    cursor = conn.cursor()
    
    query = """
    INSERT INTO employee (name, birthday, phone) VALUES (%s, %s, %s);
    """
    
    cursor.execute(query, data)
    
    conn.commit()
    
    cursor.close()

def input_employee(conn):
    while True:
        name = input("Name: ")
        birthday = datetime.datetime.strptime(input("Birthday: "), '%d/%m/%Y')
        phone = input("Phone: ")
        data = (name, birthday, phone)
        
        create(data, conn)
        
        choose = input("Continue ? (y/n): ")
        if choose == "n":
            print("Input data completed")
            break

def show_all(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM employee")
    
    my_table = from_db_cursor(cursor)

    print(my_table)
    cursor.close()

def is_exist(update_id, conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM employee WHERE id = %s", (update_id,))
    result = cursor.fetchone()
    
    if result[0] == 0:
        return False
    return True

def update(data, conn):
    cursor = conn.cursor()
    
    # Define the SQL query to update the record based on the provided parameters
    sql_query = "UPDATE employee SET name = %s, birthday = %s, phone = %s WHERE id = %s"

    # Execute the SQL query with the provided parameters
    cursor.execute(sql_query, data)

    # Commit the changes to the database
    conn.commit()
    cursor.close()

def delete(data, conn):
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM employee WHERE id = {data}')
    
    conn.commit()
    cursor.close()

def main():
    conn = create_database('python_employee')
    while True:
        print("\n1. Input employees.")
        print("2. Show all employees.")
        print("3. Search employees by name.")
        print("4. Update employee.")
        print("5. Delete employee.")
        print("0. Quit program.")
        
        choose = int(input("Enter your choice: "))
        
        if choose == 1:
            input_employee(conn=conn)
        elif choose == 2:
            show_all(conn=conn)
        elif choose == 3:
            pass
        elif choose == 4:
            _id = input("Enter the id to update: ")
            if is_exist(_id, conn=conn):
                name = input("Name: ")
                birthday = datetime.datetime.strptime(input("Birthday: "), '%d/%m/%Y')
                phone = input("Phone: ")
                data = (name, birthday, phone, _id)
                update(data=data, conn=conn)
            else:
                print("Not found id to update")
        elif choose == 5:
            _id = input("Enter the id to delete: ")
            if is_exist(_id, conn=conn):
                delete(data=_id, conn=conn)
            else:
                print("Not found id to delete")
        elif choose == 0:
            conn.close()
            break
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()