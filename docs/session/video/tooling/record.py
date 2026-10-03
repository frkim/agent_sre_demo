"""Record demo scenes with Playwright (Edge). Usage: python record.py <scene> [<scene> ...]"""

import json
import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

HERE = Path(__file__).parent
CLIPS = HERE / "clips"
URL = "https://ca-trek-web-demo.proudocean-95776aec.francecentral.azurecontainerapps.io"
SIZE = {"width": 1920, "height": 1080}


def slow_type(page: Page, locator, text: str) -> None:
    locator.click()
    for ch in text:
        page.keyboard.type(ch)
        page.wait_for_timeout(110)


def storefront(page: Page) -> None:
    page.goto(URL)
    page.wait_for_timeout(5000)
    page.get_by_text("Price", exact=True).first.click()
    page.wait_for_timeout(2500)
    page.get_by_text("Price", exact=True).first.click()
    page.wait_for_timeout(2500)
    slow_type(page, page.get_by_role("textbox", name="Search products"), "tent")
    page.wait_for_timeout(3000)
    page.get_by_role("textbox", name="Search products").fill("")
    page.wait_for_timeout(2000)
    page.get_by_text("Aurora Ridge 2P Tent").first.click()
    page.wait_for_timeout(3500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1500)


def failure(page: Page) -> None:
    page.goto(URL)
    page.wait_for_timeout(4000)
    page.get_by_text("Axis Comfort Harness").first.click()
    page.wait_for_timeout(4500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)
    page.get_by_text("BelayPro Assist Device").first.click()
    page.wait_for_timeout(3000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(6000)


def outage(page: Page) -> None:
    page.goto(URL)
    page.wait_for_timeout(9000)


def recovered(page: Page) -> None:
    page.goto(URL)
    page.wait_for_timeout(5000)
    page.get_by_text("Aurora Ridge 2P Tent").first.click()
    page.wait_for_timeout(3000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(2000)


def scroll_page(page: Page, url: str, steps: int = 8, pause: int = 1400, first_wait: int = 3500) -> None:
    page.goto(url)
    page.wait_for_timeout(first_wait)
    for _ in range(steps):
        page.mouse.wheel(0, 420)
        page.wait_for_timeout(pause)
    page.wait_for_timeout(1500)


def github_issue(page: Page) -> None:
    scroll_page(page, "https://github.com/frkim/agent_sre_demo/issues/4", steps=10)


def github_pr(page: Page) -> None:
    scroll_page(page, "https://github.com/frkim/agent_sre_demo/pull/5/files", steps=6, first_wait=5000)


def actions(page: Page) -> None:
    page.goto("https://github.com/frkim/agent_sre_demo/actions/runs/37111646368")
    page.wait_for_timeout(6000)
    page.get_by_text("Deploy", exact=True).first.click()
    page.wait_for_timeout(5000)
    for _ in range(4):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(1500)
    page.wait_for_timeout(2000)


def html_scene(name: str):
    def _run(page: Page) -> None:
        file = HERE / "scenes" / f"{name}.html"
        page.goto(file.as_uri())
        meta = json.loads((HERE / "scenes" / f"{name}.json").read_text()) if (HERE / "scenes" / f"{name}.json").exists() else {}
        page.wait_for_timeout(meta.get("wait", 2500))
        for _ in range(meta.get("scroll_steps", 0)):
            page.mouse.wheel(0, meta.get("scroll_px", 300))
            page.wait_for_timeout(meta.get("scroll_pause", 1500))
        page.wait_for_timeout(meta.get("tail", 1500))
    return _run


SCENES = {
    "storefront": storefront,
    "failure": failure,
    "outage": outage,
    "recovered": recovered,
    "github_issue": github_issue,
    "github_pr": github_pr,
    "actions": actions,
}


def record(name: str) -> None:
    fn = SCENES.get(name) or html_scene(name)
    CLIPS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        ctx = browser.new_context(viewport=SIZE, record_video_dir=str(CLIPS / "_tmp"), record_video_size=SIZE,
                                  color_scheme="light", device_scale_factor=1)
        page = ctx.new_page()
        fn(page)
        video = page.video
        ctx.close()
        browser.close()
        target = CLIPS / f"{name}.webm"
        target.unlink(missing_ok=True)
        Path(video.path()).rename(target)
        print("recorded", target)


if __name__ == "__main__":
    for scene in sys.argv[1:]:
        record(scene)
