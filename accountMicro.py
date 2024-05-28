import zmq
import sqlite3
import signal
import threading
import os
import json


def signal_term(signal, frame):
        print("Received termination.")
        os._exit(1)


def signal_handler():
        signal.signal(signal.SIGINT, signal_term)
        while True:
            pass

def setup_database():
    """"""
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (username TEXT UNIQUE, password TEXT)''')
    connection.commit()
    connection.close()

def add_user(username, password):
    """"""
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()

def check_user(username, password):
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM user WHERE username=?', (username,))
    data = cursor.fetchone()
    connection.close()
    if data is None:
        return 'username_error'
    elif data[0] == password:
        return 'valid'
    else:
        return 'password_error'

def main_function():
    """"""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:8321')
    setup_database()

    while True:
        message = socket.recv_json()
        message = json.loads(message)
        print(message['type'])
        if message['type'] == 'login':
            result = check_user(message['username'], message['password'])
            if result == 'valid':
                response = 'Login successful'
            elif result == 'username_error':
                response = 'Invalid username'
            elif result == 'password_error':
                response = 'Invalid password'
            else:
                response = 'Login failed'
        elif message['type'] == 'create_account':
            result = add_user(message['username'], message['password'])
            response = 'account created successfully' if result else 'Error: Username already exists'
        else:
            response = 'Unknown command'

        socket.send_string(response)

if __name__ == "__main__":
    thread = threading.Thread(target=main_function)
    thread.start()
    signal_handler()