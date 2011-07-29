import sublime, sublime_plugin, string_util as su, re

def getVarName(string):
	return su.uncamelize(string, "_").upper()

def getVarValue(string):
	return su.camelize(string)

class ExtractStringsToConstantsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	output = ""
    	wordList = []

    	pattern = re.compile("['\"][a-zA-Z]+['\"]")

    	for region in self.view.sel():
    		selectedContent = self.view.substr(region)

    		for rLine in self.view.lines(region):
    			for word in pattern.findall(self.view.substr(rLine)):
    				strippedWord = re.sub("['\"]", "", word)
    				wordList.append(strippedWord);
    				selectedContent = selectedContent.replace(word, getVarName(strippedWord))

    		self.view.replace(edit, region, selectedContent)

      	wordList.sort(su.strcmp)
      	wordList = list(set(wordList))

    	for word in wordList:
    		name = getVarName(word)
    		value = getVarValue(word)
    		output += name + " = '" + value + "',\n"

		sublime.set_clipboard(output)
		sublime.status_message("Copied extracted words to clipboard.")