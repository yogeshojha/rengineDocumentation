/* rengine.wiki: Copy page, search shortcut, query chips, pane sync. */
(() => {
  "use strict";

  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);

  // ---------- Copy page ----------
  function copyPage() {
    $$(".rn-copy-page").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      const label = btn.querySelector("span");
      btn.addEventListener("click", async () => {
        try {
          const res = await fetch(btn.dataset.mdUrl, { credentials: "same-origin" });
          if (!res.ok) throw new Error(String(res.status));
          const text = await res.text();
          await navigator.clipboard.writeText(text);
          btn.classList.add("is-done");
          if (label) label.textContent = "Copied";
        } catch (err) {
          if (label) label.textContent = "Copy failed";
        }
        setTimeout(() => {
          btn.classList.remove("is-done");
          if (label) label.textContent = "Copy page";
        }, 1800);
      });
    });
  }

  // ---------- search shortcut ----------
  function searchShortcut() {
    const form = document.querySelector(".rn-header .md-search__form");
    if (form) form.setAttribute("data-rn-kbd", isMac ? "⌘K" : "Ctrl K");
    if (document.body.dataset.rnKeys) return;
    document.body.dataset.rnKeys = "1";
    document.addEventListener("keydown", (ev) => {
      if ((ev.metaKey || ev.ctrlKey) && !ev.altKey && ev.key.toLowerCase() === "k") {
        const toggle = document.getElementById("__search");
        const input = document.querySelector(".md-search__input");
        if (!toggle || !input) return;
        ev.preventDefault();
        toggle.checked = true;
        toggle.dispatchEvent(new Event("change", { bubbles: true }));
        setTimeout(() => input.focus(), 0);
      }
    });
  }

  // ---------- query chips ----------
  const FIELD = /(^|[\s(!-])((?:[a-z][a-z0-9_]*)(?:\.[a-z0-9_]+)*)(?=(?:!=|>=|<=|!~|[:=<>~]))/g;
  function queryChips() {
    $$("code.rn-q").forEach((el) => {
      if (el.dataset.rnq) return;
      el.dataset.rnq = "1";
      const text = el.textContent;
      const parts = [];
      let last = 0;
      text.replace(FIELD, (m, pre, name, offset) => {
        const start = offset + pre.length;
        let end = start + name.length;
        const op = text.slice(end).match(/^(!=|>=|<=|!~|[:=<>~])/);
        if (op) end += op[0].length;
        parts.push(document.createTextNode(text.slice(last, start)));
        const span = document.createElement("span");
        span.className = "f";
        span.textContent = text.slice(start, end);
        parts.push(span);
        last = end;
        return m;
      });
      if (!parts.length) return;
      parts.push(document.createTextNode(text.slice(last)));
      el.replaceChildren(...parts);
    });
  }

  // ---------- pane sync ----------
  function selectTab(pane, name) {
    if (!name) return null;
    const want = name.trim().toLowerCase();
    for (const set of $$(".tabbed-set", pane)) {
      const labels = $$(":scope > .tabbed-labels > label", set);
      const idx = labels.findIndex((l) => l.textContent.trim().toLowerCase() === want);
      if (idx < 0) continue;
      const input = document.getElementById(labels[idx].htmlFor);
      if (input && !input.checked) {
        input.checked = true;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      }
      const blocks = $$(":scope > .tabbed-content > .tabbed-block", set);
      return blocks[idx] || null;
    }
    return null;
  }

  function markIn(pane, block, marks) {
    $$(".is-marked", pane).forEach((el) => el.classList.remove("is-marked"));
    if (!marks) return;
    const scope = block || pane;
    marks.split(/\s+/).filter(Boolean).forEach((m) => {
      $$(`[data-mark~="${CSS.escape(m)}"]`, scope).forEach((el) => el.classList.add("is-marked"));
    });
  }

  function paneSync() {
    $$(".rn-split").forEach((split) => {
      if (split.dataset.rnSync) return;
      split.dataset.rnSync = "1";
      const pane = split.querySelector(":scope > .rn-pane");
      if (!pane) return;
      const steps = $$(".rn-prose li", split).filter((li) => li.querySelector(":scope > .rn-ref, :scope > p > .rn-ref"));
      if (!steps.length) return;
      let current = null;

      const activate = (li, flash) => {
        if (current === li) return;
        current = li;
        steps.forEach((s) => s.classList.toggle("is-current", s === li));
        const ref = li.querySelector(".rn-ref");
        const block = selectTab(pane, ref.dataset.tab);
        markIn(pane, block, ref.dataset.mark);
        if (flash) {
          pane.classList.add("is-flash");
          setTimeout(() => pane.classList.remove("is-flash"), 500);
        }
      };

      steps.forEach((li) => {
        li.classList.add("rn-step--ref");
        li.addEventListener("click", (ev) => {
          if (ev.target.closest("a, button, code")) return;
          current = null;
          activate(li, getComputedStyle(pane).position === "sticky");
        });
      });

      activate(steps[0], false);

      if (!("IntersectionObserver" in window)) return;
      const visible = new Set();
      const io = new IntersectionObserver(
        (entries) => {
          if (getComputedStyle(pane).position !== "sticky") return;
          entries.forEach((e) => (e.isIntersecting ? visible.add(e.target) : visible.delete(e.target)));
          const first = steps.find((s) => visible.has(s));
          if (first) activate(first, false);
        },
        { rootMargin: "-25% 0px -45% 0px", threshold: 0 }
      );
      steps.forEach((s) => io.observe(s));
    });
  }

  // ---------- home: Burp Suite connector scene ----------
  // Static final frame without JavaScript or with reduced motion; a looping scene otherwise.
  function burpScene() {
    $$(".rn-burp").forEach((section) => {
      if (section.dataset.rnScene) return;
      section.dataset.rnScene = "1";
      const stage = section.querySelector(".rn-burp__stage");
      const toggle = section.querySelector(".rn-burp__toggle");
      if (!stage || !stage.animate || matchMedia("(prefers-reduced-motion: reduce)").matches) return;

      const q = (sel) => stage.querySelector(sel);
      const cursor = q(".rn-burp__cursor");
      const out = q(".rn-burp__packet--out");
      const back = q(".rn-burp__packet--back");
      const payload = q(".rn-burp__pl");
      const steps = $$(".rn-burp__steps li", section);
      const FROM = payload.dataset.from;
      const TO = payload.dataset.to;
      const STATES = ["is-arrived", "is-responded", "is-sent", "is-toast", "is-flash", "is-select", "is-typing", "is-captured", "is-reset"];

      let paused = false;
      let inView = false;
      let started = false;
      let pos = [0, 0];

      const live = () => !paused && inView && !document.hidden;
      const wait = (ms) =>
        new Promise((resolve) => {
          let left = ms;
          let last = performance.now();
          const tick = (now) => {
            if (live()) left -= now - last;
            last = now;
            if (left <= 0) resolve();
            else requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        });
      const until = async (anim) => {
        await anim.finished.catch(() => {});
        try { anim.commitStyles(); } catch (err) { /* element detached */ }
        anim.cancel();
      };
      const point = (el) => {
        const s = stage.getBoundingClientRect();
        const r = el.getBoundingClientRect();
        return [r.left - s.left + r.width / 2, r.top - s.top + r.height / 2];
      };
      // the arrow tip sits at the top left of the cursor graphic
      const tipAt = ([x, y]) => `translate(${x - 2}px, ${y - 2}px)`;
      const moveTo = async (el, ms) => {
        const to = point(el);
        await until(cursor.animate([{ transform: tipAt(pos) }, { transform: tipAt(to) }], { duration: ms, easing: "cubic-bezier(.45,.05,.25,1)", fill: "forwards" }));
        pos = to;
      };
      const press = async (cls) => {
        stage.classList.add(cls);
        await until(cursor.animate([{ transform: tipAt(pos) + " scale(1)" }, { transform: tipAt(pos) + " scale(.82)" }, { transform: tipAt(pos) + " scale(1)" }], { duration: 220, fill: "forwards" }));
        stage.classList.remove(cls);
      };
      const fly = async (el, from, to, ms) => {
        const w = el.offsetWidth;
        const h = el.offsetHeight;
        const at = ([x, y], s) => `translate(${x - w / 2}px, ${y - h / 2}px) scale(${s})`;
        const across = Math.abs(to[0] - from[0]) >= Math.abs(to[1] - from[1]);
        const mid = across
          ? [(from[0] + to[0]) / 2, Math.max(h, Math.min(from[1], to[1]) - 48)]
          : [Math.max(from[0], to[0]) + 40, (from[1] + to[1]) / 2];
        await until(
          el.animate(
            [
              { transform: at(from, 0.6), opacity: 0 },
              { transform: at(from, 1), opacity: 1, offset: 0.12 },
              { transform: at(mid, 1), opacity: 1, offset: 0.55 },
              { transform: at(to, 1), opacity: 1, offset: 0.88 },
              { transform: at(to, 0.6), opacity: 0 },
            ],
            { duration: ms, easing: "ease-in-out", fill: "forwards" }
          )
        );
      };
      const step = (n) =>
        steps.forEach((li, i) => {
          li.classList.toggle("is-on", i === n - 1);
          li.classList.toggle("is-past", i < n - 1);
        });

      const scene = async () => {
        for (;;) {
          stage.classList.remove(...STATES);
          stage.classList.add("is-playing");
          payload.textContent = FROM;
          step(1);
          pos = point(q(".rn-burp__title"));
          await until(cursor.animate([{ transform: tipAt(pos) }, { transform: tipAt(pos) }], { duration: 1, fill: "forwards" }));
          await wait(1200);

          const send = q(".rn-burp__sendmain");
          await moveTo(send, 900);
          await wait(250);
          step(2);
          await press("is-press-send");
          stage.classList.add("is-sent", "is-toast");
          await fly(out, point(send), point(q(".rn-burp__rep")), 1200);

          step(3);
          stage.classList.add("is-arrived", "is-flash");
          await wait(900);
          stage.classList.remove("is-flash");
          await wait(700);
          stage.classList.remove("is-toast");

          step(4);
          await moveTo(payload, 1000);
          stage.classList.add("is-select");
          await wait(700);
          stage.classList.remove("is-select");
          stage.classList.add("is-typing");
          payload.textContent = "";
          for (const ch of TO) {
            payload.textContent += ch;
            await wait(36);
          }
          stage.classList.remove("is-typing");
          await wait(400);

          await moveTo(q(".rn-burp__bsend"), 800);
          await wait(200);
          await press("is-press-bsend");
          await wait(300);
          stage.classList.add("is-responded");
          await wait(700);
          await fly(back, point(q(".rn-burp__respane")), point(q(".rn-burp__rn .rn-burp__chrome")), 1200);
          stage.classList.add("is-captured");
          step(5);
          await wait(3400);

          stage.classList.add("is-reset");
          await wait(450);
        }
      };

      const setPaused = (value) => {
        paused = value;
        section.classList.toggle("is-paused", paused);
        toggle.setAttribute("aria-pressed", String(paused));
        toggle.querySelector("span").textContent = paused ? "Play" : "Pause";
      };
      toggle.hidden = false;
      toggle.addEventListener("click", () => setPaused(!paused));

      const io = new IntersectionObserver(
        (entries) => {
          inView = entries.some((e) => e.isIntersecting);
          if (inView && !started) {
            started = true;
            scene();
          }
        },
        { threshold: 0.35 }
      );
      io.observe(stage);
    });
  }

  // ---------- motion helpers ----------
  const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // Calls cb once, the first time el is visible.
  function onView(el, cb, threshold = 0.3) {
    if (!("IntersectionObserver" in window)) return cb();
    const io = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting)) return;
        io.disconnect();
        cb();
      },
      { threshold }
    );
    io.observe(el);
  }

  // A wait() that only counts time while el is on screen and the tab is visible.
  function gatedWait(el) {
    let inView = !("IntersectionObserver" in window);
    if (!inView) new IntersectionObserver((es) => { inView = es.some((e) => e.isIntersecting); }, { threshold: 0.1 }).observe(el);
    const live = () => inView && !document.hidden;
    const wait = (ms, onTick) =>
      new Promise((resolve) => {
        let done = 0;
        let last = performance.now();
        const tick = (now) => {
          if (live()) done += now - last;
          last = now;
          if (onTick) onTick(Math.min(1, done / ms));
          if (done >= ms) resolve();
          else requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    return wait;
  }

  // Types the text of el, keeping its child spans (query field names stay coloured).
  async function typeInto(el, wait, perChar = 40) {
    if (el.dataset.full === undefined) el.dataset.full = el.innerHTML;
    const tmpl = document.createElement("span");
    tmpl.innerHTML = el.dataset.full;
    const parts = Array.from(tmpl.childNodes, (n) => ({ text: n.textContent, cls: n.nodeType === 1 ? n.className : null }));
    el.textContent = "";
    el.classList.add("is-typing");
    for (const p of parts) {
      const node = p.cls ? Object.assign(document.createElement("span"), { className: p.cls }) : document.createTextNode("");
      el.appendChild(node);
      for (const ch of p.text) {
        node.textContent += ch;
        await wait(perChar);
      }
    }
    el.classList.remove("is-typing");
  }

  function staggerIn(items) {
    items.forEach((it, i) => {
      it.style.setProperty("--i", i);
      it.classList.remove("rn-in");
      void it.offsetWidth;
      it.classList.add("rn-in");
    });
  }

  // Prints each code block of a pane tab line by line.
  function printBlocks(block) {
    $$(":scope > .rn-pane-label, :scope > .highlight, :scope > pre", block).forEach((el, i) => {
      const pre = el.matches("pre") ? el : el.querySelector("pre");
      const delay = i * 260;
      if (!pre) {
        el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220, delay, fill: "backwards" });
        return;
      }
      const lines = (pre.textContent.match(/\n/g) || []).length + 1;
      pre.animate([{ clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0 0)" }], {
        duration: Math.min(1600, lines * 120),
        delay,
        easing: `steps(${lines}, end)`,
        fill: "backwards",
      });
    });
  }

  async function playChat(chat, wait) {
    const msgs = $$(":scope > .rn-ui-msg", chat);
    msgs.forEach((m) => m.classList.add("rn-hide"));
    for (const m of msgs) {
      if (m.classList.contains("out")) {
        await wait(450);
      } else {
        const dots = document.createElement("span");
        dots.className = "rn-ui-msg rn-dots";
        dots.innerHTML = "<i></i><i></i><i></i>";
        chat.insertBefore(dots, m);
        await wait(750);
        dots.remove();
      }
      m.classList.remove("rn-hide");
      staggerIn([m]);
      await wait(350);
    }
  }

  async function playUi(ui, wait) {
    const q = ui.querySelector(".rn-ui-qb .rn-q");
    if (q) {
      const qb = q.closest(".rn-ui-qb");
      qb.classList.add("is-pending");
      ui.classList.add("rn-pre");
      await wait(250);
      await typeInto(q, wait, 45);
      await wait(200);
      qb.classList.remove("is-pending");
    }
    const rows = $$(".rn-ui-row, .rn-ui-item", ui);
    ui.classList.remove("rn-pre");
    if (rows.length) staggerIn(rows);
    const chat = ui.querySelector(".rn-ui-chat");
    if (chat) await playChat(chat, wait);
  }

  // ---------- panes: interface recreations play once in view ----------
  function paneRecreations() {
    if (reduced()) return;
    $$(".rn-pane .rn-ui").forEach((ui) => {
      if (ui.dataset.rnPlay || ui.closest(".rn-pane--home")) return;
      ui.dataset.rnPlay = "1";
      if (!ui.querySelector(".rn-ui-qb .rn-q, .rn-ui-row, .rn-ui-chat, .rn-ui-item")) return;
      if (ui.querySelector(".rn-ui-qb .rn-q, .rn-ui-row, .rn-ui-item")) ui.classList.add("rn-pre");
      $$(".rn-ui-chat > .rn-ui-msg", ui).forEach((m) => m.classList.add("rn-hide"));
      onView(ui, () => playUi(ui, sleep), 0.25);
    });
  }

  // ---------- home: the hero pane cycles through its surfaces ----------
  function heroAutoplay() {
    const pane = document.querySelector(".rn-pane--home[data-autoplay]");
    if (!pane || pane.dataset.rnAuto) return;
    pane.dataset.rnAuto = "1";
    const inputs = $$(".tabbed-set > input", pane);
    const blocks = $$(".tabbed-content > .tabbed-block", pane);
    const select = (i) => {
      const input = inputs[i];
      if (input && !input.checked) {
        input.checked = true;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      }
    };
    let stopped = false;
    const bar = document.createElement("i");
    bar.className = "rn-autobar";
    const stop = () => {
      stopped = true;
      bar.remove();
    };
    // the audience rows select their surface
    $$(".rn-start__row").forEach((row, i) => {
      const go = () => {
        stop();
        select(i);
      };
      row.addEventListener("mouseenter", go);
      row.addEventListener("focus", go);
    });
    $$(".tabbed-labels > label", pane).forEach((label) => label.addEventListener("click", stop));
    if (reduced()) return;

    pane.appendChild(bar);
    const wait = gatedWait(pane);
    const dwell = Number(pane.dataset.autoplay) || 7000;
    (async () => {
      await wait(600);
      for (;;) {
        for (let i = 0; i < blocks.length; i++) {
          if (stopped) return;
          select(i);
          const ui = blocks[i].querySelector(".rn-ui");
          if (ui) playUi(ui, wait);
          else printBlocks(blocks[i]);
          await wait(dwell, (p) => { bar.style.transform = `scaleX(${p})`; });
        }
      }
    })();
  }

  // ---------- home: counts tick up once in view ----------
  function countUp() {
    if (reduced()) return;
    $$(".rn-counts b").forEach((b) => {
      if (b.dataset.rnCount) return;
      b.dataset.rnCount = "1";
      const target = parseInt(b.textContent.replace(/[^0-9]/g, ""), 10);
      if (!target) return;
      b.textContent = "0";
      onView(b, () => {
        const t0 = performance.now();
        const dur = 900 + Math.min(700, target / 2);
        const frame = (now) => {
          const p = Math.min(1, (now - t0) / dur);
          b.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString("en-US");
          if (p < 1) requestAnimationFrame(frame);
        };
        requestAnimationFrame(frame);
      }, 0.6);
    });
  }

  function init() {
    copyPage();
    searchShortcut();
    queryChips();
    paneSync();
    burpScene();
    heroAutoplay();
    countUp();
    paneRecreations();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
