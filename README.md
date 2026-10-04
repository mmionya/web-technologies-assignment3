# Jamie Paige — Assignment 3

A responsive, fan-made listening guide built for **Miras Zhumazhan, IT-2512**. The page combines one section made with custom mobile-first media queries with Bootstrap 5.3.8 for the remaining sections.

## Open the page

From this folder, run:

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>. The website has no build step. Bootstrap loads from a CDN, so an internet connection is needed for its layout and interactions. Fonts use the system's installed typefaces, and album images are stored locally.

## What to submit

- `report/Assignment3_Miras_Zhumazhan.pdf` or the editable `.docx` with the same name.
- The [GitHub repository](https://github.com/mmionya/web-technologies-assignment3) containing the source files and local assets. Its URL is included inside both report formats.

The supplied report includes browser screenshots at 375, 768 and 1280 px, each task in order, a comparison table and a conclusion. Review its wording so you can explain it yourself. The assignment requires a live defense; the practice prompts below help you prepare.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Page sections, Bootstrap grid, navigation, cards and accordion |
| `style.css` | Colors, typography and the custom responsive section |
| `assets/` | Local album artwork and `CREDITS.md` with its sources |
| `tests/check_page.py` | Browser assertions and screenshot capture |
| `tools/build_report.py` | Produces PDF and editable Word reports from the screenshots |
| `report/screenshots/` | Original full-page and section screenshots |

## Read the code in this order

1. In the HTML `<head>`, find the viewport meta tag, the Bootstrap CSS link and then `style.css`. The viewport tag lets CSS use the phone's actual viewport width; loading custom CSS last lets equal-specificity custom rules override Bootstrap.
2. Follow the navigation's `href="#..."` links to matching section IDs. The menu toggler targets the collapsible navigation through `data-bs-target` and describes its state with `aria-expanded`.
3. Read `#about`. Bootstrap's container, row and columns make its two parts stack on narrow screens. Responsive `order-*` classes put the text first on mobile and the artwork first on desktop.
4. Read `#values`, then search for `.values-grid` in the CSS. This section has its own classes and no Bootstrap grid classes. Its base rule is one column; `@media (min-width: 768px)` gives two, and `@media (min-width: 1200px)` gives three. The queries also change typography or spacing.
5. Read `#releases`. Each Bootstrap column uses `col-12 col-md-6 col-xl-4`: 12/12 of a row on a phone, 6/12 on a tablet and 4/12 on a laptop. Its `.card` contains the local artwork, release information and an official listening link.
6. Read `#questions`. Each accordion button targets one answer panel. Bootstrap's JavaScript bundle updates the open state from the `data-bs-*` attributes; no custom JavaScript is needed.
7. Find a `d-none` utility to see which decorative text is hidden on phones. Check the matching breakpoint class to explain when it returns.

## Verify the page and regenerate the report

The website itself needs no Python packages. These packages are only for browser checks and report generation:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install playwright reportlab python-docx pillow
python -m playwright install chromium
python tests/check_page.py
python tools/build_report.py --repository 'https://github.com/mmionya/web-technologies-assignment3'
```

The browser check starts and stops its own local server. It uses installed Google Chrome if available, otherwise Playwright Chromium. It checks the requested 375, 768 and 1280 px widths plus 320, 1024 and 1440 px, and saves the report screenshots. Checks cover both grids, hero ordering, responsive visibility, keyboard operation of the menu and accordion, successful image loading, browser errors and horizontal overflow.

For this workspace, the prepared tools environment is `/tmp/assignment3-venv`. The same commands can be run as `/tmp/assignment3-venv/bin/python tests/check_page.py` and `/tmp/assignment3-venv/bin/python tools/build_report.py --repository 'https://github.com/mmionya/web-technologies-assignment3'`.

Run the browser check before rebuilding the report after a visual edit; otherwise the report will contain older screenshots. The generator accepts `--name` and `--group` if those details need correcting. The Word copy can also be edited directly.

## Defense practice

Open browser developer tools and use responsive device mode. Demonstrate 375, 768 and 1280 px, open and close the menu and FAQ with both mouse and keyboard, and show that the page has no horizontal scroll.

| Likely question | What to explain using this page |
| --- | --- |
| What does mobile-first mean? | The default `.values-grid` works on a phone. The two `min-width` queries add columns as space becomes available. |
| What happens exactly at 768 px? | The custom grid becomes two columns, and Bootstrap's `md` album columns become half the row. |
| Why do `col-md-6` and `col-xl-4` give two and three columns? | Bootstrap divides the row into 12 units. Two columns of 6 units or three columns of 4 units fill it. |
| Why use `order-*`? | It changes visual order at a chosen breakpoint without duplicating the introduction content. |
| Why is `style.css` loaded after Bootstrap? | Later rules can override earlier rules when their cascade priority and specificity are equal. |
| What makes the menu and accordion work? | The Bootstrap bundle reads the data attributes and updates collapse classes and expanded state. |
| When would you choose custom CSS? | For a small distinctive section, such as the reasons to listen, where direct control is useful. |
| When would you choose Bootstrap? | For repeated layouts and standard interactive components already supplied by the framework. |

Practise these changes, then undo them:

- Make the custom grid switch to two columns at 800 px. Test just below and at the new breakpoint.
- Change the album grid to two columns on desktop by using `col-xl-6` on each album column.
- Add a fourth reason to listen and explain why the last row has one item at the current desktop breakpoint.
- Change the hidden text's display breakpoint and demonstrate it on both sides of that width.
- Add one FAQ answer with a unique panel ID and matching `aria-controls` / `data-bs-target` values.

## Sources

Artwork and music sources are documented in [assets/CREDITS.md](assets/CREDITS.md). This is an unofficial educational fan page.

- [Bootstrap 5.3 introduction](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap grid](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Bootstrap navbar](https://getbootstrap.com/docs/5.3/components/navbar/)
- [Bootstrap accordion](https://getbootstrap.com/docs/5.3/components/accordion/)
