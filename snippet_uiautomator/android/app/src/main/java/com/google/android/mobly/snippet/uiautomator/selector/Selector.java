/*
 * Copyright 2023 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.android.mobly.snippet.uiautomator.selector;

import androidx.test.uiautomator.BySelector;
import androidx.test.uiautomator.UiDevice;
import androidx.test.uiautomator.UiObject2;
import androidx.test.uiautomator.Until;
import com.google.android.mobly.snippet.uiautomator.ConfiguratorSnippet;
import com.google.android.mobly.snippet.util.Log;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.ImmutableSet;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Converts the selector properties from Python to UiAutomator selector and object.
 *
 * <p>Selector will return the first object to match the selector criteria, or null if no matching
 * objects are found. The behavior is the same as {@link UiDevice#findObject(BySelector)}.
 */
public class Selector {
  private static final ImmutableSet<String> SUB_SELECTORS =
      ImmutableSet.of("child", "parent", "sibling", "bottom", "left", "right", "top");
  private final UiDevice uiDevice = ConfiguratorSnippet.getUiDevice();
  private final ImmutableMap<String, IBySelector> bySelectorMap = BySelectorMap.create();
  private final JSONObject selector;

  public Selector(JSONObject selector) {
    this.selector = selector;
  }

  private @Nullable BySelector getBySelector(JSONObject selector) throws SelectorException {
    Log.d(String.format("Receive selector: %s", selector));
    BySelector bySelector = null;
    Iterator<String> keys = selector.keys();
    while (keys.hasNext()) {
      String key = keys.next();
      if (SUB_SELECTORS.contains(key)) {
        continue;
      }
      try {
        bySelector =
            Objects.requireNonNull(bySelectorMap.get(key)).select(bySelector, selector.get(key));
      } catch (JSONException e) {
        throw new SelectorException(String.format("Fail to deserialize Selector<%s>", selector), e);
      } catch (NullPointerException e) {
        Log.d(String.format("Receive key: %s (NullPointerException)", key));
        throw new SelectorException(String.format("No such key<%s> in BySelector", key), e);
      }
    }
    return bySelector;
  }

  private @Nullable UiObject2 getUiObject2(
      JSONObject selector, @Nullable UiObject2 baseUiObject2, String type)
      throws SelectorException {
    BySelector bySelector = getBySelector(selector);
    if (bySelector == null && type.equals("self")) {
      return null;
    }

    List<UiObject2> uiObject2List = new ArrayList<>();
    switch (type) {
      case "child":
        uiObject2List = baseUiObject2.findObjects(bySelector);
        break;
      case "parent":
        uiObject2List.add(baseUiObject2.getParent());
        break;
      case "sibling":
        UiObject2 parentUiObject2 = baseUiObject2.getParent();
        if (parentUiObject2 == null) {
          return null;
        }
        uiObject2List = parentUiObject2.findObjects(bySelector);
        break;
      case "bottom":
      case "left":
      case "right":
      case "top":
        uiObject2List.add(PositionSelector.findObject(baseUiObject2, bySelector, type));
        break;
      case "self":
        uiObject2List = uiDevice.findObjects(bySelector);
        break;
      default:
        throw new SelectorException(String.format("No such key (%s) in Selector", type));
    }

    if (uiObject2List.isEmpty() || uiObject2List.get(0) == null) {
      return null;
    }

    for (UiObject2 uiObject2 : uiObject2List) {
      UiObject2 matchedUiObject2 = null;

      try {
        if (selector.has("child")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("child"), uiObject2, "child");
        } else if (selector.has("parent")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("parent"), uiObject2, "parent");
        } else if (selector.has("sibling")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("sibling"), uiObject2, "sibling");
        } else if (selector.has("bottom")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("bottom"), uiObject2, "bottom");
        } else if (selector.has("left")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("left"), uiObject2, "left");
        } else if (selector.has("right")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("right"), uiObject2, "right");
        } else if (selector.has("top")) {
          matchedUiObject2 = getUiObject2(selector.getJSONObject("top"), uiObject2, "top");
        } else {
          return uiObject2;
        }
      } catch (JSONException e) {
        throw new SelectorException(String.format("Fail to deserialize Selector<%s>", selector), e);
      }

      if (matchedUiObject2 != null) {
        return matchedUiObject2;
      }
    }

    return null;
  }

  public @Nullable BySelector toBySelector() throws SelectorException {
    return getBySelector(selector);
  }

  public @Nullable UiObject2 toUiObject2() throws SelectorException {
    BySelector bySelector = getBySelector(selector);
    if (bySelector == null) {
      return null;
    }
    uiDevice.wait(Until.hasObject(bySelector), 1000L);
    return getUiObject2(selector, null, "self");
  }

  public @Nullable UiObject2 toUiObject2NoWait() {
    try {
      return getUiObject2(selector, null, "self");
    } catch (SelectorException e) {
      return null;
    }
  }
}
