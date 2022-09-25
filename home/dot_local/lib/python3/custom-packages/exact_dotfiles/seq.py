class seq:
  """A lazy iterator with a fluent interface."""

  def __init__(self, *iterables):
    self.__its = iterables

  def all(self, pred):
    """Test if all items satisfy a predicate."""
    for x in self:
      if not pred(x):
        return False
    return True

  def any(self, pred):
    """Test if any items satisfy a predicate."""
    for x in self:
      if pred(x):
        return True
    return False

  def concat(self, it, *its):
    """Concatenate iterators on the end."""
    return seq(self, it, *its)

  def count(self, pred):
    """Count items that satisfy a predicate."""
    c = 0
    for x in self:
      if pred(x):
        c += 1
    return c

  def drop(self, n):
    """Drop the next n items."""
    it = iter(self)
    for _ in range(n):
      try:
        next(it)
      except StopIteration:
        break
    return seq(it)

  def each(self, f):
    """Evaluate a function on each item."""
    for x in self:
      f(x)
    return self

  def enum(self):
    """Enumerate the items."""
    return seq(enumerate(self))

  def first(self):
    """Take the first item."""
    return next(iter(self))

  def fold(self, f, v=None):
    """Fold a function from left to right."""
    it = iter(self)
    if v is None:
      v = next(it)
    for x in it:
      v = f(v, x)
    return v

  def join(self, sep=""):
    """Join a sequence of strings."""
    return sep.join(self)

  def keep(self, pred):
    """Keep items that satisfy a predicate."""
    return seq(filter(pred, self))

  def last(self):
    """Take the last item."""
    v = None
    for x in self:
      v = x
    return v

  def map(self, f):
    """Modify each item."""
    return seq(map(f, self))

  def max(self):
    """The maximum item."""
    return max(self)

  def min(self):
    """The minimum item."""
    return min(self)

  def none(self, pred):
    """Test if no items satisfy a predicate."""
    for x in self:
      if pred(x):
        return False
    return True

  def one(self, pred):
    """Test if one item satisfies a predicate."""
    count = 0
    for x in self:
      if pred(x):
        count += 1
        if count > 1:
          break
    return count == 1

  def remove(self, pred):
    """Remove items that satisfy a predicate."""
    return self.keep(lambda x: not pred(x))

  def reverse(self):
    """Reverse the sequence."""
    return seq(reversed(self))

  def sort(self, key=None, reverse=False):
    """Sort the sequence."""
    return seq(sorted(self, key=key, reverse=reverse))

  def sum(self):
    """Sum the sequence."""
    return sum(self)

  def take(self, n):
    """Take up to n items."""
    return taker(n, self)

  def __add__(self, other):
    return self.concat(other)

  def __radd__(self, other):
    return seq(other) + self

  def __iter__(self):
    for s in self.__its:
      for x in s:
        yield x

  def __reversed__(self):
    return reversed(list(self))

class taker(seq):
  def __init__(self, n, *its):
    super().__init__(*its)
    self.__n = n
    self.__taken = 0
  def __iter__(self):
    for x in super().__iter__():
      if self.__taken >= self.__n:
        break
      self.__taken += 1
      yield x
