class array:
  """An array that acts like a list but with convenient methods."""
  def __init__(self, it=None):
    """Create a new array from an iterator."""
    self.__xs = list(it) if it is not None else []

  def __cp(self, arr):
    """Copy an array into this one."""
    self.__xs = arr.__xs
    return self

  def all(self, pred):
    """Test if a predicate is true for any items."""
    for v in self:
      if not pred(v):
        return False
    return True

  def any(self, pred):
    """Test if a predicate is true for any items."""
    for v in self:
      if pred(v):
        return True
    return False

  def append(self, *xs):
    """Append to end."""
    return self + xs

  def appendi(self, *xs):
    """In place append."""
    self.__xs.extend(xs)
    return self

  def each(self, f):
    """Evaluate a function on each item."""
    self.map(f)

  def extend(self, *its):
    """Extend by appending iterators to end."""
    xs = list(self)
    for it in its:
      xs.extend(it)
    return array(xs)

  def extendi(self, *its):
    """In-place extend."""
    for it in its:
      self.__xs.extend(it)
    return self

  def fold(self, f, v=None):
    """Fold a function from left to right."""
    it = iter(self)
    if v is None:
      v = next(it)
    for x in it:
      v = f(v, x)
    return v

  def keep(self, pred):
    """Keep items that satisfy a predicate."""
    return array(filter(pred, self.__xs))

  def keepi(self, f):
    """In-place keep."""
    return self.__cp(self.keep(f))

  def map(self, f):
    """Produce a new array by transforming each element."""
    return array(map(f, self.__xs))

  def mapi(self, f):
    """In-place map."""
    return self.__cp(self.map(f))

  def max(self):
    """The maximum item."""
    return max(self)

  def min(self):
    """The minimum item."""
    return min(self)

  def remove(self, pred):
    """Remove items that satisfy a predicate."""
    return array(filter(lambda x: not pred(x), self.__xs))

  def removei(self, f):
    """In-place remove."""
    return self.__cp(self.remove(f))

  def reverse(self):
    """Reverse the array."""
    return array(reversed(self))

  def reversei(self):
    """In-place reverse."""
    return self.__cp(self.reverse())

  def sort(self, key=None, reverse=False):
    """Sort the array."""
    return array(sorted(self.__xs, key=key, reverse=reverse))

  def sorti(self, key=None, reverse=False):
    """In-place sort."""
    return self.__cp(self.sort(key=key, reverse=reverse))

  def sum(self):
    """Sum the array."""
    return self.fold(lambda x, y: x + y)

  def __add__(self, it):
    return array(list(self) + list(it))

  def __contains__(self, key):
    return key in self.__xs

  def __delitem__(self, key):
    del self.__xs[key]

  def __getitem__(self, key):
    return self.__xs[key]

  def __iter__(self):
    return iter(self.__xs)

  def __len__(self):
    return len(self.__xs)

  def __repr__(self):
    return repr(self.__xs)

  def __setitem__(self, key, value):
    self.__xs[key] = value

  def __str__(self):
    return str(self.__xs)
