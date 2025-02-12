# This is the release version of the plugin file io_import_scene_osm_dev.py
# If you would like to make edits, make them in the file io_import_scene_osm_dev.py and the other related modules
# To create the release version of io_import_scene_osm_dev.py, executed:
# python plugin_builder.py io_import_scene_osm_dev.py:
bl_info = {
	"name": "Import OpenStreetMap (.osm)",
	"author": "Vladimir Elistratov <vladimir.elistratov@gmail.com>",
	"version": (1, 0, 0),
	"blender": (2, 80, 0),
	"location": "File > Import > OpenStreetMap (.osm)",
	"description": "Import a file in the OpenStreetMap format (.osm)",
	"warning": "",
	"wiki_url": "https://github.com/vvoovv/blender-geo/wiki/Import-OpenStreetMap-(.osm)",
	"tracker_url": "https://github.com/vvoovv/blender-geo/issues",
	"support": "COMMUNITY",
	"category": "Learnbgame",
}

import bpy, bmesh
# ImportHelper is a helper class, defines filename and invoke() function which calls the file selector
from bpy_extras.io_utils import ImportHelper

import sys, os
import math

# see conversion formulas at
# http://en.wikipedia.org/wiki/Transverse_Mercator_projection
# and
# http://mathworld.wolfram.com/MercatorProjection.html
class TransverseMercator:
	radius = 6378137

	def __init__(self, **kwargs):
		# setting default values
		self.lat = 0 # in degrees
		self.lon = 0 # in degrees
		self.k = 1 # scale factor
		
		for attr in kwargs:
			setattr(self, attr, kwargs[attr])
		self.latInRadians = math.radians(self.lat)

	def fromGeographic(self, lat, lon):
		lat = math.radians(lat)
		lon = math.radians(lon-self.lon)
		B = math.sin(lon) * math.cos(lat)
		x = 0.5 * self.k * self.radius * math.log((1+B)/(1-B))
		y = self.k * self.radius * ( math.atan(math.tan(lat)/math.cos(lon)) - self.latInRadians )
		return (x,y)

	def toGeographic(self, x, y):
		x = x/(self.k * self.radius)
		y = y/(self.k * self.radius)
		D = y + self.latInRadians
		lon = math.atan(math.sinh(x)/math.cos(D))
		lat = math.asin(math.sin(D)/math.cosh(x))

		lon = self.lon + math.degrees(lon)
		lat = math.degrees(lat)
		return (lat, lon)

import xml.etree.cElementTree as etree
import inspect, importlib

def prepareHandlers(kwArgs):
	nodeHandlers = []
	wayHandlers = []
	# getting a dictionary with local variables
	_locals = locals()
	for handlers in ("nodeHandlers", "wayHandlers"):
		if handlers in kwArgs:
			for handler in kwArgs[handlers]:
				if isinstance(handler, str):
					# we've got a module name
					handler = importlib.import_module(handler)
				if inspect.ismodule(handler):
					# iterate through all module functions
					for f in inspect.getmembers(handler, inspect.isclass):
						_locals[handlers].append(f[1])
				elif inspect.isclass(handler):
					_locals[handlers].append(handler)
		if len(_locals[handlers])==0: _locals[handlers] = None
	return (nodeHandlers if len(nodeHandlers) else None, wayHandlers if len(wayHandlers) else None)

