from src.serializers import Notice


class TxtNoticesWriter:
    def __init__(self, filepath):
        self.filepath = filepath

    def write(self, data):
        if isinstance(data, Notice):
            self._write_one(data)
        elif isinstance(data, list):
            for item in data:
                self._write_one(item)

    def _write_one(self, item):
        with open(self.filepath, mode='a', encoding='utf-8') as f:
            f.write(item.for_txt())

