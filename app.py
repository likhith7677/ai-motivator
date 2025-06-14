from flask import Flask, render_template, url_for, request, redirect
import random

app = Flask(__name__)

# Movie recommendations for each mood with OTT platforms
movies = {
    "happy": {
        "Telugu": [
            ("Bommarillu", "YouTube"),
            ("Nuvvu Naaku Nachav", "JioCinema"),
            ("Sarangapani Jathakam", "Prime Video"),
            ("Attarintiki Daredi", "Netflix"),
            ("Mahanati", "Amazon Prime Video"),
            ("Fidaa", "Netflix"),
            ("Pellichoopulu", "Netflix")
        ],
        "Kannada": [
            ("Kirik Party", "JioCinema"),
            ("Googly", "Amazon Prime Video"),
            ("Simple Agi Ondh Love Story", "Amazon Prime Video"),
            ("Rama Rama Re", "Netflix"),
            ("Bell Bottom", "Amazon Prime Video")
        ],
        "English": [
            ("The Pursuit of Happyness", "Netflix"),
            ("Zootopia", "Disney+"),
            ("Forrest Gump", "Netflix"),
            ("The Intouchables", "Amazon Prime Video"),
            ("Paddington", "Netflix")
        ],
        "Tamil": [
            ("Anniyan", "Netflix"),
            ("Ghajini", "Amazon Prime Video"),
            ("Boss Engira Bhaskaran", "Amazon Prime Video"),
            ("Soodhu Kavvum", "Netflix"),
            ("Raja Rani", "Disney+ Hotstar")
        ],
        "Malayalam": [
            ("Drishyam", "Amazon Prime Video"),
            ("Premam", "Netflix"),
            ("Bangalore Days", "Amazon Prime Video"),
            ("Ohm Shanthi Oshaana", "Netflix"),
            ("Ustad Hotel", "Amazon Prime Video")
        ],
        "Hindi": [
            ("3 Idiots", "Netflix"),
            ("Queen", "Amazon Prime Video"),
            ("Zindagi Na Milegi Dobara", "Netflix"),
            ("Dil Chahta Hai", "Amazon Prime Video"),
            ("Barfi!", "Netflix")
        ]
    },
    "sad": {
        "Telugu": [
            ("Malleswari", "Amazon Prime Video"),
            ("Manasantha Nuvve", "Amazon Prime Video"),
            ("Seethamma Vakitlo Sirimalle Chettu", "Amazon Prime Video"),
            ("Nuvvu Leka Nenu Lenu", "Amazon Prime Video"),
            ("Godavari", "Amazon Prime Video")
        ],
        "Kannada": [
            ("Dia", "Amazon Prime Video"),
            ("Sanju Weds Geetha", "Amazon Prime Video"),
            ("Lucia", "Amazon Prime Video")
        ],
        "English": [
            ("Forrest Gump", "Netflix"),
            ("A Beautiful Mind", "Amazon Prime Video")
        ],
        "Tamil": [
            ("Autograph", "Amazon Prime Video"),
            ("Vaaranam Aayiram", "Netflix")
        ],
        "Malayalam": [
            ("Ustad Hotel", "Amazon Prime Video"),
            ("Charlie", "Netflix")
        ],
        "Hindi": [
            ("Taare Zameen Par", "Netflix"),
            ("Barfi", "Amazon Prime")
        ]
    },
    "bored": {
        "Telugu": [
            ("Ala Modalaindi", "Netflix"),
            ("Julayi", "Amazon Prime")
        ],
        "Kannada": [
            ("Victory", "Netflix"),
            ("Simple Aagi Ondu Love Story", "Amazon Prime")
        ],
        "English": [
            ("Jumanji", "Amazon Prime"),
            ("Inception", "Netflix")
        ],
        "Tamil": [
            ("Boss Engira Bhaskaran", "Amazon Prime"),
            ("Soodhu Kavvum", "Netflix")
        ],
        "Malayalam": [
            ("Ohm Shanthi Oshaana", "Netflix"),
            ("Bangalore Days", "Amazon Prime")
        ],
        "Hindi": [
            ("Hera Pheri", "Netflix"),
            ("3 Idiots", "Netflix")
        ]
    }
}

