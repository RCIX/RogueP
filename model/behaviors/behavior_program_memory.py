import libtcodpy as libtcod
from model.action import ActionTag
from model.attribute import Attribute, AttributeTag
from model.entity import Entity
from ui.game.frame_world import WorldRenderType
from behavior import Behavior

#note: an explicit from [] import * because if I don't, using entity_utilities functions in lambdas throws a fit
from model.entity_utilities import *

# TODO: pull this code out into a more generic one for programs
class ProgramMemoryRemoveBehavior(Behavior):
	def remove_memory(self, parent_id, position):
		parent = self.manager.get_entity_by_id(parent_id)
		memory_at_position = filter(lambda ent: is_owned_memory(parent_id, ent), self.manager.get_world_data_for_position(position)['entities'])
		if len(memory_at_position) > 0:
			#will remove multiple copies of memory, best to be safe and do so to trim down on excess floating memory
			#may shoot me in the foot later if i actually have memory duplication bugs somewhere along the line
			for entity in memory_at_position:

				parent.get_attribute(AttributeTag.OwnedMemory).data['segments'].remove(entity)
				self.manager.remove_entity_by_id(entity.id)


	def handle_action(self, action):
		if action.type == ActionTag.ProgramMemoryRemove:
			#going to leave it broken out like this for the moment, if time goes by and I don't need aditional validation logic then ill fold it back into this
			self.remove_memory(action.data['parent_id'], action.data['position'])
		return []


class ProgramMemoryAddBehavior(Behavior):
	def handle_action(self, action):
		if action.type == ActionTag.ProgramMemoryAdd:
			position = action.data['position']
			parent_id = action.data['parent_id']

			world_data_for_position = self.manager.get_world_data_for_position(position)
			if not entities_occupy_position(parent_id, world_data_for_position):
				#todo - consider making this an explicit action instead of just chucking it into the manager? for now, this is fine
				memory_segment = Entity([
						Attribute(AttributeTag.ProgramMemory, {'parent_id': parent_id}),
						Attribute(AttributeTag.Visible),
						Attribute(AttributeTag.WorldPosition, {'value': position}),
						Attribute(AttributeTag.DrawInfo, {'draw_type': WorldRenderType.Memory, 'draw_type': WorldRenderType.Memory, 'z_level': 2})
					])
				self.manager.add_entity(memory_segment)

				parent = self.manager.get_entity_by_id(parent_id)
				parent.get_attribute(AttributeTag.OwnedMemory).data['segments'].append(memory_segment)

		return []