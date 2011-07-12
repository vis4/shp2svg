#
# shp2svg
#
# simple script to convert shapefile polygons to svg
# uses pyproj to project the lat,lng values to pixels
# 
# unlike mapnik, shp2svg will keep all metadata in svg
#
# -a shpfile 	analyses the given shapefile
#
#

import sys, getopt, os.path

encoding = 'utf-8'
meta_keys = range(100)
output = 'out.svg'
proj4str = ''

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ace:k:o:p:u")
	except getopt.GetoptError, err:
		# print help information and exit:
		print opts
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	
	if len(args) != 1:
		usage()
		sys.exit(2)
	
	shpFile = args[0]
	
	if not os.path.exists(shpFile) and not os.path.exists(shpFile+".shp"):
		print shpFile,"does not exist"
		# usage()
		sys.exit(2)
	
	verbose = False
	
	for o, a in opts:
		if o == "-o":
			global output
			output = a
		if o == "-p":
			global proj4str
			proj4str = a
		if o == "-e": 
			global encoding
			encoding = a
		if o == "-k":
			global meta_keys
			meta_keys = a.split(',')
	
	for o, a in opts:
		if o == "-a": 
			anaylze(shpFile) 
			return
		if o == "-c":
			convert(shpFile)
	usage()
	# ...



def usage():
	print "usage: shp2svg [-acekop] [shpfile]     \n"
	print "Options:"
	print "   -a             Analyses the content of the shapefile"
	print "   -c             Converts the shapefile to SVG"
	print "   -e [encoding]  Specify a charset to decode the metadata (default is utf-8)"
	print "   -k [keys]      Comma-separated list of keys to use as metadata in SVG"
	print "   -o [svgfile]   Filename to write SVG (default is out.svg)"
	print "   -p [proj]      Proj.4 projection to use"
	
	print "\nExamples:"
	print "shp2svg -k ,ags,name,,area"


def anaylze(shp_url):
	import shapefile
	print "\nanalyzing shapefile ",shp_url
	print "\nGeometry:"
	sf = shapefile.Reader(shp_url)
	shapeRecs = sf.shapeRecords()
	print '  ',len(shapeRecs), "\tRecords (total)"
	shapeTypes = [0]*10
	for rec in shapeRecs:
		shapeTypes[rec.shape.shapeType] += 1
	for i in range(len(shapeTypeNames)):
		shpType = shapeTypeNames[i]
		if shpType == '' or shapeTypes[i] == 0: continue
		print '  ',shapeTypes[i], "\t"+shpType+'s'
	
	print "\nMetadata:"
	
	metaData = []
	for i in range(len(shapeRecs[0].record)): metaData.append([])
	for i in range(len(metaData)):
		for rec in shapeRecs[:5]:	
			metaData[i].append(str(rec.record[i]).decode(encoding, 'replace'))
	
	global meta_keys
	for i in range(len(metaData)):
		if len(meta_keys) == 100 or (len(meta_keys) > i and meta_keys[i] != ''):
			print '  ',str(meta_keys[i])+": ",", ".join(metaData[i])+", ..."
		

def convert(shp_url):
	return


shapeTypeNames = ['']*10
shapeTypeNames[0] = 'Null shape'
shapeTypeNames[1] = 'Point'
shapeTypeNames[3] = 'Polyline'
shapeTypeNames[5] = 'Polygon'
shapeTypeNames[8] = 'Multipoint'


if __name__ == "__main__":
    main()
    print


exit()



import shapefile, Polygon, Polygon.IO, Polygon.Utils
from svgfig import *
from pyproj import Proj


	
shp_url = sys.argv[1]
svg_url = sys.argv[2]

sf = shapefile.Reader(shp_url)

print "reading shapefile.."
shapeRecs = sf.shapeRecords()

pname = 'aeqd'

proj = '+proj='+pname+' +lat_0=25 +lat_1=70 +lat_2=20 +lon_0=-23'
p = Proj(proj)

gcrop = (-10, -135, 90, 70)
bbox = [(22.8, -85.5), (19, -77), (73, -44), (52, 16), (40, 18.5)]

x1 = y1 =x2 = y2 = False

for c in bbox:
	if not x1:
		x1, y1 = x2, y2 = p(c[1], c[0])
	else:
		x,y = p(c[1], c[0])
		x1 = min(x1, x)
		y1 = min(y1, y)
		x2 = max(x2, x)
		y2 = max(y2, y)

cropRect = Polygon.Polygon([(x1,y1),(x2,y1),(x2,y2),(x1, y2)])

scale = 2000.0 / (x2 - x1)

polys = []

print "creating polygons"

for rec in shapeRecs:
	for part_index in range(len(rec.shape.parts)):
		part_begin = rec.shape.parts[part_index]
		if part_index+1 == len(rec.shape.parts):
			part_end = len(rec.shape.points)
		else:
			part_end = rec.shape.parts[part_index+1]-1
		points = []

		for px in range(part_begin, part_end):
			lng, lat = rec.shape.points[px]
			if lat > gcrop[0] and lat < gcrop[2] and lng > gcrop[1] and lng < gcrop[3]:
				x,y = p(lng, lat)
				points.append((x,y))
		
		if len(points) > 3:
			poly = Polygon.Polygon(points)
			#poly = poly & cropRect
			if poly.overlaps(cropRect):
				polys.append(poly)
 
#polys.append(cropRect) 
print "exporting SVG"
#Polygon.IO.writeSVG('cropped.svg', polys)

import svgfig
h = str((y1-y2)*scale*-1)
svg = svgfig.canvas(width='2000px', height=h+'px', viewBox='0 0 2000 '+h, style='stroke-width:0.5pt,fill:#fbf5ed')

svg.append(SVG('rect', width='2000px', height=h+'px', fill='#006179', stroke='none'))

def view(x,y):
	x = (x - x1) * scale
	y = (y - y2) * scale * -1
	return (x,y)
		
# equator

grid = SVG('g')

for lat in range(0,90,10):
	p_str = ''
	for lng in range(gcrop[1], gcrop[3]):
		x,y = p(lng, lat)
		x,y = view(x, y)
		p_str += str(x)+','+str(y)+' '
	grid.append(SVG('polyline', points=p_str, fill='none', stroke='#000', stroke_width='0.05px'))

for lng in range(gcrop[1], gcrop[3], 15):
	p_str = ''
	for lat in range(0,90):
		x,y = p(lng, lat)
		x,y = view(x, y)
		p_str += str(x)+','+str(y)+' '
	grid.append(SVG('polyline', points=p_str, fill='none', stroke='#000', stroke_width='0.05px'))

svg.append(grid)

empty = 0

for poly in polys:
	try:
		pts = poly.contour(0)
		p_str = ''
		for pt in pts:
			x,y = view(pt[0], pt[1])
			p_str += str(x)+','+str(y)+' '
		svg.append(SVG('polygon', points=p_str, stroke_linejoin='round', fill='#fbf5ed', stroke='#000', stroke_width='0.1px'))
	except IndexError:
		empty+= 1

svg.save(pname+'.svg')

