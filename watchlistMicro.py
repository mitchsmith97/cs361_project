import sqlite3
import random
import zmq
import json
import signal
import os
import threading


def signal_term(signal, frame):
        print("Received termination.")
        os._exit(1)


def signal_handler():
        signal.signal(signal.SIGINT, signal_term)
        while True:
            pass
def server():

    conn = sqlite3.connect('watchlist.db')

    cursor1 = conn.cursor()

    #cursor1.execute('''CREATE TABLE IF NOT EXISTS watchlist
    #                    (username text, title_id INTEGER)''')

    conn2 = sqlite3.connect('imdb.db')
    cursor2 = conn2.cursor()


    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:1357")


    while True:
        rows = []
        data = socket.recv_string()
        print(f"Received: {data}")
        json_data = json.loads(data)

        if json_data['req_type'] == 'view':
            cursor1.execute('''SELECT title_id
            FROM watchlist
            WHERE username = ?''',
            (json_data['username'],))

            movie_ids = cursor1.fetchall()

            if movie_ids:
                movie_ids = [row[0] for row in movie_ids]
                print(movie_ids)
                placeholders = ','.join('?' * len(movie_ids))
            
                query = f'''
                SELECT t.primary_title as title, t.premiered as year, r.rating as rating
                FROM titles t
                JOIN ratings r ON t.title_id = r.title_id
                WHERE t.title_id IN ({placeholders})
                '''
                cursor2.execute(query, movie_ids)
                results = cursor2.fetchall()
                print(results)

                response = json.dumps(results)
                socket.send_string(response)

            else:
                response = "No results"
                socket.send_string(response) 
            
        
        elif json_data['req_type'] == 'search':
            print(json_data['partial_title'])
            cursor2.execute('''
            SELECT t.primary_title, t.runtime_minutes, r.rating, r.votes, t.premiered, t.title_id
            FROM titles t INNER JOIN ratings r ON (r.title_id = t.title_id)
            WHERE t.type = 'movie' AND r.votes > 10000 
            AND t.primary_title LIKE ?
            ORDER BY r.votes DESC
            LIMIT 10''',
            ("%" + json_data['partial_title'] + "%",))

            rows = cursor2.fetchall()

            search_json = []
            for row in rows:
                print(row)
                json_inst = {
                    'title_ID': row[5],
                    'title': row[0],
                    'year': row[4],
                    'rating': row[2]
                }
                search_json.append(json_inst)
                

            json_resp = json.dumps(search_json)
            socket.send_json(json_resp)    

        elif json_data['req_type'] == 'insert':
            try:
                cursor1.execute('''INSERT INTO watchlist
                (username, title_ID)
                VALUES (?, ?)''',
                (json_data['username'], json_data['title_ID'],))
                conn.commit()
                socket.send_string("Inserted!")
            except:
                socket.send_string("Unable to add")




if __name__ == '__main__':
    thread = threading.Thread(target=server)
    thread.start()
    signal_handler()