from tracer import *
import extui
from ui_config import *
from pygame import *


## RPOS - Relative POSition - position relative for aligning position
## SPOS - Sticking POSition - position for sticking (0 - left/top, 1 - center, 2 - right/bottom)


class UIAsset:
	def __init__(self):
		self.pos, self.rect = Vector2(0,0), Rect(0,0,0,0)
		pass

	def draw(self, sc=None):
		pass

	def update(self, sc, delta):
		pass

	def handle(self, sc, event):
		pass

	def get_rect(self, sc):
		return self.rect

	def get_pos(self, sc):
		return self.pos


class Subtitle(UIAsset):
	def __init__(self,parent,text,rpos=Vector2(0,0),spos=Vector2(1,0)):
		self.parent = parent
		self.text = text
		self.rpos = rpos
		self.spos = spos
		self.render = True
		self.rect = Rect(0,0,0,0)
		self.draw()

	def draw(self, sc=None):
		if self.render:
			self.texture = subtitle_fnt.render(self.text,1,subtitle_fg)
			r = self.parent.get_rect(sc)
			self.pos = Vector2()
			if self.spos.x == 0:
				self.pos.x += self.rpos.x
			if self.spos.x == 1:
				self.pos.x = r.w/2 - self.texture.get_width()/2
				self.pos.x += self.rpos.x
			if self.spos.x == 2:
				self.pos.x = r.w - self.texture.get_width()
				self.pos.x -= self.rpos.x
			if self.spos.y == 0:
				self.pos.y += self.rpos.y
			if self.spos.y == 1:
				self.pos.y = r.h/2 - self.texture.get_height()/2
				self.pos.y += self.rpos.y
			if self.spos.y == 2:
				self.pos.y = r.h - self.texture.get_height()
				self.pos.y -= self.rpos.y
			self.pos += self.parent.get_pos(sc)
			self.rect = Rect(self.pos.x, self.pos.y, self.texture.get_width(), self.texture.get_height())
			self.render = False
		if sc:
			sc.blit(self.texture, self.pos)

