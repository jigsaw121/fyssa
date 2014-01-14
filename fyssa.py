def set(var, val): db[var] = val

def get(var): return db[var]

def skip(): pass

def quit(): return "quit"
	
def out(var):
	print "The %s is %s" % (var, get(var))

def rawfetch(var, prompt):
	val = raw_input("Set %s (%s): " % (var, prompt))
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
		rawfetch("cmd", "'list' to see all")
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

def factorof(b):
	if not "x" in b:
		return int(b)
	factor = b[:-1]
	if not factor:
		return 1
	return int(factor)

def multiply(a, b):
	return str(factorof(a)*factorof(b))+"x"

def next_op(eq):
	if eq[0] in "+-/*^()":
		return eq[0]

	i = 1
	while 1:
		if i>=len(eq) or eq[i] in "+-/*^()":
			return eq[:i]
		i += 1
		
def prio(op):
	if op=="^": return 4
	if op in "*/": return 3
	if op in "+-": return 2
	
	print "Priorization warning"
	return 0

def topostfix(eq):
	out=[]
	ops=[]
	
	while eq:
		nxt = next_op(eq)
		if nxt not in "+-/*^()": 
			out.append(nxt)
			if ops and ops[-1]=="^":
				out.append(ops[-1])
				ops.pop()
		else: 
			if nxt==")":
				while ops[-1] != "(":
					out.append(ops[-1])
					ops.pop()
				ops.pop()
			
			else:
				print nxt, ops
				if ops and nxt != "(" and prio(nxt) <= prio(ops[-1]):
					out.append(ops[-1])
					ops.pop()
				ops.append(nxt)
		
		eq = eq[len(nxt):]
		
	while ops:
		out.append(ops[-1])
		ops.pop()
		
	return out

#def xsum(a,b):

def varop(lst, i, op, nvarbeh):
	# an operation on two numbers, defined by the 'op' function
	# modifies the list 'lst' from the starting index 'i' onwards
	
	xc = int("x" in lst[i]) + int("x" in lst[i+1])
	
	for c in "+-*/":
		if lst[i].find(c) != -1 or lst[i+1].find(c) != -1:
			xc = 1
			break
	
	# for zero xc, both just numbers
	# for one, incompatible operation ax op b
	# for two, both of form ax
	if xc==1: 
		out = nvarbeh(lst)
	elif xc==0:
		out = op(factorof(lst[i]), factorof(lst[i+1]))
	elif xc==2:
		out = op(factorof(lst[i]), factorof(lst[i+1]))+"x"
	lst.pop(i)
	lst.pop(i)
	lst.insert(i,out)
	return 1
	
def add(lst, i):
	return varop(lst, i, (lambda x,y: str(int(x) + int(y))), (lambda lst: lst[i] + lst[i+2] + lst[i+1]))

def sub(lst, i):
	return varop(lst, i, (lambda x,y: str(int(x) - int(y))), (lambda lst: lst[i] + lst[i+2] + lst[i+1]))

def mul(lst, i):
	return varop(lst, i, (lambda x,y: str(int(x) * int(y))), (lambda lst: str(int(factorof(lst[i])) * int(factorof(lst[i+1]))) + "x"))

def div(lst, i):
	return varop(lst, i, (lambda x,y: str(int(x) / int(y))), (lambda lst: str(int(factorof(lst[i])) / int(factorof(lst[i+1]))) + "x"))
	
def pow2(lst, i):
	return varop(lst, i, (lambda x,y: str(int(x) ^ int(y))), (lambda lst: lst[i] + lst[i+2] + lst[i+1]))

def toint(op):
	if op in "+-/*^": return op
	if "x" in op: return op
	return int(op)

def dopostfix(eq):
	#eq = [toint(op) for op in eq]
	i = 0
	while eq and i<len(eq):
		if eq[i]=="+":
			gone = add(eq, i-2)
			if gone:
				eq.pop(i-gone)
				i-=gone
			else:
				i+=1
		elif eq[i]=="-":
			gone = sub(eq, i-2)
			if gone:
				eq.pop(i-gone)
				i-=gone
			else:
				i+=1
		elif eq[i]=="*":
			gone = mul(eq, i-2)
			if gone:
				eq.pop(i-gone)
				i-=gone
			else:
				i+=1
		elif eq[i]=="/":
			gone = div(eq, i-2)
			if gone:
				eq.pop(i-gone)
				i-=gone
			else:
				i+=1
		elif eq[i]=="^":
			gone = div(eq, i-2)
			if gone:
				eq.pop(i-gone)
				i-=gone
			else:
				i+=1
		else:
			i+=1
		print eq, i

	return eq

def repostfix(eq):
	# forces an incomplete attempt together
	#eq = 
	return eq
	
def derive():
	rawfetch("eq", "equation")
	oldeq = get("eq")
	
	eq = topostfix(oldeq)
	print "postfix form: %s" % " ".join(eq)
	eq = dopostfix(eq)
	eq = repostfix(eq)
	#while eq[0] != oldeq[0]:
	#	oldeq = eq
	#	eq = topostfix(oldeq)
	#	print "postfix form: %s" % " ".join(eq)
	#	eq = dopostfix(eq)
	#	eq = repostfix(eq)
		
	#eq = eq.split("^")
	#eq = multiply(eq[1], eq[0])+"^"+str(int(eq[1])-1) 
	set("eq", eq)
	out("eq")

funcs = [list, quit, rect2polar, polar2rect, derive]
db = {}
dbinit()

while call(): print ""