const $ = (id) => document.getElementById(id);
const video = $("video");
let data = {};
let current = null;
let steps = [];
let lastK = -2;

const tex = (el, s) => katex.render(s, el, { throwOnError: false, strict: false });

const rich = (el, s) => {
  el.textContent = "";
  s.split(/\$(.+?)\$/g).forEach((part, i) => {
    if (i % 2) {
      const m = document.createElement("span");
      tex(m, part);
      el.append(m);
    } else el.append(part);
  });
};

const stepIndex = (t) => {
  let k = -1;
  steps.forEach((s, i) => {
    if (s.t <= t + 0.05) k = i;
  });
  return k;
};

const setRate = () => {
  const r = Number($("speed").value);
  video.defaultPlaybackRate = r;
  video.playbackRate = r;
};

function buildCards() {
  const box = $("cards");
  box.innerHTML = "";
  current.cards.forEach((c) => {
    const card = document.createElement("div");
    card.className = "info";
    const h = document.createElement("h3");
    h.textContent = c.label;
    const v = document.createElement("div");
    v.className = "value";
    card.append(h, v);
    box.append(card);
  });
}

function buildLegend() {
  const box = $("legend");
  box.innerHTML = "";
  (current.legend || []).forEach((l) => {
    const item = document.createElement("span");
    const dot = document.createElement("i");
    dot.style.background = l.color;
    item.append(dot, l.name);
    box.append(item);
  });
}

function render() {
  if (!current) return;
  $("bar").style.width = `${(video.currentTime / (video.duration || 1)) * 100}%`;
  const k = stepIndex(video.currentTime);
  if (k === lastK) return;
  lastK = k;
  $("stepcount").textContent = `${k + 1} of ${steps.length}`;
  $("subtitle").textContent = k < 0 ? "" : `Step ${k + 1} / ${steps.length} | ${steps[k].label}`;
  current.cards.forEach((c, i) => {
    const el = $("cards").children[i].querySelector(".value");
    const v = k < 0 ? (c.math ? "\\text{—}" : "—") : steps[k].values[i];
    if (c.math) tex(el, v);
    else el.textContent = v;
  });
}

function load(id) {
  current = data[id];
  steps = current.steps;
  lastK = -2;
  video.pause();
  video.src = current.video;
  setRate();
  const heading = current.heading || current.title;
  $("title").textContent = heading;
  document.title = heading;
  const d = current.discussion;
  $("discussion").hidden = !d;
  $("d-title").textContent = d?.title || "";
  $("d-sub").textContent = d?.subtitle || "";
  rich($("d-text"), d?.text || "");
  $("d-code").hidden = !d?.code;
  $("d-pre").textContent = d?.code || "";
  $("copy").textContent = "Copy";
  buildCards();
  buildLegend();
  render();
}

function go(delta) {
  const cur = stepIndex(video.currentTime);
  let k = cur + delta;
  if (delta < 0 && cur >= 0 && video.currentTime - steps[cur].t > 0.3) k = cur;
  k = Math.min(Math.max(k, -1), steps.length - 1);
  video.pause();
  video.currentTime = k < 0 ? 0 : steps[k].t;
}

function tick() {
  render();
  if (!video.paused) requestAnimationFrame(tick);
}

const updateButton = () => {
  $("start").textContent = !video.paused
    ? "Pause"
    : video.currentTime > 0 && !video.ended
      ? "Resume"
      : "Start";
};

video.addEventListener("play", () => requestAnimationFrame(tick));
["loadedmetadata", "seeked", "pause", "ended"].forEach((e) => video.addEventListener(e, render));
["play", "pause", "ended", "seeked"].forEach((e) => video.addEventListener(e, updateButton));

$("start").addEventListener("click", () => {
  if (!video.paused) video.pause();
  else {
    if (video.ended) video.currentTime = 0;
    video.play();
  }
});

$("reset").addEventListener("click", () => {
  video.pause();
  video.currentTime = 0;
});

$("prev").addEventListener("click", () => go(-1));
$("next").addEventListener("click", () => go(1));
$("speed").addEventListener("change", setRate);

$("copy").addEventListener("click", () => {
  navigator.clipboard.writeText($("d-pre").textContent);
  $("copy").textContent = "Copied";
});

$("progress").addEventListener("click", (e) => {
  const r = e.currentTarget.getBoundingClientRect();
  video.currentTime = ((e.clientX - r.left) / r.width) * video.duration;
});

fetch("steps.json")
  .then((r) => r.json())
  .then((json) => {
    data = json;
    const sel = $("animation");
    const id = currentId();
    const first = data[id] ? id : Object.keys(data)[0];
    const group = data[first].group;
    Object.entries(data)
      .filter(([, v]) => v.group === group)
      .forEach(([key, v]) => sel.add(new Option(v.title, key)));
    sel.value = first;
    history.replaceState(null, "", `?id=${first}`);
    if (sel.options.length < 2) sel.parentElement.style.display = "none";
    sel.addEventListener("change", () => {
      history.replaceState(null, "", `?id=${sel.value}`);
      load(sel.value);
    });
    load(sel.value);
  });
