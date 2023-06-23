from pygame import *


font.init()

title_fnt = font.Font("fonts/Caviar_Dreams_Bold.ttf", 32)
title_fg = Color(199, 160, 246)

text_fnt = font.Font("fonts/Caviar_Dreams_Bold.ttf", 18)
text_fg = Color(203, 208, 236)

sysind_fnt = font.Font("fonts/Caviar_Dreams_Bold.ttf", 18)
sysind_fg = Color(203, 208, 236)

subtitle_fnt = font.Font("fonts/Caviar_Dreams_Bold.ttf", 28)
subtitle_fg = Color(203, 208, 236)

radiolist_fnt = font.Font("fonts/CaviarDreams.ttf", 18)
radiolist_idle_fg = Color(203, 208, 236)
radiolist_idle_bg = Color(36, 40, 57)
radiolist_hover_fg = Color(36, 40, 57)
radiolist_hover_bg = Color(98, 80, 123)
radiolist_active_fg = Color(36, 40, 57)
radiolist_active_bg = Color(199, 160, 246)

border_fg = Color(int(203*2/3), int(208*2/3), int(236*2/3))
border_width = 1

main_bg = Color(36, 40, 57)

margin = 12
radiolist_margin = 4
