from pygame import *
from time import sleep
from extui import *
from colors import *
from thread import *
import tempfile


TMP = tempfile.gettempdir()


def compile(n):
    ret = {}

    for func in n:
        func_name = func["name"]

        code = "("

        for command in func["body"]:
            code += repr(compile_line(command)) + ", "

        code = code[:-2] + ")"

        ret[func_name] = code

    return ret


def compile_line(n):
    if type(n) == str:
        return "python", {"code": n}
    return n.type, n.data


def super_color(data):
    if data[0] == "#":
        return ColorHex(data)
    else:
        return Color(data)


class NoneDebugger:
    def __init__(self, execer):
        self.execer = execer
        self.pos = []

    def __iadd__(self, pos):
        self.pos.append(pos)
        self.dump()
        return self

    def pop(self):
        self.pos.pop()

    def dump(self):
        return


class Executor:
    def __init__(self, res, binary, fnt: font.FontType=None, scene=None):
        self.res = res
        self.code = {**binary}

        self.font = fnt if fnt else font.SysFont(None, 28)

        self.images: dict[str, Surface] = {}

        self.scene_cmd = r'(lambda: None)()'

        self.d_proc = False
        self.d_func = None
        self.d_line = None
        self.process, self.error = 0, 0

        self.dbg = NoneDebugger(self)

    def execute_threaded(self, func):
        self.process, self.error = 1, 0
        self.p = thread(self.execute)(func, 1)

    def stop(self):
        self.process = 0

    def execute(self, func, threaded=0):
        print(f"[LOG] [{__file__}] executing vnb function \"{func}\"...")
        code = eval(self.code[func])
        self.func = func
        self.line = 0

        for cmd in code:
            if not self.process and threaded:
                return
            self.line += 1

            if self.func == "init" and cmd[0] in ("call", "jump"):
                popup(POPUP_ERROR, "RightsViolanceError",
                      f"({self.func},{self.line}) You cannot use calls or jumps in system functions")

            if cmd[0] == "load":
                self.dbg += "load"
                if cmd[1]["type"] == "image":
                    self.dbg += "image"
                    self.images[" ".join(cmd[1]["name"])] = image.load(
                        self.res.get_name(cmd[1]["path"]))
                    self.dbg.pop()
                else:
                    popup(POPUP_ERROR, "TypeError",
                          f"({self.func},{self.line}) unsupported operand type for 'load': '{cmd[1]['type']}'")
                self.dbg.pop()

            elif cmd[0] == "python":
                self.dbg += "python"
                self.dbg.pop()
                try:exec(cmd[1]["code"])
                except Exception as e:
                    popup(POPUP_ERROR, e.__class__.__name__, f"({self.func},{self.line}) "+str(e))
            elif cmd[0] == "wait":
                self.dbg += "wait"
                sleep(cmd[1]["duration"])
                self.dbg.pop()
            elif cmd[0] == "show":
                self.dbg += "show"
                data = cmd[1]["data"]
                if data["type"] == "text":
                    text = data["value"]
                    stext = self.font.render(text, 1, super_color(cmd[1]["color"]["value"]))
                    pos = Vector2(display.get_surface().get_size())/2-Vector2(stext.get_size())/2
                    pos = (int(pos.x), int(pos.y))
                    image.save(stext, path:=TMP+"/vne_show_cache.png")
                    with open(TMP+"/vne_fgr.tmp", "wt") as f:
                        f.write(fr"blit_centered(win.surf, image.load('{path}'))")
                self.dbg.pop()
                pass
            elif cmd[0] == "hide":
                self.dbg += "hide"
                self.dbg.pop()
                pass
            elif cmd[0] == "scene":
                self.dbg += "scene"
                if cmd[1]["data"]["type"] == "color":
                    self.dbg += "color"
                    if cmd[1]["data"]["value"][0] != "#":
                        self.dbg += "const"
                        try:
                            color = super_color(cmd[1]["data"]["value"])
                        except:
                            popup(POPUP_ERROR, "ColorError",
                                  f"({self.func},{self.line}) unknown color name: '{cmd[1]['data']['value']}'")
                        self.dbg.pop()
                    else:
                        self.dbg += "hex"
                        try:
                            color = Color(ColorHex(cmd[1]["data"]["value"]))
                        except:
                            popup(POPUP_ERROR, "ColorError",
                                  f"({self.func},{self.line}) invalid color argument")
                        self.dbg.pop()
                    with open(TMP+"/vne_bgr.tmp", "wt") as f:
                        f.write(
                            f'display.get_surface().fill(({color.r}, {color.g}, {color.b}))')
                    self.last_bg = f'display.get_surface().fill(({color.r}, {color.g}, {color.b}))'
                    self.dbg.pop()
                self.dbg.pop()
            else:
                popup(POPUP_ERROR, "NameError",
                      f"({self.func},{self.line}) unknown command: '{cmd[0]}'")

        if threaded:
            self.process = 0
        print(f"[LOG] [{__file__}] Done")
