import os
import sys
import winsound
from classes import Settings as settings

def play(appType):
	if settings.sounds == 1:
		if appType == 'opening':
			winsound.PlaySound(settings.workingPath + "\\sounds\\opening.wav", winsound.SND_FILENAME)
		elif appType == 'sent':
			winsound.PlaySound(settings.workingPath + "\\sounds\\sent.wav", winsound.SND_FILENAME)
		elif appType == 'alert':
			winsound.PlaySound(settings.workingPath + "\\sounds\\alert.wav", winsound.SND_FILENAME)
		else:
			winsound.PlaySound(settings.workingPath + "\\sounds\\info.wav", winsound.SND_FILENAME)