from playwright.sync_api import sync_playwright
import time

B = "http://localhost:5000"

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)

    # 1. Landing hero
    pg.goto(B, wait_until="networkidle")
    time.sleep(3)
    pg.screenshot(path="shots/01_hero.png")

    # 2. Features section
    pg.evaluate("document.getElementById('features').scrollIntoView()")
    time.sleep(1.5)
    pg.screenshot(path="shots/02_features.png")

    # 3. Pricing
    pg.evaluate("document.getElementById('pricing').scrollIntoView()")
    time.sleep(1.5)
    pg.screenshot(path="shots/03_pricing.png")

    # 4. Chat widget open with an answer
    pg.evaluate("window.scrollTo(0,0)")
    time.sleep(0.5)
    pg.click("#widgetBtn")
    time.sleep(0.8)
    pg.fill("#widgetInput", "what is the price?")
    pg.press("#widgetInput", "Enter")
    time.sleep(2.5)
    pg.screenshot(path="shots/04_widget.png")

    # 5. Demo page: load sample, ask a known question
    pg.goto(B + "/demo.html", wait_until="networkidle")
    time.sleep(2)
    pg.click("#kbSample")
    time.sleep(1.5)
    pg.fill("#demoInput", "do you deliver to my home?")
    pg.press("#demoInput", "Enter")
    time.sleep(2.5)
    pg.screenshot(path="shots/05_demo_answer.png")

    # 6. Unknown question -> lead
    pg.fill("#demoInput", "do you sell laptops?")
    pg.press("#demoInput", "Enter")
    time.sleep(2.5)
    pg.screenshot(path="shots/06_demo_unknown.png")

    # 7. Leads table
    pg.evaluate("document.querySelector('.leads-table').scrollIntoView({block:'center'})")
    time.sleep(1.2)
    pg.screenshot(path="shots/07_leads.png")

    br.close()
print("screenshots done")
