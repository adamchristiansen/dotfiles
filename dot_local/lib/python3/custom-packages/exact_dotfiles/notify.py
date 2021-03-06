import shutil

from .numeric import clamp
from .run import run

def notify(
    app=None,
    summary=None,
    body=None,
    icon=None,
    urgency=None,
    tag=None,
    progress=None,
    hints=None
  ):
  """
  Create a notification.

  # Arguments

  - `app` (str|None): The name of the app.
  - `summary` (str|None): The notification summary.
  - `body` (str|None): The notification body.
  - `icon` (str|None): The notification icon.
  - `urgency` (str|None): The notification urgency.
  - `tag` (str|None): The stacking tag.
  - `progrees` (int|None): Progress as a percentage.
  - `hints` (dict<str,(int|float|str)>): Extra hints to pass. The hint type is
    automatically determined from the argument type.

  # Returns

  (Run): Output of sending the notification.
  """
  if shutil.which("osascript") is not None:
    cmd = ["osascript", "-e"]
    title = app if app is not None else "Notification"
    message = body
    text = "display notification"
    if body is not None:
      text += f' "{message}"'
    if app is not None:
      text += f' with title "{app}"'
    cmd.append(text)
  else:
    cmd = ["notify-send"]
    if urgency is not None:
      cmd.extend(["--urgency", urgency])
    if app is not None:
      cmd.extend(["--app-name", app])
    if icon is not None:
      cmd.extend(["--icon", icon])
    if tag is not None:
      cmd.extend(["--hint", f"string:x-dunst-stack-tag:{tag}"])
    if progress is not None:
      progress = clamp(progress, 0, 100)
      cmd.extend(["--hint", f"int:value:{progress}"])
    if hints is not None:
      for k, v in hints.items():
        if isinstance(v, int):
          cmd.extend(["--hint", f"int:{k}:{v}"])
        elif isinstance(v, float):
          cmd.extend(["--hint", f"float:{k}:{v}"])
        elif isinstance(v, str):
          cmd.extend(["--hint", f"string:{k}:{v}"])
        else:
          raise TypeError("hints must be int, float, or string")
    cmd.append("--")
    if summary is not None:
      cmd.append(summary)
    else:
      cmd.append(" ")
    if body is not None:
      cmd.append(body)
  return run(cmd)
