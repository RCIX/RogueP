import libtcodpy as libtcod
from model.attribute import AttributeTag
from ui.frame import Frame
from model.action import ActionTag
from vec2d import Vec2d
from ui.ui_event import UIEventType


class FrameActionsOverlay(Frame):

	def __init__(self, root_console_width, root_console_height, world_x_start, world_y_start, frame_manager):
		#TODO manage offset of code
		Frame.__init__(self, root_console_width, root_console_height, root_console_width - world_x_start, root_console_height - world_y_start, frame_manager)
		self.world_x_start = world_x_start
		self.world_y_start = world_y_start
		self.entity_manager = frame_manager.parent_menu.entity_manager
		self.actions = []
		libtcod.console_set_default_background(self.console, libtcod.Color(255, 0, 255))
		libtcod.console_set_key_color(self.console, libtcod.Color(255, 0, 255))

	def handle_ui_event(self, event):
		if event.type == UIEventType.ActionQueueAdd:
			self.actions.append(event.data['action'])
		elif event.type == UIEventType.ActionQueueRemove:
			self.actions.remove(event.data['action'])
		elif event.type == UIEventType.ActionQueueClear:
			self.actions = []

	#is mostly temporary proof of concept - will need to be a lot more nuanced to render library executes, memory scans, etc etc
	def draw(self):
		libtcod.console_clear(self.console)
		player = filter(lambda ent: ent[1].get_attribute(AttributeTag.Player), self.entity_manager.entities.iteritems())[0][1]
		player_position = player.get_attribute(AttributeTag.WorldPosition).data['value']
		position_delta = Vec2d(0, 0)

		cur_action_number = 1
		for queued_action in self.actions:
			if queued_action.type == ActionTag.ProgramMovement:
				position_delta += queued_action.data['value']
				draw_info = player.get_attribute(AttributeTag.DrawInfo)
				target_position = player_position + position_delta
				libtcod.console_put_char_ex(self.console, target_position.x, target_position.y, str(cur_action_number), libtcod.blue, libtcod.black)
			elif queued_action.type == ActionTag.DamagePosition:
				target_position = None
				if 'relative' in queued_action.data:
					target_position = player_position + position_delta + queued_action.data['relative']
				else: #assume there's an absolute position listed. proibably should be generating a nice error here but that can be done soon(TM)
					target_position = queued_action.data['absolute']
				libtcod.console_put_char_ex(self.console, target_position.x, target_position.y, str(cur_action_number), libtcod.dark_red, libtcod.black)
			cur_action_number += 1
			if cur_action_number != 0 and cur_action_number == 10:
				cur_action_number = 0

		libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, self.world_x_start, self.world_y_start)