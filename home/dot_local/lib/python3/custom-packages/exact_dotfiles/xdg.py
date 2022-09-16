import os

class xdg:
  """
  Get XDG paths.
  """

  @staticmethod
  def home(*paths):
    """Get the home directory."""
    return os.path.join(os.environ["HOME"], *paths)

  @staticmethod
  def _get_join(var, default, *paths):
    """
    Quickly get an XDG path with optional paths joined on the end.
    """
    return os.path.join(os.getenv(var, xdg.home(default)), *paths)

  @staticmethod
  def cache_home(*paths):
    """Get the XDG cache home directory."""
    return xdg._get_join("XDG_CACHE_HOME", ".cache", *paths)

  @staticmethod
  def config_home(*paths):
    """Get the XDG config home directory."""
    return xdg._get_join("XDG_CONFIG_HOME", ".config", *paths)

  @staticmethod
  def data_home(*paths):
    """Get the XDG data home directory."""
    return xdg._get_join("XDG_DATA_HOME", ".local/share", *paths)

  @staticmethod
  def state_home(*paths):
    """Get the XDG state home directory."""
    return xdg._get_join("XDG_STATE_HOME", ".local/state", *paths)

  @staticmethod
  def desktop_dir(*paths):
    """Get the XDG desktop directory."""
    return xdg._get_join("XDG_DESKTOP_HOME", "Desktop", *paths)

  @staticmethod
  def documents_dir(*paths):
    """Get the XDG documents directory."""
    return xdg._get_join("XDG_DOCUMENTS_HOME", "Documents", *paths)

  @staticmethod
  def download_dir(*paths):
    """Get the XDG download directory."""
    return xdg._get_join("XDG_DOWNLOAD_HOME", "Downloads", *paths)

  @staticmethod
  def music_dir(*paths):
    """Get the XDG music directory."""
    return xdg._get_join("XDG_MUSIC_HOME", "Music", *paths)

  @staticmethod
  def pictures_dir(*paths):
    """Get the XDG pictures directory."""
    return xdg._get_join("XDG_PICTURES_HOME", "Pictures", *paths)

  @staticmethod
  def publicshare_dir(*paths):
    """Get the XDG public share directory."""
    return xdg._get_join("XDG_PUBLICSHARE_HOME", "Public", *paths)

  @staticmethod
  def templates_dir(*paths):
    """Get the XDG templates directory."""
    return xdg._get_join("XDG_TEMPLATES_HOME", "Templates", *paths)

  @staticmethod
  def videos_dir(*paths):
    """Get the XDG videos directory."""
    return xdg._get_join("XDG_VIDEOS_HOME", "Videos", *paths)
