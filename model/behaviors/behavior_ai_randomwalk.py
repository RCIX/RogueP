import libtcodpy as libtcod
from vec2d import Vec2d
from model.action import Action, ActionTag
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from math import sqrt, fabs
from ui.frame_world import FrameWorld
from behavior import Behavior


class AIRandomWalkBehavior(Behavior):
	def __init__(self, manager):
		Behavior.__init__(self, manager)

	def generate_actions(self):
		events = []

		for entity in filter(lambda ent: ent.get_attribute(AttributeTag.HostileProgram), self.manager.entities):
			#TODO: pull an RNG out into entity manager so I can properly save and control rng generation for the purposes of 
			new_position = Vec2d(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
			#mildly biases horizontal movement 
			if new_position[0] != 0:
				new_position[1] = 0
			events.append(Action(ActionTag.ProgramMovement, {'target_id':entity.id, 'value':new_position}))

		return events