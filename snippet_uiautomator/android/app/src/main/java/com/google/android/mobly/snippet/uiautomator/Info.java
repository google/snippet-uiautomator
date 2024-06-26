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

import android.graphics.Point;
import android.graphics.Rect;
import android.os.Build.VERSION;
import androidx.test.uiautomator.UiDevice;
import androidx.test.uiautomator.UiObject2;
import com.google.auto.value.AutoValue;
import java.util.Optional;
import java.util.function.Function;
import org.checkerframework.checker.nullness.qual.Nullable;

/** Converts UiAutomator related information Java and Python. */
public final class Info {
  public Info() {}

  public static UiDeviceInfo getUiDeviceInfo(UiDevice uidevice) {
    Point point = uidevice.getDisplaySizeDp();
    return UiDeviceInfo.create(
        /* naturalOrientation= */ uidevice.isNaturalOrientation(),
        /* displayRotation= */ uidevice.getDisplayRotation(),
        /* displayHeight= */ uidevice.getDisplayHeight(),
        /* displaySizeDpX= */ point.x,
        /* displaySizeDpY= */ point.y,
        /* displayWidth= */ uidevice.getDisplayWidth(),
        /* currentPackageName= */ uidevice.getCurrentPackageName(),
        /* productName= */ uidevice.getProductName());
  }

  public static UiObject2Info getUiObject2Info(UiObject2 uiObject2) {
    if (uiObject2 == null) {
      return null;
    }

    Point point = uiObject2.getVisibleCenter();
    Rect rect = uiObject2.getVisibleBounds();
    return UiObject2Info.create(
        /* childCount= */ uiObject2.getChildCount(),
        /* displayId= */ uiObject2.getDisplayId(),
        /* className= */ getString(uiObject2, UiObject2::getClassName),
        /* contentDescription= */ getString(uiObject2, UiObject2::getContentDescription),
        /* hint= */ getString(uiObject2, UiObject2::getHint),
        /* packageName= */ getString(uiObject2, UiObject2::getApplicationPackage),
        /* resourceId= */ getString(uiObject2, UiObject2::getResourceName),
        /* text= */ getString(uiObject2, UiObject2::getText),
        /* checkable= */ uiObject2.isCheckable(),
        /* checked= */ uiObject2.isChecked(),
        /* clickable= */ uiObject2.isClickable(),
        /* enabled= */ uiObject2.isEnabled(),
        /* focusable= */ uiObject2.isFocusable(),
        /* focused= */ uiObject2.isFocused(),
        /* longClickable= */ uiObject2.isLongClickable(),
        /* scrollable= */ uiObject2.isScrollable(),
        /* selected= */ uiObject2.isSelected(),
        /* visibleBounds= */ RectInfo.create(rect.top, rect.bottom, rect.left, rect.right),
        /* visibleCenter= */ PointInfo.create(point.x, point.y));
  }

  public static PointInfo getPointInfo(Point point) {
    return PointInfo.create(point.x, point.y);
  }

  public static RectInfo getRectInfo(Rect rect) {
    return RectInfo.create(rect.top, rect.bottom, rect.left, rect.right);
  }

  private static String getString(UiObject2 uiObject2, Function<UiObject2, String> function) {
    return Optional.ofNullable(uiObject2).map(function).orElse("");
  }

  /** Corresponds to android.graphics.Point. */
  @AutoValue
  public abstract static class PointInfo {

    public static PointInfo create(int x, int y) {
      return new AutoValue_Info_PointInfo(x, y);
    }

    /** Returns the X coordinate represents the point. 0 is the left edge of the screen. */
    abstract int x();

    /** Returns the Y coordinate represents the point. 0 is the top edge of the screen. */
    abstract int y();
  }

  /** Corresponds to android.graphics.Rect. */
  @AutoValue
  public abstract static class RectInfo {

    public static RectInfo create(int top, int bottom, int left, int right) {
      return new AutoValue_Info_RectInfo(top, bottom, left, right);
    }

    /** Returns the X coordinate represents the top sideline of this object. */
    abstract int top();

    /** Returns the X coordinate represents the bottom sideline of this object. */
    abstract int bottom();

    /** Returns the Y coordinate represents the left sideline of this object. */
    abstract int left();

    /** Returns the Y coordinate represents the right sideline of this object. */
    abstract int right();
  }

  /** Corresponds to the properties of androidx.test.uiautomator.Configurator. */
  @AutoValue
  public abstract static class ConfiguratorInfo {

