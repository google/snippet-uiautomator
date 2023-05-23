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

"""This module is corresponding to the "androidx.test.uiautomator.UiObject2".

https://developer.android.com/reference/androidx/test/uiautomator/UiObject2
"""

from __future__ import annotations

from typing import Mapping, Optional, Sequence, Union

from mobly.controllers.android_device_lib import snippet_client_v2

from snippet_uiautomator import byselector
from snippet_uiautomator import constants
from snippet_uiautomator import errors
from snippet_uiautomator import utils


class _Click:
  """Performs a click action on a specific UiObject2."""

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
  ) -> None:
    self._ui = ui
    self._selector = selector

  def __call__(self, timeout: Optional[utils.TimeUnit] = None) -> bool:
    """Clicks on this object.

    Args:
      timeout: The time in milliseconds to click and hold.

    Returns:
      True if operation succeeds, False otherwise.
    """
    if timeout is None:
      return self._ui.clickObj(self._selector.to_dict())
    timeout_ms = utils.covert_to_millisecond(timeout)
    return self._ui.clickObj(self._selector.to_dict(), timeout_ms)

  def bottomright(self) -> bool:
    """Clicks the lower right corner of this object."""
    bounds = self._ui.getVisibleBounds(self._selector.to_dict())
    if bounds is None:
      return False
    return self._ui.click(bounds['right'], bounds['bottom'])

  def topleft(self) -> bool:
    """Clicks the upper left corner of this object."""
    bounds = self._ui.getVisibleBounds(self._selector.to_dict())
    if bounds is None:
      return False
    return self._ui.click(bounds['left'], bounds['top'])

  def wait(
      self, timeout: utils.TimeUnit = constants.DEFAULT_UI_WAIT_TIME
  ) -> bool:
    """Clicks on this object and waits for window transitions.

    Args:
      timeout: The time in milliseconds to wait for window transitions after
        clicked.

    Returns:
      True if a window update occurred after clicked, False otherwise.
    """
    timeout_ms = utils.covert_to_millisecond(timeout)
    return self._ui.clickObjAndWait(self._selector.to_dict(), timeout_ms)


class _Drag:
  """Performs a drag action on a specific UiObject2."""

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
  ) -> None:
    self._ui = ui
    self._selector = selector

  def __call__(
      self,
      x: Optional[int] = None,
      y: Optional[int] = None,
      speed: Optional[int] = None,
      **kwargs,
  ) -> bool:
    return self.to(x, y, speed, **kwargs)

  def to(
      self,
      x: Optional[int] = None,
      y: Optional[int] = None,
      speed: Optional[int] = None,
      **kwargs,
  ) -> bool:
    """Drags this object to the specified location.

    Args:
      x: The X coordinate of the destination.
      y: The Y coordinate of the destination.
      speed: The speed at which to perform this gesture in pixels per second.
      **kwargs: The search criteria for matching the destination object.

    Returns:
      True if operation succeeds, False otherwise.

    Raises:
      errors.ApiError: When given incorrect arguments to this method.
    """
    if x is None and y is None and kwargs:
      return self._ui.dragObjToObj(
          self._selector.to_dict(),
          byselector.BySelector(**kwargs).to_dict(),
          speed,
      )
    elif x is not None and y is not None and not kwargs:
      return self._ui.dragObj(self._selector.to_dict(), x, y, speed)
    else:
      raise errors.ApiError(
          'Drag to object and drag to coordinates cannot be mixed'
      )


