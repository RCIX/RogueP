# added specifically to make floating point division apply to code in bar position calculation
from __future__ import division

import libtcodpy as libtcod
import xp_loader
import gzip
from vec2d import Vec2d

from ui.strings.command_responses import command_response_table
from ui.frame import Frame
from ui.ui_event import UIEvent, UIEventType

# pseudoterminal frame - sits on the left and displays current input and input history to the player - primary interface to the actual game
# also manages keyboard input and generates events to the game state to signal commands
class FramePseudoTerminal(Frame):

	def __init__(self, root_console_width, root_console_height, terminal_width, terminal_height, frame_manager):
		# constants and initialization
		self.prompt_string = "X:\\>"
		self.input_command = ""
		self.blinking_cursor = "_"
		self.cursor_blink_delay = 500
		self.cursor_timer = 0
		self.console_command_history = []
		self.console_max_history_length = terminal_height - 2
		self.input_enabled = True

		Frame.__init__(self, root_console_width, root_console_height, terminal_width, terminal_height, frame_manager)
		#-1 to account for border tile
		self.max_command_size = self.width - len(self.prompt_string) - 1 

		libtcod.console_set_key_color(self.console, libtcod.Color(255, 0, 255))

	def update(self, delta):
		key = libtcod.console_check_for_keypress(True)

		self.update_blinky_cursor(delta)

		if self.input_enabled:

			if len(self.input_command) < self.max_command_size:
				if key.vk == libtcod.KEY_CHAR:
					self.input_command += chr(key.c)
				#add numbers, because these are separate keycodes for some godforsaken reason
				#really, libtcod?
				elif key.vk == libtcod.KEY_0:
					self.input_command += '0'
				elif key.vk == libtcod.KEY_1:
					self.input_command += '1'
				elif key.vk == libtcod.KEY_2:
					self.input_command += '2'
				elif key.vk == libtcod.KEY_3:
					self.input_command += '3'
				elif key.vk == libtcod.KEY_4:
					self.input_command += '4'
				elif key.vk == libtcod.KEY_5:
					self.input_command += '5'
				elif key.vk == libtcod.KEY_6:
					self.input_command += '6'
				elif key.vk == libtcod.KEY_7:
					self.input_command += '7'
				elif key.vk == libtcod.KEY_8:
					self.input_command += '8'
				elif key.vk == libtcod.KEY_9:
					self.input_command += '9'
				elif key.vk == libtcod.KEY_UP:
					self.input_command += chr(24)
				elif key.vk == libtcod.KEY_DOWN:
					self.input_command += chr(25)
				elif key.vk == libtcod.KEY_LEFT:
					self.input_command += chr(27)
				elif key.vk == libtcod.KEY_RIGHT:
					self.input_command += chr(26)
			#send command
				elif key.vk == libtcod.KEY_ENTER and self.input_command != "":
					self.add_line_to_history(self.prompt_string + self.input_command)
					self.frame_manager.parent_menu.handle_input_command(self.input_command)
					self.input_command = ""
				elif key.vk == libtcod.KEY_BACKSPACE:
					self.input_command = self.input_command[:-1]

	def update_blinky_cursor(self, delta):
		self.cursor_timer += delta
		if self.cursor_timer > self.cursor_blink_delay:
			self.cursor_timer = 0
			if self.blinking_cursor == "_":
				self.blinking_cursor = " "
			else:
				self.blinking_cursor = "_"

	def handle_ui_event(self, event):
		if event.type == UIEventType.InputDisabled:
			self.input_enabled = False
		elif event.type == UIEventType.InputEnabled:
			#add a blank line
			self.add_line_to_history('') 
			self.input_enabled = True
		elif event.type == UIEventType.InvalidCommand and len(event.data['command']) > 1:
			#if it was a non single character command and the result was not found, try splitting the command out into characters and trying each one
			#TODO move this into command strings file
			self.add_line_to_history('Event sequence:')
			for char in list(event.data['command']):
				self.frame_manager.parent_menu.handle_input_command(char)
		elif event.type in command_response_table:
			if 'command' in event.data:
				self.add_line_to_history(command_response_table[event.type].format(event.data['command']))
			else:
				self.add_line_to_history(command_response_table[event.type])

	def add_line_to_history(self, line):
		#remove the oldest history line - the best way I can think of to do it right now
		if len(self.console_command_history) >= self.console_max_history_length:
			self.console_command_history.reverse()
			self.console_command_history.pop()
			self.console_command_history.reverse()

		self.console_command_history.append(line)


	def draw(self):
		libtcod.console_clear(self.console)

		libtcod.console_set_default_background(self.console, libtcod.Color(255,0,255))
		libtcod.console_rect(self.console, 0, 0, self.width, self.height, libtcod.BKGND_SET)
		libtcod.console_set_default_background(self.console, libtcod.black)

		libtcod.console_set_alignment(self.console, libtcod.LEFT)

		current_height = 0
		for line in self.console_command_history:
			libtcod.console_print(self.console, 0, current_height, line)
			current_height += 1
		if self.input_enabled:
			libtcod.console_print(self.console, 0, current_height, self.prompt_string + self.input_command + self.blinking_cursor)

		libtcod.console_vline(self.console, self.width - 1, 0, self.height)

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, self.root_console_height - self.height)