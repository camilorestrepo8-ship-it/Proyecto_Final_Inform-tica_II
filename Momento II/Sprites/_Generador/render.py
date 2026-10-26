"""Renderiza SVG/HTML a PNG con Chromium headless (Playwright)."""
from playwright.sync_api import sync_playwright

_pw = None
_browser = None


def _page():
    global _pw, _browser
    if _browser is None:
        _pw = sync_playwright().start()
        _browser = _pw.chromium.launch()
    return _browser.new_page()


def render_svg(svg: str, out_png: str, w: int, h: int, scale: float = 1.0):
    pg = _page()
    pg.set_viewport_size({"width": w, "height": h})
    html = ("<html><head><style>html,body{margin:0;padding:0;background:transparent;}"
            "svg{display:block}</style></head><body>" + svg + "</body></html>")
    pg.set_content(html)
    pg.screenshot(path=out_png, omit_background=True, clip={"x": 0, "y": 0, "width": w, "height": h})
    pg.close()


def render_html(html: str, out_png: str, w: int, h: int, transparent=False):
    pg = _page()
    pg.set_viewport_size({"width": w, "height": h})
    pg.set_content(html)
    pg.wait_for_timeout(150)
    pg.screenshot(path=out_png, omit_background=transparent, full_page=True)
    pg.close()


def render_element(html: str, out_png: str, selector=".wrap", w=1700, h=600, transparent=False):
    pg = _page()
    pg.set_viewport_size({"width": w, "height": h})
    pg.set_content(html)
    pg.wait_for_timeout(150)
    pg.locator(selector).screenshot(path=out_png, omit_background=transparent)
    pg.close()


def close():
    global _pw, _browser
    if _browser:
        _browser.close()
        _pw.stop()
        _browser = None
