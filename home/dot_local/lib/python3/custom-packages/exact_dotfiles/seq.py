class seq:
  """A sequence that acts like a list but with convenient methods."""
  def __init__(self, it=None):
    """Create a new sequence from an iterator."""
    self.__xs = list(it) if it is not None else []

  def dup(self):
    """Make a duplicate of the seqeunce."""
    return seq(self)

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

  def clear(self):
    """Empty the sequence."""
    self.__xs.clear()

  def collect(self):
    """Collect into a list."""
    return list(self)

  def concat(self, it, *its):
    """Concatenate iterators on the end."""
    self.__xs.extend(it)
    for it in its:
      self.__xs.extend(it)
    return self

  def count(self, pred):
    """Count items that satisfy a predicate."""
    c = 0
    for x in self:
      if pred(x):
        c += 1
    return c

  def each(self, f):
    """Evaluate a function on each item."""
    for x in self:
      f(x)
    return self

  def enum(self):
    """Enumerate the items."""
    for i in range(len(self)):
      self[i] = (i, self[i])
    return self

  def first(self):
    """Take the first item."""
    return self[0]

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
    self.__xs[:] = [x for x in self.__xs if pred(x)]
    return self

  def last(self):
    """Take the last item."""
    return self[-1]

  def map(self, f):
    """Modify each item."""
    for i in range(len(self)):
      self[i] = f(self[i])
    return self

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

  def push(self, x, *xs):
    """Append to end."""
    self.__xs.append(x)
    self.__xs.extend(xs)
    return self

  def remove(self, pred):
    """Remove items that satisfy a predicate."""
    self.__xs[:] = [x for x in self.__xs if not pred(x)]
    return self

  def reverse(self):
    """Reverse the sequence."""
    for i in range(len(self) // 2):
      j = len(self) - i - 1
      self[i], self[j] = self[j], self[i]
    return self

  def sort(self, key=None, reverse=False):
    """Sort the sequence."""
    self.__xs.sort(key=key, reverse=reverse)
    return self

  def sum(self):
    """Sum the sequence."""
    return sum(self)

  def __add__(self, it):
    return self.dup().concat(it)

  def __radd__(self, it):
    return self + it

  def __iadd__(self, it):
    return self.concat(it)

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
