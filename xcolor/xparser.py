import re

class Xparser(object):
    """Match color line definitions from Xdefaults style files"""

    @classmethod
    def valid(cls, line):
        """line starting with '*' or '*' with whitespace prepended are valid
        also, lines starting with "Urxvt*" "Urxvt." are valid
        """
        pattern = r'^\s*[a-zA-Z]*[\*\.]'
        return True if re.match(pattern, line) else False

    @classmethod
    def rgb(cls, line):
        """matches lines with values using slashes and the rgb keyword

        *color4: rgb:ff/ff/ff
        Urxvt*color4: rgb:ff/ff/ff
        Urxvt.color4: rgb:ff/ff/ff
        """
        pattern = r'(?:^\*|^\w*[\*\.])\.*(?P<name>[a-zA-Z]+\d{,2})\s*:\s*'\
            'rgb:(?P<value>[a-zA-Z0-9/]*)'

        match = re.match(pattern, line)
        if match:
            return dict(name=match.group('name'), value=match.group('value').replace('/', ''))

        return {}

    @classmethod
    def hex(cls, line):
        """matches lines using the hash symbol before the hex value

        *color4: #ffffff
        Urxvt*color4: #ffffff
        Urxvt.color4: #ffffff
        """
        pattern = r'(?:^\*|^\w*[\*\.])\.*(?P<name>[a-zA-Z]+\d{,2})\s*:\s*'\
            '#(?P<value>[a-zA-Z0-9]{6})'

        match = re.match(pattern, line)
        if match:
            return dict(name=match.group('name'), value=match.group('value'))

        return {}