class OsmParser:
	
	def __init__(self, filename, **kwargs):
		self.nodes = {}
		self.ways = {}
		self.relations = {}
		self.minLat = 90
		self.maxLat = -90
		self.minLon = 180
		self.maxLon = -180
		# self.bounds contains the attributes of the bounds tag of the .osm file if available
		self.bounds = None
		
		(self.nodeHandlers, self.wayHandlers) = prepareHandlers(kwargs)
		
		self.doc = etree.parse(filename)
		self.osm = self.doc.getroot()
		self.prepare()

	def prepare(self):
		allowedTags = set(("node", "way", "bounds"))
		for e in self.osm: # e stands for element
			attrs = e.attrib
			if e.tag not in allowedTags : continue
			if "action" in attrs and attrs["action"] == "delete": continue
			if e.tag == "node":
				_id = attrs["id"]
				tags = None
				for c in e:
					if c.tag == "tag":
						if not tags: tags = {}
						tags[c.get("k")] = c.get("v")
				lat = float(attrs["lat"])
				lon = float(attrs["lon"])
				# calculating minLat, maxLat, minLon, maxLon
				# commented out: only imported objects take part in the extent calculation
				#if lat<self.minLat: self.minLat = lat
				#elif lat>self.maxLat: self.maxLat = lat
				#if lon<self.minLon: self.minLon = lon
				#elif lon>self.maxLon: self.maxLon = lon
				# creating entry
				entry = dict(
					id=_id,
					e=e,
					lat=lat,
					lon=lon
				)
				if tags: entry["tags"] = tags
				self.nodes[_id] = entry
			elif e.tag == "way":
				_id = attrs["id"]
				nodes = []
				tags = None
				for c in e:
					if c.tag == "nd":
						nodes.append(c.get("ref"))
					elif c.tag == "tag":
						if not tags: tags = {}
						tags[c.get("k")] = c.get("v")
				# ignore ways without tags
				if tags:
					self.ways[_id] = dict(
						id=_id,
						e=e,
						nodes=nodes,
						tags=tags
					)
			elif e.tag == "bounds":
				self.bounds = {
					"minLat": float(attrs["minlat"]),
					"minLon": float(attrs["minlon"]),
					"maxLat": float(attrs["maxlat"]),
					"maxLon": float(attrs["maxlon"])
				}
		
		self.calculateExtent()

	def iterate(self, wayFunction, nodeFunction):
		nodeHandlers = self.nodeHandlers
		wayHandlers = self.wayHandlers
		
		if wayHandlers:
			for _id in self.ways:
				way = self.ways[_id]
				if "tags" in way:
					for handler in wayHandlers:
						if handler.condition(way["tags"], way):
							wayFunction(way, handler)
							continue
		
		if nodeHandlers:
			for _id in self.nodes:
				node = self.nodes[_id]
				if "tags" in node:
					for handler in nodeHandlers:
						if handler.condition(node["tags"], node):
							nodeFunction(node, handler)
							continue

	def parse(self, **kwargs):
		def wayFunction(way, handler):
			handler.handler(way, self, kwargs)
		def nodeFunction(node, handler):
			handler.handler(node, self, kwargs)
		self.iterate(wayFunction, nodeFunction)

	def calculateExtent(self):
		def wayFunction(way, handler):
			wayNodes = way["nodes"]
			for node in range(len(wayNodes)-1): # skip the last node which is the same as the first ones
				nodeFunction(self.nodes[wayNodes[node]])
		def nodeFunction(node, handler=None):
			lon = node["lon"]
			lat = node["lat"]
			if lat<self.minLat: self.minLat = lat
			elif lat>self.maxLat: self.maxLat = lat
			if lon<self.minLon: self.minLon = lon
			elif lon>self.maxLon: self.maxLon = lon
		self.iterate(wayFunction, nodeFunction)

import os, math
import bpy, bmesh
import bmesh

def extrudeMesh(bm, thickness):
	"""
	Extrude bmesh
	"""
	geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
	verts_extruded = [v for v in geom["geom"] if isinstance(v, bmesh.types.BMVert)]
	bmesh.ops.translate(bm, verts=verts_extruded, vec=(0, 0, thickness))

def assignTags(obj, tags):
	for key in tags:
		obj[key] = tags[key]


