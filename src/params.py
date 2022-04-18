import copy


class BaseParams:
    def __init__(self, empty=None, **kwargs):
        # параметр empty исползуется для определения того, какие значения должны принимать неуказанные поля
        # если None - поле не добавляется в список параметров
        self._empty = empty
        self._params_names = self.__get_class_params()
        self.__set_obj_params(**kwargs)

    def _get_dict(self):
        """ Получает и возвращает поля и их значения указанные в __init__ из списка полей объекта.
            Только те поля, которые указаны в качестве значений полей абстрактного класса """
        return {param[1]: getattr(self, param[0])
                for param in self._params_names.items()
                if getattr(self, param[0]) is not None}

    def __set_obj_params(self, **params):
        """ Присваивает полям, указанным в абстрактном классе значения, указанные в __init__ """
        for param in self._params_names.keys():
            self.__dict__[param] = params[param] if param in params else self._empty

        # for param in params.items():
        #     if param[0] in self._params_names.keys():
        #         self.__dict__[param[0]] = param[1]

    @classmethod
    def __get_class_params(cls):
        """ Получает и возвращает поля и их значения указанные в абстрактном классе """
        return {param[0]: param[1] for param in cls.__dict__.items() if not param[0].startswith('_')}

    def __get_obj_params(self):
        """ Получает и возвращает поля и их значения указанные в абстрактном классе """
        return {param[0]: param[1] for param in self.__dict__.items() if not param[0].startswith('_')}

    def __call__(self, **kwargs):
        """ Возвращает копию объекта с дополнительными параметрами """
        new_obj = copy.deepcopy(self)
        params = new_obj.__get_obj_params()
        params.update(kwargs)
        new_obj.__set_obj_params(**params)
        return new_obj


class RequestParams(BaseParams):
    @property
    def dict(self):
        return self._get_dict()

    @property
    def query_str(self):
        return '?' + '&'.join([param[0] + '=' + param[1]
                               for param in self._get_dict().items()])

    def __str__(self):
        return '\n'.join([f'{param[0]}: {param[1]}' for param in self._get_dict().items()])


class InterpolParams(RequestParams):
    family_name = 'name'
    forename = 'forename'
    nationality = 'nationality'
    gender = 'sexId'
    min_age = 'ageMin'
    max_age = 'ageMax'
    wanted_by = 'arrestWarrantCountryId'
    keyword = 'freeText'
    cards_per_page = 'resultPerPage'
    page = 'page'
    