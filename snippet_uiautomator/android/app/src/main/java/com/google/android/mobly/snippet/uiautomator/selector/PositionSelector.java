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

import android.graphics.Rect;
import androidx.test.uiautomator.BySelector;
import androidx.test.uiautomator.UiDevice;
import androidx.test.uiautomator.UiObject2;
import com.google.android.mobly.snippet.uiautomator.UiAutomator;
import com.google.common.collect.ImmutableList;
import java.util.Comparator;
import org.checkerframework.checker.nullness.qual.Nullable;

/** Finds the target UiObject2 by its relative position to the original UiObject2. */
public final class PositionSelector {
  private static final UiDevice uiDevice = UiAutomator.getUiDevice();

  private static boolean isHorizontal(Rect rectA, Rect rectB) {
    return rectA.bottom >= rectB.top && rectB.bottom >= rectA.top;
  }

  private static boolean isAtLeft(Rect rectA, Rect rectB) {
    return rectB.right <= rectA.left && isHorizontal(rectA, rectB);
  }

  private static boolean isAtRight(Rect rectA, Rect rectB) {
    return rectB.left >= rectA.right && isHorizontal(rectA, rectB);
  }

  private static boolean isVertical(Rect rectA, Rect rectB) {
    return rectA.right >= rectB.left && rectB.right >= rectA.left;
  }

  private static boolean isAtBottom(Rect rectA, Rect rectB) {
    return rectB.top >= rectA.bottom && isVertical(rectA, rectB);
  }

  private static boolean isAtTop(Rect rectA, Rect rectB) {
    return rectB.bottom <= rectA.top && isVertical(rectA, rectB);
  }

  public static @Nullable UiObject2 findObject(
      @Nullable UiObject2 uiObject2, BySelector bySelector, String position)
      throws SelectorException {
    if (uiObject2 == null) {
      return null;
    }

    ImmutableList<UiObject2> matchedUiObject2List =
        ImmutableList.copyOf(
            uiDevice.findObjects(bySelector).stream()
                .filter(
                    matchedUiObject2 -> {
                      switch (position) {
                        case "bottom":
                          return isAtBottom(
                              uiObject2.getVisibleBounds(), matchedUiObject2.getVisibleBounds());
                        case "right":
                          return isAtRight(
                              uiObject2.getVisibleBounds(), matchedUiObject2.getVisibleBounds());
                        case "top":
                          return isAtTop(
                              uiObject2.getVisibleBounds(), matchedUiObject2.getVisibleBounds());
                        case "left":
                          return isAtLeft(
                              uiObject2.getVisibleBounds(), matchedUiObject2.getVisibleBounds());
                        default:
                          return false;
                      }
                    })
                .iterator());

    switch (position) {
      case "bottom":
        return matchedUiObject2List.stream()
            .min(Comparator.comparing(matchedObject -> matchedObject.getVisibleBounds().top))
            .orElse(null);
      case "right":
        return matchedUiObject2List.stream()
            .min(Comparator.comparing(matchedObject -> matchedObject.getVisibleBounds().left))
            .orElse(null);
      case "top":
        return matchedUiObject2List.stream()
            .max(Comparator.comparing(matchedObject -> matchedObject.getVisibleBounds().bottom))
            .orElse(null);
      case "left":
        return matchedUiObject2List.stream()
            .max(Comparator.comparing(matchedObject -> matchedObject.getVisibleBounds().right))
            .orElse(null);
      default:
        throw new SelectorException(String.format("Receive unexpected position<%s>", position));
    }
  }

  private PositionSelector() {}
}
