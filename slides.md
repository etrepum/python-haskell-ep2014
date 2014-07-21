# What Python can learn from Haskell {#title}

<h3>
    Bob Ippolito (<a href="https://twitter.com/etrepum">@etrepum</a>)<br>
    EuroPython Berlin<br>
    21 July 2014
</h3>
<h4>
[bob.ippoli.to/python-haskell-ep2014]
</h4>

# Who am I?

- Python user since 2001
  ([simplejson](https://github.com/simplejson/simplejson), Mac stuff)
- Founded Mochi Media (2005-2012, sold in 2010)
- [Haskell] user since 2012
  (ported [exercism.io](http://exercism.io) curriculum)
- Doing a bit of advising/investing in startups
- Currently focusing on code education non-profit
  [Mission Bit](http://www.missionbit.com/)

# Python is not all bad!

- I love Python's community
- Many great ideas and libraries come from here
- Works wonderfully for many users
- Workarounds exist for most issues
  ([PyPy], [Numba], [Cython], …)

# Haskell is not all good!

- Smaller community
- Non-strict evaluation
- Sometimes documentation is an academic paper
- Different terminology (Monoid, Functor, Monad, …)

# Ignorance is bliss

- If you are perfectly happy with Python, and don't want it to change
  even a little bit, you might want to leave now :)
- I was a lot happier with Python until I started learning Erlang and
  then Haskell
- … but I'm a better programmer because of it ([Blub Paradox]?)

# {#paradox}

<dl>
<dt><em class="large-quote">Nasty little paradox: the better something works,
the less likely it'll be improved.</em></dt>
<dd><br>&mdash; [Richard O'Keefe](http://erlang.org/pipermail/erlang-questions/2010-February/049635.html)</dd>
</dl>

# Python makes […] hard {#hard-time}

- writing code that works
- maintaining code
- creating good abstractions
- running code efficiently

# Correctness

- You will make mistakes in any language
- Python defers all type checking to runtime
- Static analysis tools for Python are primitive
- Writing code to test for common mistakes is a lot of work

# Python nonsense

* The Python language guarantees that this should raise TypeError

```python
"""This module is nonsense!"""

def main():
    """What is this, JavaScript?"""
    print(1 + "1")

if __name__ == '__main__':
    main()
```

# Let's see what Python thinks

```bash
$ python -mcompileall nonsense.py 
Compiling nonsense.py ...
$ echo $?
0
```

# pyflakes to the rescue?

```bash
$ pyflakes nonsense.py 
$ echo $?
0
```

# What about Pylint?

```bash
$ pylint --enable=all nonsense.py
[…]

Global evaluation
-----------------
Your code has been rated at 10.00/10
```

# Do better tools exist?

* Nothing I could find could catch this simple case
* Most tools are concerned with the general case of Python, which
  makes it very difficult to do anything useful
* Python 3 already has syntax for function annotations,
  and we've had decent AST tools for years
* Will talk about one promising option in a bit

# Erlang nonsense

```erlang
-module(nonsense).
-export([start/0]).

start() ->
    io:format("~p", [1 + "1"]).
```

# erlc nonsense

```bash
$ erlc -Werror nonsense.erl 
compile: warnings being treated as errors
nonsense.erl:5: this expression will fail with a
  'badarith' exception
$ echo $?
1
```

* Note that Erlang is a dynamic language!

# Erlang dialyzer nonsense {.wide-code}

```bash
$ dialyzer nonsense.erl 
nonsense.erl:4: Function start/0 has no local return
nonsense.erl:5: The call erlang:'+'(1,[49,...])
  will never return since it differs in the 2nd
  argument from the success typing arguments:
  (number(),number())
 done in 0m0.52s
done (warnings were emitted)
```

# Haskell nonsense

```haskell

main = print (1 + "1")
```

# Haskell nonsense {#haskell-nonsense-typed}

```haskell
main :: IO ()
main = print (1 + "1")
```

# ghc nonsense {.wide-code}

```bash
$ ghc nonsense.hs 
[1 of 1] Compiling Main  ( nonsense.hs, nonsense.o )

nonsense.hs:1:17:
  No instance for (Num [Char]) arising from
    a use of ‘+’
  In the first argument of ‘print’,
    namely ‘(1 + "1")’
  In the expression: print (1 + "1")
  In an equation for ‘main’: main = print (1 + "1")
```

# No instance for… WTF? {#nonsense-instance .wide-code}

```haskell
No instance for (Num [Char]) arising from a use of '+'
```

* By default, strings in Haskell are lists of Char.
* Operations such as `+`, `-`, `*`, `negate` belong to the Num
  typeclass (handwavingly similar to a Python ABC)
* Only truly numeric types such as Int, Double, Integer, Rational have
  built-in instances for the Num typeclass
* You could (*but absolutely should not!*) implement such an instance
  to make this code compile. Don't do that. Seriously.

# Why is refactoring hard?

* Very hard to refactor without good tests
* Types *are* the obvious tests *and* documentation
* Refactoring in Haskell is easier due to types
  and referential transparency
* Can we do something like this in Python? Yes.

# {#breadth_first0 .wide-code .no-header}

```python
"""Breadth-first traversal"""



def breadth_first(starting_node,
                  edges):

	"""Yield all nodes reachable from starting_node"""
    visited = []
    queue = [starting_node]
    while queue:
        node = queue[0]; del queue[:1] # queue.pop(0)
        if node not in visited:
            yield node
            visited.append(node)
            queue.extend(edges[node])
```

# {#breadth_first1 .wide-code .no-header}

```python
"""Breadth-first traversal"""
from typing import List, Dict, Iterator


def breadth_first(starting_node: int,
                  edges: Dict[int, List[int]])
				  -> Iterator[int]:
    """Yield all nodes reachable from starting_node"""
    visited = List[int]()
    queue = [starting_node]
    while queue:
        node = queue[0]; del queue[:1] # queue.pop(0)
        if node not in visited:
            yield node
            visited.append(node)
            queue.extend(edges[node])
```

# {#breadth_first2 .wide-code .no-header}

```python
"""Breadth-first traversal"""
from typing import List, Dict, Set, Iterator
from collections import deque

def breadth_first(starting_node: int,
                  edges: Dict[int, List[int]])
				  -> Iterator[int]:
    """Yield all nodes reachable from starting_node"""
    visited = Set[int]()
    queue = deque([starting_node])
    while queue:
        node = queue[0]; del queue[:1] # queue.pop(0)
        if node not in visited:
            yield node
            visited.append(node)
            queue.extend(edges[node])
```

# {#breadth_first2_err .wide-code .no-header}

```bash
breadth_first2.py: In function "breadth_first":
breadth_first2.py, line 11:
  deque[int] has no attribute "__delitem__"
breadth_first2.py, line 14:
  Set[int] has no attribute "append"
```

# {#breadth_first3 .wide-code .no-header}

```python
"""Breadth-first traversal"""
from typing import Iterator, Dict, List, Set
from collections import deque

def breadth_first(starting_node: int,
                  edges: Dict[int, List[int]])
				  -> Iterator[int]:
    """Yield all nodes reachable from starting_node"""
    visited = Set[int]()
    queue = deque([starting_node])
    while queue:
        node = queue.popleft()
        if node not in visited:
            yield node
            visited.add(node)
            queue.extend(edges[node])
```

# Solution: mypy? {#solution-mypy}

* [mypy] is the most sensible approach I've seen so far
* The author needs some help! There are many tasks to do that do not
  require deep knowledge of mypy or type systems
* mypy does not yet catch the `1 + "1"` error yet, but can catch many
  other mistakes such as the refactoring example
* Why not X ([PyPy], [Nuitka], …): these projects do nothing to assist
  with correctness and code quality!

# Modest mypy proposal

* Start using `typing` module even in vanilla Python 3
* Support `typing` annotations in documentation tools
* Stop using [PEP 3107] function annotations for any other purpose
* Start using mypy to typecheck code when running tests /
  continuous integration
* Start contributing to mypy! :)

# So what?

* Code quality tools for Python are far behind other languages
* mypy is a huge step forward and can be used with existing Python 3
  syntax and interpreter
* Would have to give up using function annotations for other purposes

# {#mutability-img}

<img src="img/mutability.jpg" class="full">

# Mutability

* Mutability is the wrong default
* Very common source of bugs
* Prevents many optimizations (sharing, lock-free, etc.)
* Should be *opt-in*

# Why is mutability wrong?

* Hard to understand code when underlying data might change
* Defensive programming is difficult
* Sharing is prevented by copying
* Concurrent access requires synchronization

# Can we even fix this? {#immutable}

* Requires large changes to the language and libraries :(
* See [Rust] or [Swift] for good examples
* Haskell goes all the way (perhaps too far)
* Maybe opt-in immutability (Swift's `let`) is more practical for Python?

# Expensive Abstractions

* Nothing is free. Function calls, classes, etc.
  do not typically get optimized away
* Classes aren't easy to analyze for correctness, as they are
  always open. Subclasses ruin everything.

# Algebraic Data Types

* Python has grown many hacks such as Enum, namedtuple, etc. that
  solve small parts of this problem
* Haskell (and other ML family languages) have an elegant solution to
  this

# {#python-adt-1 .wide-code .no-header}

```python
class AST(object):
    def eval(self):
        raise NotImplementedError

class Constant(AST):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Minus(AST):
    def __init__(self, node):
        self.node = node

    def eval(self):
        return self.node.eval()
```

# {#python-adt-2 .wide-code .no-header}

```python
class Add(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() + self.right.eval()


class Multiply(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() + self.right.eval()
```

# ADT in Haskell

```haskell
module NumAST ( AST(..), eval ) where

data AST = Constant Int
         | Add AST AST
         | Minus AST
         | Multiply AST AST
         deriving (Show, Eq)

eval :: AST -> Int
eval node = case node of
  Constant n   -> n
  Add a b      -> eval a + eval b
  Minus n      -> negate (eval n)
  Multiply a b -> eval a * eval b
```

# {#python-adt-2-1 .wide-code .no-header}

```python
class Add(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() + self.right.eval()

	def __eq__(self, other):
		return (isinstance(other, Add) and
	            self.left == other.left and
				self.right == other.right)

    def __repr__(self):
		return 'Add(%r, %r)' % (self.left, self.right)
```

# Wrapping can be free

* Haskell can define a wrapper for an existing data type at no runtime
  space cost (`newtype`)
* Strict fields can be inlined without boxing (no object overhead)
* Functions can be inlined (even cross-module)
* No reason for `1 + True == 2`

# Performance? {#performance}

* Everything I've talked about provide more ahead-of-time information
* This information could be used by [PyPy], [Numba], [Cython], etc.
* These features save developer time by making it easier
  to write correct code
* More information means more opportunities for optimization,
  so can lead to better performance
* Writing less code in C/C++ will allow the language to improve much
  more quickly (thank you [PyPy]!)

# Concurrency? {#concurrency}

* The Python C API and current semantics make removing the GIL
  a non-starter
* Fixing other deficiencies in the language will make the necessary
  refactorings easier, and in Python
* Mixed approach with workers written in a Python subset
  might be a nice transitional step ([PyParallel])

# Summary

* Incorporate all of the good ideas from [mypy] into Python
* Add some more of the conveniences from modern languages
* Enjoy a safer, faster, more capable Python

# Thanks!

+-------------+-------------------------------------------------+
| **Slides**  | [bob.ippoli.to/python-haskell-ep2014]           |
+-------------+-------------------------------------------------+
| **Source**  | [github.com/etrepum/python-haskell-ep2014]      |
+-------------+-------------------------------------------------+
| **Email**   | bob@redivi.com                                  |
+-------------+-------------------------------------------------+
| **Twitter** | [&#64;etrepum](https://twitter.com/etrepum)     |
+-------------+-------------------------------------------------+

[github.com/etrepum/python-haskell-ep2014]: https://github.com/etrepum/python-haskell-ep2014/
[bob.ippoli.to/python-haskell-ep2014]: http://bob.ippoli.to/python-haskell-ep2014/
[PyPy]: http://pypy.org/
[Numba]: http://numba.pydata.org/
[mypy]: http://mypy-lang.org/
[Cython]: http://cython.org/
[PEP 3107]: http://legacy.python.org/dev/peps/pep-3107/
[Nuitka]: http://nuitka.net/
[Swift]: https://developer.apple.com/swift/
[Rust]: http://www.rust-lang.org/
[Haskell]: http://www.haskell.org/
[Blub Paradox]: http://www.paulgraham.com/avg.html
[PyParallel]: https://speakerdeck.com/trent/parallelism-and-concurrency-with-python
