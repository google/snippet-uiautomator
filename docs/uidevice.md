# UiDevice API Usage

This doc is showing how Snippet UiAutomator implement the
[UiDevice](https://developer.android.com/reference/androidx/test/uiautomator/UiDevice)
to control the Android device.

## UiAutomation API

### Clear Cache

Clear the accessibility cache for SDK 34 (Android 14) or above.

```python
>>> ad.ui.clear_cache()
True
```

## Device Information

```python
# The display height in pixels.
>>> ad.ui.height
1184

# The display width in pixels.
>>> ad.ui.width
720

# The display size in dp.
>>> ad.ui.size
{'x': 360, 'y': 640}

# The name of the last package to report accessibility events.
>>> ad.ui.package_name
'com.android.launcher'

# The default launcher package name.
>>> ad.ui.launcher
'com.android.launcher'

# The product name of the device.
>>> ad.ui.product
'pixel'

# Gets all information one time.
>>> ad.ui.info
{'naturalOrientation': True,
 'displayRotation': 0,
 'displayHeight': 1184,
 'displaySizeDpX': 360,
 'displaySizeDpY': 640,
 'displayWidth': 720,
 'sdkInt': 31,
 'currentPackageName': 'com.android.launcher',
 'productName': 'pixel'}
```

## Gesture Action

### Click the screen

```python
>>> ad.ui.click(x=50, y=100)
True
```

### Drag

```python
# Drags from point (0, 0) to point (50, 100).
>>> ad.ui.drag(sx=0, sy=0, ex=50, ey=100)
True

# Defines the number of steps for this gesture.
# Each step execution is throttled to 5 milliseconds. For 100 steps, it will
# take around 0.5 seconds to complete.
>>> ad.ui.drag(sx=0, sy=0, ex=50, ey=100, steps=100)
True
```

### Swipe

Performs a swipe from one coordinate to another.

```python
# Swipes from point (0, 0) to point (50, 100).
>>> ad.ui.swipe(sx=0, sy=0, ex=50, ey=100)
True

# Defines the number of steps for this gesture. The same as "drag" action.
>>> ad.ui.swipe(sx=0, sy=0, ex=50, ey=100, steps=100)
True
```

Performs a swipe between points in the Point array.

```python
# Define a Point array.
>>> from snippet_uiautomator import constants
>>> _POINTS_FOR_SWIPE = (
>>>     constants.Point(x=0, y=0),
>>>     constants.Point(x=250, y=250),
>>>     constants.Point(x=500, y=500),
>>> )

# Swipes between points.
>>> ad.ui.swipe(points=_POINTS_FOR_SWIPE)
True

# Defines the number of steps for this gesture.
>>> ad.ui.swipe(points=_POINTS_FOR_SWIPE, steps=100)
True
```



### KeyEvent Action

#### Turn On/Off Screen

Turn on screen

```python
>>> ad.ui.screen.on()
True

>>> ad.ui.wakeup()
True
```

Turn off screen

```python
>>> ad.ui.screen.off()
True

>>> ad.ui.sleep()
True
```

#### Check Screen Status

```python
>>> ad.ui.screen
'on'
```

#### Press Hard/Soft Key

Press HOME key

```python
>>> ad.ui.press.home()
True

>>> ad.ui.press('home')
True
```

The other support keys are:

-   back
-   left
-   right
-   up
-   down
-   center
-   menu
-   search
-   enter
-   delete
-   recent
-   volume_up
-   volume_down
-   volume_mute
-   camera
-   power

Or use
[KeyEvent](https://developer.android.com/reference/android/view/KeyEvent.html)

```python
>>> ad.ui.press(uiautomator.KeyEvent.KEYCODE_HOME)
True

# Press BACK then HOME
>>> ad.ui.press([
        uiautomator.KeyEvent.KEYCODE_BACK,
        uiautomator.KeyEvent.KEYCODE_HOME,
    ])
True
```

## Screen Action

### Retrieve/Set Orientation

#### Retrieve orientation

```python
>>> ad.ui.orientation
<Orientation.NATURAL: 0>
```

#### Set Orientation

The available orientation is:

-   \<Orientation.NATURAL: 0>
-   \<Orientation.LEFT: 1>
-   \<Orientation.RIGHT: 3>

```python
>>> ad.ui.orientation = Orientation.NATURAL
None
```

### Freeze/Un-Freeze rotation

```python
>>> ad.ui.freeze_rotation()  # freeze rotation
True

>>> ad.ui.freeze_rotation(False)  # un-freeze rotation
True
```

### Dump Window Hierarchy

```python
# Dumps to string.
>>> ad.ui.dump()
'...'

# Dumps with layout hierarchy compression.
>>> ad.ui.dump(compressed=True)
'...'

# Dumps without organizing the xml format beautifully
>>> ad.ui.dump(pretty=False)
'...'

# Dumps to the file saved in the log path of the Mobly Android controller.
>>> ad.ui.dump(file=True)
```

### Open Notification/Quick Settings

```python
>>> ad.ui.open.notification()
True

>>> ad.ui.open.quick_settings()
True
```

### Wait

#### Until Idle

Wait for current window to idle.

```python
>>> wait_time = datetime.timedelta(seconds=10)
>>> ad.ui.wait.idle(timeout=wait_time)
True
```

#### Until Window Update

Wait until an update event of any window occurs.

```python
>>> ad.ui.wait.update(timeout=wait_time)
True
```

#### Until Specific Window Occurs

Wait until an update event of specific window occurs.

```python
>>> package_name = 'com.android.launcher'
>>> ad.ui.wait.update(package=package_name, timeout=wait_time)
True
```

### Search

Search all objects

```python
# Returns a list of matched objects.
>>> ad.ui.find(text='Example')
[...]

# Returns True if there is a matched object.
>>> ad.ui.has(text='Example')
True
```
