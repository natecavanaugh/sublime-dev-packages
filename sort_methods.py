import os
import re
import sublime
import sublime_plugin
import subprocess

def get_matching_bracket_index(text, openBracketIndex):
    closeBracketIndex = openBracketIndex
    closings = 0
    openings = 0

    for char in text[openBracketIndex:]:
        closeBracketIndex += 1

        if char == '{':
            openings += 1
        elif char == '}':
            closings += 1

        if closings == openings and openings > 0:
            return closeBracketIndex

def run_cmd(cmd, cwd = '.'):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=cwd)
	p.wait()

	return p.stdout.readlines()

class SortMethodsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        basename, extension = os.path.splitext(filename)

        for region in self.view.sel():
            selectedContent = self.view.substr(region)

            tmpFile = open("tmp" + extension, 'w+')

            tmpFile.write(selectedContent)
            tmpFile.read()

            tags = run_cmd(['ctags', '-f', '-', tmpFile.name])

            tmpFile.close()
            os.remove(tmpFile.name)

            methods = []

            for tag in tags:
                definition = tag[tag.find('/')+2:tag.rfind('/')-1]

                start = selectedContent.find(definition)
                end = get_matching_bracket_index(selectedContent, start)

                methods.append(selectedContent[start:end])

            self.view.replace(edit, region, ',\n\n'.join(methods))