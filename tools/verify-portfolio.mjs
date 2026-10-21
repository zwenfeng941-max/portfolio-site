import playwright from "/Users/zhengwenfeng/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js";

const { chromium } = playwright;
const root = "file:///Users/zhengwenfeng/Desktop/%E5%B8%8C%E6%9C%9B%E6%88%91%E9%A1%BA%E9%A1%BA%E5%88%A9%E5%88%A9/portfolio-site";
const browser = await chromium.launch({
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
});

const pages = ["index", "capability-planning", "capability-operations", "capability-visual", "project-dossiers"];
const viewports = [
  { name: "desktop", width: 1440, height: 960, isMobile: false },
  { name: "mobile", width: 390, height: 844, isMobile: true },
];

for (const file of pages) {
  for (const viewport of viewports) {
    const page = await browser.newPage({
      viewport: { width: viewport.width, height: viewport.height },
      isMobile: viewport.isMobile,
      hasTouch: viewport.isMobile,
    });
    const errors = [];
    page.on("console", (message) => {
      if (message.type() === "error") errors.push(message.text());
    });
    await page.goto(`${root}/${file}.html`, { waitUntil: "networkidle" });
    await page.waitForTimeout(250);
    await page.evaluate(async () => {
      const height = document.documentElement.scrollHeight;
      for (let top = 0; top < height; top += 700) {
        window.scrollTo(0, top);
        await new Promise((resolve) => setTimeout(resolve, 25));
      }
      window.scrollTo(0, 0);
      document.querySelectorAll("img[loading='lazy']").forEach((image) => {
        image.loading = "eager";
      });
      await Promise.all(
        [...document.images].map((image) => image.decode().catch(() => undefined))
      );
    });
    await page.waitForTimeout(350);

    const report = await page.evaluate(() => {
      const ids = new Set([...document.querySelectorAll("[id]")].map((node) => node.id));
      const missingAnchors = [...document.querySelectorAll('a[href^="#"]')]
        .map((link) => link.getAttribute("href"))
        .filter((href) => href.length > 1 && !ids.has(href.slice(1)));
      const brokenImages = [...document.images]
        .filter((image) => !image.complete || image.naturalWidth === 0)
        .map((image) => image.getAttribute("src"));
      const overflowElements = [...document.querySelectorAll("body *")]
        .filter((node) => {
          const rect = node.getBoundingClientRect();
          return rect.width > 0 && rect.right > document.documentElement.clientWidth + 1;
        })
        .slice(0, 12)
        .map((node) => ({
          tag: node.tagName.toLowerCase(),
          className: node.className || "",
          right: Math.round(node.getBoundingClientRect().right),
        }));
      return {
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        missingAnchors,
        brokenImages,
        overflowElements,
      };
    });

    await page.screenshot({
      path: `/private/tmp/portfolio-${file}-${viewport.name}-top.png`,
      fullPage: false,
    });
    if (file === "capability-planning") {
      await page.evaluate(() => {
        document.documentElement.style.scrollBehavior = "auto";
        const section = document.querySelector("#project-portfolio");
        const top = section.getBoundingClientRect().top + window.scrollY - 90;
        window.scrollTo(0, top);
      });
      await page.waitForTimeout(250);
      await page.screenshot({
        path: `/private/tmp/portfolio-${file}-${viewport.name}-projects.png`,
        fullPage: false,
      });
      const closedCount = await page.locator(".project-accordion:not([open])").count();
      await page.locator("#yangcheng > summary").click();
      await page.waitForTimeout(250);
      const firstOpenCount = await page.locator(".project-accordion[open]").count();
      await page.locator("#hahean-generation > summary").click();
      await page.waitForTimeout(250);
      const singleOpen = await page.evaluate(() => ({
        openCount: document.querySelectorAll(".project-accordion[open]").length,
        firstOpen: document.querySelector("#yangcheng").open,
        secondOpen: document.querySelector("#hahean-generation").open,
      }));
      console.log("accordion", JSON.stringify({ closedCount, firstOpenCount, ...singleOpen }));
      await page.locator("#summit > summary").click();
      await page.waitForTimeout(250);
      await page.evaluate(() => {
        document.documentElement.style.scrollBehavior = "auto";
        const section = document.querySelector("#summit");
        const top = section.getBoundingClientRect().top + window.scrollY - 90;
        window.scrollTo(0, top);
      });
      await page.waitForTimeout(250);
      await page.screenshot({
        path: `/private/tmp/portfolio-${file}-${viewport.name}-summit.png`,
        fullPage: false,
      });
      await page.evaluate(() => {
        document.documentElement.style.scrollBehavior = "auto";
        const section = document.querySelector("#calcium-plan");
        const top = section.getBoundingClientRect().top + window.scrollY - 90;
        window.scrollTo(0, top);
      });
      await page.waitForTimeout(250);
      await page.screenshot({
        path: `/private/tmp/portfolio-${file}-${viewport.name}-calcium.png`,
        fullPage: false,
      });
    }
    const sectionIds = {
      "capability-operations": ["account-report"],
      "capability-visual": ["video-works", "on-site-shooting"],
    }[file] || [];
    for (const sectionId of sectionIds) {
      await page.evaluate((id) => {
        document.documentElement.style.scrollBehavior = "auto";
        const section = document.querySelector(`#${id}`);
        const top = section.getBoundingClientRect().top + window.scrollY - 90;
        window.scrollTo(0, top);
      }, sectionId);
      await page.waitForTimeout(250);
      await page.screenshot({
        path: `/private/tmp/portfolio-${file}-${viewport.name}-${sectionId}.png`,
        fullPage: false,
      });
    }
    console.log(file, JSON.stringify({ ...viewport, ...report, consoleErrors: errors }));
    await page.close();
  }
}

await browser.close();
