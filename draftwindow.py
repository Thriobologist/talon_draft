from tkinter import *
from tkinter import font
import threading
import socket
import time

class DraftWindow():

	def __init__(self):
		threading.Thread(target=self.spawn, daemon=False).start()

	def spawn(self):
		while True: # recreate the window when closed
			self.gui = Tk()
			self.gui.client(socket.gethostname())
			self.gui.title("Talon Draft")
			w = self.gui.winfo_screenwidth()
			h = self.gui.winfo_screenheight()
			f = font.nametofont("TkFixedFont").actual()

			self.gui.geometry(f"{int(w*0.8)}x{int(h*0.7)}+{int(w*0.1)}+{int(h*0.15)}")
			self.text = Text(self.gui, font=(f['family'], 40), height=1, width=1)
			self.text.pack(side=TOP, fill=BOTH, expand=True)

			# buffers for thread communication
			self.content = ""
			self.insertQueue = []
			self.action = ""

			self.text.tag_add("highlight", "1.0", "1.0")
			self.text.tag_config("highlight", foreground="red")
			self.text.bind("<Any-Motion>", self.on_mouse_move)
			self.text.bind("<Button>", self.on_click)
			self.text.bind("<<Modified>>", self.on_change)
			self.onChangeSentinel = False

			self.statusbar = Label(self.gui, text="status bar", bd=1, relief=SUNKEN, anchor=W)
			self.statusbar.pack(side=BOTTOM, fill=X)

			self.close()
			self.poll()
			self.gui.mainloop()

	def poll(self):
		if len(self.insertQueue) > 0:
			self.text.insert(INSERT, self.insertQueue.pop(0))
		if self.action == "show":
			self.action = ""
			self.gui.deiconify()
			self.gui.lift()
			self.gui.focus_force()
			self.text.focus()
		if self.action == "close":
			self.action = ""
			self.text.delete("1.0", "end")
			self.gui.withdraw()
		self.gui.after(10, self.poll)

	def on_mouse_move(self, event):
		self.text.tag_remove("highlight", "1.0", "end")
		index = self.text.index("@%s,%s" % (event.x, event.y))
		self.text.tag_add("highlight", index + " wordstart", index + " wordend")

	def on_click(self, event):
		index = self.text.index("highlight.first")
		word = self.text.get("highlight.first", "highlight.last")
		if word == '\n':
			return
		self.text.delete("highlight.first", "highlight.last")
		if word[0] == word[0].lower():
			self.text.insert(index, word[0].upper() + word[1:])
		else:
			self.text.insert(index, word[0].lower() + word[1:])

	def on_change(self, event):
		if self.onChangeSentinel:
			self.onChangeSentinel = False
			return
		self.content = self.text.get("1.0", "end-1c")
		self.statusbar['text'] = self.content.replace('\n', '\\n')
		self.onChangeSentinel = True
		self.text.tk.call(self.text._w, 'edit', 'modified', 0)

	def insert(self, string):
		self.insertQueue.append(string)

	def get_content(self):
		return self.content

	def show(self):
		self.action = "show"

	def close(self):
		self.action = "close"










from talon import Module
#from .draftwindow import DraftWindow

mod = Module()

window = DraftWindow()

@mod.action_class
class Actions:

	def show_draft_window():
		"""shows draft window"""
		window.show()

	def close_draft_window():
		"""closes draft window"""
		window.close()
