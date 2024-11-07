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

import android.os.SystemClock;
import androidx.annotation.NonNull;
import androidx.test.uiautomator.StaleObjectException;
import com.google.android.mobly.snippet.util.Log;
import java.util.function.Supplier;

/** Utils for operating UiAutomator. */
final class Utils {
  private static final long DEFAULT_CPU_SLEEP_MS = 100L;

  public static boolean waitUntilTrue(@NonNull Supplier<Boolean> supplier, long timeoutInMillis) {
    final long endTime = SystemClock.uptimeMillis() + timeoutInMillis;
    do {
      try {
        if (supplier.get()) {
          return true;
        }
      } catch (StaleObjectException e) {
        Log.e("UI has been updated since the last retrieval, retrying...", e);
      }
      SystemClock.sleep(DEFAULT_CPU_SLEEP_MS);
    } while (SystemClock.uptimeMillis() < endTime);
    return false;
  }

  private Utils() {}
}