def blit_text(surface, text, pos, font, color=Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class Text(UIAsset):
	def __init__(self,parent,text,rpos=Vector2(0,0),spos=Vector2(1,0),size=Vector2(250,250)):
		self.parent = parent
		self.text = text
		self.rpos = rpos
		self.spos = spos
		self.render = True
		self.size = Vector2(size)
		self.rect = Rect(0,0,0,0)
		self.draw()

	def draw(self, sc=None):
		if self.render:
			self.texture = Surface((int(self.size.x), int(self.size.y)), SRCALPHA)
			blit_text(self.texture, self.text, (0, 0), text_fnt, text_fg)
			r = self.parent.get_rect(sc)
			self.pos = Vector2()
			if self.spos.x == 0:
				self.pos.x += self.rpos.x
			if self.spos.x == 1:
				self.pos.x = r.w/2 - self.texture.get_width()/2
				self.pos.x += self.rpos.x
			if self.spos.x == 2:
				self.pos.x = r.w - self.texture.get_width()
				self.pos.x -= self.rpos.x
			if self.spos.y == 0:
				self.pos.y += self.rpos.y
			if self.spos.y == 1:
				self.pos.y = r.h/2 - self.texture.get_height()/2
				self.pos.y += self.rpos.y
			if self.spos.y == 2:
				self.pos.y = r.h - self.texture.get_height()
				self.pos.y -= self.rpos.y
			self.pos += self.parent.get_pos(sc)
			self.rect = Rect(self.pos.x, self.pos.y, self.texture.get_width(), self.texture.get_height())
			self.render = False
		if sc:
			sc.blit(self.texture, self.pos)


class Title(UIAsset):
	def __init__(self,parent,text,rpos=Vector2(0,0),spos=Vector2(1,0)):
		self.parent = parent
		self.text = text
		self.rpos = rpos
		self.spos = spos
		self.render = True
		self.rect = Rect(0,0,0,0)
		self.draw()

	def draw(self, sc=None):
		if self.render:
			self.texture = title_fnt.render(self.text,1,title_fg)
			r = self.parent.get_rect(sc)
			self.pos = Vector2()
			if self.spos.x == 0:
				self.pos.x += self.rpos.x
			if self.spos.x == 1:
				self.pos.x = r.w/2 - self.texture.get_width()/2
				self.pos.x += self.rpos.x
			if self.spos.x == 2:
				self.pos.x = r.w - self.texture.get_width()
				self.pos.x -= self.rpos.x
			if self.spos.y == 0:
				self.pos.y += self.rpos.y
			if self.spos.y == 1:
				self.pos.y = r.h/2 - self.texture.get_height()/2
				self.pos.y += self.rpos.y
			if self.spos.y == 2:
				self.pos.y = r.h - self.texture.get_height()
				self.pos.y -= self.rpos.y
			self.pos += self.parent.get_pos(sc)
			self.rect = Rect(self.pos.x, self.pos.y, self.texture.get_width(), self.texture.get_height())
			self.render = False
		if sc:
			sc.blit(self.texture, self.pos)


class Container(UIAsset):
	def __init__(self,parent,rpos,spos,size,border=0):
		self.parent = parent
		self.rect=rect
		self.rpos = rpos
		self.spos = spos
		self.size = size
		self.border = border
		self.render = True
		self.draw()

	def draw(self, sc=None):
		if self.render:
			r = self.parent.get_rect(sc)
			self.pos = Vector2()
			if self.spos.x == 0:
				self.pos.x += self.rpos.x
			if self.spos.x == 1:
				self.pos.x = r.w/2 - self.size.x/2
				self.pos.x += self.rpos.x
			if self.spos.x == 2:
				self.pos.x = r.w - self.size.x
				self.pos.x -= self.rpos.x
			if self.spos.y == 0:
				self.pos.y += self.rpos.y
			if self.spos.y == 1:
				self.pos.y = r.h/2 - self.size.y/2
				self.pos.y += self.rpos.y
			if self.spos.y == 2:
				self.pos.y = r.h - self.size.y
				self.pos.y -= self.rpos.y
			self.pos += self.parent.get_pos(sc)
			self.rect = Rect(self.pos.x+margin, self.pos.y+margin, self.size.x-margin*2, self.size.y-margin*2)
			self.render = False
		if self.border:
			if sc:
				draw.rect(sc,border_fg,self.rect,self.border)


class RadioList(UIAsset):
	def __init__(self,parent,items,active=-1,rpos=Vector2(),spos=Vector2(),dsiz=Vector2()):
		self.parent = parent
		self.items = items
		self.hover = -1
		self.active = active
		self.rpos = rpos
		self.spos = spos
		self.dsiz = dsiz
		self.render = True
		self.draw()

	def get_active(self):
		return self.items[self.active]

	def draw(self, sc=None):
		if self.render:
			r = self.parent.get_rect(sc)
			self.size = Vector2(r.w-margin*2,r.h-margin*2) + self.dsiz
			self.pos = Vector2()
			if self.spos.x == 0:
				self.pos.x += self.rpos.x
			if self.spos.x == 1:
				self.pos.x = r.w/2 - self.size.x/2
				self.pos.x += self.rpos.x
			if self.spos.x == 2:
				self.pos.x = r.w - self.size.x
				self.pos.x -= self.rpos.x
			if self.spos.y == 0:
				self.pos.y += self.rpos.y
			if self.spos.y == 1:
				self.pos.y = r.h/2 - self.size.y/2
				self.pos.y += self.rpos.y
			if self.spos.y == 2:
				self.pos.y = r.h - self.size.y
				self.pos.y -= self.rpos.y
			self.pos += self.parent.get_pos(sc)
			self.rect = Rect(self.pos.x+margin, self.pos.y+margin, self.size.x-margin*2, self.size.y-margin*2)

			self.texture = Surface((int(self.size.x), int(self.size.y)))
			self.texture.fill(main_bg)
			draw.rect(self.texture, border_fg, (0, 0, *self.size), border_width)
			em = radiolist_fnt.get_height()
			dpos = Vector2(0,0)
			self.rects = []
			for n, i in enumerate(self.items):
				r = Rect(*(dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1)),self.size.x-radiolist_margin*2,em)
				r.x += self.pos.x
				r.y += self.pos.y
				self.rects.append(r)
				if n == self.hover:
					draw.rect(self.texture,radiolist_hover_bg,(*(dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1)),self.size.x-radiolist_margin*2,em))
				if n == self.active:
					draw.rect(self.texture,radiolist_active_bg,(*(dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1)),self.size.x-radiolist_margin*2,em))
				self.texture.blit(radiolist_fnt.render(i,1,radiolist_active_fg if n == self.active else radiolist_hover_fg if n == self.hover else radiolist_idle_fg),
					dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1))
				dpos += Vector2(0,em)

			self.render = False
		if sc:
			sc.blit(self.texture, self.pos)

	def handle(self, sc, e):
		if e.type == MOUSEMOTION:
			if self.rect.collidepoint(e.pos):
				n = -1
				for nex, r in enumerate(self.rects):
					if r.collidepoint(e.pos):
						n = nex
						break
				self.render = True
				self.hover = n
			else:
				self.hover = -1
		if e.type == MOUSEBUTTONUP:
			if self.rect.collidepoint(e.pos):
				n = -1
				for nex, r in enumerate(self.rects):
					if r.collidepoint(e.pos):
						n = nex
						break
				self.render = True
				self.active = n


