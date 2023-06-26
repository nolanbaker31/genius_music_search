import requests
import time
from bs4 import BeautifulSoup
import re
import lxml
import cchardet
import pickle

def retrieve_albums(artist_link):
    response = requests.get(artist_link)
    soup = BeautifulSoup(response.content, "lxml") #replace with html.parser if lxml doesnt work
    album_divs = soup.select(".thumbnail_grid-grid_element")
    albums = []
    
    i = 0
    # Get links to top 2 albums per artist
    while len(albums) < 2 and i < len(album_divs):
        album_link = album_divs[i].find("a")['href']
        albums.append(album_link)
        i += 1
    return albums

def extract_song_links(album_links): # Get link to each song within the albums
    all_songs = []
    for link in album_links:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        song_links = []
        songs = soup.find_all('div', {'class': 'chart_row-content'})
        for song in songs:
            link = song.find('a')['href']
            song_links.append(link)
        all_songs.extend(song_links)
    return all_songs

def extract_lyrics(song_links): # Extract lyrics to songs
    all_lyrics = []
    all_links = []
    all_song_names = []
    for link in song_links:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        try: # if song name not available, use blank name
            song_name = soup.select_one('h1[class^="SongHeaderWithPrimis__Title"] span').text.strip()
        except AttributeError:
            song_name = ''

        # Extract the song description and lyrics
        song_description = soup.select_one('div[class^="SongDescription__Content"]')
        lyrics_container = soup.select_one('div[class^="Lyrics__Container"], .song_body-lyrics')

        # Combine the song description and lyrics into a single value
        if song_description and lyrics_container:
            t = song_description.get_text(strip=True, separator='\n') + '\n' + lyrics_container.get_text(strip=True, separator='\n')
        elif song_description:
            t = song_description.get_text(strip=True, separator='\n')
        elif lyrics_container:
            t = lyrics_container.get_text(strip=True, separator='\n')
        else:
            t = ''

        # Remove unecessary text
        t = re.sub(r'\n', ' ', t)
        t = re.sub(r'\[.*?\]', '', t)


        # Add the lyrics to the lists
        if t:
            all_lyrics.append(t)
        else:  # If lyrics not available, add blank lyrics
            all_lyrics.append('')
        all_links.append(link)
        all_song_names.append(song_name)

    return all_song_names, all_lyrics, all_links

start_time = time.time()

#Get starting links
url = "https://genius.com/artists-index/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "lxml")
links = soup.select(".character_index_list-link")

# Extract the links for artists A through Z
a_to_z_links = [link['href'] for link in links if link.get_text() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

# Retrieve links to popular artists for each letter
popular_artists_links = []
for link in a_to_z_links:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "lxml")
    popular_artists = soup.select(".artists_index_list-popular_artist")
    popular_artists_links.extend([artist.a['href'] for artist in popular_artists])

lyrics = [] # holds ALL song lyrics & descriptions
song_links = [] # hold the link to EVERY song
song_names = [] # holds the name to EVERY song
for artist_link in popular_artists_links:
    album_song_lyrics = []
    album_song_links = []
    print(f"Retrieving albums for {artist_link}:")
    albums = retrieve_albums(artist_link) # Retrieve the artist's album links
    songs = extract_song_links(albums) # Retrieve the album's song links
    album_song_names, artist_lyrics, album_song_links = extract_lyrics(songs) # Retrieve the song names, song lyrics & song links for each song
    # Add lyrics, links & name to lists
    lyrics.extend(album_song_lyrics)
    song_links.extend(album_song_links)
    song_names.extend(album_song_names)
    # Save periodically in case of crash
    with open('song_dict.pkl', 'wb') as fp:
        pickle.dump(lyrics, fp)
        print('dictionary successfuly saved')

    with open('song_links.pkl', 'wb') as fp:
        pickle.dump(song_links, fp)

    with open('song_names.pkl', 'wb') as fp:
        pickle.dump(song_names, fp)
    
    

end_time = time.time() - start_time

print(end_time)

#Store lists in .pkl files
with open('song_dict.pkl', 'wb') as fp:
    pickle.dump(lyrics, fp)
    print('dictionary successfuly saved')

with open('song_links.pkl', 'wb') as fp:
    pickle.dump(song_links, fp)

with open('song_names.pkl', 'wb') as fp:
    pickle.dump(song_names, fp)
