from src.serializers import NoticeSerializer
import requests


class BaseResponse:
    def __init__(self, response: requests.Response):
        self._json = self._get_json(response)

    @staticmethod
    def _get_json(response):
        return response.json()


class RedNoticesResponse(BaseResponse):
    def __init__(self, response):
        super().__init__(response)
        self.data = NoticeSerializer(self._get_data()).get_obj()
        self.count = self._get_count()
        self.total = self._get_total()

    def _get_data(self):
        return self._json['_embedded']['notices']

    def _get_count(self):
        return len(self._json['_embedded']['notices'])

    def _get_total(self):
        return self._json['total']

