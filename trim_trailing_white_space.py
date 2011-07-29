import sublime, sublime_plugin

class TrimTrailingWhiteSpace(sublime_plugin.TextCommand):
    def run(self, edit):
        trailing_white_space = self.view.find_all("[\t ]+$")
        trailing_white_space.reverse()
        edit = self.view.begin_edit()

        for r in trailing_white_space:
            self.view.erase(edit, r)
        self.view.end_edit(edit)