    public static ConfiguratorInfo create(
        @Nullable Integer toolType,
        @Nullable Integer uiAutomationFlags,
        @Nullable Long waitForIdleTimeout) {
      return new AutoValue_Info_ConfiguratorInfo(toolType, uiAutomationFlags, waitForIdleTimeout);
    }

    /** Returns the current tool type to use for motion events. */
    abstract @Nullable Integer toolType();

    /** Returns the current flags that are used to obtain a android.app.UiAutomation instance. */
    abstract @Nullable Integer uiAutomationFlags();

    /**
     * Returns the current timeout in milliseconds used for waiting for the user interface to go
     * into an idle state.
     */
    abstract @Nullable Long waitForIdleTimeout();
  }

  /** Corresponds to the properties of androidx.test.uiautomator.UiDevice. */
  @AutoValue
  abstract static class UiDeviceInfo {
    static UiDeviceInfo create(
        boolean naturalOrientation,
        int displayRotation,
        int displayHeight,
        int displaySizeDpX,
        int displaySizeDpY,
        int displayWidth,
        @Nullable String currentPackageName,
        String productName) {
      return new AutoValue_Info_UiDeviceInfo(
          naturalOrientation,
          displayRotation,
          displayHeight,
          displaySizeDpX,
          displaySizeDpY,
          displayWidth,
          VERSION.SDK_INT,
          currentPackageName,
          productName);
    }

    /** Checks if the device is in its natural orientation. */
    abstract boolean naturalOrientation();

    /** Returns the current rotation of the display, as defined in {@code Surface}. */
    abstract int displayRotation();

    /** Gets the height of the display, in pixels. */
    abstract int displayHeight();

    /** Returns the X coordinate of the display size in dp (device-independent pixel). */
    abstract int displaySizeDpX();

    /** Returns the Y coordinate of the display size in dp (device-independent pixel). */
    abstract int displaySizeDpY();

    /** Gets the width of the display, in pixels. */
    abstract int displayWidth();

    /** Retrieves the SDK version number of the device. */
    abstract int sdkInt();

    /** Retrieves the name of the last package to report accessibility events. */
    abstract @Nullable String currentPackageName();

    /** Retrieves the product name of the device. */
    abstract String productName();
  }

  /** Corresponds to the properties of androidx.test.uiautomator.UiObject2. */
  @AutoValue
  public abstract static class UiObject2Info {
    public static UiObject2Info create(
        int childCount,
        int displayId,
        String className,
        String contentDescription,
        String hint,
        String packageName,
        String resourceId,
        String text,
        boolean checkable,
        boolean checked,
        boolean clickable,
        boolean enabled,
        boolean focusable,
        boolean focused,
        boolean longClickable,
        boolean scrollable,
        boolean selected,
        RectInfo visibleBounds,
        PointInfo visibleCenter) {
      return new AutoValue_Info_UiObject2Info(
          childCount,
          displayId,
          className,
          contentDescription,
          hint,
          packageName,
          resourceId,
          text,
          checkable,
          checked,
          clickable,
          enabled,
          focusable,
          focused,
          longClickable,
          scrollable,
          selected,
          visibleBounds,
          visibleCenter);
    }

    /** Returns the number of child elements directly under this object. */
    abstract int childCount();

    /** Returns the ID of the display containing this object. */
    abstract int displayId();

    /** Returns the class name of the underlying {@code View} represented by this object. */
    abstract String className();

    /** Returns the content description for this object. */
    abstract String contentDescription();

    /** Returns the hint text of this object. */
    abstract String hint();

    /** Returns the package name of the app that this object belongs to. */
    abstract String packageName();

    /** Returns the fully qualified resource name for this object's id. */
    abstract String resourceId();

    /** Returns the text value for this object. */
    abstract String text();

    /** Returns whether this object is checkable. */
    abstract boolean checkable();

    /** Returns whether this object is checked. */
    abstract boolean checked();

    /** Returns whether this object is clickable. */
    abstract boolean clickable();

    /** Returns whether this object is enabled. */
    abstract boolean enabled();

    /** Returns whether this object is focusable. */
    abstract boolean focusable();

    /** Returns whether this object is focused. */
    abstract boolean focused();

    /** Returns whether this object is long clickable. */
    abstract boolean longClickable();

    /** Returns whether this object is scrollable. */
    abstract boolean scrollable();

    /** Returns whether this object is selected. */
    abstract boolean selected();

    /** Returns the visible bounds of this object in screen coordinates. */
    abstract RectInfo visibleBounds();

    /** Returns a point in the center of the visible bounds of this object. */
    abstract PointInfo visibleCenter();
  }
}
