from playwright.sync_api import sync_playwright

BASE = "http://localhost:5000"
OUT = "img/"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1366, "height": 900}, device_scale_factor=2)

    # ---------------- HOME ----------------
    pg.goto(BASE + "/index.html")
    pg.wait_for_timeout(2500)

    pg.screenshot(path=OUT + "s01_hero.png", clip={"x": 0, "y": 0, "width": 1366, "height": 820})
    print("s01 hero")

    for sec, name in [("#features", "s02_features"), ("#how", "s03_how"),
                      ("#bots", "s04_bots"), ("#pricing", "s05_pricing")]:
        el = pg.query_selector(sec)
        el.scroll_into_view_if_needed()
        pg.wait_for_timeout(1200)
        el.screenshot(path=OUT + name + ".png")
        print(name)

    # stats strip
    el = pg.query_selector(".stats")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(1500)
    el.screenshot(path=OUT + "s06_stats.png")
    print("s06 stats")

    # FAQ with first item open
    el = pg.query_selector("#faq")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(800)
    btns = pg.query_selector_all("#faqList button")
    if btns:
        btns[0].click()
        pg.wait_for_timeout(700)
    el.screenshot(path=OUT + "s07_faq.png")
    print("s07 faq")

    # contact form validation errors
    el = pg.query_selector("#contact")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(600)
    pg.fill("#name", "A")
    pg.fill("#email", "wrong-email")
    pg.fill("#website", "ab")
    pg.fill("#message", "hi")
    pg.click("#contactForm button[type=submit]")
    pg.wait_for_timeout(700)
    el.screenshot(path=OUT + "s08_form_errors.png")
    print("s08 form errors")

    # contact form success
    pg.fill("#name", "Ishika Mittal")
    pg.fill("#email", "ishika@example.com")
    pg.fill("#website", "www.mystore.in")
    pg.fill("#message", "We want the chatbot on our store website. Please share the setup steps.")
    pg.click("#contactForm button[type=submit]")
    pg.wait_for_timeout(1500)
    el.screenshot(path=OUT + "s09_form_success.png")
    print("s09 form success")

    # chat widget
    pg.click("#widgetBtn")
    pg.wait_for_timeout(900)
    pg.fill("#widgetInput", "what is the price?")
    pg.click("#widgetForm button[type=submit]")
    pg.wait_for_timeout(2600)
    pg.screenshot(path=OUT + "s10_widget.png",
                  clip={"x": 820, "y": 150, "width": 546, "height": 740})
    print("s10 widget")

    # ---------------- DEMO ----------------
    pg.goto(BASE + "/demo.html")
    pg.wait_for_timeout(2000)
    pg.click("#kbSample")
    pg.wait_for_timeout(1500)
    pg.screenshot(path=OUT + "s11_kb.png", clip={"x": 0, "y": 0, "width": 1366, "height": 900})
    print("s11 kb")

    # teach one item manually
    pg.fill("#kbQ", "Do you give a warranty on products?")
    pg.fill("#kbA", "Yes, every product carries a one year warranty against manufacturing defects.")
    pg.click("#kbForm button[type=submit]")
    pg.wait_for_timeout(1200)
    el = pg.query_selector("#kbList")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(500)
    pg.screenshot(path=OUT + "s12_kb_added.png")
    print("s12 kb added")

    # ask a known question
    pg.fill("#demoInput", "do you deliver?")
    pg.click("#demoForm button[type=submit]")
    pg.wait_for_timeout(2600)
    pg.fill("#demoInput", "what is the return policy?")
    pg.click("#demoForm button[type=submit]")
    pg.wait_for_timeout(2600)
    el = pg.query_selector("#demoChat")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(600)
    pg.screenshot(path=OUT + "s13_chat_answer.png")
    print("s13 chat answer")

    # ask an unknown question -> lead
    pg.fill("#demoInput", "do you sell laptops?")
    pg.click("#demoForm button[type=submit]")
    pg.wait_for_timeout(2800)
    pg.screenshot(path=OUT + "s14_unknown.png")
    print("s14 unknown")

    el = pg.query_selector("#leadsBody")
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(700)
    pg.screenshot(path=OUT + "s15_leads.png")
    print("s15 leads")

    # ---------------- API / JSON ----------------
    pg.goto(BASE + "/api/health")
    pg.wait_for_timeout(600)
    pg.screenshot(path=OUT + "s16_health.png",
                  clip={"x": 0, "y": 0, "width": 1100, "height": 150})
    print("s16 health")

    pg.goto(BASE + "/api/leads")
    pg.wait_for_timeout(600)
    pg.screenshot(path=OUT + "s17_leads_json.png",
                  clip={"x": 0, "y": 0, "width": 1100, "height": 320})
    print("s17 leads json")

    # ---------------- MOBILE ----------------
    m = b.new_page(viewport={"width": 414, "height": 896}, device_scale_factor=2)
    m.goto(BASE + "/index.html")
    m.wait_for_timeout(2500)
    m.screenshot(path=OUT + "s18_mobile_hero.png")
    print("s18 mobile")
    m.query_selector("#features").scroll_into_view_if_needed()
    m.wait_for_timeout(1200)
    m.screenshot(path=OUT + "s19_mobile_features.png")
    print("s19 mobile features")

    b.close()
print("DONE")
