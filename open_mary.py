"""
Module facilitates translating texts into phonemes using Open Mary's online API.

@author: Hardik
"""

import requests, urllib

from xml.dom import minidom
from xml.parsers.expat import ExpatError


class OpenMaryClient():
	"""
	Open Mary client.
	"""

	# Mary TTS server URL.
	URL = "http://mary.dfki.de:59125/process"

	# Post request headers.
	HEADERS = {
		"Content-type": "application/x-www-form-urlencoded",
		"Accept": "text/plain"
	}

	# (US) English locale.
	EN_LOCALE = "en_US"
	# French locale.
	FR_LOCALE = "fr"
	# German locale.
	GERM_LOCALE = "de"
	# Italian locale.
	IT_LOCALE = "it"
	# Russian locale.
	RU_LOCALE = "ru"
	# Swedish locale.
	SV_LOCALE = "sv"
	# Telugu locale.
	TE_LOCALE = "te"
	# Turkish locale.
	TU_LOCALE = "tr"

	def __init__(self):
		pass

	def locales(self):
		"""
		Returns a list of supported locales.

		@return List of supported locales.
		"""

		return [
			OpenMaryClient.EN_LOCALE,
			OpenMaryClient.FR_LOCALE,
			OpenMaryClient.GERM_LOCALE
		]

	def translate(self, text, locale):
		"""
		Translates raw text in a specified locale to phonemes by posting to
		the Mary TTS server. The response is directly returned.

		(Repeated calls to this method should be interweaved with timeouts in
		order to prevent overloading of the Mary TTS server.)

		@param text - Raw text to translate.
		@param locale - Locale of raw text.
		@raises requests.exceptions.HTTPError if the Mary TTS server responds
			with an error.
		@return XML response from the Mary TTS server as a string.
		"""

		data = urllib.urlencode({
			"INPUT_TYPE": "TEXT",
			"OUTPUT_TYPE": "PHONEMES",
			"INPUT_TEXT": text,
			"LOCALE": locale
		})

		r = requests.get(OpenMaryClient.URL, data,
			headers=OpenMaryClient.HEADERS)

		# We good.
		if r.status_code == requests.codes.ok:
			return r.text
		# Internal server error.
		elif r.status_code == 500:
			try:
				dom = minidom.parseString(r.text)
			# Usually a missing closing p tag.
			except ExpatError as e:
				dom = minidom.parseString(r.text.replace('<pre>', '</p><pre>'))

			try:
				r.raise_for_status()
			except requests.exceptions.HTTPError as e:
				pre_tags = dom.getElementsByTagName('pre')
				server_exception_msg = pre_tags[0].firstChild.data.strip()

				raise requests.exceptions.HTTPError("%s\nServer Exception: %s" %
					(str(e), server_exception_msg))
		else:			
			r.raise_for_status()


class OpenMaryXMLParser():
	"""
	Parses XML reponses produced by the Mary TTS server.
	"""

	def __init__(self):
		pass

	def __parse_dom_to_text(self, open_mary_xml_dom):
		para_prons = []
		for para in open_mary_xml_dom.getElementsByTagName('p'):
			sent_prons = []
			for sent in para.getElementsByTagName('s'):
				token_prons = []
				for token in sent.getElementsByTagName('t'):
					if token.firstChild:
						token_text = token.firstChild.data.strip()

						if 'ph' in dict(token.attributes):
							pronounciation = token.attributes['ph'].value
							token_prons.append(pronounciation)
						else:
							token_prons.append(token_text)

				sent_prons.append(' '.join(token_prons))

			para_prons.append('\n'.join(sent_prons))

		return '\n\n'.join(para_prons)

	def parse_string_to_text(self, open_mary_xml_str):
		"""
		Parses the phonetic pronounciations contained in an Open Mary XML string
		and outputs them according to the original text, with each token
		replaced with its pronounciation.

		The formatting of the output text is also normalized such that phonemes
		are separated by a single space, sentences by a single CR, and
		paragraphs by a double CR.

		@param open_mary_xml_str - Open Mary XML as a string.
		@return Pronounciation text.
		"""

		dom = minidom.parseString(open_mary_xml_str)
		return self.__parse_dom_to_text(dom)

	def parse_file_to_text(self, open_mary_xml_path):
		"""
		Parses the phonetic pronounciations contained in an Open Mary .xml and
		outputs them according to the original text, with each token replaced
		with its pronounciation.

		The formatting of the output text is also normalized such that phonemes
		are separated by a single space, sentences by a single CR, and
		paragraphs by a double CR.

		@param open_mary_xml_path - Path to Open Mary .xml file.
		@return Pronounciation text.
		"""

		dom = minidom.parse(open_mary_xml_path)
		return self.__parse_dom_to_text(dom)
	