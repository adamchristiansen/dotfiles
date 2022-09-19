from .numeric import clamp
from .plat import plat
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
  Create a notification using the name of the app, a summary, and body. An icon
  can be specified as either an icon name or an absolute path to the image.

  The urgency can be low, normal, or critical.

  The tag is a name used for notification stacking, so that similar
  notifications overwrite each other instead of creating a new one.

  The progress in percent can be given to display a progress bar.

  Any extra hints that are given are passed along. Hints are dictionary of
  strings mapping to ints, floats, or strings for the data to pass.

  The output of running the notification is returned.
  """
  if plat.has_cmd("osascript"):
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
