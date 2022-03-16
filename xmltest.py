import xml.sax
import pygame
import resources as res

class MapHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.window = pygame.display.set_mode((400,300))
		self.surface = pygame.Surface((0,0))
		self.current = ''
		self.map = None
		self.properties = {}
		self.tileset = []
		self.layers = []
		self.content = ''
   
	def startElement(self, tag, attributes):
		tag = tag.lower()
		self.current = tag
		if tag == 'map':
			self.map = {i[0]: int(i[1]) for i in attributes.items() if i[0] not in ['version','tiledversion','orientation','renderorder']}
			self.surface = pygame.Surface((self.map['width'] * self.map['tilewidth'],self.map['height'] * self.map['tileheight']))
		if tag == 'property': self.properties[attributes['name']] = attributes['value']
		if tag == 'tileset': pass

	def endElement(self, tag):
		tag = tag.lower()
		if tag == 'data':
			if self.content:
				tt = []
				for t in range(len(self.content[::3])):
					lid = self.content[t * 3:(t + 1) * 3]
					if int(lid) not in self.tileset: self.tileset.append(int(lid))
					tt.append(int(lid))
				self.layers.append(tt)
		if tag == 'map':
			parser = xml.sax.make_parser()
			parser.setFeature(xml.sax.handler.feature_namespaces, 0)
			tls = {}
			gid = 626
			for t in ['streets.tsx']: #os.listdir(res.TILESETS_PATH):
				hh = TileHandler(self.tileset,gid)
				parser.setContentHandler(hh)
				parser.parse(res.TILESETS_PATH + t)
				tls = {**tls,**hh.tiles}
				gid += hh.properties['length']
			for i in self.layers:
				pos = 0
				for y in range(self.map['height']):
					for x in range(self.map['width']):
						if i[pos] > 0: self.surface.blit(tls[i[pos]]['IMG'],(x * self.map['tilewidth'],y * self.map['tileheight']))
						pos += 1
		self.current = ''

	def characters(self, content):
		content = content.lower()
		if self.current == "data" and content:
			tt = content
			for i in ['\n',' ','	',',']:
				tt = tt.replace(i,'')
			self.content += tt
	
	def test(self):
		for event in pygame.event.get(): pass
		self.window.fill((100,100,100))
		self.window.blit(self.surface,(0,0))
		pygame.display.flip()
		pygame.time.Clock().tick(60)

class TileHandler(xml.sax.ContentHandler):
	def __init__(self,lst,first):
		self.ind = ''
		self.img = None
		self.properties = {}
		self.tileset = lst
		self.tiles = {}
		self.tilprp = {}
		self.first = first
   
	def startElement(self, tag, attributes):
		if tag == 'tileset':
			self.properties = {i[0]: int(i[1]) for i in attributes.items() if i[0] not in ['version','tiledversion','name']}
			self.properties['length'] = self.properties['rows'] * self.properties['columns']
		if tag == 'img':
			self.img = pygame.image.load(res.TILESETS_PATH + attributes['source'])
		if tag == 'tile':
			if int(attributes['id']) + self.first in self.tileset:
				lid = int(attributes['id'])
				gid = int(attributes['id']) + self.first
				xx = (lid - (int(lid/self.properties['columns']) * self.properties['columns'])) * self.properties['tilewidth']
				yy = int(lid/self.properties['rows']) * self.properties['tileheight']
				rct = (xx,yy,self.properties['tilewidth'],self.properties['tileheight'])
				self.tiles[gid] = {'IMG': self.img.subsurface(rct).copy(),'RECT': (0,0,0,0), 'PROPERTIES': self.tilprp}
		if tag == 'properties': self.tilprp = {}
		if tag == 'property': self.tilprp[attributes['name']] = attributes['value']
		self.ind = tag

	def endElement(self, tag): self.ind = ''

	def characters(self, content): pass
	
	def save(self, f=None):
		contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
		'<tileset version="1.2" name="{}" tilewidth="{}" tileheight="{}" rows="{}" columns="{}">\n'.format(self.mapdata['WIDTH'],self.mapdata['HEIGHT'])
		contents += '	<img source="{}" width="{}" height="{}"/>'
		id = 1
		for i in tilset:
			gid += tst.tilecount
			contents += '	<tile id="{}" mask="{}" step="{}">\n'.format(id,(0,0,30,30),0)
			id += 1
		contents += '</tilset>'
		
		if f: ff = self.name
		else: ff = f
		file = open(res.MAPS_PATH + ff + '.xml','w')
		file.write(contents)
		file.close()
         
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = MapHandler()
parser.setContentHandler(Handler)
parser.parse(res.MAPS_PATH + 'savetest.tmx')
while True: Handler.test()