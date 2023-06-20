from include import include
from parser import parser
from pprint import pprint, pformat
from thread import thread
from pygame import *
from ui_config import *
import rlfs
import ui
import extui
import os, sys
import vnb
import json
import shell
import use8


very_long_text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
       "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
       "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
       "text will disappear underneath the surface"


class Debugger(vnb.NoneDebugger):
	def __init__(self, execer):
		self.execer = execer
		self.pos = []

		init()
		display.init()
		font.init()
		mixer.init()
		self.win = ui.Window(name="VNovell Debugger")
		self.clock = time.Clock()
		self.running = 1
		self.wininit((800,600))

	def wininit(self, size):
		self.win.resize(Vector2(size))
		self.tit = ui.Title(self.win, "VNEngine Debugger", spos=Vector2(1,0))
		self.mas = ui.Container(self.win, Vector2(0,0), Vector2(1,2), Vector2(self.win.rect.w, self.win.rect.h-self.tit.rect.h))
		self.cn1 = ui.Container(self.mas, Vector2(margin,margin), Vector2(0,1), Vector2(self.mas.rect.w/2, self.mas.rect.h), 1)
		self.cn2 = ui.Container(self.mas, Vector2(-margin,margin), Vector2(2,1), Vector2(self.mas.rect.w/2, self.mas.rect.h), 1)
		self.tab = ui.Text(self.cn1,"",spos=video.math.Vector2(1,0),rpos=Vector2(margin,margin),
			size=Vector2(self.mas.rect.w/2-margin*2,self.mas.rect.h-margin*2))
	
	@thread
	def run(self):
		self.gui_part()

	def gui_part(self):
		while self.running:
			self.clock.tick(40)
			for e in event.get():
				if e.type == QUIT:
					self.running = 0
					self.execer.stop()
				if e.type == VIDEORESIZE:
					try:self.wininit((e.w,e.h))
					except:pass
			self.win.surf.fill((255,255,255))
			try: self.tit.draw(self.win.surf)
			except: pass
			try: self.mas.draw(self.win.surf)
			except: pass
			try: self.cn1.draw(self.win.surf)
			except: pass
			try: self.cn2.draw(self.win.surf)
			except: pass
			try: self.tab.draw(self.win.surf)
			except: pass
			display.flip()

	def __iadd__(self,pos):
		self.pos.append(pos)
		self.dump()
		return self

	def pop(self):
		self.pos.pop()

	@thread
	def dump(self):
		print(f"[DBG] [{self.execer.func}:{self.execer.line}] "+"    "*(len(self.pos)-1)+self.pos[-1])
