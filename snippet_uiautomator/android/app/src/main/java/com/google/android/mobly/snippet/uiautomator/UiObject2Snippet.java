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

package com.google.android.mobly.snippet.uiautomator;

import static com.google.common.collect.ImmutableList.toImmutableList;

import android.graphics.Point;
import androidx.test.uiautomator.BySelector;
import androidx.test.uiautomator.Direction;
import androidx.test.uiautomator.StaleObjectException;
import androidx.test.uiautomator.UiObject2;
import androidx.test.uiautomator.Until;
import com.google.android.mobly.snippet.Snippet;
import com.google.android.mobly.snippet.rpc.Rpc;
import com.google.android.mobly.snippet.rpc.RpcOptional;
import com.google.android.mobly.snippet.uiautomator.Info.PointInfo;
import com.google.android.mobly.snippet.uiautomator.Info.RectInfo;
import com.google.android.mobly.snippet.uiautomator.Info.UiObject2Info;
import com.google.android.mobly.snippet.uiautomator.selector.Selector;
import com.google.android.mobly.snippet.uiautomator.selector.SelectorException;
import com.google.android.mobly.snippet.util.Log;
import com.google.common.collect.ImmutableList;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Function;
import org.checkerframework.checker.nullness.qual.Nullable;

/**
 * UiObject2 snippet class.
 *
 * <p><a
 * href="https://developer.android.com/reference/androidx/test/uiautomator/UiObject2">UiObject2</a>
 */
public class UiObject2Snippet implements Snippet {
  @Rpc(description = "Clears the text content if this object is an editable field.")
  public boolean clear(Selector selector) throws SelectorException {
    return operate(selector, UiObject2::clear);
  }

  @Rpc(description = "Clicks on this object.")
  public boolean clickObj(Selector selector, @RpcOptional Long durationInMillis)
      throws SelectorException {
    return durationInMillis == null
        ? operate(selector, UiObject2::click)
        : operate(selector, uiObject2 -> uiObject2.click(durationInMillis));
  }

  @Rpc(description = "Clicks on this object, and waits for a window content update event to occur.")
  public boolean clickObjAndWait(Selector selector, Long durationInMillis)
      throws SelectorException {
    return getBoolean(
        selector, uiObject2 -> uiObject2.clickAndWait(Until.newWindow(), durationInMillis));
  }

  @Rpc(description = "Drags this object in pixels per second to the specified location.")
  public boolean dragObj(Selector selector, int x, int y, @RpcOptional Integer speed)
      throws SelectorException {
    return speed == null
        ? operate(selector, uiObject2 -> uiObject2.drag(new Point(x, y)))
        : operate(selector, uiObject2 -> uiObject2.drag(new Point(x, y), speed));
  }

  @Rpc(description = "Drags this object in pixels per second to the another object.")
  public boolean dragObjToObj(
      Selector selector, Selector targetSelector, @RpcOptional Integer speed)
      throws SelectorException {
    UiObject2 uiObject2 = selector.toUiObject2();
    if (uiObject2 == null) {
      return false;
    }
    try {
      return speed == null
          ? operate(
              targetSelector, targetUiObject2 -> uiObject2.drag(targetUiObject2.getVisibleCenter()))
          : operate(
              targetSelector,
              targetUiObject2 -> uiObject2.drag(targetUiObject2.getVisibleCenter(), speed));
    } finally {
      uiObject2.recycle();
    }
  }

  @Rpc(description = "Checks if this object exists.")
  public boolean exists(Selector selector) {
    UiObject2 uiObject2 = selector.toUiObject2NoWait();
    if (uiObject2 == null) {
      return false;
    } else {
      uiObject2.recycle();
      return true;
    }
  }

  @Rpc(
      description =
          "Searches all elements under this object and returns all objects that match the"
              + " criteria.")
  public ImmutableList<UiObject2Info> findChildObjects(Selector selector, Selector childSelector)
      throws SelectorException {
    UiObject2 uiObject2 = selector.toUiObject2();
    if (uiObject2 == null) {
      return ImmutableList.of();
    }
    try {
      return uiObject2.findObjects(childSelector.toBySelector()).stream()
          .map(Info::getUiObject2Info)
          .collect(toImmutableList());
    } finally {
      uiObject2.recycle();
    }
  }

  @Rpc(description = "Performs a fling gesture in pixels per second on this object.")
  public boolean fling(Selector selector, String directionStr, @RpcOptional Integer speed)
      throws SelectorException {
    Direction direction = Direction.valueOf(directionStr);
    return speed == null
        ? operate(selector, uiObject2 -> uiObject2.fling(direction))
        : operate(selector, uiObject2 -> uiObject2.fling(direction, speed));
  }

  @Rpc(description = "Returns the package name of the app that this object belongs to.")
  public String getApplicationPackage(Selector selector) throws SelectorException {
    return getString(selector, UiObject2::getApplicationPackage);
  }