class _Gesture:
  """Performs a gesture in a specific direction on a specific UiObject2."""

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
      action: str,
  ) -> None:
    self._ui = ui
    self._selector = selector
    self._action = action

  def _perform_gesture(
      self, direction: str, percent: int, speed: Optional[int]
  ) -> bool:
    """Performs a gesture on this object."""
    if self._action == 'fling':
      if percent != 0:
        raise errors.ApiError(
            'fling gesture does not support changing the percent'
        )
      return self._ui.fling(self._selector.to_dict(), direction, speed)
    elif self._action == 'swipe':
      return self._ui.swipeObj(
          self._selector.to_dict(), direction, percent, speed
      )
    else:
      raise errors.ApiError(f'Unknown gesture action: {repr(self._action)}')

  def down(self, percent: int = 0, speed: Optional[int] = None) -> bool:
    """Performs a gesture on this object with direction DOWN.

    Args:
      percent: The length of the swipe or the distance to scroll as a percentage
        of this object's size. This value must between 0 and 100.
      speed: The speed at which to perform this gesture in pixels per second.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._perform_gesture('DOWN', percent, speed)

  def left(self, percent: int = 0, speed: Optional[int] = None) -> bool:
    """Performs a gesture on this object with direction LEFT.

    Args:
      percent: The length of the swipe or the distance to scroll as a percentage
        of this object's size. This value must between 0 and 100.
      speed: The speed at which to perform this gesture in pixels per second.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._perform_gesture('LEFT', percent, speed)

  def right(self, percent: int = 0, speed: Optional[int] = None) -> bool:
    """Performs a gesture on this object with direction RIGHT.

    Args:
      percent: The length of the swipe or the distance to scroll as a percentage
        of this object's size. This value must between 0 and 100.
      speed: The speed at which to perform this gesture in pixels per second.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._perform_gesture('RIGHT', percent, speed)

  def up(self, percent: int = 0, speed: Optional[int] = None) -> bool:
    """Performs a gesture on this object with direction UP.

    Args:
      percent: The length of the swipe or the distance to scroll as a percentage
        of this object's size. This value must between 0 and 100.
      speed: The speed at which to perform this gesture in pixels per second.

    Returns:
      True if operation succeeds, False otherwise.
    """
    return self._perform_gesture('UP', percent, speed)


class _Pinch:
  """Performs a pinch gesture on a specific UiObject2."""

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
  ) -> None:
    self._ui = ui
    self._selector = selector

  def close(self, percent: float, speed: Optional[int] = None) -> bool:
    """Performs a pinch close gesture on this object.

    Args:
      percent: The size of the pinch as a percentage of this object's size.
      speed: The speed at which to perform this gesture in pixels per second.

    Returns:
      True if operation succeeds, False otherwise.
    """
    selector_dict = self._selector.to_dict()
    return self._ui.pinchClose(selector_dict, percent, speed)

  def open(self, percent: float, speed: Optional[int] = None) -> bool:
    """Performs a pinch open gesture on this object.

    Args:
      percent: The size of the pinch as a percentage of this object's size.
      speed: The speed at which to perform this gesture in pixels per second.

    Returns:
      True if operation succeeds, False otherwise.
    """
    selector_dict = self._selector.to_dict()
    return self._ui.pinchOpen(selector_dict, percent, speed)


class _Scroll:
  """Performs a scroll action on a specific UiObject2."""

  class _To:
    """Scrolls from this object to specific position or object."""

    def __init__(
        self,
        ui: snippet_client_v2.SnippetClientV2,
        selector: byselector.BySelector,
        direction: str,
    ) -> None:
      self._ui = ui
      self._selector = selector
      self._direction = direction

    def __call__(
        self,
        percent: Optional[int] = None,
        speed: Optional[int] = None,
        **kwargs,
    ) -> bool:
      """Scrolls to specific position or until target object is visible.

      Args:
        percent: The length of the swipe or the distance to scroll as a
          percentage of this object's size. This value must between 0 and 100.
        speed: The speed at which to perform this gesture in pixels per second.
        **kwargs: The search criteria for matching objects.

      Returns:
        True if operation succeed, False otherwise.

      Raises:
        errors.ApiError: When given incorrect arguments to this method.
      """
      if percent is None and speed is None:
        if kwargs:
          return self._ui.scrollUntil(
              self._selector.to_dict(), kwargs, self._direction
          )
        return self._ui.scrollUntilFinished(
            self._selector.to_dict(), self._direction
        )
      elif percent is not None and not kwargs:
        return self._ui.scroll(
            self._selector.to_dict(), self._direction, percent, speed
        )
      else:
        raise errors.ApiError(
            'Scroll by percentage and scroll by condition cannot be mixed'
        )

    def click(self, **kwargs) -> bool:
      """Scrolls until the target object is visible, then clicks."""
      if not kwargs:
        raise errors.ApiError('Target to scroll to is not defined')
      if self.__call__(**kwargs):
        return self._ui.clickObj(kwargs)
      return False

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
  ) -> None:
    self._ui = ui
    self._selector = selector

  @property
  def down(self) -> _Scroll._To:
    """Performs a scroll gesture on this object with direction DOWN."""
    return self._To(self._ui, self._selector, 'DOWN')

  @property
  def left(self) -> _Scroll._To:
    """Performs a scroll gesture on this object with direction LEFT."""
    return self._To(self._ui, self._selector, 'LEFT')

  @property
  def right(self) -> _Scroll._To:
    """Performs a scroll gesture on this object with direction RIGHT."""
    return self._To(self._ui, self._selector, 'RIGHT')

  @property
  def up(self) -> _Scroll._To:
    """Performs a scroll gesture on this object with direction UP."""
    return self._To(self._ui, self._selector, 'UP')


class _Wait:
  """Waits for a specific UiObject2 to appear or disappear."""

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
      raise_error: bool = False,
  ) -> None:
    self._ui = ui
    self._selector = selector
    self._serial = self._ui._adb.serial  # pylint: disable=protected-access
    self._raise_error = raise_error

  def click(
      self, timeout: utils.TimeUnit = constants.DEFAULT_UI_WAIT_TIME
  ) -> bool:
    """Waits for this object to appear, then clicks.

    Args:
      timeout: The time in milliseconds to wait to appear.

    Returns:
      True if the object exists and click successfully, False otherwise.
    """
    timeout_ms = utils.covert_to_millisecond(timeout)
    if self._ui.waitForExists(self._selector.to_dict(), timeout_ms):
      return self._ui.clickObj(self._selector.to_dict())
    return False

  def exists(
      self,
      timeout: utils.TimeUnit = constants.DEFAULT_UI_WAIT_TIME,
      raise_error: bool = False,
  ) -> bool:
    """Waits for this object to appear.

    Args:
      timeout: The time in milliseconds to wait to appear.
      raise_error: Set True to raise an error when the object is not found,
        False to return a False value.

    Returns:
      True if this object exists, False otherwise.
    """
    timeout_ms = utils.covert_to_millisecond(timeout)
    is_exists = self._ui.waitForExists(self._selector.to_dict(), timeout_ms)
    if is_exists:
      return True
    if self._raise_error or raise_error:
      raise errors.UiObjectSearchError(
          self._serial,
          f'Not found Selector{self._selector.to_dict()} over {timeout_ms} ms',
      )
    return False

  def gone(
      self,
      timeout: utils.TimeUnit = constants.DEFAULT_UI_WAIT_TIME,
      raise_error: bool = False,
  ) -> bool:
    """Waits for this object to disappear.

    Args:
      timeout: The time in milliseconds to wait to disappear.
      raise_error: Set True to raise an error when the object is still found,
        False to return a False value.

    Returns:
      True if this object was not found, False otherwise.
    """
    timeout_ms = utils.covert_to_millisecond(timeout)
    is_gone = self._ui.waitUntilGone(self._selector.to_dict(), timeout_ms)
    if is_gone:
      return True
    if self._raise_error or raise_error:
      raise errors.UiObjectSearchError(
          self._serial,
          f'Still found Selector{self._selector.to_dict()} over'
          f' {timeout_ms} ms',
      )
    return False


class UiObject2:
  """Represents an UiObject2.

  https://developer.android.com/reference/androidx/test/uiautomator/UiObject2
  """

  def __init__(
      self,
      ui: snippet_client_v2.SnippetClientV2,
      selector: byselector.BySelector,
      raise_error: bool = False,
  ) -> None:
    self._ui = ui
    self._selector = selector
    self._serial = self._ui._adb.serial  # pylint: disable=protected-access
    self._raise_error = raise_error

  @property
  def parent(self) -> UiObject2:
    """Finds this object's parent, or null if it has no parent."""
    self._selector.append('parent')
    return self

  def child(self, **kwargs) -> UiObject2:
    """Finds the child object directly under this object."""
    self._selector.append('child', **kwargs)
    return self

  def sibling(self, **kwargs) -> UiObject2:
    """Finds the sibling object which has the same parent with this object."""
    self._selector.append('sibling', **kwargs)
    return self

  def bottom(self, **kwargs) -> UiObject2:
    """Finds the closest object that is below this object."""
    self._selector.append('bottom', **kwargs)
    return self

  def left(self, **kwargs) -> UiObject2:
    """Finds the closest object that is to the left of this object."""
    self._selector.append('left', **kwargs)
    return self

  def right(self, **kwargs) -> UiObject2:
    """Finds the closest object that is to the right of this object."""
    self._selector.append('right', **kwargs)
    return self

  def top(self, **kwargs) -> UiObject2:
    """Finds the closest object that is above this object."""
    self._selector.append('top', **kwargs)
    return self

  def clear_text(self) -> bool:
    """Clears the text content if this object is an editable field."""
    return self._ui.clear(self._selector.to_dict())

  def find(self, **kwargs) -> Sequence[byselector.SelectorType]:
    """Finds all objects under this object to match the selector criteria."""
    return self._ui.findChildObjects(
        self._selector.to_dict(), byselector.BySelector(**kwargs).to_dict()
    )

  def has(self, **kwargs) -> bool:
    """Returns if there is a match for the given criteria under this object."""
    return self._ui.hasChildObject(
        self._selector.to_dict(), byselector.BySelector(**kwargs).to_dict()
    )

  def long_click(self) -> bool:
    """Performs a long click on this object."""
    return self._ui.longClick(self._selector.to_dict())

  def set_text(self, text: str) -> bool:
    """Sets the text content if this object is an editable field."""
    return self._ui.setText(self._selector.to_dict(), text)

  @property
  def children(self) -> Sequence[byselector.SelectorType]:
    """The child objects directly under this object."""
    return self._ui.getChildren(self._selector.to_dict())

  @property
  def click(self) -> _Click:
    """Clicks on this object."""
    return _Click(self._ui, self._selector)

  @property
  def drag(self) -> _Drag:
    """Drags this object to the specified location."""
    return _Drag(self._ui, self._selector)

  @property
  def exists(self) -> bool:
    """Checks if the this UI object exists."""
    is_exists = self._ui.exists(self._selector.to_dict())
    if not is_exists and self._raise_error:
      raise errors.UiObjectSearchError(
          self._serial, f'Not found Selector{self._selector.to_dict()}'
      )
    return is_exists

  @property
  def fling(self) -> _Gesture:
    """Performs a fling gesture on this object."""
    return _Gesture(self._ui, self._selector, 'fling')

  @property
  def info(self) -> Mapping[str, Union[bool, int, str, Mapping[str, int]]]:
    """Returns all properties of the UI element."""
    return self._ui.getObjInfo(self._selector.to_dict())

  @property
  def pinch(self) -> _Pinch:
    """Performs a pinch gesture on this object."""
    return _Pinch(self._ui, self._selector)

  @property
  def scroll(self) -> _Scroll:
    """Performs a scroll gesture on this object."""
    return _Scroll(self._ui, self._selector)

  @property
  def swipe(self) -> _Gesture:
    """Performs a swipe gesture on this object."""
    return _Gesture(self._ui, self._selector, 'swipe')

  @property
  def wait(self) -> _Wait:
    """Performs wait action on this object."""
    return _Wait(self._ui, self._selector, self._raise_error)

  @property
  def count(self) -> int:
    """The number of objects that match this selector criteria."""
    return len(self._ui.findObjects(self._selector.to_dict()))

  @property
  def display_id(self) -> int:
    """The ID of the display containing this object."""
    return self._ui.getDisplayId(self._selector.to_dict())

  @property
  def class_name(self) -> str:
    """The class name of this object."""
    return self._ui.getClassName(self._selector.to_dict())

  @property
  def description(self) -> str:
    """The content description for this object."""
    return self._ui.getContentDescription(self._selector.to_dict())

  @property
  def hint(self) -> str:
    """The hint text of this object."""
    return self._ui.getHint(self._selector.to_dict())

  @property
  def package_name(self) -> str:
    """The package name of the app that this object belongs to."""
    return self._ui.getApplicationPackage(self._selector.to_dict())

  @property
  def resource_id(self) -> str:
    """The fully qualified resource name for this object's id."""
    return self._ui.getResourceName(self._selector.to_dict())

  @property
  def text(self) -> str:
    """The text value for this object."""
    return self._ui.getText(self._selector.to_dict())

  @property
  def checkable(self) -> bool:
    """Whether this object is checkable."""
    return self._ui.isCheckable(self._selector.to_dict())

  @property
  def checked(self) -> bool:
    """Whether this object is checked."""
    return self._ui.isChecked(self._selector.to_dict())

  @property
  def clickable(self) -> bool:
    """Whether this object is clickable."""
    return self._ui.isClickable(self._selector.to_dict())

  @property
  def enabled(self) -> bool:
    """Whether this object is enabled."""
    return self._ui.isEnabled(self._selector.to_dict())

  @property
  def focusable(self) -> bool:
    """Whether this object is focusable."""
    return self._ui.isFocusable(self._selector.to_dict())

  @property
  def focused(self) -> bool:
    """Whether this object is focused."""
    return self._ui.isFocused(self._selector.to_dict())

  @property
  def long_clickable(self) -> bool:
    """Whether this object is long clickable."""
    return self._ui.isLongClickable(self._selector.to_dict())

  @property
  def scrollable(self) -> bool:
    """Whether this object is scrollable."""
    return self._ui.isScrollable(self._selector.to_dict())

  @property
  def selected(self) -> bool:
    """Whether this object is selected."""
    return self._ui.isSelected(self._selector.to_dict())

  @property
  def visible_bounds(self) -> constants.Rect:
    """This object's visible bounds."""
    rect = self._ui.getVisibleBounds(self._selector.to_dict())
    return constants.Rect(**rect)

  @property
  def visible_center(self) -> constants.Point:
    """The point in the center of this object's visible bounds."""
    point = self._ui.getVisibleCenter(self._selector.to_dict())
    return constants.Point(**point)

