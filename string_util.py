import sublime, sublime_plugin, re

def uncamelize(stringAsCamelCase, separator = "-"):
	if stringAsCamelCase is None:
		return None

	pattern = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')

	return pattern.sub(lambda m: m.group()[:1] + separator + m.group()[1:], stringAsCamelCase).lower()

def camelize(string, separator = "-_ "):
	if string is None:
		return None

	pattern = re.compile('[' + separator + '](\w)', re.IGNORECASE)

	return pattern.sub(lambda m: m.group()[1:].upper(), string)


class CamelizeTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	for region in self.view.sel():
			self.view.replace(edit, region, camelize(self.view.substr(region)))

class UncamelizeTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	for region in self.view.sel():
			self.view.replace(edit, region, uncamelize(self.view.substr(region)))

