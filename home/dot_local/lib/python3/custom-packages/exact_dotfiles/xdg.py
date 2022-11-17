import os

def home(*paths):
  """Get the home directory."""
  return os.path.join(os.environ["HOME"], *paths)

def _get_join(var, default, *paths):
  """Quickly get an XDG path with optional paths joined on the end."""
  return os.path.join(os.getenv(var, home(default)), *paths)

def cache_home(*paths):
  """Get the XDG cache home directory."""
  return _get_join("XDG_CACHE_HOME", ".cache", *paths)

def config_home(*paths):
  """Get the XDG config home directory."""
  return _get_join("XDG_CONFIG_HOME", ".config", *paths)

def data_home(*paths):
  """Get the XDG data home directory."""
  return _get_join("XDG_DATA_HOME", ".local/share", *paths)

def state_home(*paths):
  """Get the XDG state home directory."""
  return _get_join("XDG_STATE_HOME", ".local/state", *paths)

def desktop_dir(*paths):
  """Get the XDG desktop directory."""
  return _get_join("XDG_DESKTOP_DIR", "Desktop", *paths)

def documents_dir(*paths):
  """Get the XDG documents directory."""
  return _get_join("XDG_DOCUMENTS_DIR", "Documents", *paths)

def download_dir(*paths):
  """Get the XDG download directory."""
  return _get_join("XDG_DOWNLOAD_DIR", "Downloads", *paths)

def music_dir(*paths):
  """Get the XDG music directory."""
  return _get_join("XDG_MUSIC_DIR", "Music", *paths)

def pictures_dir(*paths):
  """Get the XDG pictures directory."""
  return _get_join("XDG_PICTURES_DIR", "Pictures", *paths)

def publicshare_dir(*paths):
  """Get the XDG public share directory."""
  return _get_join("XDG_PUBLICSHARE_DIR", "Public", *paths)

def templates_dir(*paths):
  """Get the XDG templates directory."""
  return _get_join("XDG_TEMPLATES_DIR", "Templates", *paths)

def videos_dir(*paths):
  """Get the XDG videos directory."""
  return _get_join("XDG_VIDEOS_DIR", "Videos", *paths)
