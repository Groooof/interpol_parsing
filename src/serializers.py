

class Notice:
    def __init__(self, name, forename, date_of_birth, nationalities, link, img):
        self.name = name
        self.forename = forename
        self.date_of_birth = date_of_birth
        self.nationalities = nationalities
        self.link = link
        self.img = img

    def for_txt(self):
        return f'NAME: {self.name}\n' + \
               f'FORENAME: {self.forename}\n' + \
               f'DATE_OF_BIRTH: {self.date_of_birth}\n' + \
               f'NATIONALITIES: {", ".join(self.nationalities)}\n' + \
               f'LINK: {self.link}\n' + \
               f'IMG_LINK: {self.img}\n' + \
                '--------------------------------------------------\n'


class NoticeSerializer:
    def __init__(self, data):
        self.data = data

    def get_obj(self):
        if isinstance(self.data, list):
            return [self._data_to_obj(item) for item in self.data]
        return self._data_to_obj(self.data)

    @staticmethod
    def _data_to_obj(data: dict):
        return Notice(name=data['name'],
                      forename=data['forename'],
                      date_of_birth=data['date_of_birth'],
                      nationalities=data['nationalities'] if isinstance(data['nationalities'], list) else str(data['nationalities']),
                      link=data['_links']['self']['href'],
                      img=data['_links']['thumbnail']['href'] if 'thumbnail' in data['_links'] else '')

