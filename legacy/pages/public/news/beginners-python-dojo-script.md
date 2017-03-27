Here is the script from which <a href="/author/richard">Richard</a> steered the Beginners Python Dojo at <a href="http://www.dev8d.org/">dev8d</a> on 14th Feb 2012.

This goes alongside the <a href="http://cottagelabs.com/python-language-syntax-cheat-sheet/" title="Python Cheat Sheet">Python Cheat Sheet</a>, and you can also download the associated example python files referenced in the text from <a href="http://cottagelabs.com/wp-content/uploads/2012/02/python-dojo.tar_.gz">here</a>.

<pre>
<blockquote>
1 - Starting the Python REPL/Interactive Mode

Simply type "python" at the command line, and we will enter interactive mode

2 - Introducing the Interactive Mode

# assign an integer variable
>>> a = 3

# to print a variable just type it
>>> a
3

# now try some basic arithmetic
>>> b = 8
>>> a + b
11
>>> a - b
-5
>>> a * b
24

# when we do / we get 0, because the real outcome isn't an integer
>>> a / b
0

3 - Floats

# Although python is duck typed, we can explicitly cast the 
# variables to the required type (if such a type cast is 
# supported)
>>> float(a) / float(b)
0.375

# we can also make a variable a float by declaring it in the
# right way
>>> a = 3.0
>>> b = 8.0
>>> a / b
0.375


4 - Strings

# declare an ordinary string
>>> s = "hello world"
>>> s
'hello world'

# declare a unicode formatted string.
>>> s = u"hello world"
>>> s
u'hello world'

# if we try to cut a string over many lines we get an error
# because python takes the end of line to mean the end of an
# expression
>>> s = "hello
  File "<stdin>", line 1
    s = "hello
             ^
SyntaxError: EOL while scanning string literal

# we use the """ delimiter to declare a string over multiple
# lines
>>> s = """hello
... world"""
>>> s
'hello\nworld'


5 - Lists

# declare a list between square brackets
>>> l = [1,2,3]

# get the length of the list
>>> len(l)
3

# access individual elements of the list
>>> l[1]
2

# assign to a specific element in the list
>>> l[0] = 4
>>> l
[4, 2, 3]

# append to a list
>>> l.append(6)

# lists are mixed type
>>> l.append("seven")
>>> l
[4, 2, 3, 6, 'seven']

# list slices give you portions of the full list
>>> l[2:4]
[3, 6]

# determine if an element is in a list
>>> 6 in l
True


6 - Exercise: Create a List containing a mix of integers, floats and strings;
then use the array slicing feature to extract the last two elements

>>> l = [1, 2.0, "three"]
>>> l[1:3]
[2.0, 'three']
>>> l[1:]
[2.0, 'three']


7 - Tuples

# Tuples are very similar to lists
>>> t = (1,2,3)
>>> t
(1, 2, 3)
>>> len(t)
3
>>> t[1]
2
>>> t[1:3]
(2, 3)

# The key difference between a tuple and a list is that a tuple
# is immutable
>>> t[0] = 5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment

# single element tuples must be declared in a special way
# because the () can also be used to split clauses over 
# multiple lines)
>>> t = (1)
>>> t
1
>>> t = (1,)
>>> t
(1,)

# Tuples are quite often used to return multiple values from
# functions, so Python makes it easy to unpack a tuple into
# individual variables
>>> t = (1,2,3)
>>> a, b, c = t
>>> a
1
>>> b
2
>>> c
3

# you can also print multiple elements thus (see how they
# are printed just like a tuple)
>>> a, b, c
(1, 2, 3)


8 - Dictionaries

# A dictionary is a hash or linked list and is declared
# in key/value pairs
>>> d = {"one" : 1, "two" : 2, "three" : 3}

# access an element by its key
>>> d['two']
2

# get a list of the keys
>>> d.keys()
['three', 'two', 'one']

