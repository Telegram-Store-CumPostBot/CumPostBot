from errors.ValidationError import ValidationError


class NoFoundKeysError(ValidationError):
    def __init__(self, arg_name, keys):
        self.arg_name = arg_name
        self.keys = keys

    def __str__(self):
        return f'No found keys: {self.keys} in {self.arg_name}'
