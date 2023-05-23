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

"""This module is corresponding to the "androidx.test.uiautomator.UiWatcher".

https://developer.android.com/reference/androidx/test/uiautomator/UiWatcher
"""

from __future__ import annotations

from typing import Optional, Union

from mobly.controllers.android_device_lib import snippet_client_v2

from snippet_uiautomator import byselector
from snippet_uiautomator import constants
from snippet_uiautomator import errors


class UiWatchers(list):
  """Operates all registered UiWatchers."""

  def __init__(self, ui: snippet_client_v2.SnippetClientV2) -> None:
    super().__init__()
    self._ui = ui
    for watcher in self._ui.getWatchers():
      self.append(watcher)

  @property
  def triggered(self) -> bool:
    """Checks if any watcher is triggered."""
    return self._ui.hasAnyWatcherTriggered()

  def remove(self, name: Optional[str] = None) -> None:
    """Removes all watchers or specific watcher.

    Args:
      name: The name of the watcher to be removed. If not specified, all
        watchers will be removed.
    """
    if name is None:
      self._ui.removeWatchers()
    else:
      self._ui.removeWatcher(name)

  def reset(self) -> None:
    """Resets all triggered watchers."""
    self._ui.resetWatcherTriggers()

  def run(self) -> None:
    """Forces all registered watchers to run."""
    self._ui.runWatchers()


class UiWatcher:
  """Represents an UiWatcher.

  https://developer.android.com/reference/androidx/test/uiautomator/UiWatcher
  """

  name: str

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      name: str,
  ) -> None:
    self._ui = ui
    self._condition = byselector.BySelector()
    self.name = name

  @property
  def triggered(self) -> bool:
    """Checks if this watcher is triggered."""
    return self._ui.hasWatcherTriggered(self.name)

  def click(self, **kwargs) -> None:
    """Clicks a specific UiObject2 when this watcher is triggered.

    Args:
      **kwargs: If no search criteria is passed in, when the watcher is
        triggered, the object that triggers the watch condition will be clicked.
        If there is search criteria, the matching object will be clicked.
    """
    action_dict = byselector.BySelector(**kwargs).to_dict() if kwargs else None
    self._ui.registerWatcher(self.name, self._condition.to_dict(), action_dict)

  def press(self, *args: int) -> None:
    """Presses KeyEvents in sequence when this watcher is triggered.

    https://developer.android.com/reference/android/view/KeyEvent

    Args:
      *args: One or more KeyEvents, the order in which they are passed in
        determines the order they are pressed when watcher is triggered.
    """
    if not args:
      raise errors.ApiError(
          'At least one key code required when UiWatcher is triggered.'
      )
    self._ui.registerWatcherForKeycodes(
        self.name, self._condition.to_dict(), list(args)
    )

  def swipe(
      self,
      direction: constants.Direction,
      percent: int,
      speed: int,
      **kwargs,
  ) -> None:
    """Swipes a specific UiObject2 when this watcher is triggered.

    Args:
      direction: The direction to swipe ("DOWN", "LEFT", "RIGHT", "UP").
      percent: The length of the swipe or the distance to scroll as a percentage
        of this object's size. This value must between 0 and 100.
      speed: The speed at which to perform this gesture in pixels per second.
      **kwargs: If no search criteria is passed in, when the watcher is
        triggered, the object that triggers the watch condition will be swiped.
        If there is search criteria, the matching object will be swiped.
    """
    action_dict = byselector.BySelector(**kwargs).to_dict() if kwargs else None
    self._ui.registerWatcherForSwipe(
        self.name,
        self._condition.to_dict(),
        action_dict,
        direction.value,
        percent,
        speed,
    )

  def when(self, **kwargs) -> UiWatcher:
    """Indicates a matched condition to trigger this watcher.

    Args:
      **kwargs: The search criteria for matching objects.

    Returns:
      A UiWatcher object which needs to further define the action to be
      performed when this watcher is triggered.
    """
    self._condition = byselector.BySelector(**kwargs)
    return self

  def remove(self) -> None:
    """Removes this Watcher from UiAutomator."""
    self._ui.removeWatcher(self.name)

