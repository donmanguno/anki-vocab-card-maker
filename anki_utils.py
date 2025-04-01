import logging

from config import env
from anki.collection import Collection

logger = logging.getLogger(__name__)

col = Collection(env['ANKI_COLLECTION_PATH'])
deck_id = col.decks.id(env['ANKI_DECK_NAME'])
col.decks.select(deck_id)
model = col.models.by_name(env['ANKI_MODEL_NAME'])

def add_card_to_anki(word, definition):
	if not model:
		logger.error(f"Error: Model '{env['ANKI_MODEL_NAME']}' not found.")
		col.close()
		return
	
	note = col.new_note(model)
	note.deck_id = deck_id