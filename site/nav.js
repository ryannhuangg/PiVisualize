const make = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
};

const link = (href, text, cls) => {
  const a = make("a", cls, text);
  a.href = href;
  return a;
};

const pageUrl = (id) => `visualize.html?id=${id}#${id}`;

const currentId = () => new URLSearchParams(location.search).get("id") || location.hash.slice(1);

function buildNav(site) {
  const nav = document.getElementById("nav");
  site.forEach((s) => {
    const menu = make("div", "menu");
    const items = make("div", "menu-items");
    s.groups.forEach((g) =>
      g.topics.forEach((t) => {
        if (!t.pages) items.append(link("#", t.name, "soon"));
        else t.pages.forEach((p) => items.append(link(pageUrl(p.id), `${t.name}: ${p.label}`)));
      })
    );
    menu.append(make("button", "", s.name), items);
    nav.append(menu);
  });
}

function buildColumns(site) {
  const box = document.getElementById("columns");
  if (!box) return;
  site.forEach((s) => {
    const col = make("section", "column");
    col.append(make("h2", "", s.title || s.name));
    s.groups.forEach((g) => {
      col.append(make("h3", "", g.name));
      g.topics.forEach((t) => {
        if (!t.pages) return col.append(link("#", t.name, "soon"));
        const d = make("details");
        d.append(make("summary", "", t.name));
        t.pages.forEach((p) => d.append(link(pageUrl(p.id), p.label)));
        col.append(d);
      });
    });
    box.append(col);
  });
}

function buildPager(site, steps) {
  const box = document.getElementById("next-page");
  if (!box) return;
  const param = currentId();
  const id = steps[param] ? param : Object.keys(steps)[0];
  const group = steps[id].group;
  site.forEach((s) =>
    s.groups.forEach((g) => {
      const pages = g.topics.flatMap((t) =>
        (t.pages || []).map((p) => ({ id: p.id, name: `${t.name}: ${p.label}` }))
      );
      const i = pages.findIndex((p) => p.id === group);
      if (i < 0) return;
      if (i > 0) box.append(link(pageUrl(pages[i - 1].id), `\u2190 Previous: ${pages[i - 1].name}`, "next-link"));
      if (i < pages.length - 1)
        box.append(link(pageUrl(pages[i + 1].id), `Next: ${pages[i + 1].name} \u2192`, "next-link forward"));
    })
  );
}

Promise.all([fetch("site.json"), fetch("steps.json")])
  .then((rs) => Promise.all(rs.map((r) => r.json())))
  .then(([site, steps]) => {
    buildNav(site);
    buildColumns(site);
    buildPager(site, steps);
  });
