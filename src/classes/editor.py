import tkinter as tk
from tkinter.filedialog import asksaveasfilename


class EditorWindow:
    def __init__(self, name, text, edit):
        self.root = tk.Tk()
        self.name = name
        self.content = text
        self.edit = edit
        self.text = tk.Text(self.root)

    def run(self):
        self.root.title(self.name)
        self.text.insert(tk.INSERT, self.content)
        self.text.grid()

        def saveas():
            self.content = self.text.get("1.0", "end-1c")
            self.root.destroy()

        if (self.edit == True):
            button = tk.Button(self.root, text="Salvar", command=saveas)
            button.grid()
        else:
            self.text.config(state=tk.DISABLED)

        self.root.mainloop()