class buildings:
	@staticmethod
	def condition(tags, way):
		return "building" in tags
	
	@staticmethod
	def handler(way, parser, kwargs):
		wayNodes = way["nodes"]
		numNodes = len(wayNodes)-1 # we need to skip the last node which is the same as the first ones
		# a polygon must have at least 3 vertices
		if numNodes<3: return
		
		if not kwargs["bm"]: # not a single mesh
			tags = way["tags"]
			thickness = kwargs["thickness"] if ("thickness" in kwargs) else 0
			osmId = way["id"]
			# compose object name
			name = osmId
			if "addr:housenumber" in tags and "addr:street" in tags:
				name = tags["addr:street"] + ", " + tags["addr:housenumber"]
			elif "name" in tags:
				name = tags["name"]
		
		bm = kwargs["bm"] if kwargs["bm"] else bmesh.new()
		verts = []
		for node in range(numNodes):
			node = parser.nodes[wayNodes[node]]
			v = kwargs["projection"].fromGeographic(node["lat"], node["lon"])
			verts.append( bm.verts.new((v[0], v[1], 0)) )
		
		bm.faces.new(verts)
		
		if not kwargs["bm"]:
			thickness = kwargs["thickness"] if ("thickness" in kwargs) else 0
			# extrude
			if thickness>0:
				extrudeMesh(bm, thickness)
			
			bm.normal_update()
			
			mesh = bpy.data.meshes.new(osmId)
			bm.to_mesh(mesh)
			
			obj = bpy.data.objects.new(name, mesh)
			bpy.context.collection.objects.link(obj)
			bpy.context.scene.update()
			
			# final adjustments
			obj.select_set(True)
			# assign OSM tags to the blender object
			assignTags(obj, tags)


class highways:
	@staticmethod
	def condition(tags, way):
		return "highway" in tags
	
	@staticmethod
	def handler(way, parser, kwargs):
		wayNodes = way["nodes"]
		numNodes = len(wayNodes) # we need to skip the last node which is the same as the first ones
		# a way must have at least 2 vertices
		if numNodes<2: return
		
		if not kwargs["bm"]: # not a single mesh
			tags = way["tags"]
			osmId = way["id"]
			# compose object name
			name = tags["name"] if "name" in tags else osmId
		
		bm = kwargs["bm"] if kwargs["bm"] else bmesh.new()
		verts = []
		prevVertex = None
		for node in range(numNodes):
			node = parser.nodes[wayNodes[node]]
			v = kwargs["projection"].fromGeographic(node["lat"], node["lon"])
			v = bm.verts.new((v[0], v[1], 0))
			if prevVertex:
				bm.edges.new([prevVertex, v])
			prevVertex = v
		
		if not kwargs["bm"]:
			mesh = bpy.data.meshes.new(osmId)
			bm.to_mesh(mesh)
			
			obj = bpy.data.objects.new(name, mesh)
			bpy.context.collection.objects.link(obj)
			bpy.context.scene.update()
			
			# final adjustments
			obj.select_set(True)
			# assign OSM tags to the blender object
			assignTags(obj, tags)

import os, math
import bpy, bmesh
import bmesh

def extrudeMesh(bm, thickness):
	"""
	Extrude bmesh
	"""
	geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
	verts_extruded = [v for v in geom["geom"] if isinstance(v, bmesh.types.BMVert)]
	bmesh.ops.translate(bm, verts=verts_extruded, vec=(0, 0, thickness))

def assignTags(obj, tags):
	for key in tags:
		obj[key] = tags[key]


