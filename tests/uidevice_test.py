# Copyright 2026 Google Inc. All Rights Reserved.
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
"""Tests for snippet_uiautomator.uidevice."""

import time
from unittest import mock

from snippet_uiautomator import uidevice
from snippet_uiautomator import uiobject2


def test_any_exists_positional_args_first_found():
  mock_ui = mock.Mock()
  mock_ui.exists.side_effect = lambda selector: selector == {'text': 'obj1'}

  wait_obj = uidevice._Wait(mock_ui)

  obj1 = mock.Mock(spec=uiobject2.UiObject2)
  obj1.selector.to_dict.return_value = {'text': 'obj1'}

  obj2 = mock.Mock(spec=uiobject2.UiObject2)
  obj2.selector.to_dict.return_value = {'text': 'obj2'}

  result = wait_obj.any_exists(obj1, obj2, timeout=1000)
  assert result == obj1
  mock_ui.exists.assert_called_once_with({'text': 'obj1'})


def test_any_exists_list_arg_second_found():
  mock_ui = mock.Mock()
  mock_ui.exists.side_effect = lambda selector: selector == {'text': 'obj2'}

  wait_obj = uidevice._Wait(mock_ui)

  obj1 = mock.Mock(spec=uiobject2.UiObject2)
  obj1.selector.to_dict.return_value = {'text': 'obj1'}

  obj2 = mock.Mock(spec=uiobject2.UiObject2)
  obj2.selector.to_dict.return_value = {'text': 'obj2'}

  result = wait_obj.any_exists([obj1, obj2], timeout=1000)
  assert result == obj2
  mock_ui.exists.assert_has_calls(
      [
          mock.call({'text': 'obj1'}),
          mock.call({'text': 'obj2'}),
      ]
  )


def test_any_exists_found_after_delay():
  mock_ui = mock.Mock()
  calls = []

  def exists_side_effect(selector):
    calls.append(selector)
    if len(calls) > 2 and selector == {'text': 'obj2'}:
      return True
    return False

  mock_ui.exists.side_effect = exists_side_effect

  wait_obj = uidevice._Wait(mock_ui)

  obj1 = mock.Mock(spec=uiobject2.UiObject2)
  obj1.selector.to_dict.return_value = {'text': 'obj1'}

  obj2 = mock.Mock(spec=uiobject2.UiObject2)
  obj2.selector.to_dict.return_value = {'text': 'obj2'}

  result = wait_obj.any_exists(obj1, obj2, timeout=1000)
  assert result == obj2
  assert len(calls) == 4
  assert calls == [
      {'text': 'obj1'},
      {'text': 'obj2'},
      {'text': 'obj1'},
      {'text': 'obj2'},
  ]


def test_any_exists_not_found_timeout():
  mock_ui = mock.Mock()
  mock_ui.exists.return_value = False

  wait_obj = uidevice._Wait(mock_ui)

  obj1 = mock.Mock(spec=uiobject2.UiObject2)
  obj1.selector.to_dict.return_value = {'text': 'obj1'}

  obj2 = mock.Mock(spec=uiobject2.UiObject2)
  obj2.selector.to_dict.return_value = {'text': 'obj2'}

  start_time = time.time()
  result = wait_obj.any_exists(obj1, obj2, timeout=250)
  elapsed = (time.time() - start_time) * 1000

  assert result is None
  assert mock_ui.exists.call_count >= 4  # 2 objects * 2+ loops
  assert elapsed >= 200
