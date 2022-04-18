from src.api import RedNoticesApi, BaseNoticesApi
from src.writer import TxtNoticesWriter
from src.params import InterpolParams
from math import floor


class BaseCriteriaParser:
    _base_params = InterpolParams()

    def __init__(self, nested=None, api: BaseNoticesApi = RedNoticesApi()):
        self._nested = nested
        self._api = api

    def run(self, prev_params=None, prev_total=-1):
        pass


class CriteriaParser:
    _base_params = InterpolParams()

    def __init__(self, names, values, nested=None, api: BaseNoticesApi = RedNoticesApi()):
        self._params_names = names
        self._params_values = values
        self._nested = nested
        self._api = api

    def run(self, prev_params=None, prev_total=-1):
        full_data = list()
        count = 0
        for value in self._params_values:
            print(f'Parsing records for {self._params_names}={value}:')

            params = prev_params if prev_params is not None else self._base_params
            params = params(**{param: value for param in self._params_names})
            result = self._api.search_max(params)
            print(f'Total: {result.total}')

            if (result.count == result.total) or (self._nested is None):
                data = result.data
            else:  # elif result.count < result.total:
                data = self._nested.run(params, result.total)

            full_data.extend(data)
            count += len(data)
            print(f'Found: {len(data)}')
            if count == prev_total:
                break

        return full_data


class AgeParser(BaseCriteriaParser):
    def __init__(self, age_range, nested=None, api: BaseNoticesApi = RedNoticesApi()):
        super().__init__(nested=nested, api=api)
        self._age_range = age_range

    def run(self, prev_params=None, prev_total=-1):
        if prev_params is None:
            params = self._base_params(min_age=self._age_range[0], max_age=self._age_range[1])
        else:
            min_age = prev_params.min_age or self._age_range[0]
            max_age = prev_params.max_age or self._age_range[1]
            params = prev_params(min_age=min_age, max_age=max_age)

        print(f'Parsing records for age from {params.min_age} to {params.max_age}:')

        result = self._api.search_max(params)

        if result.count != result.total:  # если лимит превышен
            if params.min_age != params.max_age:  # если можем разделить диапазон возраста
                avg_age = self.__split_age((params.min_age, params.max_age))
                data1 = self.run(params(max_age=avg_age))
                data2 = self.run(params(min_age=avg_age+1))
                full_data = data1 + data2
            elif self._nested is not None:  # иначе, если есть вложенный парсер
                full_data = self._nested.run(params, result.total)
            else:  # иначе - возвращаем то что есть
                full_data = result.data
        else:
            full_data = result.data

        return full_data

    @staticmethod
    def __split_age(age_range):
        return floor((age_range[0] + age_range[1]) / 2)


class Parser:
    def __init__(self, api: RedNoticesApi, writer=TxtNoticesWriter):
        self.api = api
        self.writer_class = writer

    def parse(self, wanted_by_countries: list or str):
        if wanted_by_countries == 'all':
            wanted_by_countries = self.api.countries.keys()

        gender_parser = CriteriaParser(('gender',), self.api.genders.keys())
        # age_parser = CriteriaParser(('min_age', 'max_age'), range(self.api.min_age_limit, self.api.max_age_limit + 1), gender_parser)
        age_parser = AgeParser((18, 120), gender_parser)

        full_data = []
        for country in wanted_by_countries:
            country_parser = CriteriaParser(('wanted_by',), (country,), age_parser)
            country_data = country_parser.run()
            full_data.extend(country_data)

            writer = self.writer_class(f'./results/{country}.txt')
            if country_data: writer.write(country_data)
            print(f'*** For country {country} was found {len(country_data)} notices! ***')

        return full_data


