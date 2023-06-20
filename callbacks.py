from pygame import *
from thread import *
import ini
import os
import sys
import b64


try:
	projects = ini.load("./saves/projects.ini")
except FileNotFoundError:
	os.system("touch ./saves/projects.ini")
	projects = ini.load("./saves/projects.ini")
clock = time.Clock()


def cb_create(active_project):
	print('Кнопка "Создать" была нажата!')


def cb_edit(active_project):
	folder = projects[active_project]
	run_threaded(f"subl \"{folder}\"")


def cb_delete(active_project):
	print('Кнопка "Удалить" была нажата!')


def cb_run(active_project):
	folder = b64.encode(projects[active_project])
	shell = sys.executable+" vne-vm.py "+folder
	run_threaded(shell)


def cb_build(active_project):
	print('Кнопка "Запустить" была нажата!')


def cb_open_folder(active_project):
	from showinfm import show_in_file_manager as sifm
	sifm(projects[active_project])


@thread
def run_threaded(shell):
	os.system(shell)
