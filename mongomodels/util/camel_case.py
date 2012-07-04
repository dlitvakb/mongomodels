import re


class CamelCaseConverter(object):

    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')

    def __init__(self, text):
        self.text = text

    def convert(self):
            s1 = self.first_cap_re.sub(r'\1_\2', self.text)
            return self.all_cap_re.sub(r'\1_\2', s1).lower()
