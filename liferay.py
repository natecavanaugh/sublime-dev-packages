import string_util as su
import sublime
import sublime_plugin

class WrapInJspLanguageTaglibCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	for region in self.view.sel():
    		self.view.replace(edit, region, '<liferay-ui:message key="' + su.uncamelize(su.camelize(self.view.substr(region))) + '" />')