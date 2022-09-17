import os
import pathlib
import shutil

class fs:
  """File system operations."""

  @staticmethod
  def cleardir(dir_path):
    """Clear the contents of a directory."""
    for path in pathlib.Path(dir_path).iterdir():
      if path.is_file():
        path.unlink()
      elif path.is_dir():
        shutil.rmtree(path)

  @staticmethod
  def cp(src, dest):
    """Copy a file or directory to a new location."""
    shutil.copy(src, dest)

  @staticmethod
  def mkdir(dir_path):
    """Make a directory."""
    os.makedirs(dir_path, exist_ok=True)
