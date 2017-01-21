from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Repl(GridLayout):

    def __init__(self, **kwargs):
        super(Repl, self).__init__(**kwargs)

        self.cols = 2
        self.codeHistory = ""

        self.output = TextInput(multiline=True)
        self.add_widget(self.output)
        
        clear_btn = Button(text='Clear', size_hint_x=None, width=100)
        def clear(instance):
            self.output.text = ""
        clear_btn.bind(on_press=clear)
        self.add_widget(clear_btn)

        self.input = TextInput(multiline=True)
        self.add_widget(self.input)

        run_btn = Button(text='Run', size_hint_x=None, width=100)
        def run(instance):
            self.output.text += ">>> " + self.input.text + "\n"
            self.output.text += self.run_script(self.input.text) + "\n"

            self.input.text = ""
            self.input.focus = True
        run_btn.bind(on_press=run)
        self.add_widget(run_btn)

    def run_script(self, code):
        import sys
        from StringIO import StringIO
        import traceback
        # run script

        try:
            self.old_stdout = sys.stdout
            self.redirected_output = sys.stdout = StringIO()
            try:
                print eval(self.codeHistory + "\n" + code)
            except:
                exec(self.codeHistory + "\n" + code)

            sys.stdout = self.old_stdout
            self.result = self.redirected_output.getvalue()
            self.codeHistory += code + "\n"
        except Exception, e:
            self.errorstring = traceback.format_exc()
            self.result = ("ERROR: " + self.errorstring)
        return self.result[:-1]

class Python2Repl(App):
    def build(self):
        return Repl()


if __name__ == '__main__':
    Python2Repl().run()
