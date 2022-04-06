from cx_Freeze import *
import resources as res
import subprocess as subp
import sys
import os

sys.path.insert(0,'databases')
if res.FILES != []: dtb = __import__('database_' + res.FILES[0][4])
else: dtb = __import__('database_' + res.MAINLANG)

os.system('cls')
print( 	'╔═════════════════════════════════════════════╗\n' \
		'║ ┌──┐ ┌──┐ ◊ ┌─┬─┐ ┌──┐ ─┬─ ┌──  ┌──┐ ◊ ┌──┐ ║\n' \
		'║ │──┘ │ ─┘ │ │ │ │ │──│  │  │──  │ ─┘ │ │──│ ║\n' \
		'║ │    │  \\ │ │   │ │  │  │  │__  │  \\ │ │  │ ║\n' \
		'╚═════════════════════════════════════════════╝\n')

fn = input("Name: ")
if not fn: fn = res.FNAME
gv = input("Version: ")
if not gv: gv = res.VERSION
ga = input("Author: ")
if not ga: ga = res.AUTHOR
2
print('\n{}\n'.format(dtb.BUILDING[0]))

INCLUDES = ['collections','datetime','mutagen','numpy','os','PIL','platform','plyer','pygame','sqlite3','subprocess','sys',
	'threading','traceback','urllib','xml']

installed = subp.check_output(['python3', '-m', 'pip', 'freeze']).decode('utf-8')
installed = installed.split('\r\n')
EXCLUDES = ['asyncio','concurrent','ctypes','curses','distutils','tkinter']
EXCLUDES += [pkg.split('==')[0] for pkg in installed if pkg != '']
for pkg in INCLUDES:
	if pkg in EXCLUDES:
		if type(pkg) == str: EXCLUDES.remove(pkg)
		else: EXCLUDES.remove(pkg[1])

FOLDERS = [res.BACKG_PATH,res.SPRITES_PATH,res.SFX_PATH,res.MUSIC_PATH,res.MAPS_PATH,res.TILES_PATH,res.FONTS_PATH,'plugins/','databases/']

setup(
	name = res.GNAME,
	version = gv,
	description = res.DESCRIPTION,
	author = ga,
	executables = [
		Executable(
			script = r'main.py',
			target_name = fn,
			shortcut_name = fn,
			shortcut_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop'),
			copyright = 'GNU General Public License {}'.format(res.YEAR),
			icon = 'icon.ico',
			base = 'Win32GUI',
			)
		],
	options = {
		'build_exe': {
			'path': sys.path + ["app"],
			'no_compress': True,
			'includes': INCLUDES,
			'excludes': EXCLUDES,
			'include_files': FOLDERS + ['GUI.py','minigames.py','resources.py','icon.ico','README.md','LICENSE','CREDITS.txt'],
			'include_msvcr': True,
			'optimize': 1,
			},
		'bdist_msi': {
			'target_name': '{}-setup'.format(fn),
			'install_icon': 'icon.ico',
			'initial_target_dir': r'[ProgramFilesFolder]\\Primateria\%s' % fn,
			'product_code': None, #inserir um código massa aqui viu
			'upgrade_code': '{96a85bac-52af-4019-9e94-3afcc9e1ad0c}',
			'add_to_path': False,
			'all_users': False,
			'data': {
				'Directory': [(r'[ProgramFilesFolder]\\Primateria\%s' % fn,r'[ProgramFilesFolder]\\Primateria', r'[ProgramFilesFolder]\\Primateria\%s' % fn)],
				'Icon': [('IconId','icon.ico')],
				'ProgId': [('ID',None,None,res.DESCRIPTION,'IconId',None)],
				#'Shortcut':  [('ShortcutId',fn,res.GNAME,'TARGETDIR','[TARGETDIR]OpenCvAPI.exe',None,res.DESCRIPTION,None,'IconId',0,1,'TARGETDIR')]
				},
			},
		'bdist_mac': {
			'iconfile': 'icon.ico',
			'bundle_name': fn,
			}
		}
	)

print('\n{}{}.\n{}{}.'.format(dtb.BUILDING[1],os.getcwd() + '\\build',dtb.BUILDING[2],os.getcwd() + '\\dist'))