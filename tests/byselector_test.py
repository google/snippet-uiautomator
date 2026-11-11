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
"""Tests for snippet_uiautomator.byselector."""

from unittest import mock

import pytest
from snippet_uiautomator import byselector
from snippet_uiautomator import uidevice


def test_copy_flat_selector_does_not_mutate_original():
  original = byselector.BySelector(res='root')
  copied = original.copy()

  copied.append('child', text='item')

  assert original.to_dict() == {'res': 'root'}
  assert copied.to_dict() == {'res': 'root', 'child': {'text': 'item'}}


def test_copy_nested_selector_does_not_mutate_original():
  root = byselector.BySelector(res='root')
  root.append('child', clazz='android.view.ViewGroup')

  derived_selectors = []
  for i in range(3):
    branch = root.copy()
    branch.append('child', desc=f'item-{i}')
    derived_selectors.append(branch.to_dict())

  assert root.to_dict() == {
      'res': 'root',
      'child': {'clazz': 'android.view.ViewGroup'},
  }
  assert derived_selectors == [
      {
          'res': 'root',
          'child': {
              'clazz': 'android.view.ViewGroup',
              'child': {'desc': 'item-0'},
          },
      },
      {
          'res': 'root',
          'child': {
              'clazz': 'android.view.ViewGroup',
              'child': {'desc': 'item-1'},
          },
      },
      {
          'res': 'root',
          'child': {
              'clazz': 'android.view.ViewGroup',
              'child': {'desc': 'item-2'},
          },
      },
  ]


def test_copy_deeply_nested_selector_preserves_bottom_pointer():
  selector = byselector.BySelector(res='root')
  selector.append('child', clazz='android.widget.LinearLayout')
  selector.append('sibling', pkg='com.example')

  copied = selector.copy()
  copied.append('ancestor', text='Header')

  assert selector.to_dict() == {
      'res': 'root',
      'child': {
          'clazz': 'android.widget.LinearLayout',
          'sibling': {'pkg': 'com.example'},
      },
  }
  assert copied.to_dict() == {
      'res': 'root',
      'child': {
          'clazz': 'android.widget.LinearLayout',
          'sibling': {
              'pkg': 'com.example',
              'ancestor': {'text': 'Header'},
          },
      },
  }


def test_uiobject2_child_from_nested_selector_does_not_mutate_parent():
  mock_ui = mock.MagicMock()
  ui_device = uidevice.UiDevice(ui=mock_ui)

  root = ui_device(res='root')
  view_group = root.child(clazz='android.view.ViewGroup')
  first = view_group.child(desc='first')
  second = view_group.child(desc='second')

  assert view_group._selector.to_dict() == {
      'res': 'root',
      'child': {'clazz': 'android.view.ViewGroup'},
  }
  assert first._selector.to_dict() == {
      'res': 'root',
      'child': {
          'clazz': 'android.view.ViewGroup',
          'child': {'desc': 'first'},
      },
  }
  assert second._selector.to_dict() == {
      'res': 'root',
      'child': {
          'clazz': 'android.view.ViewGroup',
          'child': {'desc': 'second'},
      },
  }


def test_append_invalid_subselector_raises_error():
  selector = byselector.BySelector(text='hello')
  with pytest.raises(byselector.SelectorError):
    selector.append('invalid_subselector', text='world')


def test_append_subselector_in_kwargs_raises_error():
  selector = byselector.BySelector(text='hello')
  with pytest.raises(byselector.SelectorError):
    selector.append('child', sibling={'text': 'world'})
