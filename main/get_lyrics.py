import requests
from bs4 import BeautifulSoup


def format_url(str):
    remove = ["-", "'"]
    for char in remove:
        str = str.replace(char, "")
    str = str.replace(" ", "-")
    return(str.lower())


def get_song(song, artist):
    song = format_url(song)
    artist = format_url(artist)
    url = 'http://www.metrolyrics.com/' + song +  '-lyrics-' + artist + '.html'
    return get_lyrics(url)


def get_all_songs(artist):
    artist = format_url(artist)
    sites = []
    page_num = 1
    #Finds how many pages of songs there are
    while page_num > 0:
        url = "http://www.metrolyrics.com/" + artist + "-alpage-%d.html" % page_num
        site = requests.get(url)
        #Adds working sites to sites list (metrolyrics goes to main page if num is greater than num of pages)
        if site.url == url:
            sites.append(site)
            page_num += 1
        else:
            page_num = -1
    lyrics = {}
    print("Found the following songs:")
    for site in sites:
        page = BeautifulSoup(site.text, 'html.parser')
        not_allowed = ['remix', 'mix', 'remaster', 'remastered', 'version', 'live', 'spanish']
        #Finds all links to songs
        for link in page.find_all('a'):
            lnk = link.get('href')
            #Removes invalid links, or link to page of songs
            if lnk == 'http://www.metrolyrics.com/' + artist + '-lyrics.html' or lnk == url or lnk == None:
                continue
            #Removes metrolyrics so we can check if the link contains the string 'lyrics'
            tst = lnk.replace('http://www.metrolyrics.com/', '')
            #Additional checks to make sure link leads to lyrics
            if ('lyrics' in tst
                     and 'https' not in tst
                     and '?' not in tst
                     and "correction" not in tst
                     and artist in tst):
                #Checks if any of the not allowed words are in the song title
                allowed = True
                for word in not_allowed:
                    if word in lnk.lower():
                        allowed = False
                if allowed:
                    name = get_song_name(lnk)
                    words = get_lyrics(lnk)
                    #Checks that there are lyrics for the song, no duplicate titles, no duplicate lyrics
                    if len(words) > 1 and name not in lyrics and words not in lyrics.values():
                        print(name)
                        lyrics[name] = words
    return lyrics


def get_lyrics(link):
    website = requests.get(link)
    code = website.status_code
    if code != requests.codes.ok:
        return
    soup = BeautifulSoup(website.text, 'html.parser')
    txt = soup.find_all('p', {"class":"verse"})
    txt = [part.text.split() for part in txt]
    #Splits list of lists into one list
    txt = [word for part in txt for word in part]
    lyrics = " ".join(txt)
    lyrics = clean_lyrics(lyrics)
    return lyrics


def get_song_name(link):
    website = requests.get(link)
    soup = BeautifulSoup(website.text, 'html.parser')
    header = soup.find('h1').text.split()
    split_indeces = []
    for i, part in enumerate(header):
        if part == '-' or part == 'Lyrics':
            split_indeces.append(i)
    name = header[split_indeces[0] + 1 : split_indeces[1]]
    return(" ".join(name))


def clean_lyrics(lyrics):
    lyrics = lyrics.split()
    lyrics = [lyric for lyric in lyrics if '[' not in lyric and ']' not in lyric]
    return " ".join(lyrics)
