# UiWatcher API Usage

This doc is showing how Snippet UiAutomator implement the
[UiWatcher](https://developer.android.com/reference/androidx/test/uiautomator/UiWatcher)
to handle unexpected object on the screen.

## Register UiWatcher

Support to click on object, press key code, or swipe on object.

### When condition matches

Define what the UiWatcher should do when Selector cannot find a match and the
specific object shows in screen.

#### Click the object that matches condition

```python
ad.ui.watcher('ITSELF').when(text='Something Pop Up').click()
```

#### Click other object

```python
ad.ui.watcher('OTHER').when(text='Something Pop Up').click(text='Click Me')
```

#### Press key code

```python
# Press HOME key
ad.ui.watcher('KEYCODE').when(text='Something Pop Up').press(uiautomator.KeyEvent.KEYCODE_HOME)

# Press BACK key then HOME key
ad.ui.watcher('KEYCODES').when(text='Something Pop Up').press(uiautomator.KeyEvent.KEYCODE_BACK, uiautomator.KeyEvent.KEYCODE_HOME)
```

#### Swipe the object that matches condition

```python
ad.ui.watcher('ITSELF').when(text='Something Pop Up').swipe(Direction.UP, percent=100, speed=1000)
```

#### Swipe other object

```python
ad.ui.watcher('OTHER').when(text='Something Pop Up').swipe(Direction.LEFT, percent=50, speed=1000, text='Swipe me')
```

## Check UiWatcher Status

Check whether an UiWatcher is triggered or not, which means the UiWatcher was
run and its conditions matched.

### Check specific UiWatcher by name

```python
>>> ad.ui.watcher('ITSELF').triggered
False  # Default is False, True if it is triggered at least once.
```

### Check all UiWatchers

```python
>>> ad.ui.watchers.triggered
False  # Default is False, True if any UiWatcher is triggered.
```

## List UiWatchers

Get the names of all registered UiWatchers.

```python
>>> ad.ui.watchers
['ITSELF', 'OTHER', 'KEYCODE', 'KEYCODES']
```

## Remove UiWatcher

When you don't need a registered UiWatcher, you can remove it.

### Remove specific UiWatcher by name

```python
ad.ui.watcher('ITSELF').remove()
ad.ui.watchers.remove('ITSELF')
```

### Remove all UiWatchers

```python
ad.ui.watchers.remove()
```

## Reset UiWatchers

After an UiWatcher is triggered, its status will always be `True` unless reset
it.

> Important: When call this method, all UiWatchers will be reset, there is no
> way to recover.

```python
ad.ui.watchers.reset()
```

## Force Run UiWatchers

Force all registered UiWatchers to run.

```python
ad.ui.watchers.run()
```
