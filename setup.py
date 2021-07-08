from cx_Freeze import *
import resources as res
import sys
import os

FOLDERS = [res.BACKG_PATH,res.SPRITES_PATH,
res.SFX_PATH,res.MUSIC_PATH,res.MAPS_PATH,res.TILES_PATH,res.FONTS_PATH]

build = {
"path": sys.path + ["app"],
"no_compress": True,
"packages": ["pygame","pytmx","math","random","sys","database"],
"include_files": FOLDERS + ['database_PT.py','database_EN.py','GUI.py','icon.ico','readme.txt'],
}

bdist = {
	"initial_target_dir": os.path.expanduser('~') + '/Primateria',
	"all_users": False
}

exe = Executable(
	script = r"main.py",
	targetName = res.GNAME,
	shortcutName = res.GNAME,
	shortcutDir =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
	icon = "icon.ico",
    base = "Win32GUI",
)

setup(
	name = res.GNAME,
	version = res.VERSION,
	description = res.DESCRIPTION,
	author = res.AUTHOR,
	executables = [exe],
	options = {"build_exe": build}
	)