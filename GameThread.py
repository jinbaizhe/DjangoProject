import urllib.request
import re
import time
from datetime import datetime
import sqlite3
import http.cookiejar
import threading


def openURL(url):
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    }
    request = urllib.request.Request(url, headers=headers)
    response = opener.open(request)
    result = response.read().decode()
    return result


class CurrentAllGame:
    def __init__(self):
        pass
    def getCurrentAllGame(self):
        result = openURL('https://www.reddit.com/r/nbastreams/',)
        result_list = []
        for item in re.findall(r'<p\s*class="title">\s*<a[^>]*?href="([^"]*)"[^>]*>([^<]*)</a>', result, re.DOTALL):
            if item[1].startswith('Game Thread') or item[1].startswith('Event Thread'):
                result_list.append((item[1], 'https://www.reddit.com' + item[0]))
        return result_list

    def getGameInfo(self, gameUrl):
        result = openURL(gameUrl)
        streamList = []
        for item in re.findall(r'<form action="#" class="usertext warn-on-unload"[^>]+>.*?<p>(.*?)</p>.*?</form>', result, re.DOTALL):
            if re.search(r'(?:HD|hd|SD|sd)', item):
                streamList.append(item)
        return streamList


def updateDB():
    currentAllGame = CurrentAllGame()
    while True:
        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            game_list = currentAllGame.getCurrentAllGame()
            for content, url in game_list:
                cursor.execute('select * from NBAStream_game where title=? and date=?',
                               (content, datetime.date(datetime.now())))
                item = cursor.fetchone()
                if item:
                    gameid = item[0]
                else:
                    cursor.execute("insert into NBAStream_game(title,date) values(?,?)",
                                   (content, datetime.date(datetime.now())))
                    gameid = cursor.lastrowid
                cursor.execute(
                    'update NBAStream_gameinfo set orderid=? where game_id=?',
                    (-1, gameid))
                for index, stream in enumerate(currentAllGame.getGameInfo(url), 1):
                    try:
                        cursor.execute('select * from NBAStream_gameinfo where content=? and game_id=?', (stream, gameid))
                        temp = cursor.fetchone()
                        if temp:
                            game_info_id = temp[0]
                            cursor.execute('update NBAStream_gameinfo set orderid=? where id=?',
                                           (index, game_info_id))
                        else:
                            cursor.execute('insert into NBAStream_gameinfo(content,game_id,orderid) values(?,?,?)',
                                           (stream, gameid, index))
                    except Exception as e:
                        print(str(e))
        except Exception as e:
            time.sleep(60)
            print(str(e))
            continue
        else:
            print('success')
        cursor.close()
        conn.commit()
        conn.close()
        time.sleep(60*5)


t = threading.Thread(target=updateDB, daemon=True)
t.start()
t.join()
