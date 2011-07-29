import sublime
import sublime_plugin
import string_util as su
import subprocess
import re

class OpenAlloyDemoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	fileName = self.view.file_name()

        self.open_url(fileName[fileName.find("alloy-ui/"):])

    def open_url(self, url):
        url = "http://localhost/liferay/%s" % url

        sublime.status_message("Opening file " + url + "...")

        subprocess.Popen(["open", url], stdout=subprocess.PIPE)