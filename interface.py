
from talon import Module
from .draftwindow import DraftWindow

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

	def get_draft_window_content()->str:
		"""retrieve text from draft window"""
		return window.get_content()
