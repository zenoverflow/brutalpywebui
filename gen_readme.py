import sys

sys.dont_write_bytecode = True
import textwrap, re

from brutalpywebui import BrutalPyWebUI

result = textwrap.dedent(BrutalPyWebUI.__doc__)

result += f"""
## Python reference

"""

doc_sub = [
    l
    for l in dir(BrutalPyWebUI)
    if (l in ("__init__", "run") or l.startswith("pg_") or l.startswith("el_"))
]

for l in doc_sub:
    # name = re.sub(r"^_", "\_", l)
    result += f"\n### `{l}`\n\n"
    result += textwrap.dedent(getattr(BrutalPyWebUI, l).__doc__)
    result += "\n"

result += """
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
"""

with open("README.md", "w") as f:
    f.write(result)
