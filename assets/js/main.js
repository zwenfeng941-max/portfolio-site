(() => {
  const nav = document.querySelector(".nav");
  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const menuBtn = document.querySelector(".nav__menu");
  const panel = document.querySelector(".menu-panel");
  if (menuBtn && panel) {
    const close = () => {
      panel.classList.remove("is-open");
      document.body.classList.remove("no-scroll");
      menuBtn.setAttribute("aria-expanded", "false");
    };
    menuBtn.addEventListener("click", () => {
      const open = panel.classList.toggle("is-open");
      document.body.classList.toggle("no-scroll", open);
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    panel.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
  }

  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  const yearEls = document.querySelectorAll("[data-year]");
  yearEls.forEach((el) => (el.textContent = new Date().getFullYear()));

  const projectAccordions = [...document.querySelectorAll(".project-accordion")];
  projectAccordions.forEach((item) => {
    item.querySelector("summary")?.addEventListener("click", () => {
      if (item.open) return;
      projectAccordions.forEach((other) => {
        if (other !== item) other.open = false;
      });
    });
    item.addEventListener("toggle", () => {
      if (!item.open) return;
      projectAccordions.forEach((other) => {
        if (other !== item) other.open = false;
      });
    });
  });

  document.querySelectorAll('[data-carousel="life"]').forEach((root) => {
    const slides = [...root.querySelectorAll(".life-slide")];
    const dots = [...root.querySelectorAll(".life-carousel__dots button")];
    const prev = root.querySelector(".life-carousel__nav--prev");
    const next = root.querySelector(".life-carousel__nav--next");
    const counter = root.querySelector(".life-carousel__counter");
    const caption = root.querySelector(".life-carousel__caption");
    const captions = ["日常 · 海边", "创作 · 花与镜头", "工作 · 峰会现场", "幕后 · 拍摄进行时", "日常 · 看展"];
    let index = 0;
    let startX = null;

    const show = (nextIndex) => {
      index = (nextIndex + slides.length) % slides.length;
      slides.forEach((slide, i) => {
        const active = i === index;
        slide.classList.toggle("is-active", active);
        slide.setAttribute("aria-hidden", String(!active));
      });
      dots.forEach((dot, i) => {
        dot.classList.toggle("is-active", i === index);
        if (i === index) dot.setAttribute("aria-current", "true");
        else dot.removeAttribute("aria-current");
      });
      counter.textContent = `${String(index + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
      caption.textContent = captions[index];
    };

    prev.addEventListener("click", () => show(index - 1));
    next.addEventListener("click", () => show(index + 1));
    dots.forEach((dot, i) => dot.addEventListener("click", () => show(i)));

    root.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        show(index - 1);
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        show(index + 1);
      }
    });

    root.addEventListener("pointerdown", (event) => {
      startX = event.clientX;
    });
    root.addEventListener("pointerup", (event) => {
      if (startX === null) return;
      const delta = event.clientX - startX;
      startX = null;
      if (Math.abs(delta) < 42) return;
      show(index + (delta < 0 ? 1 : -1));
    });
    root.addEventListener("pointercancel", () => {
      startX = null;
    });
  });

  const operationGroups = {
    "ip-wechat": { prefix: "ip-wechat", count: 5, label: "熊晓杰说文旅 · 视频号", sub: "账号主页与内容页" },
    bilibili: { prefix: "bilibili", count: 2, label: "熊晓杰说文旅 · B 站", sub: "主页与合集" },
    "xhs-ip": { prefix: "xhs-ip", count: 4, label: "熊晓杰说文旅 · 小红书", sub: "栏目与内容页" },
    "xhs-editor": {
      prefix: "xhs-editor",
      count: 7,
      order: [5, 6, 7, 1, 2, 3, 4],
      label: "时代文旅编辑部 · 小红书",
      sub: "账号搭建与内容页",
    },
    "dsd-wechat": { prefix: "dsd-wechat", count: 9, label: "大时代文旅 · 视频号", sub: "主页与内容矩阵" },
    xiaoyuzhou: { prefix: "xiaoyuzhou", count: 6, label: "熊晓杰说文旅 · 小宇宙", sub: "节目与内容页" },
    plan: { prefix: "dsd-plan", count: 18, label: "大时代文旅 · 视频号对标", sub: "账号内容与栏目参考" },
  };

  document.querySelectorAll("[data-scroller]").forEach((root) => {
    const track = root.querySelector(".ops-scroller__track");
    const prev = root.querySelector(".ops-scroller__prev");
    const next = root.querySelector(".ops-scroller__next");
    const counter = root.querySelector(".ops-scroller__counter");
    const caption = root.querySelector(".ops-scroller__caption");
    const group = operationGroups[root.dataset.scroller];
    const groups = group ? [group] : [];
    if (!track || !counter || !caption) return;

    const slides = [];
    groups.forEach((group) => {
      const sequence = group.order || Array.from({ length: group.count }, (_, index) => index + 1);
      sequence.forEach((index, position) => {
        const number = String(index).padStart(2, "0");
        const src = `assets/img/${group.folder || "ops"}/${group.prefix}-${number}.jpg`;
        const figure = document.createElement("figure");
        figure.className = "ops-scroller__slide";
        figure.innerHTML = `
          <div class="ops-scroller__media">
            <img src="${src}" alt="${group.label}${group.sub}截图 ${position + 1}" loading="${position === 0 ? "eager" : "lazy"}" decoding="async">
          </div>
          <figcaption class="ops-scroller__label">
            <strong>${group.label}</strong>
            <span>${group.sub}</span>
          </figcaption>
        `;
        const meta = { group, figure };
        figure.__opsMeta = meta;
        track.append(figure);
        slides.push(figure);
      });
    });

    const pad = (value) => String(value).padStart(2, "0");
    const scrollToSlide = (index, behavior = "smooth") => {
      const target = slides[Math.max(0, Math.min(index, slides.length - 1))];
      if (!target) return;
      track.scrollTo({ left: target.offsetLeft - track.offsetLeft, behavior });
    };

    let raf = 0;
    const update = () => {
      raf = 0;
      const center = track.scrollLeft + track.clientWidth / 2;
      let active = 0;
      let best = Infinity;
      slides.forEach((slide, index) => {
        const slideCenter = slide.offsetLeft - track.offsetLeft + slide.offsetWidth / 2;
        const distance = Math.abs(slideCenter - center);
        if (distance < best) {
          best = distance;
          active = index;
        }
      });
      slides.forEach((slide, index) => slide.classList.toggle("is-active", index === active));
      counter.textContent = `${pad(active + 1)} / ${pad(slides.length)}`;
      caption.textContent = `${slides[active].__opsMeta.group.label} · ${slides[active].__opsMeta.group.sub}`;
    };

    track.addEventListener("scroll", () => {
      if (raf) return;
      raf = requestAnimationFrame(update);
    }, { passive: true });
    prev?.addEventListener("click", () => {
      const active = slides.findIndex((slide) => slide.classList.contains("is-active"));
      scrollToSlide(active - 1);
    });
    next?.addEventListener("click", () => {
      const active = slides.findIndex((slide) => slide.classList.contains("is-active"));
      scrollToSlide(active + 1);
    });
    root.addEventListener("keydown", (event) => {
      const active = slides.findIndex((slide) => slide.classList.contains("is-active"));
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        scrollToSlide(active - 1);
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        scrollToSlide(active + 1);
      }
    });

    let startX = null;
    let startScroll = 0;
    track.addEventListener("pointerdown", (event) => {
      if (event.pointerType !== "mouse") return;
      startX = event.clientX;
      startScroll = track.scrollLeft;
      track.style.scrollSnapType = "none";
      track.classList.add("is-dragging");
      track.setPointerCapture(event.pointerId);
    });
    track.addEventListener("pointermove", (event) => {
      if (startX === null) return;
      track.scrollLeft = startScroll - (event.clientX - startX);
    });
    const endDrag = () => {
      if (startX === null) return;
      startX = null;
      track.style.scrollSnapType = "";
      track.classList.remove("is-dragging");
      update();
    };
    track.addEventListener("pointerup", endDrag);
    track.addEventListener("pointercancel", endDrag);

    update();
  });

  const deckConfigs = {
    calcium: {
      total: 28,
      source: (page) => `assets/img/calcium/slide-${String(page).padStart(2, "0")}.jpg`,
      alt: (page) => `钙世英雄甜伴三十策划案第 ${page} 页`,
      label: "查看策划案",
    },
    cattery: {
      total: 31,
      source: (page) => `assets/img/cattery/slide-${String(page).padStart(2, "0")}.jpg`,
      alt: (page) => `潮猫舍社交媒体矩阵运营汇报第 ${page} 页`,
      label: "查看运营汇报",
    },
  };

  document.querySelectorAll("[data-deck]").forEach((root) => {
    const config = deckConfigs[root.dataset.deck];
    if (!config) return;
    const total = config.total;
    const image = root.querySelector(".deck-viewer__stage img");
    const counter = root.querySelector(".deck-viewer__counter");
    const prev = root.querySelector(".deck-viewer__nav--prev");
    const next = root.querySelector(".deck-viewer__nav--next");
    const grid = document.querySelector("[data-deck-grid]");
    if (!image || !counter || !grid) return;

    const source = config.source;
    const buttons = [];
    for (let page = 1; page <= total; page += 1) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "deck-thumb";
      button.setAttribute("aria-label", `${config.label}第 ${page} 页`);
      button.innerHTML = `<img src="${source(page)}" alt="" loading="lazy"><span>${String(page).padStart(2, "0")}</span>`;
      grid.append(button);
      buttons.push(button);
    }

    let index = 0;
    let startX = null;
    const show = (nextIndex) => {
      index = (nextIndex + total) % total;
      const page = index + 1;
      image.src = source(page);
      image.alt = config.alt(page);
      counter.textContent = `${String(page).padStart(2, "0")} / ${total}`;
      buttons.forEach((button, i) => button.classList.toggle("is-active", i === index));
    };

    prev.addEventListener("click", () => show(index - 1));
    next.addEventListener("click", () => show(index + 1));
    buttons.forEach((button, i) => button.addEventListener("click", () => show(i)));
    root.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        show(index - 1);
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        show(index + 1);
      }
    });
    root.addEventListener("pointerdown", (event) => {
      startX = event.clientX;
    });
    root.addEventListener("pointerup", (event) => {
      if (startX === null) return;
      const delta = event.clientX - startX;
      startX = null;
      if (Math.abs(delta) < 48) return;
      show(index + (delta < 0 ? 1 : -1));
    });
    root.addEventListener("pointercancel", () => {
      startX = null;
    });
    show(0);
  });

  const openHashDetails = () => {
    if (!location.hash) return;
    const target = document.querySelector(location.hash);
    if (target && target.tagName === "DETAILS") target.open = true;
  };
  openHashDetails();
  window.addEventListener("hashchange", openHashDetails);
})();
