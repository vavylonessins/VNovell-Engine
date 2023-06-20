from showinfm import show_in_file_manager as sifm
from pygame import *
from thread import *
import ini
import os
import sys
import use8


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
	folder = use8.encode(projects[active_project])
	shell = sys.executable+" vne-vm.py "+folder
	run_threaded(shell)


def cb_build(active_project):
	print('Кнопка "Запустить" была нажата!')


def cb_open_folder(active_project):
	sifm(projects[active_project])


@thread
def run_threaded(shell):
	os.system(shell)