# get the key/value pairs as a list of tuples
>>> d.items()
[('three', 3), ('two', 2), ('one', 1)]

# attempts to access non-existant elements
>>> d["four"]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'four'
>>> d.get("four")
>>> d.get("four", 4)
4

# assigning new keys
>>> d["four"] = 4


9 - Exercise: create a dictionary; then extract a tuple for it and unpack 
that tuple into two variables all in one operation

>>> d = {'four': 4, 'three': 3, 'two': 2, 'one': 1}
>>> n, m = d.items()[3]
>>> n, m
('one', 1)


10 - More string operations

# here we explore how similar to lists strings are
>>> s = "hello world"

# get the length
>>> len(s)
11

# access characters
>>> s[4]
'o'

# string slices
>>> s[4:8]
'o wo'

# looking for substrings
>>> "llo" in "hello world"
True

# Now string concatenation

# the old fashioned way
>>> "hello" + "world"
'helloworld'

# the modern way
>>> "%s %s" % ("hello", "world")
'hello world'


11 - Finding out about the operations on an object

# get a list of the attributes of a specific object
>>> dir(s)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', 
'__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', 
'__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', 
'__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', 
'__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
'_formatter_field_name_split', '_formatter_parser', 'capitalize', 
'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 
'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 
'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 
'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 
'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 
'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']

# get the help text for a type
>>> help(str)

12 - Exercise: do the following string exercises:
    - get the index of the first "o" in "hello world"
    - cast an upper case string to lower case
    - cast a lower case string to upper case
    - trim the excess white-space from around a string

>>> s
'hello world'
>>> s.find("o")
4
>>> s.index("o")
4
>>> s.upper()
'HELLO WORLD'
>>> s.upper().lower()
'hello world'
>>> w = "    hello world     "
>>> w.strip()
'hello world'


13 - Code blocks and indenting

>>> l
[4, 2, 3, 6, 'seven']

# code blocks are preceeded on the previous line by a ":"
# and then indented.  By convention we use 4 spaces rather 
# than tabs.  If you mix tabs and spaces your code won't work
# so stick to the convention when writing your code.

# for the purposes of the Interactive Mode we will use tabs
# because it is quicker
>>> if 2 in l:
...     print "yes"
... 
yes

14 - Control Flow

>>> l
[4, 2, 3, 6, 'seven']

# if-elif-else conditional
>>> if 5 in l:
...     print "five"
... elif 4 in l:
...     print "four"
... else:
...     print "not five or four"
... 
four

# for loop.
# The range function produces a list from 0 to n-1
>>> for i in range(10):
...     print i
... 
0
1
2
3
4
5
6
7
8
9

# while loop.
# Note that python does not have a ++ operator, so we use
# += 1.
# all other mathematical operators work the same way
>>> i = 0
>>> while i < 10:
...     i += 1
...     print i
... 
1
2
3
4
5
6
7
8
9
10
>>> 

16 - Exercise: write a loop which iterates over a dictionary and
prints out the key/value pairs

>>> for k in d.keys():
...     print k, d[k]
... 
four 4
three 3
two 2
one 1
>>> for k, v in d.items():
...     print k, v
... 
four 4
three 3
two 2
one 1


17 - Exercise: write a loop which iterates over a list of numbers 
but only prints out those greater than 5

>>> for i in l:
...     if i > 5:
...             print i
... 
6
8
10
12
14
16


18 - Functions

# define a function
>>> def sum(x, y):
...     return x + y
... 

# once we have defined a function we can use it at any time
# in this Interactive Mode session
>>> sum(5, 10)
15
>>> sum(4,12)
16


# keyword arguments
>>> def sum(x, y, z=0):
...     return x + y + z
... 

# works as before, z defaults to 0
>>> sum(5, 10)
15

# we can specify z like this
>>> sum(5, 10, 15)
30

# or explicitly like this
>>> sum(5, 10, z=25)
40


