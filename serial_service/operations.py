import requests
from pydub import AudioSegment
from pydub.playback import play


def run_operation(op_id, data):
    if op_id == 'check_card':
        return check_card(data['card'])


def check_card(card):
    res = requests.post('http://176.99.11.114/card', {'card': card})
    res = res.text.split(';')
    return res[0]


def play_sound(sounds):
    for sound in sounds:
        sound = AudioSegment.from_mp3(sound)
        play(sound)
