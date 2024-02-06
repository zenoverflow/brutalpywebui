ENCODED_SCRIPT = """
(function () {
    var DEBUG = false;

    var ws = new WebSocket("ws://" + window.location.host + "/wui");

    ws.onmessage = function (event) {
        var payload;
        var ev;

        try {
            payload = JSON.parse(event.data);
            ev = payload.event;
        } catch (error) {
            try {
                if (DEBUG) {
                    console.error("PARSE ERROR:" + error);
                }
            } catch (error) {}
            return;
        }

        if (!payload || !ev) {
            try {
                if (DEBUG) {
                    console.log("Invalid payload: " + payload);
                }
            } catch (error) {}
            return;
        }

        if (DEBUG) {
            console.log(payload);
        }

        if (ev.startsWith("pg_")) {
            switch (ev) {
                case "pg_set_title":
                    document.title = payload.data;
                    break;

                case "pg_eval":
                    eval(payload.data);
                    break;

                default:
                    break;
            }
            return;
        }

        try {
            for (var selector of Object.keys(payload.data)) {
                var rels = Array.from(document.querySelectorAll(selector));
                var data = payload.data[selector];
                for (var rel of rels) {
                    try {
                        // /** @type {HTMLElement} **/
                        // const _dummy = null;
                        switch (ev) {
                            case "el_html":
                                rel.innerHTML = data;
                                break;

                            case "el_text":
                                rel.innerText = data;
                                break;

                            case "el_text_append":
                                rel.innerText = rel.innerText + (data || "");
                                break;

                            case "el_value":
                                rel.value = data;
                                break;

                            case "el_value_append":
                                rel.value = rel.value + (data || "");
                                break;

                            case "el_set_attr":
                                rel.setAttribute(data[0], data[1]);
                                break;

                            case "el_set_style":
                                rel.style[data[0]] = data[1];
                                break;

                            case "el_class_add":
                                rel.classList.add(data);
                                break;

                            case "el_class_remove":
                                rel.classList.remove(data);
                                break;

                            case "el_enable":
                            case "el_disable":
                                rel.disabled = ev !== "el_enable";
                                break;

                            default:
                                break;
                        }
                    } catch (error) {
                        if (DEBUG) {
                            console.error(error);
                        }
                    }
                }
            }
        } catch (error) {
            if (DEBUG) {
                console.error(error);
            }
        }
    };
    ws.onopen = function () {
        if (DEBUG) {
            console.log("conn open");
        }
    };
    ws.onclose = function () {
        if (DEBUG) {
            console.log("conn close");
        }
    };
    ws.onerror = function () {
        if (DEBUG) {
            console.error("conn error");
        }
    };

    window._wuiVal = function (selector) {
        try {
            return document.querySelector(selector).value || "";
        } catch (error) {
            return "";
        }
    };

    window._wuiChecked = function (selector) {
        try {
            return document.querySelector(selector).checked || false;
        } catch (error) {
            return false;
        }
    };

    window._wuiSelected = function (selector) {
        try {
            return document.querySelector(selector).selected || false;
        } catch (error) {
            return false;
        }
    };

    window._wuiEvent = function (ev, args) {
        try {
            ws.send(JSON.stringify({ event: ev, data: args }));
        } catch (error) {
            if (DEBUG) {
                console.error(error);
            }
        }
    };
})();

""".lstrip()
