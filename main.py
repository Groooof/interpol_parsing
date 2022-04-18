from src.parser import Parser
from src.api import RedNoticesApi
from pprint import pprint


countries_for_parse = ('US', )

api = RedNoticesApi()
parser = Parser(api)
cards = parser.parse(countries_for_parse)

print(f'{len(cards)} cards was found')

# parser.parse('all')  # Все страны
# pprint(api.genders)
# pprint(api.countries)


