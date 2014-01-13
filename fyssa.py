def set(var, val): db[var] = val

def get(var): return db[var]

def skip(): pass

def quit(): return "quit"
	
def out(var):
	print "The %s is %s" % (var, get(var))

def rawfetch(var):
	val = raw_input("Set %s ('list' to see all): " % var)
	set(var, val)
	
def fetch(var, typ="float"):
	try:
		val = float(raw_input("Set %s (%s): " % (var, typ)))
		set(var, val)
	except ValueError:
		print "Not a number"
		fetch(var)

def is_func(fn):
	return hasattr(fn, '__call__')

def list():
	# in case you can remove/add functions
	print [key for key in db if is_func(db[key])]
	#print [f.__name__ for f in funcs]

def func(var):
	return db[var]() is None

def call():
	try:
		rawfetch("cmd")
		return func(get("cmd"))
	except (TypeError, KeyError):
		print "Not a function"
		return call()
	return True

def dbinit():
	for f in funcs:
		set(f.__name__, f)

#def test():
#	fetch("nana")
#	set("the area", get("nana")*get("nana"))
#	out("the area")

#############################################

import math	

def rect2polar():
	fetch("x")
	fetch("y")
	print "-> (sqrt(x^2 + y^2), tan^-1(y/x))"
	set("polar coordinate", (math.sqrt(get("x")**2+get("y")**2), math.degrees(math.atan2(get("y"), get("x")))))
	out("polar coordinate")
	
def polar2rect():
	fetch("r")
	fetch("q", "degrees")
	print "-> (r*cos(q), r*sin(q))"
	set("rect coordinate", (get("r")*math.cos(math.radians(get("q"))), get("r")*math.sin(math.radians(get("q")))))
	out("rect coordinate")

funcs = [list, quit, rect2polar, polar2rect]
db = {}
dbinit()

while call(): print ""