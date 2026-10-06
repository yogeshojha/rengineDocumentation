/* rengine.wiki: Copy page, search shortcut, query chips, pane sync, and the home page scenes. */
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

  // ---------- home: the reNgine shell ----------
  // Points the sidebar and the breadcrumb of a shell at the page an element describes
  // through its data-nav and data-crumb attributes.
  function shellTo(app, el) {
    if (!app || !el) return;
    const nav = el.dataset.nav || "";
    $$("[data-nav]", app).forEach((it) => it.classList.toggle("is-active", it.dataset.nav === nav));
    app.classList.toggle("is-assets", nav.startsWith("assets"));
    app.classList.toggle("is-findings", nav.startsWith("findings"));
    const crumbs = app.querySelector("[data-crumbs]");
    if (crumbs && el.dataset.crumb) {
      const parts = el.dataset.crumb.split("›").map((s) => s.trim()).filter(Boolean);
      const nodes = [];
      parts.forEach((p, i) => {
        if (i) {
          const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
          const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
          use.setAttribute("href", "#rni-chev");
          svg.appendChild(use);
          nodes.push(svg);
        }
        const span = document.createElement("span");
        span.textContent = p;
        if (i === parts.length - 1) span.className = "is-cur";
        nodes.push(span);
      });
      crumbs.replaceChildren(...nodes);
    }
  }

  // ---------- home: scroll-driven layers and tour ----------
  const clamp = (v, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, v));
  const seg = (p, a, b) => clamp((p - a) / (b - a));
  const scrollJobs = [];

  function onScroll(job) {
    scrollJobs.push(job);
    if (scrollJobs.length > 1) return;
    let queued = false;
    const run = () => {
      queued = false;
      scrollJobs.forEach((j) => j());
    };
    const req = () => {
      if (!queued) {
        queued = true;
        requestAnimationFrame(run);
      }
    };
    addEventListener("scroll", req, { passive: true });
    addEventListener("resize", req);
  }

  // The reading line: the middle of the viewport, or on a phone the middle of the space below the pinned stage.
  function readingLine(stage) {
    const r = stage.getBoundingClientRect();
    const pinned = innerWidth < 960 && r.top < innerHeight / 2;
    return pinned ? r.bottom + (innerHeight - r.bottom) / 2 : innerHeight / 2;
  }

  // The step whose middle is nearest the reading line, and how far through it the reader is.
  function activeStep(steps, mid = innerHeight / 2) {
    let on = -1;
    let best = Infinity;
    steps.forEach((el, i) => {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      const d = Math.abs(r.top + r.height / 2 - mid);
      if (d < best) {
        best = d;
        on = i;
      }
    });
    if (on < 0) return { on, local: 0 };
    const r = steps[on].getBoundingClientRect();
    return { on, local: clamp((mid - r.top) / r.height) };
  }

  // The layers: one pinned window, one page per step. The page of the active step is in,
  // the pages before it have lifted off, the sidebar and the breadcrumb follow.
  function surface() {
    const root = document.querySelector("[data-rn-surface]");
    if (!root || root.dataset.rnOn) return;
    root.dataset.rnOn = "1";
    const stage = root.querySelector(".rn-surface__stage");
    const app = root.querySelector("[data-app]");
    const steps = $$(".rn-surface__steps .rn-step", root);
    const views = $$(".rn-layer", root);
    const byView = Object.fromEntries(views.map((v) => [v.dataset.view, v]));
    const slabs = $$(".rn-surface__slabs i", root);
    const label = root.querySelector("[data-rail-label]");
    let last = -1;
    const update = () => {
      let { on } = activeStep(steps, readingLine(stage));
      if (on < 0) on = last < 0 ? 0 : last;
      if (on === last) return;
      const view = byView[steps[on].dataset.view] || views[0];
      const idx = views.indexOf(view);
      views.forEach((v, i) => {
        v.classList.toggle("is-on", i === idx);
        v.classList.toggle("is-out", i < idx);
      });
      steps.forEach((s, i) => s.classList.toggle("is-on", i === on));
      slabs.forEach((s, i) => {
        s.classList.toggle("is-on", i === idx);
        s.classList.toggle("is-past", i < idx);
      });
      if (label) label.textContent = steps[on].dataset.label || "";
      shellTo(app, view);
      last = on;
    };
    onScroll(update);
    update();
  }

  // Puts a scene's cursor over the middle of el, offset by dx and dy pixels.
  function aim(sc, el, dx = 0, dy = 0) {
    const cur = sc.querySelector("[data-cursor]");
    if (!cur || !el) return;
    const host = cur.parentElement || sc;
    const h = host.getBoundingClientRect();
    const r = el.getBoundingClientRect();
    cur.style.left = `${r.left - h.left + r.width / 2 + dx}px`;
    cur.style.top = `${r.top - h.top + r.height / 2 + dy}px`;
  }

  // The tour: one pinned window, one scene per step, each scene played by the reader's scroll.
  const TOUR = {
    query(sc, p) {
      const q = sc.querySelector("[data-q]");
      const full = q.dataset.q;
      const n = Math.round(seg(p, 0.06, 0.6) * full.length);
      const typed = full.slice(0, n);
      q.innerHTML = typed.replace(/\b(tech:|is:)/g, '<span class="k">$1</span>');
      sc.querySelector("[data-ph]").hidden = n > 0;
      sc.querySelector("[data-qb]").classList.toggle("is-focus", n > 0);
      const stage = n >= full.length ? 2 : n >= 12 ? 1 : 0;
      let shift = 0;
      $$("[data-m]", sc).forEach((row) => {
        const keep = +row.dataset.m >= stage;
        row.classList.toggle("is-out", !keep);
        row.style.transform = keep ? `translateY(${-shift}px)` : "";
        if (!keep) shift += row.offsetHeight;
      });
      sc.querySelector("[data-count]").textContent = stage === 2 ? "3" : stage === 1 ? "4" : "53,142";
      const sug = sc.querySelector("[data-sug]");
      const show = n >= 2 && n < 5 ? "field" : n >= 5 && n < 12 ? "value" : n >= 16 && n < full.length ? "flag" : "";
      sug.classList.toggle("is-on", !!show);
      if (show) sug.dataset.show = show;
    },
    watch(sc, p) {
      const pressed = p > 0.4;
      const prog = sc.querySelector("[data-prog]");
      const press = sc.querySelector("[data-press]");
      prog.classList.toggle("is-on", p > 0.08);
      sc.querySelector("[data-dlg]").classList.toggle("is-on", p > 0.22 && p < 0.55);
      press.classList.toggle("is-press", p > 0.4 && p < 0.46);
      const cur = sc.querySelector("[data-cursor]");
      cur.style.opacity = p > 0.12 && p < 0.55 ? "1" : "0";
      if (p < 0.22) aim(sc, prog, prog.getBoundingClientRect().width * 0.28, 0);
      else aim(sc, press, 0, 0);
      sc.querySelector("[data-toast]").classList.toggle("is-on", pressed && p < 0.62);
      sc.querySelector("[data-wcount]").textContent = pressed ? "1" : "0";
      sc.querySelector("[data-hosts]").classList.toggle("is-on", p > 0.58);
      sc.querySelector("[data-alert]").classList.toggle("is-on", p > 0.72);
    },
    tripwire(sc, p) {
      sc.querySelector("[data-press]").classList.toggle("is-press", p > 0.14 && p < 0.2);
      sc.querySelector("[data-pop]").classList.toggle("is-on", p > 0.18 && p < 0.6);
      sc.querySelector("[data-create]").classList.toggle("is-press", p > 0.52 && p < 0.6);
      sc.querySelector("[data-alert]").classList.toggle("is-on", p > 0.66);
    },
    telegram(sc, p) {
      const step = Math.floor(seg(p, 0.06, 0.78) * 4.999);
      $$("[data-step]", sc).forEach((m) => {
        const s = +m.dataset.step;
        const gone = m.dataset.gone ? +m.dataset.gone : 99;
        m.classList.toggle("is-hidden", s > step);
        m.classList.toggle("is-gone", step >= gone);
      });
    },
    mcp(sc, p) {
      const step = Math.floor(seg(p, 0.04, 0.72) * 5.999);
      $$("[data-step]", sc).forEach((el) => el.classList.toggle("is-hidden", +el.dataset.step > step));
    },
  };

  function tour() {
    const root = document.querySelector("[data-rn-tour]");
    if (!root || root.dataset.rnOn) return;
    root.dataset.rnOn = "1";
    const steps = $$(".rn-tour__steps .rn-step", root);
    const scenes = $$(".rn-scene", root);
    const dots = $$(".rn-tour__dots i", root);
    const stage = root.querySelector(".rn-tour__stage");
    let last = -1;
    const update = () => {
      let { on, local } = activeStep(steps, readingLine(stage));
      if (on < 0) on = last < 0 ? 0 : last;
      if (on !== last) {
        steps.forEach((s, i) => s.classList.toggle("is-on", i === on));
        scenes.forEach((s, i) => s.classList.toggle("is-on", i === on));
        dots.forEach((d, i) => d.classList.toggle("is-on", i === on));
        last = on;
      }
      const sc = scenes[on];
      const play = TOUR[sc.dataset.scene];
      if (play) play(sc, reduced() ? 1 : local);
    };
    onScroll(update);
    update();
  }

  // ---------- home: one run, end to end ----------
  // Five chapters played in one window. Reduced motion shows each chapter's last frame.
  const RUN_W = 1120;
  const fmt = (n) => Math.round(n).toLocaleString("en-US");
  const setText = (root, sel, text) => $$(sel, root).forEach((el) => { el.textContent = text; });

  const RUN = {
    target: {
      reset(sc) {
        sc.classList.remove("s-sw", "s-added", "s-typed");
        sc.querySelector("[data-dlg]").classList.remove("is-on");
        sc.querySelector("[data-at=input]").classList.remove("is-focus");
        sc.querySelector("[data-type]").textContent = "";
        setText(sc, "[data-targets], [data-shown], [data-shown2]", "3");
        setText(sc, "[data-livecount]", "0");
      },
      added(sc) {
        sc.classList.add("s-added");
        setText(sc, "[data-targets], [data-shown], [data-shown2]", "4");
        setText(sc, "[data-livecount]", "1");
        sc.closest("[data-app]").classList.add("is-scanning");
      },
      finish(sc) {
        sc.querySelector("[data-type]").textContent = sc.querySelector("[data-type]").dataset.type;
        sc.classList.add("s-sw", "s-typed");
        this.added(sc);
      },
      async play(sc, k) {
        const input = sc.querySelector("[data-at=input]");
        await k.wait(500);
        await k.click(sc.querySelector("[data-at=open]"));
        sc.querySelector("[data-dlg]").classList.add("is-on");
        await k.wait(450);
        await k.click(input);
        input.classList.add("is-focus");
        await k.type(sc.querySelector("[data-type]"), 70);
        sc.classList.add("s-typed");
        await k.wait(300);
        await k.click(sc.querySelector("[data-at=switch]"));
        sc.classList.add("s-sw");
        await k.wait(350);
        await k.click(sc.querySelector("[data-at=add]"));
        input.classList.remove("is-focus");
        sc.querySelector("[data-dlg]").classList.remove("is-on");
        k.hide();
        await k.wait(250);
        this.added(sc);
        await k.wait(1700);
      },
    },
    scan: {
      reset(sc) {
        sc.classList.remove("s-done");
        sc.querySelector("[data-state]").textContent = "Running";
        sc.querySelector(".rn-run__bar").style.setProperty("--p", 0);
        $$("[data-stage]", sc).forEach((st) => st.classList.remove("is-run", "is-done"));
        $$("[data-tick]", sc).forEach((b) => { b.textContent = "0"; });
        $$("[data-feed]", sc).forEach((r) => r.classList.remove("is-in"));
      },
      finish(sc) {
        sc.classList.add("s-done");
        sc.querySelector("[data-state]").textContent = "Completed";
        sc.querySelector(".rn-run__bar").style.setProperty("--p", 1);
        $$("[data-stage]", sc).forEach((st) => st.classList.add("is-done"));
        $$("[data-tick]", sc).forEach((b) => { b.textContent = fmt(+b.dataset.tick); });
        $$("[data-feed]", sc).forEach((r) => r.classList.add("is-in"));
      },
      async play(sc, k) {
        const stages = $$("[data-stage]", sc);
        const funnel = $$(".rn-run__funnel [data-tick]", sc);
        const bar = sc.querySelector(".rn-run__bar");
        const gap = 620;
        const each = 1050;
        const total = gap * (stages.length - 1) + each;
        await k.wait(300);
        await Promise.all([
          k.tween(total, (p) => bar.style.setProperty("--p", p.toFixed(3))),
          ...stages.map(async (st, i) => {
            await k.wait(i * gap);
            st.classList.add("is-run");
            if (i === 2) {
              (async () => {
                for (const r of $$("[data-feed]", sc).reverse()) {
                  r.classList.add("is-in");
                  await k.wait(380);
                }
              })().catch(() => {});
            }
            const ticks = $$("[data-tick]", st);
            const twins = ticks.map((b) => funnel.find((f) => f.dataset.tick === b.dataset.tick && !f.dataset.taken));
            twins.forEach((f) => f && (f.dataset.taken = "1"));
            await k.tween(each, (p) => {
              const e = 1 - Math.pow(1 - p, 3);
              [...ticks, ...twins.filter(Boolean)].forEach((b) => { b.textContent = fmt(+b.dataset.tick * e); });
            });
            st.classList.remove("is-run");
            st.classList.add("is-done");
          }),
        ]);
        funnel.forEach((f) => delete f.dataset.taken);
        sc.classList.add("s-done");
        sc.querySelector("[data-state]").textContent = "Completed";
        sc.closest("[data-app]").classList.remove("is-scanning");
        await k.wait(1500);
      },
    },
    results: {
      rows: (sc) => $$(".rn-x-tr[data-keep]", sc),
      reset(sc) {
        sc.classList.remove("s-hit");
        const q = sc.querySelector("[data-query]");
        if (q.dataset.html === undefined) q.dataset.html = q.innerHTML;
        q.textContent = "";
        sc.querySelector("[data-qb]").classList.remove("is-focus");
        sc.querySelector("[data-count]").textContent = "412";
        this.rows(sc).forEach((r) => r.classList.remove("is-gone"));
      },
      narrow(sc) {
        this.rows(sc).forEach((r) => r.classList.toggle("is-gone", r.dataset.keep !== "1"));
        sc.classList.add("s-hit");
      },
      finish(sc) {
        const q = sc.querySelector("[data-query]");
        if (q.dataset.html !== undefined) q.innerHTML = q.dataset.html;
        sc.querySelector("[data-count]").textContent = "2";
        this.narrow(sc);
      },
      async play(sc, k) {
        const q = sc.querySelector("[data-query]");
        const full = q.dataset.query;
        await k.wait(600);
        sc.querySelector("[data-qb]").classList.add("is-focus");
        for (let n = 1; n <= full.length; n++) {
          q.innerHTML = full.slice(0, n).replace(/\b(tech:|is:)/g, '<span class="k">$1</span>');
          await k.wait(75);
        }
        await k.wait(300);
        this.narrow(sc);
        const count = sc.querySelector("[data-count]");
        await k.tween(600, (p) => { count.textContent = fmt(412 - 410 * (1 - Math.pow(1 - p, 3))); });
        sc.querySelector("[data-qb]").classList.remove("is-focus");
        await k.wait(1900);
      },
    },
    ask: {
      STATES: ["s-sent", "s-work", "s-lead", "s-text", "s-block"],
      reset(sc) {
        sc.classList.remove(...this.STATES);
        const work = sc.querySelector("[data-work-text]");
        if (work.dataset.done === undefined) work.dataset.done = work.textContent;
        work.textContent = work.dataset.running;
        sc.querySelector("[data-type]").textContent = "";
        sc.querySelector("[data-composer]").classList.remove("is-focus");
      },
      finish(sc) {
        sc.querySelector("[data-type]").textContent = "";
        const work = sc.querySelector("[data-work-text]");
        if (work.dataset.done !== undefined) work.textContent = work.dataset.done;
        sc.classList.add(...this.STATES);
      },
      async play(sc, k) {
        const composer = sc.querySelector("[data-composer]");
        const text = sc.querySelector("[data-type]");
        await k.wait(450);
        composer.classList.add("is-focus");
        await k.type(text, 30);
        await k.wait(350);
        await k.press(sc.querySelector(".rn-run__send"));
        text.textContent = "";
        sc.classList.add("s-sent");
        await k.wait(550);
        sc.classList.add("s-work");
        await k.wait(1500);
        sc.querySelector("[data-work-text]").textContent = sc.querySelector("[data-work-text]").dataset.done;
        sc.classList.add("s-lead");
        await k.wait(550);
        sc.classList.add("s-text");
        await k.wait(500);
        sc.classList.add("s-block");
        await k.wait(2600);
        composer.classList.remove("is-focus");
      },
    },
    act: {
      reset(sc) {
        $$("[data-dest]", sc).forEach((d) => d.classList.remove("is-on", "is-settled"));
      },
      finish(sc) {
        $$("[data-dest]", sc).forEach((d) => d.classList.add("is-on", "is-settled"));
      },
      async play(sc, k) {
        const dest = (name) => sc.querySelector(`[data-dest=${name}]`);
        const land = async (from, name) => {
          await k.fly(from, dest(name), 750);
          dest(name).classList.add("is-on");
          await k.wait(900);
          dest(name).classList.add("is-settled");
        };
        await k.wait(900);
        await land(sc.querySelector(".rn-run__chips"), "alert");
        await k.click(sc.querySelector("[data-at=repeater]"));
        await land(sc.querySelector("[data-at=repeater]"), "repeater");
        await k.click(sc.querySelector("[data-at=issue]"));
        await land(sc.querySelector("[data-at=issue]"), "issue");
        k.hide();
        await k.wait(1800);
      },
    },
  };

  function runHero() {
    const root = document.querySelector("[data-rn-run]");
    if (!root || root.dataset.rnOn) return;
    root.dataset.rnOn = "1";
    const frame = root.querySelector("[data-run-frame]");
    const body = root.querySelector("[data-run-body]");
    const app = root.querySelector("[data-app]");
    const urlbar = root.querySelector("[data-urlbar]");
    const cursor = root.querySelector("[data-cursor]");
    const dot = root.querySelector("[data-packet]");
    const scenes = $$(".rn-run__scene", root);
    const items = $$(".rn-run__chapters > li", root);
    const toggle = root.querySelector(".rn-run__toggle");

    const fit = () => frame.style.setProperty("--k", (frame.clientWidth / RUN_W).toFixed(4));
    fit();
    if ("ResizeObserver" in window) new ResizeObserver(fit).observe(frame);
    const scale = () => parseFloat(frame.style.getPropertyValue("--k")) || 1;

    let current = 0;
    let token = 0;
    let paused = false;
    let inView = false;
    const live = () => !paused && inView && !document.hidden;

    const show = (i, done = false) => {
      scenes.forEach((sc, j) => sc.classList.toggle("is-on", j === i));
      items.forEach((li, j) => {
        li.classList.toggle("is-on", j === i);
        li.style.setProperty("--p", j < i || (j === i && done) ? 1 : 0);
      });
      shellTo(app, scenes[i]);
      if (urlbar) urlbar.textContent = scenes[i].dataset.url || "";
      app.classList.toggle("is-scanning", scenes[i].dataset.scene === "scan");
    };
    const settle = (i) => {
      const sc = scenes[i];
      const spec = RUN[sc.dataset.scene];
      spec.reset(sc);
      show(i, true);
      spec.finish(sc);
      cursor.classList.remove("is-on");
    };

    // every wait counts only while the hero is on screen, the tab is visible and nothing is paused
    function kit(my, li, length) {
      const cut = new Error("cut");
      let spent = 0;
      const wait = (ms) =>
        new Promise((resolve, reject) => {
          let left = ms;
          let last = performance.now();
          const tick = (now) => {
            if (my !== token) return reject(cut);
            if (live()) {
              const dt = Math.min(64, now - last);
              left -= dt;
              spent += dt;
              li.style.setProperty("--p", Math.min(1, spent / length).toFixed(3));
            }
            last = now;
            if (left <= 0) resolve();
            else requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        });
      const tween = async (ms, draw) => {
        let t = 0;
        while (t < ms) {
          await wait(16);
          t += 16;
          draw(Math.min(1, t / ms));
        }
      };
      const at = (el) => {
        const b = body.getBoundingClientRect();
        const r = el.getBoundingClientRect();
        const s = scale();
        return [(r.left - b.left + r.width / 2) / s, (r.top - b.top + r.height / 2) / s];
      };
      const k = {
        wait,
        tween,
        hide: () => cursor.classList.remove("is-on"),
        async move(el, ms = 560) {
          const [x, y] = at(el);
          if (!cursor.classList.contains("is-on")) {
            cursor.style.transitionDuration = "0ms";
            cursor.style.transform = `translate(${x + 60}px, ${y + 70}px)`;
            void cursor.offsetWidth;
            cursor.classList.add("is-on");
          }
          cursor.style.transitionDuration = "";
          cursor.style.transform = `translate(${x - 3}px, ${y - 3}px)`;
          await wait(ms);
        },
        async press(el) {
          el.classList.add("is-press");
          cursor.classList.add("is-down");
          await wait(170);
          el.classList.remove("is-press");
          cursor.classList.remove("is-down");
        },
        async click(el) {
          await k.move(el);
          await k.press(el);
        },
        async type(el, per) {
          const text = el.dataset.type;
          el.textContent = "";
          for (const ch of text) {
            el.textContent += ch;
            await wait(per);
          }
        },
        async fly(from, to, ms) {
          const a = at(from);
          const b = at(to);
          const lift = Math.min(60, Math.abs(b[0] - a[0]) / 3);
          await tween(ms, (p) => {
            const e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
            const x = a[0] + (b[0] - a[0]) * e;
            const y = a[1] + (b[1] - a[1]) * e - Math.sin(Math.PI * e) * lift;
            dot.style.transform = `translate(${x}px, ${y}px)`;
            dot.style.opacity = p < 0.1 ? p * 10 : p > 0.9 ? (1 - p) * 10 : 1;
          });
          dot.style.opacity = 0;
        },
      };
      return k;
    }

    const LENGTH = { target: 7400, scan: 5950, results: 4900, ask: 8200, act: 9400 };

    async function play(from) {
      const my = ++token;
      for (let i = from; ; i = (i + 1) % scenes.length) {
        current = i;
        const sc = scenes[i];
        const spec = RUN[sc.dataset.scene];
        spec.reset(sc);
        cursor.classList.remove("is-on");
        show(i);
        try {
          await spec.play(sc, kit(my, items[i], LENGTH[sc.dataset.scene] || 6000));
        } catch (err) {
          return;
        }
        if (my !== token) return;
        items[i].style.setProperty("--p", 1);
      }
    }

    const still = reduced() || !("IntersectionObserver" in window);
    items.forEach((li, i) => {
      li.querySelector(".rn-run__chapter").addEventListener("click", () => {
        if (still) return settle(i);
        if (paused) setPaused(false);
        play(i);
      });
    });
    if (still) return settle(0);

    const setPaused = (value) => {
      paused = value;
      root.classList.toggle("is-paused", paused);
      toggle.setAttribute("aria-pressed", String(paused));
      toggle.querySelector("span").textContent = paused ? "Play" : "Pause";
    };
    toggle.hidden = false;
    toggle.addEventListener("click", () => setPaused(!paused));

    let started = false;
    new IntersectionObserver(
      (entries) => {
        inView = entries.some((e) => e.isIntersecting);
        if (inView && !started) {
          started = true;
          play(current);
        }
      },
      { threshold: 0.25 }
    ).observe(frame);
    scenes.forEach((sc) => RUN[sc.dataset.scene].reset(sc));
    show(0);
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

  // ---------- home: reveal on scroll, spotlight on hover, parallax in the hero ----------
  function reveal() {
    const els = $$("[data-reveal]").filter((el) => !el.dataset.rnReveal);
    if (!els.length) return;
    els.forEach((el) => { el.dataset.rnReveal = "1"; });
    if (reduced() || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }),
      { threshold: 0.1, rootMargin: "0px 0px -6% 0px" }
    );
    els.forEach((el) => {
      el.classList.add("rn-reveal");
      io.observe(el);
    });
  }

  function spotlight() {
    $$("[data-spotlight]").forEach((grid) => {
      if (grid.dataset.rnSpot) return;
      grid.dataset.rnSpot = "1";
      grid.addEventListener("pointermove", (ev) => {
        const a = ev.target.closest("a");
        if (!a) return;
        const r = a.getBoundingClientRect();
        a.style.setProperty("--mx", `${ev.clientX - r.left}px`);
        a.style.setProperty("--my", `${ev.clientY - r.top}px`);
      });
    });
  }

  // Each banded section carries --py, its position relative to the middle of the viewport, from -1 to 1.
  function bands() {
    const secs = $$("[data-band]").filter((el) => !el.dataset.rnBand);
    if (!secs.length) return;
    secs.forEach((el) => { el.dataset.rnBand = "1"; });
    if (reduced()) return;
    onScroll(() => {
      secs.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.bottom < -400 || r.top > innerHeight + 400) return;
        const p = (innerHeight / 2 - (r.top + r.height / 2)) / (r.height / 2 + innerHeight / 2);
        el.style.setProperty("--py", clamp(p, -1, 1).toFixed(3));
      });
    });
  }

  function init() {
    copyPage();
    searchShortcut();
    queryChips();
    paneSync();
    burpScene();
    runHero();
    surface();
    tour();
    countUp();
    reveal();
    spotlight();
    bands();
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
