import os
import pathlib
import shutil

def clear_dir(dir_path):
  """Clear the contents of a directory."""
  for path in pathlib.Path(dir_path).iterdir():
    if path.is_file():
      path.unlink()
    elif path.is_dir():
      shutil.rmtree(path)

def cp(src, dest):
  """Copy a file or directory to a new location."""
  shutil.copy(src, dest)

def exists(path, kind="any"):
  """Test that a path exists."""
  kind = kind.lower()
  p = pathlib.Path(path)
  return any([
    "any" in kind and p.exists(),
    "file" in kind and p.is_file(),
    "dir" in kind and p.is_dir(),
  ])

def mkdir(dir_path):
  """Make a directory."""
  os.makedirs(dir_path, exist_ok=True)

def read_file(file_path, mode='r'):
  """Read file contents."""
  with open(file_path, mode=mode) as f:
    return f.read()

def write_file(file_path, data, mode='w', mkdir=False):
  """Write to file."""
  if mkdir:
    fs.mkdir(os.path.dirname(file_path))
  with open(file_path, mode=mode) as f:
    f.write(data)
