from playwright.sync_api import sync_playwright
import pathlib
ids = ["usecase","er","dfd0","dfd1","schema","arch","seq","flow","modes","sitemap"]
src = pathlib.Path("figs.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1300,"height":1100}, device_scale_factor=2)
    pg.goto(src)
    pg.wait_for_timeout(600)
    for i in ids:
        el = pg.query_selector("#"+i)
        el.screenshot(path=f"img/fig_{i}.png")
        print("ok", i)
    b.close()