  @Rpc(description = "Returns a collection of the child elements directly under this object.")
  public ImmutableList<UiObject2Info> getChildren(Selector selector) throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty
          .map(
              uiObject2 ->
                  uiObject2.getChildren().stream()
                      .map(Info::getUiObject2Info)
                      .collect(toImmutableList()))
          .orElse(ImmutableList.of());
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  @Rpc(description = "Returns the class name of the underlying View represented by this object.")
  public String getClassName(Selector selector) throws SelectorException {
    return getString(selector, UiObject2::getClassName);
  }

  @Rpc(description = "Returns the content description for this object.")
  public String getContentDescription(Selector selector) throws SelectorException {
    return getString(selector, UiObject2::getContentDescription);
  }

  @Rpc(description = "Returns the ID of the display containing this object.")
  public int getDisplayId(Selector selector) throws SelectorException {
    return getInt(selector, UiObject2::getDisplayId);
  }

  @Rpc(description = "Returns the hint text of this object.")
  public String getHint(Selector selector) throws SelectorException {
    return getString(selector, UiObject2::getHint);
  }

  @Rpc(description = "Returns all properties of the UI element.")
  public @Nullable UiObject2Info getObjInfo(Selector selector) throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty.map(Info::getUiObject2Info).orElse(null);
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  @Rpc(description = "Returns the fully qualified resource name for this object's id.")
  public String getResourceName(Selector selector) throws SelectorException {
    return getString(selector, UiObject2::getResourceName);
  }

  @Rpc(description = "Returns the text value for this object.")
  public String getText(Selector selector) throws SelectorException {
    return getString(selector, UiObject2::getText);
  }

  @Rpc(description = "Returns the visible bounds of this object in screen coordinates.")
  public @Nullable RectInfo getVisibleBounds(Selector selector) throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty
          .map(uiObject2 -> Info.getRectInfo(uiObject2.getVisibleBounds()))
          .orElse(null);
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  @Rpc(description = "Returns a point in the center of the visible bounds of this object.")
  public @Nullable PointInfo getVisibleCenter(Selector selector) throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty
          .map(uiObject2 -> Info.getPointInfo(uiObject2.getVisibleCenter()))
          .orElse(null);
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  @Rpc(description = "Returns whether there is a match for the given criteria under this object.")
  public boolean hasChildObject(Selector selector, Selector childSelector)
      throws SelectorException {
    UiObject2 uiObject2 = selector.toUiObject2NoWait();
    if (uiObject2 == null) {
      return false;
    }
    try {
      return Optional.ofNullable(childSelector.toBySelector())
          .map(uiObject2::hasObject)
          .orElse(false);
    } finally {
      uiObject2.recycle();
    }
  }

