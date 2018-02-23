import re,urllib.request
request = urllib.request.urlopen('https://www.reddit.com/r/nbastreams/comments/7x5n9c/game_thread_san_antonio_spurs_utah_jazz_210000_et/')
result = request.read().decode()
for item in re.findall(r'<form action="#" class="usertext warn-on-unload"[^>]+>.*?<p>(.*?)</p>.*?</form>', result,re.DOTALL):
    print(item)
