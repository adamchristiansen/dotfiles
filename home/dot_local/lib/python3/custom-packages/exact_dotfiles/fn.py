"""Return the argument."""
id = lambda x: x

"""Wrap a function to call it with a splat."""
splat = lambda f: lambda x: f(*x)

"""Get a function which returns the nth item of an iterator."""
nth = lambda n: \
        lambda xs: \
          (lambda it: [next(it) for _ in range(n + 1)][n])(iter(xs))

"""Get the first value of an iterator."""
first = nth(0)

"""Get the second value of an iterator."""
second = nth(1)

"""Get the third value of an iterator."""
third = nth(2)

"""Get the last value of an iterator."""
last = lambda xs: (lambda it: [x for x in it][-1])(iter(xs))

"""Addition."""
add = lambda x, y: x + y

"""Subtraction."""
sub = lambda x, y: x - y

"""Multiplication."""
mul = lambda x, y: x * y

"""Division."""
div = lambda x, y: x / y

"""Floor division."""
fdiv = lambda x, y: x // y

"""Modulo."""
mod = lambda x, y: x % y

"""Exponentation."""
pow = lambda x, y: x ** y

"""Negate a value."""
neg = lambda x: - x

"""Invert a value."""
inv = lambda x: 1 / x

"""Strip whitespace."""
strip  = lambda x: x.strip()

"""Strip left whitespace."""
lstrip  = lambda x: x.lstrip()

"""Strip right whitespace."""
rstrip  = lambda x: x.rstrip()

"""Convert to lowercase."""
lower = lambda x: x.lower()

"""Convert to uppercase."""
upper = lambda x: x.upper()

"""Convert to titlecase."""
title = lambda x: x.title()
