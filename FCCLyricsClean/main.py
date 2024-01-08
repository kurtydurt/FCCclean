import selenium
import csv
from selenium import webdriver
#import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def initiate_driver():
    # instantiate options
    #options = webdriver.ChromeOptions()
    # run browser in headless mode

    # instantiate driver
    # options = webdriver.ChromeOptions()
    # options.add_argument("start-maximized")
    # #options.add_argument("--headless=new")
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # driver = uc.Chrome(options=options)
    options = webdriver.ChromeOptions()
    # run browser in headless mode
    #options.add_argument("--headless=new")
    options.add_argument('--disable-blink-features=AutomationControlled')
    # instantiate driver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)
    return driver


def big_scrape(songs, driver=initiate_driver()):
    search_results = {}
    for song in songs:
        search_results[song] = lyrics_scrape(driver, f'https://genius.com/search?q={song}')
    driver.quit()
    return search_results


def lyrics_scrape(driver, url):
    #driver.set_page_load_timeout(10)
    driver.implicitly_wait(1)
    driver.get(url)

    try:
        driver.find_element(By.TAG_NAME, 'search-result-items').click()
        print("clicked")

        lyrics = driver.find_element(By.CLASS_NAME, 'Lyrics__Container-sc-1ynbvzw-1').text
        artist = driver.find_element(By.CLASS_NAME, 'HeaderArtistAndTracklistdesktop__Artist-sc-4vdeb8-1').text
        song_title = driver.find_element(By.CLASS_NAME, 'SongHeaderdesktop__Title-sc-1effuo1-8').text
    except selenium.common.exceptions.NoSuchElementException:
        artist, song_title, lyrics = "Not Found", "Not Found", "Not Found"
    return artist, song_title, lyrics


def bad_words_checker(songs, bad_words):
    search_to_lyrics = big_scrape(songs)
    search_to_contains_word = []
    for search, lyrics in search_to_lyrics.items():
        contains_bad_word = 'False'
        for word in bad_words:
            if word in lyrics[2]:
                contains_bad_word = 'True'
        search_to_contains_word.append([search, lyrics[0], lyrics[1], contains_bad_word])
    with open('potty_words.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for entry in search_to_contains_word:
            writer.writerow(entry)


if __name__ == "__main__":
    songs = []
    with open('source.csv', 'r', newline='') as source:
        reader = csv.reader(source)
        for row in reader:
            if row[0]:
                x = " ".join(row)
                songs.append(x)

    bad_words_checker(songs, ["Fuck", "fucked", "fucking", "shit", "bitch", "piss", "cocksucker", "god damn", "goddamn", "asshole", "motherfucker", "cunt"])
