
## Intro
BrutalPyWebUI is a brutalist async Python framework for building
utilitarian desktop applications that require a tried-and-true
web-based cross-platform interface with realtime capabilities and no hassle.

## Simple and focused
BrutalPyWebUI exposes a basic web interface bound to a host and port of
your choice, and provides you a selection of very basic utility
functions to update the DOM on the frontend from your Python backend,
as well as a few global javascript functions for quickly
grabbing data from the interface on the frontend and sending
it to the backend.

## Light on dependencies
BrutalPyWebUI depends only on:
- [hypercorn (the ASGI server)](https://github.com/pgjones/hypercorn),
- [Quart (a Flask replacement for asyncio)](https://github.com/pallets/quart)

## Light on assets
BrutalPyWebUI bundles only:
- [a default favicon (the Pyton logo)](https://www.favicon.cc/?action=icon&file_id=831343)
- [a default font (JetBrains Mono Regular)](https://github.com/JetBrains/JetBrainsMono)
- [a default css reset (Normalize.css)](https://github.com/necolas/normalize.css)

Note that you can disable all three separately.

## Flexible UI design
There are three main approaches in regards to actually
building the user interface:

### Utilitarian
Write most of your logic in Python and use the UI
as a barebones interface that sends events by calling
the special global `_wuiEvent()` function from a script
or an onclick attribute, etc., and gets updated
on-demand, from your Python code, by calling any
of the `wui.el_*()` or `wui.pg_*()` utility functions.

### Embrace Modernity
Use Python-land as more of a complementary backend and
inject heavier javascript and css that can contain
anything from logic and styling for basic web components
to the bundled code of a full-fledged React app. Note that
any js you inject using `base_js` in the constructor
is injected after the definitions for the global `_wui*()` functions
so they will not be overriden and you can call them normally
from within your app. You could also just use `asset_handler`
to serve your scripts along with other files.

### Anything in the middle / anything you can think of
Self-explanatory.

The idea is to give the developer a sturdy platform to
build upon, expanding freely as needed, without
highly specific enforced patterns.


## Installation
```bash
pip install brutalpywebui
```

## Basic usage
```python
import typing as t
from brutalpywebui import BrutalPyWebUI


example_html = '''
<input id="inp_regular_txt" value="Updated value" />
<button onclick="_wuiEvent('btn_press', _wuiVal('#inp_regular_txt'))">{{ button_text }}</button>
<div>Result: <span id="txt_result">Old value</span></div>
<div>Ticker: <span id="txt_ticker">{{ ticker_text }}</span></div>
'''

example_css = '''
body {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 20px;
}

body > * {
    width: 100%;
    height: 24px;
    max-width: 300px;
    margin-bottom: 10px;
    padding: 0;
    border: none;
    outline: none;
    box-sizing: border-box;
}

body > input {
    border: 1px solid black;
    padding: 0 3px;
}
'''

wui: BrutalPyWebUI | None = None

ticker = 0


async def on_background():
    global ticker

    ticker += 1
    await wui.el_set_text(["#txt_ticker"], str(ticker))


async def on_event(event: str, data: t.Any):
    match event:
        case "btn_press":
            await wui.el_set_text(["#txt_result"], data)

        case _:
            pass


async def on_init():
    # this uses Jinja2 templates
    await wui.el_set_html_templ(
        ["body"],
        example_html,
        button_text="Press me!",
        ticker_text=str(ticker),
    )


wui = BrutalPyWebUI(
    page_title="MyApp",
    init_handler=on_init,
    event_handler=on_event,
    background_handler=on_background,
    background_interval=5.2,  # seconds
    base_css=example_css,
)

# these are the default host and port
# specified here for the sake of the example
wui.run(host="localhost", port=7865)

```

## Technical note
The run() method uses asyncio.run() and is meant
to be run on the main thread. The app will not be
served until run() is called.

## Python reference


### `__init__`


```python
async def on_init():
    pass

async def on_event(name: str, data: t.Any):
    pass

async def on_asset(asset_name: str):
    # served at yourhost:port/assets/<asset_name>
    asset_bytes, content_type = mock_read_asset(asset_name)
    return asset_bytes, content_type

wui = BrutalPyWebUI(
    page_title="MyApp",
    init_handler=on_init,
    event_handler=on_event,
    asset_handler=on_asset,
    background_handler=on_background,
    background_interval=5.2,  # seconds
    base_css=lambda: mock_read_asset("bundle.css")  # or pass str directly,
    base_js=lambda: mock_read_asset("bundle.js")  # or pass str directly,
    inject_python_favicon=True,
    inject_jetbrains_font=True,
    inject_normalize_css=True,
    page_websocket_use_tls=False,
    page_lang=lambda: "en",  # or pass str directly,
    page_encoding=lambda: "UTF-8",  # or pass str directly,
    page_viewport=lambda: "width=device-width, initial-scale=1.0", # or pass str directly,
    debug=False,  # print debug logs where applicable
)
```

- `page_title(str|()->str)` -- title of the page.
- `init_handler(async()->None)` -- coroutine to run on init.
- `event_handler(async(str,Any)->None)` -- coroutine to handle your custom events
from the frontend.
- `asset_handler(async(str)->(asset_content(Any), content_type(str)))` -- coroutine
to handle serving your custom assets for the frontend.
- `background_handler(async()->None)` -- coroutine called periodically in the background
controlled by the background_interval arg.
- `background_interval(float)` -- how often (in seconds with subsecond precision)
to call the background_handler.
- `base_css(str|()->str)` -- css string to inject in the main css file
for the frontend.
- `base_js(str|()->str)` -- js string to inject into the main js file
for the frontend.
- `inject_python_favicon(bool)` -- whether to use a default favicon.
- `inject_jetbrains_font(bool)` -- whether to use the JetBrains Mono Regular font.
- `inject_normalize_css(bool)` -- whether to inject NormalizeCSS into the main css file
for the frontend.
- `page_websocket_use_tls(bool)` -- whether to use wss instead of ws for the websocket
connection on the frontend.
- `page_lang(str)` -- the lang attribute for the html tag.
- `page_encoding(str)` -- the encoding of the page, normally you should not change this.
- `page_viewport(str)` -- the value for the viewport meta tag, normally you should not
change this unless having responsive issues with CSS.
- `debug(bool)` -- whether to print debug logs where applicable.


### `el_append_text`


Append text to the current el.innerText of one or more targets.
Affects all connected instances.

```python
await wui.el_set_text(['#my_element'], 'Hello')
await wui.el_append_text(['#my_element'], ' there')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `content(str)` -- a string containing any text.


### `el_append_value`


Append text to the current el.value of one or more targets.
Affects all connected instances.

```python
await wui.el_set_value(['#my_input'], 'Hello')
await wui.el_append_value(['#my_input'], ' there')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `content(str)` -- a string containing any text.


### `el_class_add`


Add a class to el.classList on one or more targets.
Affects all connected instances.

```python
await wui.el_class_add(['#my_element'], 'my_custom_class')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `name(str)` -- name of the class.


### `el_class_remove`


Remove a class from el.classList on one or more targets.
Affects all connected instances.

```python
await wui.el_class_remove(['#my_element'], 'my_custom_class')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `name(str)` -- name of the class.


### `el_disable`


Disable an element using el.disabled.
Affects all connected instances.

```python
await wui.el_disable(['#some_input', '#some_button'])
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.


### `el_enable`


Enable an element disabled using el.disabled.
Affects all connected instances.

```python
await wui.el_enable(['#some_input', '#some_button'])
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.


### `el_set_attribute`


Use el.setAttribute on one or more targets.
Affects all connected instances.

```python
await wui.el_set_attribute(['#my_element'], 'data-something', 'the value')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `name(str)` -- name of the attribute.
- `content(str)` -- value of the attribute.


### `el_set_html_templ`


Evaluate a Jinja2 template string and set the el.innerHTML of one or more targets.
Affects all connected instances.

```python
await wui.el_set_html_templ(
    ['#my_element'],
    '<div>{{ content }}</div>',
    content='Stuff',
)
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `content(str)` -- a string containing a Jinja2 template.


### `el_set_html_unsafe`


Directly set the el.innerHTML of one or more targets.
Affects all connected instances.

```python
await wui.el_set_html_unsafe(['#my_element'], '<div>Stuff</div>')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `content(str)` -- a string containing html.


### `el_set_style`


Set a property on el.style on one or more targets.
Affects all connected instances.

```python
await wui.el_set_style(['#my_element'], 'backgroundColor', 'lightgray')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `name(str)` -- name of the style attribute (camelCase).
- `content(str)` -- value of the attribute.


### `el_set_text`


Directly set the el.innerText of one or more targets.
Affects all connected instances.

```python
await wui.el_set_text(['#my_element'], 'Hello there')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `content(str)` -- a string containing raw text.


### `el_set_value`


Set the el.value of one or more targets.
Affects all connected instances.

```python
await wui.el_set_value(['#my_input'], 'Hello')
```

- `selectors(list[str])` -- querySelectorAll selectors for targeting.
- `content(str)` -- a string containing any text.


### `pg_eval`


Eval a js string on the frontend.
Affects all connected instances.

```python
await wui.pg_eval('call_some_javascript()')
```

- `content(str)` -- the js string


### `pg_set_title`


Set the title of the page dynamically.
Affects all connected instances.

```python
await wui.pg_set_title('A New Title')
```

- `content(str)` -- the page title


### `run`


Run the BrutalPyWebUI app at host on port.

```python
await wui.run(host="localhost", port=7865)
```

- `host(str)` -- hostname.
- `port(int)` -- port number.


## JavaScript reference

### `_wuiEvent`

Send an event to your `event_handler` on the backend.

```javascript
_wuiEvent('my_event', ['some', 'data'])
```

- `name(string)` -- name of your event
- `data(any)` -- json-compatible object to send with your event

### `_wuiVal`

Returns `el.value` of an element.

```javascript
_wuiVal('#my_input')
```

- `selector(string)` -- querySelector selector

### `_wuiChecked`

Returns `el.checked` of an element.

```javascript
_wuiChecked('#my_input')
```

- `selector(string)` -- querySelector selector

### `_wuiSelected`

Returns `el.selected` of an element.

```javascript
_wuiSelected('#my_input')
```

- `selector(string)` -- querySelector selector
