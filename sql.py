
import ipaddress
import os
import logging
import psycopg2
from dotenv import load_dotenv


errorsql = 0
errordhcp = 0

# for read from env file
load_dotenv()
subnet = os.getenv('SUBNET')
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')

logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')


def creattbl():  # for create table in data base if not exist

    global creat

    try:

        conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

        conn.autocommit = True

        cursor = conn.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    use VARCHAR(50) NOT NULL,
                    ip VARCHAR(50) NOT NULL);
                    '''

        cursor.execute(tabl)
        conn.commit()
        creat = 1
        logging.debug("the connection with the database was successfull")
        logging.info("the corresponding table was created")
        cursor.close()
        conn.close()

    except Exception:
        logging.error("incorrect value for connection", exc_info=True)

        return 1


def insert(use):  # for insert user in data base if not exist

    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()

    insertt = '''
    INSERT INTO users (use , ip) VALUES (%s , %s);
    '''
    try:

        cursor.execute(insertt, (use, finderr()))
        conn.commit()

    except Exception:
        logging.error("invalid ip or subnet")
        print("invalid ip or subnet , please valid ipconfig")
        return None

    finally:

        cursor.close()
        conn.close()


def search(use):  # for search user in data base
    global i
    i = 0
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT use , ip FROM users WHERE use = %s", (use,))

    ro = cursor.fetchall()
    for r in ro:
        i = 1
        print(r)

    cursor.close()
    conn.close()
    return i


def update(use, upduse):  # for search user in data base
    global i
    i = 0
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET use = %s WHERE use = %s", (upduse, use))

    conn.commit()
    cursor.close()
    conn.close()
    return i


def searchf(use):  # for search user in database for check user exist or not exist
    global i
    i = 0
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT use , ip FROM users WHERE use = %s", (use,))

    ro = cursor.fetchall()
    for r in ro:
        logging.debug("user duplicate")

        print('_'*20+"User Duplicate"+'_'*20)
        print(r)
        i = 1
    cursor.close()
    conn.close()
    return i


def delet(use):  # for delete user in database for check user exist or not exist
    global i
    i = 0
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT use , ip FROM users WHERE use = %s", (use,))

    ro = cursor.fetchall()
    for r in ro:
        i = 1
        print(r)
    if i == 1:
        cursor.execute("DELETE FROM users WHERE use = %s", (use,))
        conn.commit()
        print("DELETE OK")

    cursor.close()
    conn.close()
    return i


def deletall():  # delete all user in table
    global i
    i = 0
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    conn.commit()
    print("All user Deleted :(")
    cursor.close()
    conn.close()


def show():

    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT use , ip FROM users")
    ro = cursor.fetchall()
    if list(ro).__len__() == 0:
        logging.info("empty database")

        print("There Are No Users")

    else:
        logging.info("show all user")

        for r in ro:
            print(r)

    cursor.close()
    conn.close()


def finderr():
    k = []
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT ip FROM users")
    ro = cursor.fetchall()
    try:
        ipr = ipaddress.IPv4Network(subnet)

        for i in ro:

            k.append(i[0])

        for ip in ipr.hosts():
            if str(ip) not in k:
                return (str(ip))
    except Exception:
        return None
    cursor.close()
    conn.close()


def check():
    global errordhcp
    global errorsql

    if creattbl() == 1:
        errorsql = 1

    if finderr() == 1:
        errordhcp = 1

    else:

        creattbl()


def dotenv():
    global errordhcp
    if not os.path.exists('.env'):
        logging.debug("not exist .envfile")
        errordhcp = 1
        with open('.env', 'w') as envfile:
            envfile.write("""#symple ip/subnet:
#'192.168.0.0/24'
SUBNET=''
#database connection
DATABASE=''
USER=''
PASSWORD=''
HOST=''
PORT=''""")
            logging.info(
                "create .envfile and write necessary enviroment variables")

    else:
        logging.debug("exist .envfile")


dotenv()
creattbl()
check()
