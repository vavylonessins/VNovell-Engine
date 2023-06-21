from tracer import *
import extui
import traceback


try:
    print(f"[LOG] [{__file__}] loading modules...")
    traceon()
    from vns_parser import parser
    from time import sleep
    from pygame import *
    import rlfs
    import ui_vm as ui
    from ui_config_vm import *
    import os
    import sys
    import vnb
    import json
    import b64
    import tempfile
    traceoff()
    print(f"[LOG] [{__file__}] Done with {round(get_trace(), 3)} ms")

    # init file systems
    print(f"[LOG] [{__file__}] mounting file systems...")
    print(f"    - res://")
    res = rlfs.Setup(b64.decode(sys.argv[-1]))
    print(f"    - res://scripts/")
    scripts_fs = rlfs.Setup(res.get_name("res://scripts"))
    print(f"[LOG] [{__file__}] Done")

    # load project config
    print(f"[LOG] [{__file__}] loading project config...")
    with open(res.system_get_name("res://project.json"), "rt") as f:
        project = json.loads(f.read())
    print(f"[LOG] [{__file__}] Done")

    # index script file system
    print(f"[LOG] [{__file__}] index scripts file systems...")

    vns_script_files = []
    pyt_script_files = []

    for file in scripts_fs.list():
        if os.path.splitext(file)[1] in (".vns", ".vnsc"):
            vns_script_files.append("res://"+file)
            print(f"    - res://{file}")

    for file in scripts_fs.list():
        if os.path.splitext(file)[1] in (".py", ".pys", ".pyt", ".pyw"):
            pyt_script_files.append("res://"+file)
            print(f"    - res://{file}")

    print(f"[LOG] [{__file__}] Done")

    # combine vns code

    print(f"[LOG] [{__file__}] compiling vns...")

    vns = ""

    for fp in vns_script_files:
        with scripts_fs.open(fp, "rt") as f:
            vns += "\n"+f.read()

    vns = vns[1:][:-1]

    # compile vns code to vnb

    parsed = parser.parse(vns)

    binary = vnb.compile(parsed)

    if "__vncache__" not in os.listdir():
        os.mkdir("__vncache__")
    for func in binary:
        with open(f"__vncache__/{func}.vnb", "wt") as f:
            f.write(binary[func])

    print(f"[LOG] [{__file__}] Bootstrap vnb pseudo-bytecode")

    execer = vnb.Executor(res, binary)

    # dbg = Debugger(execer)

    # execer.dbg = dbg

    ## GAME EXECUTING STARTS HERE ##

    # run debugger
    print(f"[LOG] [{__file__}] run debugger")
    # dbg.run()

    sleep(.5)

    # call init
    print(f"[LOG] [{__file__}] vns: call init")
    execer.execute("init")

    # try to setup UI settings
    print(f"[LOG] [{__file__}] start UI setup...")
    try:
        ui = ui.init(res.get_name("res://scripts/options.py"))
        print(f"[LOG] [{__file__}] Done")
    except FileNotFoundError as e:
        print(f"[FAT] [{__file__}] {e.__class__.__name__}: {e}")
        extui.popup(extui.POPUP_ERROR, "FileNotFoundError",
                    "file \"res://scripts/options.py\" not found")
    except Exception as e:
        print(f"[FAT] [{__file__}] {e.__class__.__name__}: {e}")
        extui.popup(extui.POPUP_ERROR, e.__class__.__name__, str(e))

    # create window
    print(f"[LOG] [{__file__}] starting window...")
    try:
        init()
        display.init()
        font.init()
        mixer.init()
        clock = time.Clock()
        win = ui.Window(name=project["project-name"],
                        icon=res.get_name(project["window-icon"]))
        execer.scene = Surface(win.surf.get_size()).convert()
        execer.scene.fill((0, 0, 0))
    except Exception as e:
        print(f"[FAT] [{__file__}] {e.__class__.__name__}: {e}")
        extui.popup(extui.POPUP_ERROR, e.__class__.__name__, str(e))
    print(f"[LOG] [{__file__}] Done")

    # call splash
    print(f"[LOG] [{__file__}] vns: call splash")
    print(f"[LOG] [{__file__}] ...")
    execer.execute_threaded("splash")

    clock = time.Clock()

    win.surf.fill(0)

    while execer.process:
        clock.tick(90)
        for e in event.get():
            if e.type == QUIT:
                execer.stop()
        try:
            with open(tempfile.gettempdir()+"/vne_bgr.tmp", "rt") as f:
                cmd = f.read().strip()
            if cmd:
                exec(cmd)
            else:
                with open(tempfile.gettempdir()+"/vne_bgr.tmp", "wt") as f:
                    f.write("")
        except:
            pass
        try:
            win.surf.blit(sysind_fnt.render(
                str(int(clock.get_fps())), 1, sysind_fg), (10, 10))
        except:
            draw.rect(win.surf, sysind_fg, win.rect, 1)
        display.flip()

    display.quit()

    print(f"[LOG] [{__file__}] Done")

except Exception as e:
    print(traceback.format_exc())
    print(
        f"[FAT] [{__file__}:{e.__traceback__.tb_lineno}] {e.__class__.__name__}: {e}")
    extui.popup(extui.POPUP_ERROR, e.__class__.__name__,
                "("+__file__.split("/")[-1].split("\\")[-1]+":"+str(e.__traceback__.tb_lineno)+") "+str(e))
