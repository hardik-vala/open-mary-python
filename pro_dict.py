"""
Pronounciation dictionary.
"""

from xml.dom import minidom


class PronounciationDictionaryGenerator():
	"""
	Generates pronounciation dictionaries.
	"""

	def __init__(self):
		pass

	def parse_open_mary_xml(self, open_mary_xml_path):
		"""
		Extracts the pronounciation dictionary contained in an Open Mary .xml
		file.

		@param open_mary_xml_path - Path to Open Mary .xml file.
		@return Dictionary mapping words to their phonetic pronounciation (as a
			string).
		"""

		dom = minidom.parse(open_mary_xml_path)

		pro_dict = {}
		for token in dom.getElementsByTagName('t'):
			if token.firstChild:
				token_text = token.firstChild.data.strip()

				if 'ph' in dict(token.attributes):
					pronounciation = token.attributes['ph'].value

					if token_text in pro_dict:
						assert pro_dict[token_text] == pronounciation
					else:
						pro_dict[token_text] = pronounciation

		return pro_dict
