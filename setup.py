import os
import pickle
os.system('cls')

from cx_Freeze import *
import resources as res
import sys

print('PRIMATERIA SOURCE\nby Matt Kai\n\nThe application setup is starting.\nPlease, wait...\n\n')

FOLDERS = [res.BACKG_PATH,res.SPRITES_PATH,res.SFX_PATH,res.MUSIC_PATH,res.MAPS_PATH,res.TILES_PATH,res.FONTS_PATH,'plugins/']

build = {
"path": sys.path + ["app"],
"no_compress": True,
"packages": ["pygame","pytmx","plyer","math","random","datetime","traceback","platform","numpy","sys","os"],
"include_files": FOLDERS + ['database_PT.py','database_EN.py','GUI.py','minigames.py','resources.py','splash.png','icon.ico','README.md','LICENSE','CREDITS.txt'],
}

shortcut_table = [
(
	res.GNAME,
	res.FNAME,
	res.GNAME,
	"TARGETDIR",
	"[TARGETDIR]OpenCvAPI.exe",
	None,
	res.DESCRIPTION,
	None,
	'icon.ico',
	None,
	None,
	'TARGETDIR'
)]

bdist = {
	"all_users": False,
    'data': {"Shortcut": shortcut_table},
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % res.FNAME,
    "upgrade_code": "{96a85bac-52af-4019-9e94-3afcc9e1ad0c}"
}

exe = Executable(
	script = r"main.py",
	targetName = res.FNAME,
	shortcutName = res.FNAME,
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
	options = {"build_exe": build,"bdist_msi": bdist}
	)