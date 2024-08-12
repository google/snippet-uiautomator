# Selector API Usage

This doc is showing how Snippet UiAutomator implement the
[BySelector](https://developer.android.com/reference/androidx/test/uiautomator/BySelector)
to specify criteria for matching UI elements.

## Search by Criteria

Selector supports multiple parameters for matching.

*   Boolean

    [checkable](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#checkable(boolean)),
    [checked](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#checked(boolean)),
    [clickable](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#clickable(boolean)),
    [enabled](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#enabled(boolean)),
    [focusable](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#focusable(boolean)),
    [focused](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#focused(boolean)),
    [longClickable](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#longClickable(boolean)),
    [scrollable](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#scrollable(boolean)),
    [selected](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#selected(boolean))

*   Integer

    [depth](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#depth(int)),
    [displayId](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#displayId(int))

> Important: Not support `index` and `instance` as parameters because these
> search criteria are for UiSelector.

*   String

    [clazz](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#clazz(java.lang.Class)),
    [desc](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#desc(java.lang.String)),
    [descContains](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#descContains(java.lang.String)),
    [descEndsWith](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#descEndsWith(java.lang.String)),
    [descStartsWith](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#descStartsWith(java.lang.String)),
    [hint](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#hint(java.lang.String)),
    [hintContains](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#hintContains(java.lang.String)),
    [hintEndsWith](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#hintEndsWith(java.lang.String)),
    [hintStartsWith](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#hintStartsWith(java.lang.String)),
    [pkg](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#pkg(java.lang.String)),
    [res](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#res(java.lang.String)),
    [text](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#text(java.lang.String)),
    [textContains](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#textContains(java.lang.String)),
    [textEndsWith](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#textEndsWith(java.lang.String)),
    [textStartsWith](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#textStartsWith(java.lang.String))

*   Regular Expression

    [clazzMatches](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#clazz(java.util.regex.Pattern)),
    [descMatches](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#desc(java.util.regex.Pattern)),
    [hintMatches](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#hint(java.util.regex.Pattern)),
    [pkgMatches](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#pkg(java.util.regex.Pattern)),
    [resMatches](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#res(java.util.regex.Pattern)),
    [textMatches](https://developer.android.com/reference/androidx/test/uiautomator/BySelector#text(java.util.regex.Pattern))

> Tip: BySelector uses some abbreviations to name Criteria, but Selector still
> supports to use their full names.
>
> Abbreviation | Full Name
> ------------ | -----------
> clazz        | className
> desc         | description
> pkg          | packageName
> res          | resourceId

Example Usage

```python
ad.ui(text='Example', enabled=True, depth=3)
```

## Search by Kinship

Selector supports to narrow down the search scope to objects that are related to
itself.

*   Ancestor

    Find the ancestor directly above present Selector.

    ```python
    ad.ui(...).ancestor(...)
    ```

*   Child

    Find the child under present Selector.

    ```python
    ad.ui(...).child(...)
    ```

    > [!TIP]
    > The child selector now supports index search, and it's recommended to pair
    > it with depth search to pinpoint the specific child element you're looking
    > for.

    ```python
    # Find the second object directly under present Selector.
    ad.ui(...).child(depth=1, index=2)
    ```

*   Parent

    Find the parent of present Selector, or null if it has no parent.

    ```python
    ad.ui(...).parent
    ```

*   Sibling

    Find the sibling or the child of the sibling, relative to the present
    Selector.

    ```python
    ad.ui(...).sibling(...)
    ```

Example Usage

```python
ad.ui(res='com.android.settings:id/settings_homepage_container')\
    .child(res='com.android.settings:id/search_bar')\
    .child(res='com.android.settings:id/search_action_bar')\
    .sibling(clazz='android.widget.ImageView').click()
```

## Search by Relative Position

Selector supports to narrow down the search scope to the object corresponding to
its own location.

*   Bottom

    Find the closest object that is below present Selector.

    ```python
    ad.ui(...).bottom(...)
    ```

*   Left

    Find the closest object that is to the left of present Selector.

    ```python
    ad.ui(...).left(...)
    ```

*   Right

    Find the closest object that is to the right of present Selector.

    ```python
    ad.ui(...).right(...)
    ```

*   Top

    Find the closest object that is above present Selector.

    ```python
    ad.ui(...).top(...)
    ```

Example Usage

```python
ad.ui(text='Airplane mode').right(clazz='android.widget.Switch').click()
```
