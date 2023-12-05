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

import androidx.test.uiautomator.By;
import androidx.test.uiautomator.BySelector;
import com.google.common.collect.ImmutableMap;
import java.util.Optional;
import java.util.regex.Pattern;

/**
 * Pattern for mapping By and BySelector.
 *
 * <p><a href="https://developer.android.com/reference/androidx/test/uiautomator/By">By</a>
 *
 * <p><a
 * href="https://developer.android.com/reference/androidx/test/uiautomator/BySelector">BySelector</a>
 */
public final class BySelectorMap {
  public static ImmutableMap<String, IBySelector> create() {
    return new ImmutableMap.Builder<String, IBySelector>()
        .put("checkable", new Checkable())
        .put("checked", new Checked())
        .put("className", new Clazz())
        .put("classNameMatches", new ClazzMatches())
        .put("clazz", new Clazz())
        .put("clazzMatches", new ClazzMatches())
        .put("clickable", new Clickable())
        .put("depth", new Depth())
        .put("desc", new Desc())
        .put("descContains", new DescContains())
        .put("descEndsWith", new DescEndsWith())
        .put("descStartsWith", new DescStartsWith())
        .put("descMatches", new DescMatches())
        .put("description", new Desc())
        .put("descriptionContains", new DescContains())
        .put("descriptionEndsWith", new DescEndsWith())
        .put("descriptionStartsWith", new DescStartsWith())
        .put("descriptionMatches", new DescMatches())
        .put("displayId", new DisplayId())
        .put("enabled", new Enabled())
        .put("focusable", new Focusable())
        .put("focused", new Focused())
        .put("hint", new Hint())
        .put("hintContains", new HintContains())
        .put("hintEndsWith", new HintEndsWith())
        .put("hintStartsWith", new HintStartsWith())
        .put("hintMatches", new HintMatches())
        .put("longClickable", new LongClickable())
        .put("packageName", new Pkg())
        .put("packageNameMatches", new PkgMatches())
        .put("pkg", new Pkg())
        .put("pkgMatches", new PkgMatches())
        .put("res", new Res())
        .put("resMatches", new ResMatches())
        .put("resourceId", new Res())
        .put("resourceIdMatches", new ResMatches())
        .put("scrollable", new Scrollable())
        .put("selected", new Selected())
        .put("text", new Text())
        .put("textContains", new TextContains())
        .put("textEndsWith", new TextEndsWith())
        .put("textStartsWith", new TextStartsWith())
        .put("textMatches", new TextMatches())
        .buildOrThrow();
  }

  static class Checkable implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.checkable((Boolean) object))
          .orElse(By.checkable((Boolean) object));
    }
  }

  static class Checked implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.checked((Boolean) object))
          .orElse(By.checked((Boolean) object));
    }
  }

  static class Clazz implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.clazz(object.toString()))
          .orElse(By.clazz(object.toString()));
    }
  }

  static class ClazzMatches implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      Pattern pattern = Pattern.compile(object.toString());
      return Optional.ofNullable(bySelector).map(b -> b.clazz(pattern)).orElse(By.clazz(pattern));
    }
  }

  static class Clickable implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.clickable((Boolean) object))
          .orElse(By.clickable((Boolean) object));
    }
  }

  static class Depth implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.depth(Integer.parseInt(object.toString())))
          .orElse(By.depth(Integer.parseInt(object.toString())));
    }
  }

  static class Desc implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.desc(object.toString()))
          .orElse(By.desc(object.toString()));
    }
  }

  static class DescContains implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.descContains(object.toString()))
          .orElse(By.descContains(object.toString()));
    }
  }

  static class DescEndsWith implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.descEndsWith(object.toString()))
          .orElse(By.descEndsWith(object.toString()));
    }
  }

  static class DescStartsWith implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.descStartsWith(object.toString()))
          .orElse(By.descStartsWith(object.toString()));
    }
  }

  static class DescMatches implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      Pattern pattern = Pattern.compile(object.toString());
      return Optional.ofNullable(bySelector).map(b -> b.desc(pattern)).orElse(By.desc(pattern));
    }
  }

  static class DisplayId implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.displayId(Integer.parseInt(object.toString())))
          .orElse(By.displayId(Integer.parseInt(object.toString())));
    }
  }

  static class Enabled implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.enabled((Boolean) object))
          .orElse(By.enabled((Boolean) object));
    }
  }

  static class Focusable implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.focusable((Boolean) object))
          .orElse(By.focusable((Boolean) object));
    }
  }

  static class Focused implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.focused((Boolean) object))
          .orElse(By.focused((Boolean) object));
    }
  }

  static class Hint implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.hint(object.toString()))
          .orElse(By.hint(object.toString()));
    }
  }

  static class HintContains implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.hintContains(object.toString()))
          .orElse(By.hintContains(object.toString()));
    }
  }

  static class HintEndsWith implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.hintEndsWith(object.toString()))
          .orElse(By.hintEndsWith(object.toString()));
    }
  }

  static class HintStartsWith implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.hintStartsWith(object.toString()))
          .orElse(By.hintStartsWith(object.toString()));
    }
  }

  static class HintMatches implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      Pattern pattern = Pattern.compile(object.toString());
      return Optional.ofNullable(bySelector).map(b -> b.hint(pattern)).orElse(By.hint(pattern));
    }
  }

  static class LongClickable implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.longClickable((Boolean) object))
          .orElse(By.longClickable((Boolean) object));
    }
  }

  static class Pkg implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.pkg(object.toString()))
          .orElse(By.pkg(object.toString()));
    }
  }

  static class PkgMatches implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      Pattern pattern = Pattern.compile(object.toString());
      return Optional.ofNullable(bySelector).map(b -> b.pkg(pattern)).orElse(By.pkg(pattern));
    }
  }

  static class Res implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.res(object.toString()))
          .orElse(By.res(object.toString()));
    }
  }

  static class ResMatches implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      Pattern pattern = Pattern.compile(object.toString());
      return Optional.ofNullable(bySelector).map(b -> b.res(pattern)).orElse(By.res(pattern));
    }
  }

  static class Scrollable implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.scrollable((Boolean) object))
          .orElse(By.scrollable((Boolean) object));
    }
  }

  static class Selected implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.selected((Boolean) object))
          .orElse(By.selected((Boolean) object));
    }
  }

  static class Text implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.text(object.toString()))
          .orElse(By.text(object.toString()));
    }
  }

  static class TextContains implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.textContains(object.toString()))
          .orElse(By.textContains(object.toString()));
    }
  }

  static class TextEndsWith implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.textEndsWith(object.toString()))
          .orElse(By.textEndsWith(object.toString()));
    }
  }

  static class TextStartsWith implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      return Optional.ofNullable(bySelector)
          .map(b -> b.textStartsWith(object.toString()))
          .orElse(By.textStartsWith(object.toString()));
    }
  }

  static class TextMatches implements IBySelector {
    @Override
    public BySelector select(BySelector bySelector, Object object) {
      Pattern pattern = Pattern.compile(object.toString());
      return Optional.ofNullable(bySelector).map(b -> b.text(pattern)).orElse(By.text(pattern));
    }
  }

  private BySelectorMap() {}
}
