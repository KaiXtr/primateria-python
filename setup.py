from cx_Freeze import *
import sys
import os

build = {
"path": sys.path + ["app"],
"no_compress": True,
"packages": ["pygame","pytmx","math","random","sys","database"],
"include_files": ['Maps/','Fonts/','Tiles/','Sprites/','SFX/','Music/','Songs/','Backgrounds/','database_PT.py','database_EN.py','menu.py','icon.ico','readme.txt'],
}

bdist = {
	"initial_target_dir": os.path.expanduser('~') + '/The Freak Hunter',
	"all_users": False
}

exe = Executable(
	script = r"main.py",
	targetName = "click_here_to_play",
	shortcutName = "Mutation Purge",
	shortcutDir =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
	icon = "icon.ico",
    base = "Win32GUI",
)

setup(
	name = "Mutatoin Purge",
	version = "0.0.1",
	description = "Mutation Purge (20XX)",
	author = "Matt Kai",
	executables = [exe],
	options = {"build_exe": build}
	)