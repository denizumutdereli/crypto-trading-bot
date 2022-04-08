import os
import sys
import re

def yes_or_no(question):
	prompt = f'{question} (y/n): '
	answer = input(prompt).strip().lower()
	if answer not in ['y', 'n']:
		print(f'{answer} this answer is not correct, can you answer again...')
		return yes_or_no(question)
	if answer == 'y':
		return True
	elif answer == 'n':
		return False