class ButtonList(UIAsset):
	def __init__(self,parent,items,callbacks,fargs,rpos=Vector2(),spos=Vector2(),dsiz=Vector2()):
		self.parent = parent
		self.items = items
		self.callbacks = callbacks
		self.hover = -1
		self.pressed = -1
		self.fargs = fargs
		self.rpos = rpos
		self.spos = spos
		self.dsiz = dsiz
		self.render = True
		self.draw()

	def draw(self, sc=None):
		if self.render:
			r = self.parent.get_rect(sc)
			self.size = Vector2(r.w-margin*2,r.h-margin*2) + self.dsiz
			self.pos = Vector2()
			if self.spos.x == 0:
				self.pos.x += self.rpos.x
			if self.spos.x == 1:
				self.pos.x = r.w/2 - self.size.x/2
				self.pos.x += self.rpos.x
			if self.spos.x == 2:
				self.pos.x = r.w - self.size.x
				self.pos.x -= self.rpos.x
			if self.spos.y == 0:
				self.pos.y += self.rpos.y
			if self.spos.y == 1:
				self.pos.y = r.h/2 - self.size.y/2
				self.pos.y += self.rpos.y
			if self.spos.y == 2:
				self.pos.y = r.h - self.size.y
				self.pos.y -= self.rpos.y
			self.pos += self.parent.get_pos(sc)
			self.rect = Rect(self.pos.x+margin, self.pos.y+margin, self.size.x-margin*2, self.size.y-margin*2)

			self.texture = Surface((int(self.size.x), int(self.size.y)))
			self.texture.fill(main_bg)
			draw.rect(self.texture, border_fg, (0, 0, *self.size), border_width)
			em = radiolist_fnt.get_height()
			dpos = Vector2(0,0)
			self.rects = []
			for n, i in enumerate(self.items):
				r = Rect(*(dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1)),self.size.x-radiolist_margin*2,em)
				r.x += self.pos.x
				r.y += self.pos.y
				self.rects.append(r)
				if n == self.hover and n != self.pressed:
					draw.rect(self.texture,radiolist_hover_bg,(*(dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1)),self.size.x-radiolist_margin*2,em))
				if n == self.pressed:
					draw.rect(self.texture,radiolist_active_bg,(*(dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1)),self.size.x-radiolist_margin*2,em))
				self.texture.blit(radiolist_fnt.render(i,1,radiolist_active_fg if n == self.pressed else radiolist_hover_fg if n == self.hover else radiolist_idle_fg),
					dpos+Vector2(radiolist_margin,radiolist_margin)+Vector2(0,radiolist_margin)*(2*n-1))
				dpos += Vector2(0,em)

			self.render = False
		if sc:
			sc.blit(self.texture, self.pos)

	def handle(self, sc, e):
		if e.type == MOUSEMOTION:
			if self.rect.collidepoint(e.pos) and self.pressed == -1:
				n = -1
				for nex, r in enumerate(self.rects):
					if r.collidepoint(e.pos):
						n = nex
						break
				if self.hover != n:
					self.render = True
				self.hover = n
				self.presesd = -1
			else:
				self.hover = -1
		if e.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(e.pos):
				n = -1
				for nex, r in enumerate(self.rects):
					if r.collidepoint(e.pos):
						n = nex
						break
				if self.pressed != n:
					self.render = True
				self.pressed = n
		if e.type == MOUSEBUTTONUP:
			if self.rect.collidepoint(e.pos):
				n = -1
				for nex, r in enumerate(self.rects):
					if r.collidepoint(e.pos):
						n = nex
						break
				if self.pressed != n:
					self.render = True
				self.callbacks[n](*list(f() for f in self.fargs))
				self.pressed = -1


class Window(UIAsset):
	def __init__(self,size=Vector2(800,600),flags=RESIZABLE,name="",icon=""):
		self.pos = Vector2(0, 0)
		self.rect = Rect(0, 0, *size)
		display.set_caption(name)
		if icon:
			display.set_icon(image.load(icon))
		self.surf = display.set_mode((int(size.x), int(size.y)), HWACCEL|HWPALETTE|HWSURFACE|DOUBLEBUF|flags)
		self.flags = HWACCEL|HWPALETTE|HWSURFACE|DOUBLEBUF|flags

	def get_events(self):
		return event.get()

	def resize(self, size):
		self.rect = Rect(0, 0, *size)
