import logging

from config import env
from genanki_utils import add_card_to_anki, write_to_deck
from lexicala_scraper import lexicala_get

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
										format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

headers = {
    'x-rapidapi-key': env['RAPIDAPI_KEY'],
    'x-rapidapi-host': env['RAPIDAPI_HOST']
}

WORDLIST_FILENAME = "wordlist.txt"
WORDS_FOUND_FILENAME = "words_found.txt"
WORDS_NOT_FOUND_FILENAME = "words_not_found.txt"

def main():
	words_not_found = []
	words_found = []
	with open(WORDLIST_FILENAME, "r") as wordlist_file:
		wordlist = wordlist_file.read().splitlines()
		for word in wordlist:
			[responseObject, response] = lexicala_get(word)
			if response.status_code == 429:
				logger.warning('rate limited, aborting')
				break
			elif response.status_code == 200 and len(responseObject['results']) > 0:
				try:
					add_card_to_anki(word, responseObject['results'][0]['senses'])
					words_found.append(word)
				except Exception as e:
					logger.error(f"coundn't process word {word}")
					logger.error(e)
					words_not_found.append(word)
			else:
				logger.warning(f"status code {response.status_code} for word {word}")
				words_not_found.append(word)

	
	write_to_deck('output.apkg')

	# cleanup
	with open(WORDS_NOT_FOUND_FILENAME, "a+") as words_not_found_file:
		all_words_not_found = words_not_found_file.read().splitlines()
		for word in words_not_found:
			if word not in all_words_not_found:
				words_not_found_file.write(word + '\n')
				all_words_not_found.append(word)

	with open (WORDS_FOUND_FILENAME, "a+") as words_found_file:
		all_words_found = words_found_file.read().splitlines()
		for word in words_found:
			if word not in all_words_found:
				words_found_file.write(word + '\n')
				all_words_found.append(word)

	with open (WORDLIST_FILENAME, "w") as wordlist_file:
		for word in wordlist:
			if word not in all_words_not_found and word not in all_words_found:
				wordlist_file.write(word + '\n')

if __name__ == '__main__':
	main()