# YouTube playlists for each mood (by language)
playlists = {
    "happy": {
        "Telugu": "https://youtube.com/playlist?list=PL7potaX-C8RizOF3rsZV-bkbYR7cnXG13&si=51GaoKYulG03EUBV",
        "Kannada": "https://youtube.com/playlist?list=PL7potaX-C8RizZ3BknUV_2sC8ohfAmnbD&si=x5FHd02dQJVXsoOD",
        "Tamil": "https://youtube.com/playlist?list=PL7potaX-C8RgxY7tvctl56U8_EDG_HTkg&si=BNSL-OJlSTwH2df-",
        "Malayalam": "https://youtube.com/playlist?list=PL7potaX-C8RjxlzB0cjz6gWjvFQAasS51&si=OHl3xhpPT2-s8ikY",
        "Hindi": "https://youtube.com/playlist?list=PL7potaX-C8RguhTlTXcXTAJbUv2zMhFAa&si=7hDM-u2ZeSTL-5d8",
        "English": "https://youtube.com/playlist?list=PL7potaX-C8RjjKMpHZWaE1XAFEh-2QCiS&si=cZVUdcBHiKMACdbE"
    },
    "sad": {
        "Telugu": "https://youtube.com/playlist?list=PL7potaX-C8RiCpw8-eTFgOQnXSITLVrQa&si=EazvoNMWLRsmR28A",
        "Kannada": "https://youtube.com/playlist?list=PL7potaX-C8RgX3qmL-Fo6TebnQad-izCG&si=7cTVFB-lMc_ikLGA",
        "Tamil": "https://youtube.com/playlist?list=PL7potaX-C8Rgqy52BpHEZJoI5MSCD4WCk&si=SmSxSWr3KHnrK5je",
        "Malayalam": "https://youtube.com/playlist?list=PL7potaX-C8RjpUbPNX9nvH50eObybDUhg&si=Xk9bPY00qfsh1345",
        "Hindi": "https://youtube.com/playlist?list=PL7potaX-C8RhHwBrcocrQlV_AXJLY4-dS&si=YL0xFgnA7OImzQ7l",
        "English": "https://youtube.com/playlist?list=PL7potaX-C8RiKOlglcB9BdPMxR8Ho4VDH&si=o_4WQw4QtySsWrtt"
    },
    "bored": {
        "Telugu": "https://youtube.com/playlist?list=PL7potaX-C8RiRAxPyQMFCHtSVtCpGpr-T&si=8f5AIrqm7pd3B9ga",
        "Kannada": "https://youtube.com/playlist?list=PL7potaX-C8RgJF30RPaNPfweF1AHwaTgQ&si=Aug972Ki7Bz-lfs7",
        "Tamil": "https://youtube.com/playlist?list=PL7potaX-C8RhK2OXaTTNoIWkwPC6NLd6V&si=thebxpPciK41Mzbm",
        "Malayalam": "https://youtube.com/playlist?list=PL7potaX-C8RiPMbEVL2hNzhypQWQD87iB&si=_daX1I7psT5Y54mM",
        "Hindi": "https://youtube.com/playlist?list=PL7potaX-C8RiIXsTVib7mDI0x7ZaUizYh&si=g5EeWsvDeIMm2fmJ",
        "English": "https://youtube.com/playlist?list=PL7potaX-C8RhTc03rdIPOAsPDDvdZPTYz&si=Q0d5QsTWvKLnAX2i"
    }
}

# Short stories YouTube playlist (common for all moods)
short_stories_playlist = "https://www.youtube.com/playlist?list=PLShortStoriesPlaylist"

# Games per mood
games = {
    "happy": {
        "Tic-Tac-Toe": "https://playtictactoe.org/",
        "Memory Game": "https://www.memozor.com/memory-games/for-kids"
    },
    "sad": {
        "snake game": "https://slither.io",
        "Add puzzle ": "https://slither.io"
    },
    "bored": {
        "Chrome Dinosaur Game": "https://elgoog.im/dinosaur/",
        "Guess the Word": "https://skribbl.io"
    }
}

@app.route('/')
def entry_page():
    return render_template('entry.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/mixed')
def mixed():
    return render_template('mixed.html')

@app.route('/mood/<mood>')
def mood_page(mood):
    if mood in movies:
        # Randomly pick one movie per language
        movie_suggestions = {lang: random.choice(movies[mood][lang]) for lang in movies[mood]}
        return render_template('mood.html',
                               mood=mood,
                               movies=movie_suggestions,
                               playlists=playlists[mood],
                               games=games[mood],
                               short_stories=short_stories_playlist)
    else:
        return "Invalid mood selection!"

@app.route('/mood/mixed/<mixed_mood>')
def mixed_mood_page(mixed_mood):
    # Redirect to normal mood page for happy, sad, bored
    if mixed_mood in ['happy', 'sad', 'bored']:
        return redirect(url_for('mood_page', mood=mixed_mood))
    else:
        return "Invalid selection in mixed mood!"

if __name__ == '__main__':
    app.run(port=5002)