import requests
from src.params import InterpolParams
from src.response import RedNoticesResponse
import json


def get_json_file(path):
    with open(path) as f:
        return json.load(f)


class BaseNoticesApi:
    url = ''
    limit = 160
    min_age_limit = 0
    max_age_limit = 120
    genders = get_json_file('./data/cuts/genders.json')
    countries = get_json_file('./data/cuts/countries.json')

    def search(self, params: InterpolParams) -> RedNoticesResponse:
        response = requests.get(self.url, params=params.dict)
        return RedNoticesResponse(response)

    def search_max(self, params: InterpolParams) -> RedNoticesResponse:
        return self.search(params(cards_per_page=self.limit, page=1))


class RedNoticesApi(BaseNoticesApi):
    url = 'https://ws-public.interpol.int/notices/v1/red'



