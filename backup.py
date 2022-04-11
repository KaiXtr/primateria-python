import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

ACCESS_TOKEN = 'sl.BFMUJmAwTUFDD3MlAPLlXpogIf5RHOVbuw-Vay9AslIDQBWhEEsCfCHPw_JwSc9UWDCMI7DdhIBICl43-'
APP_KEY = 'o1zpk36995qm337'
APP_SECRET = 'hjagryc82t5fpw9'
BPATH = '/backuptest.db'

print('Hello World!')
f = open('backuptest.db','w')
f.write('This is a file uploaded to Dropbox.')
f.close()

def upload(file):
	with open(file, 'rb') as f:
		try: dbx.files_upload(f.read(), BPATH, mode=WriteMode('overwrite'))
		except ApiError as err:
			if (err.error.is_path() and err.error.get_path().reason.is_insufficient_space()):
				print("ERROR: OUT OF SPACE IN STORAGE.")
			elif err.user_message_text: print(err.user_message_text)
			else: print(err)

def download(file,rev=None):
	dbx.files_restore(BPATH, rev)
	dbx.files_download_to_file(file, BPATH, rev)

def select_revision():
	entries = dbx.files_list_revisions(BACKUPPATH, limit=30).entries
	revisions = sorted(entries, key=lambda entry: entry.server_modified)
	for revision in revisions:
		print(revision.rev, revision.server_modified)
	return revisions[0].rev

if __name__ == '__main__':
	if (len(ACCESS_TOKEN) == 0): print("ERROR: ACCESS_TOKEN NOT FOUND")
	with dropbox.Dropbox(ACCESS_TOKEN) as dbx:
		try:
			user = dbx.users_get_current_account()
			print('uploading...')
			upload('backuptest.db')
			#download(select_revision())
		except AuthError: print("ERROR: INVALID ACCESS_TOKEN")