19 - Exercise: define a function to multiply a minimum of 2 and a maximum
of 4 arguments together

>>> def multiply(a, b, c=1, d=1):
...     return a * b * c * d
... 
>>> multiply(2,3)
6
>>> multiply(2,3,4)
24
>>> multiply(2,3,4,5)
120


20 - * and **

# we can pass arrays in to standard arguments using the * modifier
>>> args = [5, 10]
>>> sum(*args)
15

# we can also pass dictionaries in as keyword arguments using the
# ** modifier
>>> kwargs = {"z" : 20}
>>> sum(*args, **kwargs)
35


# we can also define sum to have an arbitrarily long list of
# arguments
>>> def sum(*args):
...     total = 0
...     for arg in args:
...             total += arg
...     return total
... 
>>> sum(5, 10)
15
>>> sum(1,2,3,4,5,6,7,8,9)
45

# we can also do the same with kwargs, and we access the
# values of kwargs like a dictionary
>>> def sum(**kwargs):
...     return kwargs['x'] + kwargs['y']
... 
>>> sum(x=2, y=3)
5


21 - Exercise: write a "multiply" function which can take an arbitrary
number of arguments, and then multiply the numbers 2,3,4,5,6,7 together

>>> def multiply(*args):
...     total = args[0]
...     for arg in args[1:]:
...             total *= arg
...     return total
... 
>>> multiply(2,3)
6
>>> multiply(2,3,4,5,6,7)
5040


22 - List Comprehension

>>> l = [1,2,3,4,5,6,7,8,9]

# first create a list of the even numbers in this list
# the old fashioned way
>>> nl = []
>>> for n in l:
...     if n % 2 == 0: nl.append(n)
... 
>>> nl
[2, 4, 6, 8]

# now using list comprehension
>>> l
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> nl = [x for x in l if x % 2 == 0]
>>> nl
[2, 4, 6, 8]

23 - Exercise: create a list of the cubes of each element of a given list

[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> nl = [x * x * x for x in l]
>>> nl
[1, 8, 27, 64, 125, 216, 343, 512, 729]

24 - Exercise: create a list of tuples where the first number is the original
element from a list and the second element is the square of that number.  Only
include elements which are exactly divisible by 3

>>> nl = [(x, x * x) for x in l if x % 3 == 0]
>>> nl
[(3, 9), (6, 36), (9, 81)]


25 - module imports

# to import an entire module on the PYTHONPATH
>>> import uuid

# take a look at what that module contains
>>> dir(uuid)
['NAMESPACE_DNS', 'NAMESPACE_OID', 'NAMESPACE_URL', 'NAMESPACE_X500', 
'RESERVED_FUTURE', 'RESERVED_MICROSOFT', 'RESERVED_NCS', 'RFC_4122', 
'UUID', '_UuidCreate', '__author__', '__builtins__', '__doc__', 
'__file__', '__name__', '__package__', '_find_mac', '_ifconfig_getnode', 
'_ipconfig_getnode', '_last_timestamp', '_netbios_getnode', '_node', 
'_random_getnode', '_unixdll_getnode', '_uuid_generate_random', 
'_uuid_generate_time', '_windll_getnode', 'ctypes', 'getnode', 
'lib', 'libname', 'os', 'sys', 'uuid1', 'uuid3', 'uuid4', 'uuid5']

# to invoke one of the operations in the module
>>> uuid.uuid4()
UUID('81487aed-7c54-43b9-8cdd-fa0ddc6553ce')

# we can import just what we want from the module
>>> from uuid import uuid4

# so we run it differently
>>> uuid4()
UUID('dcdbff00-198a-45b0-aaa1-445768369ade')

# you can even give the function or module your own name
>>> from uuid import uuid4 as myuuid

# now run it with the given name
>>> myuuid()
UUID('7f2d691c-def1-48e0-b288-d7f079bbf1c4')


26 - Classes

# The most primitive possible class

# it extends the "object" class, the root class of all python
# classes
>>> class MyClass(object):
...     pass
... 

# instantiate
>>> c = MyClass()

# Now the core features of a class
# Here we import from the "test1" module in the working directory

# import the module (which is just a file in the current directory)
>>> import test1

# look at what the module supports
>>> dir(test1)
['Example', '__builtins__', '__doc__', '__file__', '__name__', '__package__']

# the Example object has a class variable which we can access without
# instantiating the object
>>> test1.Example.class_variable
'hello'

# We can instantiate the object with an argument which is
# passed to the __init__ method
>>> e = test1.Example("richard")

# we can now access both the class and the instance variables
# from the object
>>> e.class_variable
'hello'
>>> e.instance_variable
'richard'

27 - Class Methods

# Now how to create a class method

# first import from "test2"
>>> import test2
>>> dir(test2)
['Calculator', '__builtins__', '__doc__', '__file__', '__name__', '__package__']

# Instantiate an instance of the calculator
>>> c = test2.Calculator()

# look at the operations supported by the Calculator object
>>> dir(c)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'sum']

