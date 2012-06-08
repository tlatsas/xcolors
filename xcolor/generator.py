# -*- coding: utf-8 -*-
import re
import os
import sys
from jinja2 import Template
from glob import glob

class Generator(object):

    # map color names with codes
    code = {
        # black
        'color0': '30m',
        'color8': '1;30m',
        # red
        'color1': '31m',
        'color9': '1;31m',
        # green
        'color2': '32m',
        'color10': '1;32m',
        # yellow
        'color3': '33m',
        'color11': '1;33m',
        # blue
        'color4': '34m',
        'color12': '1;34m',
        # magenta
        'color5': '35m',
        'color13': '1;35m',
        # cyan
        'color6': '36m',
        'color14': '1;36m',
        # white
        'color7': '37m',
        'color15': '1;37m'
    }

    #bg_code_map = {
    #    'color0': '40m',
    #    'color1': '41m',
    #    'color2': '42m',
    #    'color3': '43m',
    #    'color4': '44m',
    #    'color5': '45m',
    #    'color6': '46m',
    #    'color7': '47m'
    #}

    colors = {
        0: 'color0',
        1: 'color8',
        2: 'color1',
        3: 'color9',
        4: 'color2',
        5: 'color10',
        6: 'color3',
        7: 'color11',
        8: 'color4',
        9: 'color12',
        10: 'color5',
        11: 'color13',
        12: 'color6',
        13: 'color14',
        14: 'color7',
        15: 'color15'
    }

    default_fg = 'dcdcdc'
    default_bg = '1c1c1c'

    def __init__(self, theme_folder, output_folder, text='txt'):
        self.theme_folder = theme_folder
        self.output_folder = output_folder
        self.text = text

        try:
            self.themes = os.listdir(self.theme_folder)
        except os.error:
            print("Error reading from path: {0}".format(self.theme_folder))

        # load template passed in jinja2
        path, name = os.path.split(__file__)
        tpl = os.path.join(path, 'template')
        try:
            with open(tpl, 'r') as f:
                tpl_contents = f.read()
        except IOError:
            print("Error opening template file for reading")
        self.tpl = Template(tpl_contents)

    def _parse_theme_file(self, f):
        contents = {}

        # this filters only valid lines
        valid = re.compile(r'^\*|^\s*\*!')

        # matches lines with rgb values
        # eg:
        #   *color4: rgb:ff/ff/ff
        rgb = re.compile(
                r'^\*(?P<name>[a-zA-Z]+\d{,2}):'\
                        '[ \t\n\r\f\v]*rgb:(?P<value>[a-zA-Z0-9/]*)')

        # matches lines with hex values
        # eg:
        #   *color4: #ffffff
        hexadecimal = re.compile(
                r'^\*(?P<name>[a-zA-Z]+\d{,2}):'\
                        '[ \t\n\r\f\v]*#(?P<value>[a-zA-Z0-9]{6})')

        for line in f:
            # make regex easier
            line = line.strip()

            if valid.match(line):
                # try matchig a line with rgb values
                match = rgb.match(line)
                if match:
                    contents[match.group('name')] = match.group('value').replace('/', '')
                    continue

                # rgb match failed, try with hex
                match = hexadecimal.match(line)
                if match:
                    contents[match.group('name')] = match.group('value')
        return contents

    def _write_html_file(self, name, rgb):
        if 'foreground' not in rgb.keys():
            rgb['foreground'] = self.default_fg

        if 'background' not in rgb.keys():
            rgb['background'] = self.default_bg

        # append extension to theme filename
        name = '.'.join((name, 'html'))
        with open(os.path.join(self.output_folder, name), 'w') as f:
            f.write(self.tpl.render(rgb=rgb, colors=self.colors,
                                    text=self.text, code=self.code))

    def generate_files(self):
        for theme in self.themes:
            with open(os.path.join(self.theme_folder, theme), 'r') as f:
                rgb = self._parse_theme_file(f)
            self._write_html_file(theme, rgb)
        return glob("{0}/*.html".format(self.output_folder.rstrip('/')))

    def cleanup(self):
        raise NotImplemented


if __name__ == '__main__':
    print "This is not intented to run stand-alone, import to use"
    sys.exit(1)

