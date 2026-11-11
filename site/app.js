const $ = (id) => document.getElementById(id);
const video = $("video");
let data = {};
let current = null;
let steps = [];
let lastK = -1;

const tex = (el, s) => katex.render(s, el, { throwOnError: false, strict: false });

const stepIndex = (t) => {
  let k = 0;
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
  const step = steps[k];
  $("status").textContent = `Step: ${k + 1} / ${steps.length} | ${step.label}`;
  $("stepcount").textContent = `Step ${k + 1} of ${steps.length}`;
  current.cards.forEach((c, i) => {
    const el = $("cards").children[i].querySelector(".value");
    if (c.math) tex(el, step.values[i]);
    else el.textContent = step.values[i];
  });
}

function load(id) {
  current = data[id];
  steps = current.steps;
  lastK = -1;
  video.pause();
  video.src = current.video;
  setRate();
  $("title").textContent = current.title;
  document.title = current.title;
  if (current.formula) tex($("formula"), current.formula);
  else $("formula").textContent = "";
  $("description").textContent = current.description || "";
  buildCards();
  buildLegend();
  render();
}

function go(delta) {
  const cur = stepIndex(video.currentTime);
  let k = cur + delta;
  if (delta < 0 && video.currentTime - steps[cur].t > 0.3) k = cur;
  k = Math.min(Math.max(k, 0), steps.length - 1);
  video.pause();
  video.currentTime = steps[k].t;
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

$("progress").addEventListener("click", (e) => {
  const r = e.currentTarget.getBoundingClientRect();
  video.currentTime = ((e.clientX - r.left) / r.width) * video.duration;
});

fetch("steps.json")
  .then((r) => r.json())
  .then((json) => {
    data = json;
    const sel = $("animation");
    Object.entries(data).forEach(([id, v]) => sel.add(new Option(v.title, id)));
    sel.addEventListener("change", () => load(sel.value));
    load(sel.value);
  });
