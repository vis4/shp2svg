shp2svg - Easy conversion from ESRI shapefiles to SVG
====

Written by Gregor Aisch

MIT license

Requirements
------------
 - Python 2.7
 - Python modules: 
	- shapefile http://code.google.com/p/shapefile/
	- pyproj http://code.google.com/p/pyproj/
	- svgfig http://code.google.com/p/svgfig/
	
Analyzing
--------
Analyzing a shapefile

	python shp2svg -a countries.shp 

Will output

	analyzing shapefile WorldCountries.shp

	Geometry:
	   253 	Records (total)
	   253 	Polygons
	
	Metadata:
	   0:  Afghanistan, Albania, Algeria, American Samoa, Andorra, ...
	   1:  AF, AL, DZ, AS, AD, ...
	   2:  AFG, ALB, DZA, ASM, AND, ...
	   3:  4, 8, 12, 16, 20, ...
	   4:  AF, AL, DZ, AS, AD, ...
	   5:  AF, AL, AG, AQ, AN, ...
	   6:  , , , , , ...
	   7:  28717213, 3582205, 32818500, 70260, 69150, ...
	   8:  14749926, 3258139, 25341272, 47199, 52837, ...
	   9:  33864492, 3826712, 36588772, 80655, 73512, ...
	   10:  40.63, 18.2, 21.94, 23.26, 9.65, ...
	   11:  17.15, 6.48, 5.09, 4.38, 5.74, ...
	   12:  10.32, -1.39, -0.4, 3.29, 6.67, ...
	   13:  2.35, 1.17, 1.69, 1.89, 0.39, ...
	   14:  3.38, 1.03, 1.65, 2.22, 1.06, ...
	   15:  142.48, 37.28, 37.74, 9.82, 4.06, ...
	   16:  145.99, 39.68, 40.34, 11.61, 4.4, ...
	   17:  138.8, 34.71, 35.02, 7.93, 3.7, ...
	   18:  46.97, 72.37, 70.54, 75.75, 83.49, ...
	   19:  47.67, 69.53, 69.14, 71.35, 80.58, ...
	   20:  46.23, 75.42, 72.01, 80.41, 86.58, ...

You now can select the metadata you want to keep in SVG output by setting the -k option

	python shp2svg -a countries.shp -k name,iso2,iso3
	
Output:

	analyzing shapefile WorldCountries
	
	Geometry:
	   253 	Records (total)
	   253 	Polygons
	
	Metadata:
	   name:  Afghanistan, Albania, Algeria, American Samoa, Andorra, ...
	   iso2:  AF, AL, DZ, AS, AD, ...
	   iso3:  AFG, ALB, DZA, ASM, AND, ...

ToDos
----------
- map projection
- svg output :)
- shape filter based on metadata queries
- geometry simplification

