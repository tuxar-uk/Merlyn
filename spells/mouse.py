
		
	if "mouse" in words[0]:
		if "click" in words:
			pyautogui.click()
		else:
			x = y = 0
			d = words.split()[2]
			print(d)
			if "up" in words:
				y = -int(d)
			elif "down" in words:
				y = int(d)
			elif "left" in words:
				x = -int(d)
			elif "right" in words:
				x = int(d)
			pyautogui.moveRel(x,y)

	if "how are you" in words:
		speak("I am fine")
