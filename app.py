import os
import urllib.parse
import genanki
import requests
from dotenv import load_dotenv

load_dotenv()
LANG=os.getenv('LEXICALA_LANG')
RAPIDAPI_KEY=os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST=os.getenv('RAPIDAPI_HOST')

my_deck = genanki.Deck(
  int(os.getenv('ANKI_DECK_ID')),
  os.getenv('ANKI_DECK_NAME'),
)

my_model = genanki.Model(
  int(os.getenv('ANKI_MODEL_ID')),
  os.getenv('ANKI_MODEL_NAME'),
  fields=[
    {'name': 'Word'},
    {'name': 'Definition'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Word}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
    },    
		{
      'name': 'Card 2',
      'qfmt': '{{Definition}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Word}}',
    },
  ])

headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST
}

with open("wordlist.txt", "r") as f:
	for word in f:
		_word = word.strip()

		url=f"https://{RAPIDAPI_HOST}/search"
		querystring = { "text": _word, "language": LANG }

		response = requests.get(url, headers=headers, params=querystring)
		responseObject=response.json()
		print(responseObject)
		my_note = genanki.Note(
			model=my_model,
			fields=[_word, responseObject['results'][0]['senses'][0]['definition']])

		my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file('output.apkg')
