import urllib.request

x = urllib.request.urlopen('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/' + \
	'?key=XXXXXXXXXXXXXXXXXXXXXXX&steamids={}'.format('$stmid6476561198423560382'))
print(x)