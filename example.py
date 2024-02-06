import typing as t
from brutalpywebui import BrutalPyWebUI


example_html = """
<input id="inp_regular_txt" value="Updated value" />
<button onclick="_wuiEvent('btn_press', _wuiVal('#inp_regular_txt'))">{{ button_text }}</button>
<div>Result: <span id="txt_result">Old value</span></div>
<div>Ticker: <span id="txt_ticker">{{ ticker_text }}</span></div>
"""

example_css = """
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
"""

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
