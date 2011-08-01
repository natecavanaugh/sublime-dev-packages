import commands
import os
import re
import sublime
import sublime_plugin
import subprocess
import tempfile

TOKEN_NL = '~~NL~~'

def get_method_content(selectedContent, definition):
    match = re.search('(^|[\n])(' + re.escape(definition) + ')([\n])', selectedContent)

    if match:
        start = match.start(2)
        end = get_matching_bracket_index(selectedContent, start)
        return selectedContent[start : end].replace(TOKEN_NL, '\n')
    return ''

def get_matching_bracket_index(selectedContent, openBracketIndex):
    closeBracketIndex = openBracketIndex
    closings = 0
    openings = 0

    for char in selectedContent[openBracketIndex:]:
        closeBracketIndex += 1

        if char == '{':
            openings += 1
        elif char == '}':
            closings += 1

        if closings == openings and openings > 0:
            return closeBracketIndex

def get_method_definition(tag):
    return tag[tag.find('/^') + 2 : tag.find('$/;')]

def normalize_method_definition(selectedContent):
    return re.sub('(\([^)]*\))', lambda match: re.sub('[\n]', TOKEN_NL, match.string[match.start(1) : match.end(1)]), selectedContent)

class SortSelectedMethodsCommand(sublime_plugin.TextCommand):
    def is_enabled(self, *args):
        return self.view.substr(self.view.sel()[0])

    def run(self, edit):
        syntax, extension = os.path.splitext(os.path.basename(self.view.settings().get('syntax')))

        languageMap = {
            "JavaScript": "js",
            "Java": "Java"
        }

        if syntax in languageMap:
            language = languageMap[syntax]
        else:
            language = syntax

        allowComma = [ "JavaScript" ]

        for region in self.view.sel():
            selectedContent = self.view.substr(region)
            selectedContent = normalize_method_definition(selectedContent)
            tmpFile = tempfile.NamedTemporaryFile()
            tmpFile.write(selectedContent)
            tmpFile.seek(0)

            tags = os.popen('ctags --language-force=%(language)s -f - %(path)s' % { "language": language, "path": tmpFile.name }).readlines()

            symbols = []

            for tag in tags:
                symbols.append(get_method_content(selectedContent, get_method_definition(tag)))

            methods = []

            for (index, symbol1) in enumerate(symbols):
                add = True

                for symbol2 in symbols:
                    if symbol1 != symbol2 and symbol2.find(symbol1) > -1:
                        add = False
                        break

                if add == True:
                    methods.append(symbol1)

            glue = ',\n\n'

            if syntax not in allowComma:
                glue = '\n\n'

            tmpFile.close()

            self.view.replace(edit, region, glue.join(methods))