  @Rpc(description = "Returns whether this object is checkable.")
  public boolean isCheckable(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isCheckable);
  }

  @Rpc(description = "Returns whether this object is checked.")
  public boolean isChecked(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isChecked);
  }

  @Rpc(description = "Returns whether this object is clickable.")
  public boolean isClickable(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isClickable);
  }

  @Rpc(description = "Returns whether this object is enabled.")
  public boolean isEnabled(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isEnabled);
  }

  @Rpc(description = "Returns whether this object is focusable.")
  public boolean isFocusable(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isFocusable);
  }

  @Rpc(description = "Returns whether this object is focused.")
  public boolean isFocused(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isFocused);
  }

  @Rpc(description = "Returns whether this object is long clickable.")
  public boolean isLongClickable(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isLongClickable);
  }

  @Rpc(description = "Returns whether this object is scrollable.")
  public boolean isScrollable(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isScrollable);
  }

  @Rpc(description = "Returns whether this object is selected.")
  public boolean isSelected(Selector selector) throws SelectorException {
    return getBoolean(selector, UiObject2::isSelected);
  }

  @Rpc(description = "Performs a long click on this object.")
  public boolean longClick(Selector selector) throws SelectorException {
    return operate(selector, UiObject2::longClick);
  }

  @Rpc(description = "Performs a pinch close gesture in pixels per second on this object.")
  public boolean pinchClose(Selector selector, int percent, @RpcOptional Integer speed)
      throws SelectorException {
    return speed == null
        ? operate(selector, uiObject2 -> uiObject2.pinchClose(percent / 100f))
        : operate(selector, uiObject2 -> uiObject2.pinchClose(percent / 100f, speed));
  }

  @Rpc(description = "Performs a pinch open gesture in pixels per second on this object.")
  public boolean pinchOpen(Selector selector, int percent, @RpcOptional Integer speed)
      throws SelectorException {
    return speed == null
        ? operate(selector, uiObject2 -> uiObject2.pinchOpen(percent / 100f))
        : operate(selector, uiObject2 -> uiObject2.pinchOpen(percent / 100f, speed));
  }

  @Rpc(description = "Performs a scroll gesture in pixels per second on this object.")
  public boolean scroll(
      Selector selector,
      String directionStr,
      int percent,
      @RpcOptional Integer speed,
      @RpcOptional Integer gestureMargin,
      @RpcOptional Integer gestureMarginPercent)
      throws SelectorException {
    final Direction direction = Direction.valueOf(directionStr);
    final UiObject2 uiObject2 = selector.toUiObject2();
    if (uiObject2 == null) {
      return false;
    }
    if (gestureMargin != null) {
      Log.i("Setting gesture margin to " + gestureMargin);
      uiObject2.setGestureMargin(gestureMargin);
    } else if (gestureMarginPercent != null) {
      Log.i("Setting gesture margin percentage to " + gestureMarginPercent);
      uiObject2.setGestureMarginPercentage(gestureMarginPercent / 100f);
    }
    try {
      if (speed == null) {
        return uiObject2.scroll(direction, percent / 100f);
      } else {
        return uiObject2.scroll(direction, percent / 100f, speed);
      }
    } finally {
      uiObject2.recycle();
    }
  }

  @Rpc(description = "Scrolls to the end of a scrollable layout element.")
  public boolean scrollUntilFinished(
      Selector selector,
      String directionStr,
      @RpcOptional Integer margin,
      @RpcOptional Integer percent)
      throws SelectorException {
    Direction direction = Direction.valueOf(directionStr);
    UiObject2 uiObject2 = selector.toUiObject2();
    if (uiObject2 == null) {
      return false;
    }
    if (margin != null) {
      uiObject2.setGestureMargin(margin);
    } else if (percent != null) {
      uiObject2.setGestureMarginPercentage(percent / 100f);
    }
    try {
      return uiObject2.scrollUntil(direction, Until.scrollFinished(direction));
    } catch (NullPointerException e) {
      Log.e("No more scrolling events occur and are considered complete.", e);
      return true;
    } finally {
      uiObject2.recycle();
    }
  }

  @Rpc(
      description =
          "Performs a scroll forward action to move through the scrollable layout element until a"
              + " visible item that matches the selector is found.")
  public boolean scrollUntil(
      Selector selector,
      Selector childSelector,
      String directionStr,
      @RpcOptional Integer margin,
      @RpcOptional Integer percent)
      throws SelectorException {
    UiObject2 uiObject2 = selector.toUiObject2();
    if (uiObject2 == null) {
      return false;
    }
    if (margin != null) {
      uiObject2.setGestureMargin(margin);
    } else if (percent != null) {
      uiObject2.setGestureMarginPercentage(percent / 100f);
    }
    BySelector childBySelector = childSelector.toBySelector();
    Direction direction = Direction.valueOf(directionStr);
    try {
      return childBySelector != null
          && uiObject2.scrollUntil(direction, Until.hasObject(childBySelector));
    } finally {
      uiObject2.recycle();
    }
  }

  @Rpc(description = "Sets the text content if this object is an editable field.")
  public boolean setText(Selector selector, String text) throws SelectorException {
    return operate(selector, uiObject2 -> uiObject2.setText(text));
  }

  @Rpc(description = "Performs a swipe gesture in pixels per second on this object.")
  public boolean swipeObj(
      Selector selector, String directionStr, int percent, @RpcOptional Integer speed)
      throws SelectorException {
    Direction direction = Direction.valueOf(directionStr);
    return speed == null
        ? operate(selector, uiObject2 -> uiObject2.swipe(direction, percent / 100f))
        : operate(selector, uiObject2 -> uiObject2.swipe(direction, percent / 100f, speed));
  }

  @Rpc(description = "Waits for given the condition to be met.")
  public boolean waitForExists(Selector selector, long timeoutInMillis) throws SelectorException {
    return Utils.waitUntilTrue(() -> selector.toUiObject2NoWait() != null, timeoutInMillis);
  }

  @Rpc(description = "Waits for given the condition to be gone.")
  public boolean waitUntilGone(Selector selector, long timeoutInMillis) throws SelectorException {
    try {
      return Utils.waitUntilTrue(() -> selector.toUiObject2NoWait() == null, timeoutInMillis);
    } catch (StaleObjectException e) {
      return true;
    }
  }

  private static boolean getBoolean(Selector selector, Function<UiObject2, Boolean> function)
      throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty.map(function).orElse(false);
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  private static int getInt(Selector selector, Function<UiObject2, Integer> function)
      throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty.map(function).orElse(-1);
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  private static String getString(Selector selector, Function<UiObject2, String> function)
      throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    try {
      return uiObject2OrEmpty.map(function).orElse("");
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  private static boolean operate(Selector selector, Consumer<UiObject2> consumer)
      throws SelectorException {
    Optional<UiObject2> uiObject2OrEmpty = Optional.ofNullable(selector.toUiObject2());
    uiObject2OrEmpty.ifPresent(consumer);
    try {
      return uiObject2OrEmpty.isPresent();
    } finally {
      recycle(uiObject2OrEmpty);
    }
  }

  private static void recycle(Optional<UiObject2> uiObject2OrEmpty) {
    uiObject2OrEmpty.ifPresent(UiObject2::recycle);
  }

  @Override
  public void shutdown() {}
}
