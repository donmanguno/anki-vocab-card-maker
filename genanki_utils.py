import logging
import genanki

from config import env

logger = logging.getLogger(__name__)

my_deck = genanki.Deck(
  int(env['ANKI_DECK_ID']),
  env['ANKI_DECK_NAME'],
)
my_model = genanki.Model(
  int(env['ANKI_MODEL_ID']),
  env['ANKI_MODEL_NAME'],
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

def add_card_to_anki(word, senses):
  word = word.strip()
  definition = ""
  for idx, sense in enumerate(senses, start=1):
    definition += f"{idx}. {sense['definition']}\n"
  definition = definition.rstrip()

  logger.debug(definition)
  my_note = genanki.Note(
		model=my_model,
		fields=[word, definition])
  my_deck.add_note(my_note)

def write_to_deck(file):
  genanki.Package(my_deck).write_to_file(file)