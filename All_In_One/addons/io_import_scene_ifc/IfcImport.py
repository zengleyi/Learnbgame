# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.4
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_IfcImport', [dirname(__file__)])
        except ImportError:
            import _IfcImport
            return _IfcImport
        if fp is not None:
            try:
                _mod = imp.load_module('_IfcImport', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _IfcImport = swig_import_helper()
    del swig_import_helper
else:
    import _IfcImport
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _IfcImport.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _IfcImport.SwigPyIterator_value(self)
    def incr(self, n = 1): return _IfcImport.SwigPyIterator_incr(self, n)
    def decr(self, n = 1): return _IfcImport.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _IfcImport.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _IfcImport.SwigPyIterator_equal(self, *args)
    def copy(self): return _IfcImport.SwigPyIterator_copy(self)
    def next(self): return _IfcImport.SwigPyIterator_next(self)
    def __next__(self): return _IfcImport.SwigPyIterator___next__(self)
    def previous(self): return _IfcImport.SwigPyIterator_previous(self)
    def advance(self, *args): return _IfcImport.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _IfcImport.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _IfcImport.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _IfcImport.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _IfcImport.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _IfcImport.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _IfcImport.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _IfcImport.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class IfcMesh(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IfcMesh, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IfcMesh, name)
    __repr__ = _swig_repr
    __swig_setmethods__["id"] = _IfcImport.IfcMesh_id_set
    __swig_getmethods__["id"] = _IfcImport.IfcMesh_id_get
    if _newclass:id = _swig_property(_IfcImport.IfcMesh_id_get, _IfcImport.IfcMesh_id_set)
    __swig_setmethods__["verts"] = _IfcImport.IfcMesh_verts_set
    __swig_getmethods__["verts"] = _IfcImport.IfcMesh_verts_get
    if _newclass:verts = _swig_property(_IfcImport.IfcMesh_verts_get, _IfcImport.IfcMesh_verts_set)
    __swig_setmethods__["faces"] = _IfcImport.IfcMesh_faces_set
    __swig_getmethods__["faces"] = _IfcImport.IfcMesh_faces_get
    if _newclass:faces = _swig_property(_IfcImport.IfcMesh_faces_get, _IfcImport.IfcMesh_faces_set)
    __swig_setmethods__["edges"] = _IfcImport.IfcMesh_edges_set
    __swig_getmethods__["edges"] = _IfcImport.IfcMesh_edges_get
    if _newclass:edges = _swig_property(_IfcImport.IfcMesh_edges_get, _IfcImport.IfcMesh_edges_set)
    def __init__(self): 
        this = _IfcImport.new_IfcMesh()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _IfcImport.delete_IfcMesh
    __del__ = lambda self : None;
IfcMesh_swigregister = _IfcImport.IfcMesh_swigregister
IfcMesh_swigregister(IfcMesh)

class IfcGeomObject(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IfcGeomObject, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IfcGeomObject, name)
    __repr__ = _swig_repr
    __swig_setmethods__["name"] = _IfcImport.IfcGeomObject_name_set
    __swig_getmethods__["name"] = _IfcImport.IfcGeomObject_name_get
    if _newclass:name = _swig_property(_IfcImport.IfcGeomObject_name_get, _IfcImport.IfcGeomObject_name_set)
    __swig_setmethods__["type"] = _IfcImport.IfcGeomObject_type_set
    __swig_getmethods__["type"] = _IfcImport.IfcGeomObject_type_get
    if _newclass:type = _swig_property(_IfcImport.IfcGeomObject_type_get, _IfcImport.IfcGeomObject_type_set)
    __swig_setmethods__["matrix"] = _IfcImport.IfcGeomObject_matrix_set
    __swig_getmethods__["matrix"] = _IfcImport.IfcGeomObject_matrix_get
    if _newclass:matrix = _swig_property(_IfcImport.IfcGeomObject_matrix_get, _IfcImport.IfcGeomObject_matrix_set)
    __swig_setmethods__["mesh"] = _IfcImport.IfcGeomObject_mesh_set
    __swig_getmethods__["mesh"] = _IfcImport.IfcGeomObject_mesh_get
    if _newclass:mesh = _swig_property(_IfcImport.IfcGeomObject_mesh_get, _IfcImport.IfcGeomObject_mesh_set)
    def __init__(self): 
        this = _IfcImport.new_IfcGeomObject()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _IfcImport.delete_IfcGeomObject
    __del__ = lambda self : None;
IfcGeomObject_swigregister = _IfcImport.IfcGeomObject_swigregister
IfcGeomObject_swigregister(IfcGeomObject)


def Next():
  return _IfcImport.Next()
Next = _IfcImport.Next

def Get():
  return _IfcImport.Get()
Get = _IfcImport.Get

def Progress():
  return _IfcImport.Progress()
Progress = _IfcImport.Progress
class IntVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IntVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IntVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _IfcImport.IntVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _IfcImport.IntVector___nonzero__(self)
    def __bool__(self): return _IfcImport.IntVector___bool__(self)
    def __len__(self): return _IfcImport.IntVector___len__(self)
    def pop(self): return _IfcImport.IntVector_pop(self)
    def __getslice__(self, *args): return _IfcImport.IntVector___getslice__(self, *args)
    def __setslice__(self, *args): return _IfcImport.IntVector___setslice__(self, *args)
    def __delslice__(self, *args): return _IfcImport.IntVector___delslice__(self, *args)
    def __delitem__(self, *args): return _IfcImport.IntVector___delitem__(self, *args)
    def __getitem__(self, *args): return _IfcImport.IntVector___getitem__(self, *args)
    def __setitem__(self, *args): return _IfcImport.IntVector___setitem__(self, *args)
    def append(self, *args): return _IfcImport.IntVector_append(self, *args)
    def empty(self): return _IfcImport.IntVector_empty(self)
    def size(self): return _IfcImport.IntVector_size(self)
    def clear(self): return _IfcImport.IntVector_clear(self)
    def swap(self, *args): return _IfcImport.IntVector_swap(self, *args)
    def get_allocator(self): return _IfcImport.IntVector_get_allocator(self)
    def begin(self): return _IfcImport.IntVector_begin(self)
    def end(self): return _IfcImport.IntVector_end(self)
    def rbegin(self): return _IfcImport.IntVector_rbegin(self)
    def rend(self): return _IfcImport.IntVector_rend(self)
    def pop_back(self): return _IfcImport.IntVector_pop_back(self)
    def erase(self, *args): return _IfcImport.IntVector_erase(self, *args)
    def __init__(self, *args): 
        this = _IfcImport.new_IntVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _IfcImport.IntVector_push_back(self, *args)
    def front(self): return _IfcImport.IntVector_front(self)
    def back(self): return _IfcImport.IntVector_back(self)
    def assign(self, *args): return _IfcImport.IntVector_assign(self, *args)
    def resize(self, *args): return _IfcImport.IntVector_resize(self, *args)
    def insert(self, *args): return _IfcImport.IntVector_insert(self, *args)
    def reserve(self, *args): return _IfcImport.IntVector_reserve(self, *args)
    def capacity(self): return _IfcImport.IntVector_capacity(self)
    __swig_destroy__ = _IfcImport.delete_IntVector
    __del__ = lambda self : None;
IntVector_swigregister = _IfcImport.IntVector_swigregister
IntVector_swigregister(IntVector)

def Init(*args):
  return _IfcImport.Init(*args)
Init = _IfcImport.Init

class FloatVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FloatVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FloatVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _IfcImport.FloatVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _IfcImport.FloatVector___nonzero__(self)
    def __bool__(self): return _IfcImport.FloatVector___bool__(self)
    def __len__(self): return _IfcImport.FloatVector___len__(self)
    def pop(self): return _IfcImport.FloatVector_pop(self)
    def __getslice__(self, *args): return _IfcImport.FloatVector___getslice__(self, *args)
    def __setslice__(self, *args): return _IfcImport.FloatVector___setslice__(self, *args)
    def __delslice__(self, *args): return _IfcImport.FloatVector___delslice__(self, *args)
    def __delitem__(self, *args): return _IfcImport.FloatVector___delitem__(self, *args)
    def __getitem__(self, *args): return _IfcImport.FloatVector___getitem__(self, *args)
    def __setitem__(self, *args): return _IfcImport.FloatVector___setitem__(self, *args)
    def append(self, *args): return _IfcImport.FloatVector_append(self, *args)
    def empty(self): return _IfcImport.FloatVector_empty(self)
    def size(self): return _IfcImport.FloatVector_size(self)
    def clear(self): return _IfcImport.FloatVector_clear(self)
    def swap(self, *args): return _IfcImport.FloatVector_swap(self, *args)
    def get_allocator(self): return _IfcImport.FloatVector_get_allocator(self)
    def begin(self): return _IfcImport.FloatVector_begin(self)
    def end(self): return _IfcImport.FloatVector_end(self)
    def rbegin(self): return _IfcImport.FloatVector_rbegin(self)
    def rend(self): return _IfcImport.FloatVector_rend(self)
    def pop_back(self): return _IfcImport.FloatVector_pop_back(self)
    def erase(self, *args): return _IfcImport.FloatVector_erase(self, *args)
    def __init__(self, *args): 
        this = _IfcImport.new_FloatVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _IfcImport.FloatVector_push_back(self, *args)
    def front(self): return _IfcImport.FloatVector_front(self)
    def back(self): return _IfcImport.FloatVector_back(self)
    def assign(self, *args): return _IfcImport.FloatVector_assign(self, *args)
    def resize(self, *args): return _IfcImport.FloatVector_resize(self, *args)
    def insert(self, *args): return _IfcImport.FloatVector_insert(self, *args)
    def reserve(self, *args): return _IfcImport.FloatVector_reserve(self, *args)
    def capacity(self): return _IfcImport.FloatVector_capacity(self)
    __swig_destroy__ = _IfcImport.delete_FloatVector
    __del__ = lambda self : None;
FloatVector_swigregister = _IfcImport.FloatVector_swigregister
FloatVector_swigregister(FloatVector)

class ObjVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ObjVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ObjVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _IfcImport.ObjVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _IfcImport.ObjVector___nonzero__(self)
    def __bool__(self): return _IfcImport.ObjVector___bool__(self)
    def __len__(self): return _IfcImport.ObjVector___len__(self)
    def pop(self): return _IfcImport.ObjVector_pop(self)
    def __getslice__(self, *args): return _IfcImport.ObjVector___getslice__(self, *args)
    def __setslice__(self, *args): return _IfcImport.ObjVector___setslice__(self, *args)
    def __delslice__(self, *args): return _IfcImport.ObjVector___delslice__(self, *args)
    def __delitem__(self, *args): return _IfcImport.ObjVector___delitem__(self, *args)
    def __getitem__(self, *args): return _IfcImport.ObjVector___getitem__(self, *args)
    def __setitem__(self, *args): return _IfcImport.ObjVector___setitem__(self, *args)
    def append(self, *args): return _IfcImport.ObjVector_append(self, *args)
    def empty(self): return _IfcImport.ObjVector_empty(self)
    def size(self): return _IfcImport.ObjVector_size(self)
    def clear(self): return _IfcImport.ObjVector_clear(self)
    def swap(self, *args): return _IfcImport.ObjVector_swap(self, *args)
    def get_allocator(self): return _IfcImport.ObjVector_get_allocator(self)
    def begin(self): return _IfcImport.ObjVector_begin(self)
    def end(self): return _IfcImport.ObjVector_end(self)
    def rbegin(self): return _IfcImport.ObjVector_rbegin(self)
    def rend(self): return _IfcImport.ObjVector_rend(self)
    def pop_back(self): return _IfcImport.ObjVector_pop_back(self)
    def erase(self, *args): return _IfcImport.ObjVector_erase(self, *args)
    def __init__(self, *args): 
        this = _IfcImport.new_ObjVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _IfcImport.ObjVector_push_back(self, *args)
    def front(self): return _IfcImport.ObjVector_front(self)
    def back(self): return _IfcImport.ObjVector_back(self)
    def assign(self, *args): return _IfcImport.ObjVector_assign(self, *args)
    def resize(self, *args): return _IfcImport.ObjVector_resize(self, *args)
    def insert(self, *args): return _IfcImport.ObjVector_insert(self, *args)
    def reserve(self, *args): return _IfcImport.ObjVector_reserve(self, *args)
    def capacity(self): return _IfcImport.ObjVector_capacity(self)
    __swig_destroy__ = _IfcImport.delete_ObjVector
    __del__ = lambda self : None;
ObjVector_swigregister = _IfcImport.ObjVector_swigregister
ObjVector_swigregister(ObjVector)

# This file is compatible with both classic and new-style classes.


