"""
This script is used to scrape singer (in this case Queen and 
Simon and Garfunkel) and their corresponding lyric from
https://www.lyrics.com and save lyrics to folder queen and 
simon_garfunkel with each song in one txt file.
"""
import requests 
from tqdm import tqdm
import time
import numpy as np
from bs4 import BeautifulSoup

import os
import glob
from fuzzywuzzy import fuzz


# procedure : 
# - Go to the page listing all songs of your favourite artist on lyrics.com.
# - Copy the URL
# - Use the requests module to download that page
# - Examine the HTML code and look for links to songs
# - Extract all links using Regular Expressions or BeautifulSoup
# - Use the requests module to download song page (with not redundent song names) containing lyrics
# - Save in artist folder text files, one songe page per text file


# function : get song urls
def get_song_urls(artist, artist_url):
    ''' input : artist str, artist_url str
        return : song_urls list '''

    request_artist_url = requests.get(artist_url)
    prefix = 'https://www.lyrics.com'
    lyric_soup = BeautifulSoup(request_artist_url.text, 'html.parser') 
    song_urls = []
    for album in lyric_soup.find('div', class_="tdata-ext").find_all('tbody'):
        song_urls += [prefix + x['href'] for x in album.find_all('a')] 
    return song_urls


# function : get song urls drop redundent ones with exact song name match
def get_song_urls_dr(artist, artist_url):
    ''' input : artist str, artist_url str
        return : song_urls list '''

    request_artist_url = requests.get(artist_url)
    prefix = 'https://www.lyrics.com'
    lyric_soup = BeautifulSoup(request_artist_url.text, 'html.parser') 
    song_urls = []
    song_titles = []
    for album in lyric_soup.find('div', class_="tdata-ext").find_all('tbody'):
        # append url if not duplicate song
        for i_title in np.arange(len(album.find_all('a'))):
            title = album.find_all('a')[i_title].text
            if title not in song_titles:
                song_titles += [title]
                song_urls += [prefix + x['href'] for x in album.find_all('a')] 
    return song_urls


# function : get song urls drop redundent ones with fuzzywuzzy 90% match
def get_song_urls_drf(artist, artist_url):
    ''' input : artist str, artist_url str
        return : song_urls list '''

    request_artist_url = requests.get(artist_url)
    prefix = 'https://www.lyrics.com'
    lyric_soup = BeautifulSoup(request_artist_url.text, 'html.parser') 
    song_urls = []
    song_titles = ['']
    for album in lyric_soup.find('div', class_="tdata-ext").find_all('tbody'):
        # append url if not duplicate song
        for i_title in np.arange(len(album.find_all('a'))):
            title = album.find_all('a')[i_title].text
            if title not in song_titles: # first layer filter to save time
                best_match = 0
                best_match_title = ''
                for given_title in song_titles:
                    score = fuzz.ratio(title.lower(), given_title.lower())
                    # TODO : check from fuzz import process; process.dedupe, threshold
                    # for more elegant solution
                    if  score > best_match:
                        best_match = score
                        best_match_title = given_title
                if best_match < 90:      
                    song_titles += [title]
                    x = album.find_all('a')[i_title]
                    song_urls += [prefix + x['href']]
                #else:
                    #print(f'fuzzy title match : {title} vs {best_match_title}') # for testing removed titles
            #else:
                #print(f'exact title match : {title}')
    return song_urls


# function : save song pages to txt files
def save_song_page(artist, song_urls, path):
    ''' input : artist str
                song_url list containing song urls of an artist
                path str
        do : save song page to txt files with filename start with artist to path artist folder'''

    if not os.path.exists(f'{path}/{artist}'):
        os.makedirs(f'{path}/{artist}')
    for i in tqdm(np.arange(len(song_urls))):
        time.sleep(0.5)
        one_song_request = requests.get(song_urls[i])
        open(f'{path}/{artist}/{artist}_song_{i}.txt', 'w').write(one_song_request.text)


# function : strip song page and save lyrics to txt file
def save_lyric_files(artist, path):
    ''' input : artist str
                path str
        do : save striped lyric to txt files with filename start with artist to path artist folder'''
    
    if not os.path.exists(path + f'/{artist}/'):
        os.makedirs(path + f'/{artist}/')

    path_filenames = (path + f'/{artist}/' + f'{artist}_song_*.txt')
    song_files = [f for f in sorted(glob.glob(path_filenames))]
    for i in tqdm(np.arange(len(song_files))):
        # save the text in the song txt files into variable text
        text = open(song_files[i], 'r').read()
        lyric_soup = BeautifulSoup(text, 'html.parser') # text here is the content of txt file, and is equivalent to requests.text
        # strip
        if lyric_soup.find('pre') is not None:
            open(f'./{artist}/{artist}_lyric_{i}.txt', 'a').write(lyric_soup.find('pre').text)

# run all steps for two artists


if __name__ == '__main__':
    artists = ['simon_garfunkel', 'queen']
    artist_urls = ['https://www.lyrics.com/artist/Simon-%26-Garfunkel/5431', 'https://www.lyrics.com/artist/Queen/5205']
    path = os.getcwd()

    for n in np.arange(len(artists)): 
        artist = artists[n]
        artist_url = artist_urls[n]

        # get song urls
        song_urls = get_song_urls_drf(artist, artist_url)
        print(len(song_urls))

        # save song page 
        save_song_page(artist, song_urls, path)

        # save striped lyric to txt files
        save_lyric_files(artist, path)

    # simon_garfunkel : no drop 1875, drop exact match 283, drop fuzzywuzzy match 204 remained
    # queen : before droping over 3800, after 578
    # some of 204 and 578, the html lyric body pre is none and skipped -> in the end two artist together 738 lyrics