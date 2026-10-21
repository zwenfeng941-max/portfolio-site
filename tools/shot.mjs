import playwright from "/Users/zhengwenfeng/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js";

const { chromium } = playwright;

const root = "file:///Users/zhengwenfeng/Desktop/%E5%B8%8C%E6%9C%9B%E6%88%91%E9%A1%BA%E9%A1%BA%E5%88%A9%E5%88%A9/portfolio-site";
const browser = await chromium.launch({
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
});

async function capture(url, out, viewport, mobile = false, openDetails = false) {
  const page = await browser.newPage({
    viewport,
    deviceScaleFactor: 1,
    isMobile: mobile,
    hasTouch: mobile,
  });
  await page.goto(url, { waitUntil: "networkidle" });
  if (openDetails) {
    await page.evaluate(() => document.querySelectorAll("details").forEach((d) => (d.open = true)));
  }
  const height = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < height; y += viewport.height * 0.8) {
    await page.evaluate((top) => window.scrollTo(0, top), y);
    await page.waitForTimeout(120);
  }
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
  await page.screenshot({ path: out, fullPage: true });
  console.log(out, viewport.width, "x", height);
  await page.close();
}

const pages = [
  ["index", "home"],
  ["about", "about"],
  ["capability-planning", "planning"],
  ["capability-operations", "operations"],
  ["capability-visual", "visual"],
  ["skills", "skills"],
  ["work-hahean", "case"],
  ["work-maofengwan", "mf"],
  ["work-jincheng", "jc"],
  ["work-summit", "summit"],
  ["work-calcium", "calcium"],
];

for (const [file, name] of pages) {
  await capture(`${root}/${file}.html`, `/private/tmp/v2-${name}-desk.png`, { width: 1440, height: 960 });
}
for (const [file, name] of [["index", "home"], ["about", "about"], ["capability-operations", "operations"], ["capability-visual", "visual"], ["work-summit", "summit"], ["work-calcium", "calcium"]]) {
  await capture(`${root}/${file}.html`, `/private/tmp/v2-${name}-mob.png`, { width: 390, height: 844 }, true);
}
await capture(`${root}/index.html`, "/private/tmp/v2-home-open.png", { width: 1440, height: 960 }, false, true);

const check = await browser.newPage({ viewport: { width: 1440, height: 960 } });
const errors = [];
check.on("console", (msg) => {
  if (msg.type() === "error") errors.push(msg.text());
});
await check.goto(`${root}/index.html`, { waitUntil: "networkidle" });
await check.click('a[href="#abilities"]');
await check.waitForTimeout(400);
console.log("abilities open:", await check.evaluate(() => document.querySelector("#abilities").open));
await check.goto(`${root}/about.html`, { waitUntil: "networkidle" });
await check.click(".life-carousel__nav--next");
console.log("life carousel:", await check.textContent(".life-carousel__counter"));
await check.goto(`${root}/work-calcium.html`, { waitUntil: "networkidle" });
await check.click(".deck-viewer__nav--next");
console.log("calcium deck:", await check.textContent(".deck-viewer__counter"));
console.log("calcium thumbnails:", await check.locator(".deck-thumb").count());
console.log("console errors:", errors.length ? errors : "none");
await check.close();

await browser.close();
