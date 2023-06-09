from .commons import reader
from .constant import *

def init_tags(tag_dict):
    new = {**tag_dict, **CLASSICS_OPERATORS}

    for item in new:
        TAGS[item] = new[item]

def catch_error(code: int, line: str, args: tuple=()) -> None:
    error = ERRORS[code].copy()

    if args != ():
        message = error.message
        for key, value in args:
            message = message.replace(key, value)

        error.message = message

    error.launch(line)

class GLD:
    def __init__(self, path, game):
        self.game = game
        self.path = path

        if path is not None:
            self.raw = reader(path).replace('\n', '').replace('\r', '').strip().split(";")

        self.code = []
        self.line_interpret = 0

    def lexer(self):
        for line_number, line in enumerate(self.raw):
            in_tag = False
            line_content = None
            last = None

            in_content = -1
            tag_name = ''
            content = ''

            actual = []

            for item in line:

                if item == '>':
                    in_tag = False
                    actual[-1]["tag"] = tag_name
                    tag_name = ''

                if item == ']':
                    if content != '' and len(actual[in_content]["content"]) == 0:
                        actual[in_content]["content"].append(content.strip())
                    last = actual.pop(-1)
                    content = ''
                    in_content -= 1

                if in_tag:
                    tag_name += item

                if item == '[':
                    in_content += 1

                if in_content and not in_tag and item not in '<>[]':
                    content += item

                if item == '<':
                    in_tag = True
                    to_add = {"tag": '', "content": []}

                    if len(actual) > 0:
                        actual[in_content]["content"].append(to_add)

                    if line_content is None:
                        line_content = to_add

                    actual.append(to_add)


            if last is not None and last != line_content:
                catch_error(103,line_number)

            if in_content < -1:
                catch_error(101,line_number)

            elif in_content > -1:
                catch_error(100,line_number)


            self.code.append(line_content)

    def interpret(self):
        for item in self.code:
            self.interpreteur(item)
            self.line_interpret += 1

    def interpreteur(self, code=None):
        if code is None:
            return

        if TAGS == {}:
            catch_error(1, None)


        if code["tag"] not in TAGS:
            catch_error(102, self.line_interpret, (('$tag$',code["tag"]),))

        return TAGS[code["tag"]](code["content"], self.game, self.interpreteur)