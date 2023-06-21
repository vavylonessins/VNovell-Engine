from tracer import *
import traceback
import extui
import os


os.system(("clear", "cls")[os.name == "nt"])
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

__file__ = os.path.abspath(__file__)


try:
    print(f"[LOG] [{__file__}] loading modules...")
    traceon()
    import ui
    from ui_config import *
    from pygame import *
    import ini
    from callbacks import *
    traceoff()
    print(f"[LOG] [{__file__}] done with {round(get_trace(), 3)} ms")

    print(f"[LOG] [{__file__}] initializing video...")
    init()
    display.init()
    font.init()
    mixer.init()
    clock = time.Clock()
    print(f"[LOG] [{__file__}] done")

    print(f"[LOG] [{__file__}] loading projects list...")
    try:
        projects = ini.load("./saves/projects.ini")
    except FileNotFoundError:
        os.system("touch ./saves/projects.ini")
        projects = ini.load("./saves/projects.ini")
    print(f"[LOG] [{__file__}] done")

    print(f"[LOG] [{__file__}] opening widow...")
    win = ui.Window(name="VNovell Engine Launcher", icon="logo.png")
    print(f"[LOG] [{__file__}] done")

    def wininit(size):
        global win, tit, mas, cn1, cn2, st1, st2, prj, pnl
        win.resize(Vector2(size))
        tit = ui.Title(win, "VNovell Engine Launcher", spos=Vector2(1, 0))
        mas = ui.Container(win, Vector2(0, 0), Vector2(
            1, 2), Vector2(win.rect.w, win.rect.h-tit.rect.h))
        cn1 = ui.Container(mas, Vector2(margin, margin), Vector2(
            0, 1), Vector2(mas.rect.w/2, mas.rect.h), 1)
        cn2 = ui.Container(mas, Vector2(-margin, margin),
                           Vector2(2, 1), Vector2(mas.rect.w/2, mas.rect.h), 1)
        st1 = ui.Subtitle(cn1, "Projects", spos=Vector2(
            1, 0), rpos=Vector2(0, margin))
        st2 = ui.Subtitle(cn2, "Instruments", spos=Vector2(
            1, 0), rpos=Vector2(0, margin))
        prj = ui.RadioList(cn1, list(projects.keys()), rpos=Vector2(
            margin, 0), spos=Vector2(1, 2), dsiz=Vector2(0, -st1.rect.h))
        pnl = ui.ButtonList(cn2, ["Create", "Edit", "Delete", "Build", "Run", "Open Folder"],
                            [cb_create, cb_edit, cb_delete, cb_build,
                                cb_run, cb_open_folder], [prj.get_active],
                            rpos=Vector2(margin, 0), spos=Vector2(1, 2), dsiz=Vector2(0, -st2.rect.h))

    print(f"[LOG] [{__file__}] initializing window...")
    wininit((800, 600))
    print(f"[LOG] [{__file__}] done")

    run = 1
    print(f"[LOG] [{__file__}] main video loop")
    while run:
        clock.tick(120)
        for e in win.get_events():
            if e.type == QUIT:
                print(f"[LOG] [{__file__}] QUIT event")
                run = 0
            if e.type == VIDEORESIZE:
                try:
                    wininit((e.w, e.h))
                except:
                    pass
            prj.handle(win.surf, e)
            if prj.active != -1:
                pnl.handle(win.surf, e)
        win.surf.fill((255, 255, 255))
        try:
            tit.draw(win.surf)
        except:
            pass
        try:
            mas.draw(win.surf)
        except:
            pass
        try:
            cn1.draw(win.surf)
        except:
            pass
        try:
            cn2.draw(win.surf)
        except:
            pass
        try:
            st1.draw(win.surf)
        except:
            pass
        try:
            st2.draw(win.surf)
        except:
            pass
        try:
            prj.draw(win.surf)
        except:
            pass
        try:
            if prj.active != -1:
                pnl.draw(win.surf)
        except:
            pass
        display.flip()
    print(f"[LOG] [{__file__}] end of main video loop")
    display.quit()
except Exception as e:
    print(traceback.format_exc())
    print(
        f"[FAT] [{__file__}:{e.__traceback__.tb_lineno}] {e.__class__.__name__}: {e}")
    extui.popup(extui.POPUP_ERROR, e.__class__.__name__, "("+__file__.split("/")
                [-1].split("\\")[-1]+":"+str(e.__traceback__.tb_lineno)+") "+str(e))
