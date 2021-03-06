import libtcodpy as libtcod
from logic.menu_main import MenuMain
from logic.menu_manager import MenuManager

screen_width = 75
screen_height = 75
limit_fps = 30

menu_manager = MenuManager(MenuMain(screen_width, screen_height))

libtcod.console_disable_keyboard_repeat()

libtcod.console_set_custom_font('cp437_10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(screen_width, screen_height, 'RogueP pre-dev', False)
libtcod.sys_set_fps(limit_fps)

while not libtcod.console_is_window_closed():
	#behavior_manager.update_behaviors(entities)
	if not menu_manager.loop(round(libtcod.sys_get_last_frame_length()*1000)):
		break