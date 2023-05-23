# Copyright 2023 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module is corresponding to the "androidx.test.uiautomator.UiDevice".

https://developer.android.com/reference/androidx/test/uiautomator/UiDevice
"""

import pathlib
from typing import Callable, Mapping, Optional, Sequence, Union
import xml

from mobly import logger as mobly_logger
from mobly.controllers.android_device_lib import snippet_client_v2
from snippet_uiautomator import byselector
from snippet_uiautomator import constants
from snippet_uiautomator import errors
from snippet_uiautomator import uiobject2
from snippet_uiautomator import uiwatcher
from snippet_uiautomator import utils


class _Open:
  """Performs a open gesture on this device."""

  def __init__(self, ui: snippet_client_v2.SnippetClientV2) -> None:
    self._ui = ui

  def notification(self) -> bool:
    """Opens the notification shade."""
    return self._ui.openNotification()

  def quick_settings(self) -> bool:
    """Opens the quick settings shade."""
    return self._ui.openQuickSettings()


class _Press:
  """Performs a press action on this device."""

  def __init__(self, ui: snippet_client_v2.SnippetClientV2) -> None:
    self._ui = ui

  def __call__(
      self, keycode: Union[int, str, Sequence[int]], meta: Optional[int] = None
  ) -> bool:
    """Calls the press action via invoke."""
    if isinstance(keycode, int):
      return self._ui.pressKeyCode(keycode, meta)
    elif isinstance(keycode, list) or isinstance(keycode, tuple):
      return self._ui.pressKeyCodes(keycode, meta)
    return self._press(keycode)

  def __getattr__(self, keycode: str) -> Callable[[], bool]:
    """Calls the press action via dot notation."""

    def wrapper():
      return self._press(keycode)

    return wrapper

  def _press(self, keycode: str) -> bool:
    """Simulates a short press on the specific button."""
    if keycode in ('back', 'delete', 'enter', 'home', 'menu', 'search'):
      return getattr(self._ui, f'press{keycode.capitalize()}')()
    elif keycode in ('center', 'down', 'left', 'right', 'up'):
      return getattr(self._ui, f'pressDPad{keycode.capitalize()}')()
    elif keycode == 'camera':
      return self._ui.pressKeyCode(0x0000001B)
    elif keycode == 'power':
      return self._ui.pressKeyCode(0x0000001A)
    elif keycode == 'recent':
      return self._ui.pressRecentApps()
    elif keycode == 'volume_down':
      return self._ui.pressKeyCode(0x00000019)
    elif keycode == 'volume_mute':
      return self._ui.pressKeyCode(0x000000A4)
    elif keycode == 'volume_up':
      return self._ui.pressKeyCode(0x00000018)
    raise AttributeError(f"'_Press' object has no attribute {repr(keycode)}")


class _Screen:
  """Performs screen on/off action on this device."""

  def __init__(self, ui: snippet_client_v2.SnippetClientV2) -> None:
    self._ui = ui

  def on(self) -> bool:
    """Simulates pressing the power button if the screen is OFF."""
    return self._ui.wakeUp()

  def off(self) -> bool:
    """Simulates pressing the power button if the screen is ON."""
    return self._ui.sleep()

  def __repr__(self) -> str:
    """Returns 'on' if screen is ON, 'off' otherwise."""
    return 'on' if self._ui.isScreenOn() else 'off'


class _Wait:
  """Waits for a specific condition to occur."""

  def __init__(self, ui: snippet_client_v2.SnippetClientV2) -> None:
    self._ui = ui

  def idle(
      self, timeout: utils.TimeUnit = constants.DEFAULT_UI_WAIT_TIME
  ) -> bool:
    """Waits for the current application to idle.

    Args:
      timeout: The time in milliseconds to wait for idle.

    Returns:
      True if the current application idle in time, False otherwise.
    """
    timeout_ms = utils.covert_to_millisecond(timeout)
    return self._ui.waitForIdle(timeout_ms)

  def update(
      self,
      package: Optional[str] = None,
      timeout: utils.TimeUnit = constants.DEFAULT_UI_WAIT_TIME,
  ) -> bool:
    """Waits for a window content update event to occur.

    Args:
      package: The package name of the window. If not specified, it can be any
        window.
      timeout: The time in milliseconds to wait for a new window.

    Returns:
      True if a window content update event occurs in time, False otherwise.
    """
    timeout_ms = utils.covert_to_millisecond(timeout)
    return self._ui.waitForWindowUpdate(package, timeout_ms)


class UiDevice:
  """Represents an UiDevice.

  https://developer.android.com/reference/androidx/test/uiautomator/UiDevice
  """

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      raise_error: bool = False,
  ) -> None:
    self._ui = ui
    self._serial = self._ui._adb.serial  # pylint: disable=protected-access
    self._raise_error = raise_error

  def __call__(self, **kwargs) -> uiobject2.UiObject2:
    return uiobject2.UiObject2(
        self._ui, byselector.BySelector(**kwargs), self._raise_error
    )

  @property
  def raise_error(self) -> bool:
    """The current status to raise an error or not."""
    return self._raise_error

  @raise_error.setter
  def raise_error(self, new_value: bool) -> None:
    """Sets True to raise an error, False to return boolean."""
    self._raise_error = new_value

  @property
  def log_path(self) -> pathlib.Path:
    """Log path of this device in Mobly."""
    return utils.get_mobly_ad_log_path(self._ui)

  @property
  def height(self) -> int:
    """The height of the display, in pixels."""
    return self._ui.getDisplayHeight()

  @property
  def width(self) -> int:
    """The width of the display, in pixels."""
    return self._ui.getDisplayWidth()

  @property
  def launcher(self) -> str:
    """The package name of the default launcher."""
    return self._ui.getLauncherPackageName()

  @property
  def package_name(self) -> str:
    """The name of the last package to report accessibility events."""
    return self._ui.getCurrentPackageName()

  @property
  def product(self) -> str:
    """The product name of this device."""
    return self._ui.getProductName()

  @property
  def size(self) -> Mapping[str, int]:
    """The display size in dp (device-independent pixel)."""
    return self._ui.getDisplaySizeDp()

  @property
  def info(self) -> Mapping[str, Union[int, str]]:
    """All properties of this device."""
    return self._ui.getDevInfo()

  @property
  def orientation(self) -> constants.Orientation:
    """The current orientation of the display."""
    return constants.Orientation(self._ui.getDisplayRotation())

  @orientation.setter
  def orientation(self, new_orientation: constants.Orientation) -> None:
    """Sets orientation and freezes rotation."""
    if new_orientation == constants.Orientation.NATURAL:
      self._ui.setOrientationNatural()
    elif new_orientation == constants.Orientation.LEFT:
      self._ui.setOrientationLeft()
    elif new_orientation == constants.Orientation.RIGHT:
      self._ui.setOrientationRight()
    else:
      raise errors.UiAutomatorError(
          f'Cannot set orientation to {new_orientation}.'
      )

  @property
  def open(self) -> _Open:
    """Performs a open gesture on this device."""
    return _Open(self._ui)

  @property
  def press(self) -> _Press:
    """Performs a press action on this device."""
    return _Press(self._ui)

  @property
  def screen(self) -> _Screen:
    """Performs screen on/off action on this device."""
    return _Screen(self._ui)

  @property
  def wait(self) -> _Wait:
    """Performs wait action on this device."""
    return _Wait(self._ui)

  @property
  def watchers(self) -> uiwatcher.UiWatchers:
    """Operates all registered UiWatchers."""
    return uiwatcher.UiWatchers(self._ui)

  def watcher(self, name: str) -> uiwatcher.UiWatcher:
    """Registers a UiWatcher to run automatically when no match can be found."""
    return uiwatcher.UiWatcher(self._ui, name)

  def freeze_rotation(self, freeze: bool = True) -> bool:
    """Freezes/Unfreezes the device rotation."""
    return self._ui.freezeRotation() if freeze else self._ui.unfreezeRotation()

  def find(self, **kwargs) -> Sequence[byselector.SelectorType]:
    """Finds all objects to match the selector criteria."""
    return self._ui.findObjects((byselector.BySelector(**kwargs).to_dict()))

  def has(self, **kwargs) -> bool:
    """Returns if there is a match for the given criteria."""
    return self._ui.hasObject(byselector.BySelector(**kwargs).to_dict())

  def click(self, x: int, y: int) -> bool:
    """Performs a click at arbitrary coordinates specified by the user.

    The coordinates of Android device screen works like following:
    (x, y) :-
    1. (0, 0) is top left corner.
    2. (maxX, 0) is top right corner.
    3. (0, maxY) is bottom left corner.
    4. (maxX, maxY) is bottom right corner.
    Here maxX and maxY are screen maximum height and width in pixels.

    Args:
      x: The X coordinate represents width.
      y: The Y coordinate represents height.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._ui.click(x, y)

  def drag(self, sx: int, sy: int, ex: int, ey: int, steps: int = 100) -> bool:
    """Performs a drag from one coordinate to another.

    https://developer.android.com/reference/androidx/test/uiautomator/UiDevice#drag(int,int,int,int,int)

    Args:
      sx: The X coordinate of the starting point.
      sy: The Y coordinate of the starting point.
      ex: The X coordinate of the end point.
      ey: The Y coordinate of the end point.
      steps: The number of steps for the drag action. Each step execution is
        throttled to 5 milliseconds, so for 100 steps, the drag will take around
        0.5 seconds to complete.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._ui.drag(sx, sy, ex, ey, steps)

  def swipe(self, sx: int, sy: int, ex: int, ey: int, steps: int = 100) -> bool:
    """Performs a swipe from one coordinate to another.

    Args:
      sx: The X coordinate of the starting point.
      sy: The Y coordinate of the starting point.
      ex: The X coordinate of the end point.
      ey: The Y coordinate of the end point.
      steps: The number of steps for the swipe action. Each step execution is
        throttled to 5 milliseconds, so for 100 steps, the swipe will take
        around 0.5 seconds to complete.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._ui.swipe(sx, sy, ex, ey, steps)

  def sleep(self) -> bool:
    """Simulates pressing the power button if the screen is ON."""
    return self._ui.sleep()

  def wakeup(self) -> bool:
    """Simulates pressing the power button if the screen is OFF."""
    return self._ui.wakeUp()

  def dump(
      self, compressed: bool = False, pretty: bool = True, file: bool = False
  ) -> Optional[str]:
    """Dumps the current window hierarchy.

    Args:
      compressed: True to enable layout hierarchy compression, False otherwise.
      pretty: True to organize the xml format beautifully, False otherwise.
      file: True to dump the window hierarchy to the file under Mobly log path,
        False to dump as a string.

    Returns:
      The current window hierarchy.
    """
    self._ui.setCompressedLayoutHierarchy(compressed)
    content = self._ui.dump()
    timestamp = mobly_logger.get_log_file_timestamp()
    if pretty and '\n ' not in content:
      content = xml.dom.minidom.parseString(content).toprettyxml(indent='  ')
    if file:
      with open(
          self.log_path.joinpath(f'window_dump,{timestamp}.xml'), 'w'
      ) as f:
        print(content, file=f)
    else:
      return content

