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

"""This module is corresponding to the "androidx.test.uiautomator.Configurator".

https://developer.android.com/reference/androidx/test/uiautomator/Configurator
"""

import dataclasses
import datetime
import enum
import functools
from typing import Mapping, Optional, Sequence

from snippet_uiautomator import constants
from snippet_uiautomator import utils


@enum.unique
class Flag(enum.IntEnum):
  """Flags to configure UiAutomator.

  https://developer.android.com/reference/android/app/UiAutomation.html#constants

  Attributes:
    FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES: Prevent the UiAutomator framework
      from suppressing accessibility services.
    FLAG_DONT_USE_ACCESSIBILITY: Prevent the UiAutomator framework from using
      accessibility services.
  """

  FLAG_DONT_SUPPRESS_ACCESSIBILITY_SERVICES = 1
  FLAG_DONT_USE_ACCESSIBILITY = 2


@enum.unique
class ToolType(enum.IntEnum):
  """Indicates the type of tool used to make contact.

  https://developer.android.com/reference/android/view/MotionEvent.html#getToolType(int)

  Attributes:
    TOOL_TYPE_UNKNOWN: When the tool type is not known or is not relevant, such
      as for a trackball or other non-pointing device.
    TOOL_TYPE_FINGER: When the tool is a finger.
    TOOL_TYPE_STYLUS: When the tool is a stylus.
    TOOL_TYPE_MOUSE: When the tool is a mouse.
    TOOL_TYPE_ERASER: When the tool is an eraser or a stylus being used in an
      inverted posture.
  """

  TOOL_TYPE_UNKNOWN = 0
  TOOL_TYPE_FINGER = 1
  TOOL_TYPE_STYLUS = 2
  TOOL_TYPE_MOUSE = 3
  TOOL_TYPE_ERASER = 4


@dataclasses.dataclass(frozen=True)
class Timeout:
  """Indicates timers to wait for UiAutomator to take specific actions.

  Attributes:
    key_injection_delay: Delay time between key presses when injecting text
      input.
    action_acknowledgment: Wait for an acknowledgment of generic uiautomator
      actions. Generally, this timeout should not be modified.
    scroll_acknowledgment: Wait for an acknowledgement of an uiautomtor scroll
      swipe action. Generally, this timeout should not be modified.
    wait_for_idle: Wait for the user interface to go into an idle state before
      starting a uiautomator action.
    wait_for_selector: Wait for a widget to become visible in the user interface
      so that it can be matched by a selector.
  """

  key_injection_delay: Optional[datetime.timedelta] = None
  action_acknowledgment: Optional[datetime.timedelta] = None
  scroll_acknowledgment: Optional[datetime.timedelta] = None
  wait_for_idle: Optional[datetime.timedelta] = None
  wait_for_selector: datetime.timedelta = (
      constants.DEFAULT_WAIT_FOR_SELECTOR_TIMEOUT
  )


@dataclasses.dataclass(frozen=True)
class Configurator:
  """Represents a Configurator.

  https://developer.android.com/reference/androidx/test/uiautomator/Configurator

  Attributes:
    flags: A list of flags to configure UiAutomator.
    timeout: The timer to configure UiAutomator.
    tool_type: The current tool type to use for motion events.
  """

  flags: Sequence[Flag] = ()
  timeout: Timeout = Timeout()
  tool_type: Optional[ToolType] = None

  def to_dict(self) -> Mapping[str, int]:
    """Converts Configurator to the ConfiguratorInfo for the RPC."""
    config = {}

    if self.tool_type is not None:
      config['toolType'] = self.tool_type.value

    if len(self.flags) == 1:
      config['uiAutomationFlags'] = self.flags[0].value
    elif len(self.flags) > 1:
      config['uiAutomationFlags'] = functools.reduce(
          lambda x, y: x | y, self.flags
      )

    if self.timeout.action_acknowledgment is not None:
      config['actionAcknowledgmentTimeout'] = utils.covert_to_millisecond(
          self.timeout.action_acknowledgment
      )
    if self.timeout.key_injection_delay is not None:
      config['keyInjectionDelay'] = utils.covert_to_millisecond(
          self.timeout.key_injection_delay
      )
    if self.timeout.scroll_acknowledgment is not None:
      config['scrollAcknowledgmentTimeout'] = utils.covert_to_millisecond(
          self.timeout.scroll_acknowledgment
      )
    if self.timeout.wait_for_idle is not None:
      config['waitForIdleTimeout'] = utils.covert_to_millisecond(
          self.timeout.wait_for_idle
      )
    if self.timeout.wait_for_selector is not None:
      config['waitForSelectorTimeout'] = utils.covert_to_millisecond(
          self.timeout.wait_for_selector
      )

    return config