class buildings:
	@staticmethod
	def condition(tags, way):
		return "building" in tags
	
	@staticmethod
	def handler(way, parser, kwargs):
		wayNodes = way["nodes"]
		numNodes = len(wayNodes)-1 # we need to skip the last node which is the same as the first ones
		# a polygon must have at least 3 vertices
		if numNodes<3: return
		
		if not kwargs["bm"]: # not a single mesh
			tags = way["tags"]
			thickness = kwargs["thickness"] if ("thickness" in kwargs) else 0
			osmId = way["id"]
			# compose object name
			name = osmId
			if "addr:housenumber" in tags and "addr:street" in tags:
				name = tags["addr:street"] + ", " + tags["addr:housenumber"]
			elif "name" in tags:
				name = tags["name"]
		
		bm = kwargs["bm"] if kwargs["bm"] else bmesh.new()
		verts = []
		for node in range(numNodes):
			node = parser.nodes[wayNodes[node]]
			v = kwargs["projection"].fromGeographic(node["lat"], node["lon"])
			verts.append( bm.verts.new((v[0], v[1], 0)) )
		
		bm.faces.new(verts)
		
		if not kwargs["bm"]:
			thickness = kwargs["thickness"] if ("thickness" in kwargs) else 0
			# extrude
			if thickness>0:
				extrudeMesh(bm, thickness)
			
			bm.normal_update()
			
			mesh = bpy.data.meshes.new(osmId)
			bm.to_mesh(mesh)
			
			obj = bpy.data.objects.new(name, mesh)
			bpy.context.collection.objects.link(obj)
			bpy.context.scene.update()
			
			# final adjustments
			obj.select_set(True)
			# assign OSM tags to the blender object
			assignTags(obj, tags)


class highways:
	@staticmethod
	def condition(tags, way):
		return "highway" in tags
	
	@staticmethod
	def handler(way, parser, kwargs):
		wayNodes = way["nodes"]
		numNodes = len(wayNodes) # we need to skip the last node which is the same as the first ones
		# a way must have at least 2 vertices
		if numNodes<2: return
		
		if not kwargs["bm"]: # not a single mesh
			tags = way["tags"]
			osmId = way["id"]
			# compose object name
			name = tags["name"] if "name" in tags else osmId
		
		bm = kwargs["bm"] if kwargs["bm"] else bmesh.new()
		verts = []
		prevVertex = None
		for node in range(numNodes):
			node = parser.nodes[wayNodes[node]]
			v = kwargs["projection"].fromGeographic(node["lat"], node["lon"])
			v = bm.verts.new((v[0], v[1], 0))
			if prevVertex:
				bm.edges.new([prevVertex, v])
			prevVertex = v
		
		if not kwargs["bm"]:
			mesh = bpy.data.meshes.new(osmId)
			bm.to_mesh(mesh)
			
			obj = bpy.data.objects.new(name, mesh)
			bpy.context.collection.objects.link(obj)
			bpy.context.scene.update()
			
			# final adjustments
			obj.select_set(True)
			# assign OSM tags to the blender object
			assignTags(obj, tags)

import bmesh

def extrudeMesh(bm, thickness):
	"""
	Extrude bmesh
	"""
	geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
	verts_extruded = [v for v in geom["geom"] if isinstance(v, bmesh.types.BMVert)]
	bmesh.ops.translate(bm, verts=verts_extruded, vec=(0, 0, thickness))


