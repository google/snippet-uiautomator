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

"""Public constants for UiAutomator."""

import dataclasses
import datetime
import enum

DEFAULT_UI_WAIT_TIME = datetime.timedelta(seconds=10)
DEFAULT_WAIT_FOR_SELECTOR_TIMEOUT = datetime.timedelta(seconds=0)


@dataclasses.dataclass(frozen=True)
class Rect:
  """Represents the android.graphics.Rect object.

  https://developer.android.com/reference/android/graphics/Rect.html

  In the uiautomatorviewer tool, the Rect object is displayed in the `bounds`
  column, and the value format is `[left, top][right, bottom]`.
  """

  bottom: int
  left: int
  right: int
  top: int


@dataclasses.dataclass(frozen=True)
class Point:
  """Represents the android.graphics.Point object.

  https://developer.android.com/reference/android/graphics/Point.html

  Attributes:
    x: The X coordinate. 0 is the left edge of the screen.
    y: The Y coordinate. 0 is the top edge of the screen.
  """

  x: int
  y: int


@enum.unique
class Direction(enum.Enum):
  """Represents the androidx.test.uiautomator.Direction object.

  https://developer.android.com/reference/androidx/test/uiautomator/Direction
  """

  DOWN = 'DOWN'
  LEFT = 'LEFT'
  RIGHT = 'RIGHT'
  UP = 'UP'


@enum.unique
class Orientation(enum.Enum):
  """Represents the orientation of the display.

  | orientation | rotation | displayRotation |
  | ----------- | -------- | --------------- |
  | natural     | 0        | 0               |
  | left        | 90       | 1               |
  | upsidedown  | 180      | 2               |
  | right       | 270      | 3               |
  """

  NATURAL = 0
  LEFT = 1
  UPSIDEDOWN = 2
  RIGHT = 3