# we can see that sum works as before
# The key difference is that the class method takes "self"
# as the first argument, and this is the Calculator object
# itself, and it is passed in implicitly
>>> c.sum(1,2,3,4,5)
15


28 - Exercise: extend the Calculator object to incorporate our
"multiply" method from earlier

(see test2exercise.py for the answer)

In order to see the code work use:

>>> reload(test2)
<module 'test2' from 'test2.pyc'>

>>> c = test2.Calculator()
>>> dir(c)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'multiply', 'sum']
>>> c.multiply(1,2,3,4)
24

29 - Running from the Command Line

# Exit Interactive Mode
>>> exit()

# Run our calculator class
# Note that nothing happens.  Python executes the file, but since this
# file does not contain any runnable code, nothing happens
$ python test2.py

# Modify the test2.py file to include some runnable code
(see test2runnable.py)

# run it
willow:files richard$ python test2.py
10
24

# Having code like this is inadvisable if you want people to
# use your module, because when they import your module, this
# code will get run.

# we can get python to only run this code if it is called from
# the command line, and not when it is imported as a module
(see test2runnable2.py)

# make a copy of the test2.py module, and modify it with
# if __name__ == "__main__"

# run it (notice it is the same as before)
willow:files richard$ python test2_1.py
10
24

# go in to Interactive mode and import both modules
willow:files richard$ python
>>> import test2_1
>>> import test2
10
24

==== End of Core Python Tutorial ====

30 - Web.py and a basic HTTP interface

# here we build a basic web server using web.py
(see test3.py)

# can we interpret what is going on in this file
# - urls is a module level tuple of url mappings and class names
# - Index in our controller, and GET will handle HTTP GET requests
# - the return value is what is sent to the browser
# - app is a web.py web application which we create to handle
#       the specified urls
# - globals() is a function which returns a dictionary of all the 
#   global scope variables and functions in the python runtime
# - note that we only start the application (app.run()) when this
#   is invoked from the command line

# start the web server
$ python test3.py 
http://0.0.0.0:8080/

# visit the web page
http://localhost:8080/

31 - Exercise: build the calculator into our webapp, so that you can
request

http://localhost:8080?sum=1,2,3,4

and get an answer back

(see test4.py for implementation)

# stop the web.py server with Ctrl-C

# restart it on test4.py
$ python test4.py 
http://0.0.0.0:8080/

# if you go the web page you will see an error, because we haven't
# done any error handling
http://localhost:8080/

# but try getting the sum
http://localhost:8080/?sum=1,2,3,4
</blockquote>
</pre>



Original Title: Beginners python dojo script
Original Author: richard
Tags: dev8d, python, richard, news, tutorial
Created: 2012-02-15 1640
Last Modified: 2013-03-02 1048
