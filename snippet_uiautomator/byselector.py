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

"""This module is corresponding to the "androidx.test.uiautomator.BySelector".

https://developer.android.com/reference/androidx/test/uiautomator/BySelector
"""

from typing import Mapping, Union

SelectorType = Mapping[str, Union[bool, int, str]]
NestedSelectorType = Mapping[
    str, Union[bool, int, str, SelectorType, 'NestedSelectorType']
]


class SelectorError(Exception):
  """Raised when user uses incorrect search criteria."""


class BySelector:
  """Represents a BySelector.

  https://developer.android.com/reference/androidx/test/uiautomator/BySelector
  """

  SUBSELECTOR = ('child', 'parent', 'sibling', 'bottom', 'left', 'right', 'top')

  def __init__(self, **kwargs) -> None:
    """Converts the keyword arguments to selector type."""
    self._selector = dict(kwargs)
    self._bottom = self._selector

  def append(self, name: str, **kwargs) -> None:
    """Adds a new selector to the bottom of main selector.

    Args:
      name: Indicates the sub-selector type.
      **kwargs: Specifies criteria for matching sub UI element.

    Raises:
      SelectorError: When the sub-selector has incorrect name or keys.
    """
    if name not in self.SUBSELECTOR:
      raise SelectorError(f'Unexpected selector type: {repr(name)}')
    if any(key in self.SUBSELECTOR for key in kwargs):
      raise SelectorError(
          f'Basic selector should not contain sub-selector: {repr(kwargs)}'
      )
    self._bottom[name] = dict(kwargs)
    self._bottom = self._bottom[name]

  def is_nested(self) -> bool:
    """Checks if this selector will be converted to a nested dictionary."""
    return any(isinstance(value, dict) for value in self._selector.values())

  def to_dict(self) -> NestedSelectorType:
    """Returns a selector as a dictionary."""
    return self._selector

