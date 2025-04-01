import json
import logging
import requests

from config import env

logger = logging.getLogger(__name__)

url=f"https://{env['RAPIDAPI_HOST']}/search"
headers = {
	'x-rapidapi-key': env['RAPIDAPI_KEY'],
	'x-rapidapi-host': env['RAPIDAPI_HOST']
}

def lexicala_get(word):
	word = word.strip()
	querystring = { "text": word, "language": env['LEXICALA_LANG'] }
	logger.debug([url, headers, querystring])

	if env.get('TESTING') == "True":
		responseObject = json.load(open('exampleresponse.json'))
	else:			
		response = requests.get(url, headers=headers, params=querystring)
		responseObject=response.json()

	logger.debug(responseObject)
	return [responseObject, response]