class CompanyNotFound(Exception):
    def __init__(self, company_shortname: str):
        self.shortname = company_shortname


class ItemTypeNotFound(Exception):
    def __init__(self, type_name: str):
        self.type_name = type_name


class StateNotFound(Exception):
    def __init__(self, shortname: str):
        self.shortname = shortname


class ItemAlreadyExists(Exception):
    def __init__(self, token: str):
        self.token = token


class ItemNotFound(Exception):
    def __init__(self, token: str):
        self.token = token


class ItemAlreadyRecycled(Exception):
    def __init__(self, token: str):
        self.token = token