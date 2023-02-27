import exif
	
with open('SS1.jpg','rb') as file:
	img = exif.Image(file)

print(img.get("user_comment"))
img.user_comment = 'X300'
#print(img.get_thumbnail())
img.artist = 'Matt Kai'
img.copyright = 'Primateria - GNU General Public License'
print(sorted(img.list_all()))
print(img.get("artist"))
print(img.get("copyright"))
print(img.get("thumbnail"))
print(img.get("user_comment"))