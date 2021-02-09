title:Talon Draft
-

^submit$:
	content = user.get_draft_window_content()
	user.close_draft_window()
	sleep(100ms)
	insert(content)
