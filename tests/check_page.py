"""Run with Python + Playwright; captures report evidence while checking the page.

    python -m pip install playwright
    python -m playwright install chromium  # unnecessary with google-chrome-stable
    python tests/check_page.py
"""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from shutil import which
from threading import Thread

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "report" / "screenshots"


def first_row_count(items):
    boxes = items.evaluate_all("items => items.map(item => item.getBoundingClientRect().top)")
    assert boxes, "Missing grid items"
    return sum(abs(top - min(boxes)) < 2 for top in boxes)


def check(page, width):
    columns = 3 if width >= 1200 else 2 if width >= 768 else 1
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Overflow at {width}px"
    assert page.locator('a[href^="#"]').evaluate_all("links => links.every(link => document.getElementById(link.hash.slice(1)))"), "Broken section link"
    assert first_row_count(page.locator("#values .value-item")) == columns, f"Custom grid at {width}px"
    assert first_row_count(page.locator("#releases .release-card")) == columns, f"Bootstrap grid at {width}px"

    copy = page.locator(".hero-copy").bounding_box()
    art = page.locator(".hero-art").bounding_box()
    assert copy and art, "Missing hero columns"
    if width < 992:
        assert copy["y"] < art["y"], "Hero copy must come first on mobile/tablet"
    else:
        assert art["x"] < copy["x"], "Hero artwork must come first on desktop"
    assert page.locator(".desktop-note").is_visible() == (width >= 768)

    toggler = page.locator(".navbar-toggler")
    menu = page.locator("#site-nav")
    if width < 992:
        expect(toggler).to_be_visible()
        expect(menu).not_to_be_visible()
        toggler.focus()
        page.keyboard.press("Space")
        expect(toggler).to_have_attribute("aria-expanded", "true")
        expect(menu).to_be_visible()
        expect(page.locator(".collapsing")).to_have_count(0)
        if width == 375:
            page.locator("nav").screenshot(path=str(SCREENSHOTS / "navbar-open-375.png"))
        toggler.focus()
        page.keyboard.press("Enter")
        expect(toggler).to_have_attribute("aria-expanded", "false")
        expect(menu).not_to_be_visible()
    else:
        expect(toggler).not_to_be_visible()
        expect(menu).to_be_visible()

    button = page.locator("#questions .accordion-button").first
    panel = page.locator("#" + button.get_attribute("aria-controls"))
    initially_open = button.get_attribute("aria-expanded") == "true"
    if initially_open:
        button.focus()
        page.keyboard.press("Enter")
        expect(panel).not_to_be_visible()
    button.focus()
    page.keyboard.press("Space")
    expect(button).to_have_attribute("aria-expanded", "true")
    expect(panel).to_be_visible()
    expect(page.locator(".collapsing")).to_have_count(0)
    if width == 375:
        page.locator("#questions").screenshot(path=str(SCREENSHOTS / "accordion-open-375.png"))
    button.focus()
    page.keyboard.press("Enter")
    expect(button).to_have_attribute("aria-expanded", "false")
    expect(panel).not_to_be_visible()
    if initially_open:
        page.keyboard.press("Enter")
        expect(panel).to_be_visible()
        expect(page.locator(".collapsing")).to_have_count(0)
    button.evaluate("button => button.blur()")


def main():
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(executable_path=which("google-chrome-stable"))
                for width in (375, 768, 1280, 320, 1024, 1440):
                    page = browser.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
                    page.goto(f"http://127.0.0.1:{server.server_port}", wait_until="networkidle")
                    page.locator("img").evaluate_all("images => images.forEach(image => image.loading = 'eager')")
                    page.wait_for_function("[...document.images].every(image => image.complete && image.naturalWidth > 0)")
                    page.evaluate("document.fonts.ready")
                    check(page, width)
                    if width in (375, 768, 1280):
                        page.screenshot(path=str(SCREENSHOTS / f"page-{width}.png"), full_page=True)
                        for section in ("values", "releases"):
                            page.locator(f"#{section}").screenshot(path=str(SCREENSHOTS / f"{section}-{width}.png"))
                        if width != 768:
                            page.locator("#about").screenshot(path=str(SCREENSHOTS / f"about-{width}.png"))
                        if width == 375:
                            page.locator(".release-card").first.screenshot(path=str(SCREENSHOTS / "release-card-375.png"))
                    assert not errors, f"Browser errors at {width}px: {errors}"
                    print(f"PASS {width}px: layout, hero order, visibility, keyboard controls, images, console")
                    page.close()
                browser.close()
        finally:
            server.shutdown()


if __name__ == "__main__":
    main()