class ImportOsm(bpy.types.Operator, ImportHelper):
	"""Import a file in the OpenStreetMap format (.osm)"""
	bl_idname = "import_scene.osm"  # important since its how bpy.ops.import_scene.osm is constructed
	bl_label = "Import OpenStreetMap"
	bl_options = {"UNDO"}

	# ImportHelper mixin class uses this
	filename_ext = ".osm"

	filter_glob = bpy.props.StringProperty(
		default="*.osm",
		options={"HIDDEN"},
	)

	ignoreGeoreferencing = bpy.props.BoolProperty(
		name="Ignore existing georeferencing",
		description="Ignore existing georeferencing and make a new one",
		default=False,
	)
	
	singleMesh = bpy.props.BoolProperty(
		name="Import as a single mesh",
		description="Import OSM objects as a single mesh instead of separate Blender objects",
		default=False,
	)

	importBuildings = bpy.props.BoolProperty(
		name="Import buildings",
		description="Import building outlines",
		default=True,
	)

	importHighways = bpy.props.BoolProperty(
		name="Import roads and paths",
		description="Import roads and paths",
		default=False,
	)

	thickness = bpy.props.FloatProperty(
		name="Thickness",
		description="Set thickness to make OSM building outlines extruded",
		default=0,
	)

	def execute(self, context):
		# setting active object if there is no active object
		if context.mode != "OBJECT":
			# if there is no object in the scene, only "OBJECT" mode is provided
			if not context.view_layer.objects.active:
				context.view_layer.objects.active = context.scene.objects[0]
			bpy.ops.object.mode_set(mode="OBJECT")
		
		bpy.ops.object.select_all(action="DESELECT")
		
		name = os.path.basename(self.filepath)
		
		if self.singleMesh:
			self.bm = bmesh.new()
		else:
			self.bm = None
			# create an empty object to parent all imported OSM objects
			bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
			parentObject = context.active_object
			self.parentObject = parentObject
			parentObject.name = name
		
		self.read_osm_file(context)
		
		if self.singleMesh:
			bm = self.bm
			# extrude
			if self.thickness>0:
				extrudeMesh(bm, self.thickness)
			
			bm.normal_update()
			
			mesh = bpy.data.meshes.new(name)
			bm.to_mesh(mesh)
			
			obj = bpy.data.objects.new(name, mesh)
			bpy.context.collection.objects.link(obj)
			
			# remove double vertices
			context.view_layer.objects.active = obj
			bpy.ops.object.mode_set(mode="EDIT")
			bpy.ops.mesh.select_all(action="SELECT")
			bpy.ops.mesh.remove_doubles()
			bpy.ops.mesh.select_all(action="DESELECT")
			bpy.ops.object.mode_set(mode="OBJECT")
			
			bpy.context.scene.update()
		else:
			# perform parenting
			context.view_layer.objects.active = parentObject
			bpy.ops.object.parent_set()
		
		bpy.ops.object.select_all(action="DESELECT")
		return {"FINISHED"}

	def read_osm_file(self, context):
		scene = context.scene
		
		wayHandlers = []
		if self.importBuildings: wayHandlers.append(buildings)
		if self.importHighways: wayHandlers.append(highways)
		
		osm = OsmParser(self.filepath,
			# possible values for wayHandlers and nodeHandlers list elements:
			#	1) a string name for the module containing classes (all classes from the modules will be used as handlers)
			#	2) a python variable representing the module containing classes (all classes from the modules will be used as handlers)
			#	3) a python variable representing the class
			# Examples:
			# wayHandlers = [buildings, highways]
			# wayHandlers = [handlers.buildings]
			# wayHandlers = [handlers]
			# wayHandlers = ["handlers"]
			wayHandlers = wayHandlers
		)
		
		if "latitude" in scene and "longitude" in scene and not self.ignoreGeoreferencing:
			lat = scene["latitude"]
			lon = scene["longitude"]
		else:
			if osm.bounds and self.importHighways:
				# If the .osm file contains the bounds tag,
				# use its values as the extent of the imported area.
				# Highways may go far beyond the values of the bounds tag.
				# A user might get confused if higways are used in the calculation of the extent of the imported area.
				bounds = osm.bounds
				lat = (bounds["minLat"] + bounds["maxLat"])/2
				lon = (bounds["minLon"] + bounds["maxLon"])/2
			else:
				lat = (osm.minLat + osm.maxLat)/2
				lon = (osm.minLon + osm.maxLon)/2
			scene["latitude"] = lat
			scene["longitude"] = lon
		
		osm.parse(
			projection = TransverseMercator(lat=lat, lon=lon),
			thickness = self.thickness,
			bm = self.bm # if present, indicates the we need to create as single mesh
		)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
	self.layout.operator(ImportOsm.bl_idname, text="OpenStreetMap (.osm)")

def register():
	bpy.utils.register_class(ImportOsm)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
	bpy.utils.unregister_class(ImportOsm)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == '__main__':
	register()