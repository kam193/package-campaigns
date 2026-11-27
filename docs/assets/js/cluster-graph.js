(function () {
  const COLORS = { CAMPAIGN: "#2A629A", CLUSTER: "#8A5A44", PACKAGE: "#2D936C", ABUSE: "#B5446E" };
  const ICONS = {
    CAMPAIGN: "M12 8H4A2 2 0 0 0 2 10V14A2 2 0 0 0 4 16H5V20A1 1 0 0 0 6 21H8A1 1 0 0 0 9 20V16H12L17 20V4L12 8M21.5 12C21.5 13.71 20.54 15.26 19 16V8C20.53 8.75 21.5 10.3 21.5 12Z",
    CLUSTER: "M12 5.5A3.5 3.5 0 0 1 15.5 9A3.5 3.5 0 0 1 12 12.5A3.5 3.5 0 0 1 8.5 9A3.5 3.5 0 0 1 12 5.5M5 8C5.56 8 6.08 8.15 6.53 8.42C6.38 9.85 6.8 11.27 7.66 12.38C7.16 13.34 6.16 14 5 14A3 3 0 0 1 2 11A3 3 0 0 1 5 8M19 8A3 3 0 0 1 22 11A3 3 0 0 1 19 14C17.84 14 16.84 13.34 16.34 12.38C17.2 11.27 17.62 9.85 17.47 8.42C17.92 8.15 18.44 8 19 8M5.5 18.25C5.5 16.18 8.41 14.5 12 14.5C15.59 14.5 18.5 16.18 18.5 18.25V20H5.5V18.25M0 20V18.5C0 17.11 1.89 15.94 4.45 15.6C3.86 16.28 3.5 17.22 3.5 18.25V20H0M24 20H20.5V18.25C20.5 17.22 20.14 16.28 19.55 15.6C22.11 15.94 24 17.11 24 18.5V20Z",
    PACKAGE: "M21 16.5C21 16.88 20.79 17.21 20.47 17.38L12.57 21.82C12.41 21.94 12.21 22 12 22S11.59 21.94 11.43 21.82L3.53 17.38C3.21 17.21 3 16.88 3 16.5V7.5C3 7.12 3.21 6.79 3.53 6.62L11.43 2.18C11.59 2.06 11.79 2 12 2S12.41 2.06 12.57 2.18L20.47 6.62C20.79 6.79 21 7.12 21 7.5V16.5Z",
    ABUSE: "M14.4 6L14 4H5V21H7V14H12.6L13 16H20V6H14.4Z",
  };
  const icon = (kind) =>
    "data:image/svg+xml;utf8," +
    encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24"><path fill="white" d="${ICONS[kind]}"/></svg>`);

  const style = [
    {
      selector: "node",
      style: {
        label: "data(label)", "font-size": 8, "text-valign": "bottom", "text-margin-y": 5,
        "text-wrap": "ellipsis", "text-max-width": 90, color: "#000",
        width: 44, height: 44, "background-color": (n) => COLORS[n.data("kind")],
        "background-image": (n) => icon(n.data("kind")), "background-fit": "none", "background-width": "60%", "background-height": "60%",
        "background-position-x": "50%", "background-position-y": "50%", "background-clip": "none",
      },
    },
    {
      selector: "edge",
      style: {
        width: 2, "curve-style": "bezier", "line-color": "#999", label: "data(label)",
        "font-size": 8, color: "#000", "text-rotation": "autorotate",
        "text-background-color": "#fff", "text-background-opacity": 0.85, "text-background-padding": 2,
      },
    },
    { selector: 'edge[confidence = "low"]', style: { "line-style": "dotted", width: 1 } },
    { selector: 'edge[confidence = "medium"]', style: { "line-style": "dashed" } },
    { selector: 'edge[confidence = "high"]', style: { width: 3 } },
  ];

  function init(container) {
    const elements = JSON.parse(container.dataset.graph);
    const cy = cytoscape({ container, elements, style, wheelSensitivity: 0.3 });
    const removed = [];
    const shown = { PACKAGE: false, ABUSE: false };

    const layout = () => {
      cy.nodes().forEach((n) => {
        const hidden = removed.includes(n) || (n.hasClass("optional") && !shown[n.data("kind")]);
        n.style("display", hidden ? "none" : "element");
      });
      cy.elements(":visible").layout({
        name: "cose", animate: false, fit: true, padding: 40, nodeRepulsion: () => 40000,
        idealEdgeLength: () => 110, nodeOverlap: 30, componentSpacing: 120, gravity: 0.2, numIter: 2000,
      }).run();
    };

    const popup = document.createElement("div");
    popup.className = "cluster-graph-popup";
    popup.hidden = true;
    container.append(popup);
    const closePopup = () => (popup.hidden = true);

    const openPopup = (n) => {
      const { kind, label, url, packages } = n.data();
      popup.replaceChildren();
      const add = (tag, text, parent = popup) => {
        const el = document.createElement(tag);
        el.textContent = text;
        parent.append(el);
        return el;
      };
      add("small", kind.charAt(0) + kind.slice(1).toLowerCase()).style.color = COLORS[kind];
      add("strong", label);
      if (packages !== undefined) add("span", `Packages: ${packages}`);
      if (url) {
        const link = add("a", "Open details");
        link.href = url;
      }
      const hide = add("button", "Remove from graph");
      hide.type = "button";
      hide.className = "md-button cluster-graph-button";
      hide.onclick = () => {
        removed.push(n);
        closePopup();
        layout();
      };
      const pos = n.renderedPosition();
      popup.hidden = false;
      popup.style.left = Math.min(pos.x + 28, container.clientWidth - popup.offsetWidth - 4) + "px";
      popup.style.top = Math.min(pos.y, container.clientHeight - popup.offsetHeight - 4) + "px";
    };

    cy.on("tap", (e) => (e.target === cy ? closePopup() : e.target.isNode() && openPopup(e.target)));
    cy.on("viewport drag", closePopup);

    const bar = document.createElement("div");
    bar.className = "cluster-graph-bar";
    const toggle = (kind, text) => {
      const label = document.createElement("label");
      const box = document.createElement("input");
      box.type = "checkbox";
      box.onchange = () => {
        shown[kind] = box.checked;
        layout();
      };
      label.append(box, " " + text);
      bar.append(label);
    };
    const button = (text, action) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "md-button md-button--primary cluster-graph-button";
      b.textContent = text;
      b.onclick = action;
      bar.append(b);
    };
    toggle("PACKAGE", "Packages");
    toggle("ABUSE", "Abuse categories");
    button("Reset", () => {
      removed.length = 0;
      layout();
    });
    button("Fullscreen", () => {
      if (document.fullscreenElement) document.exitFullscreen();
      else container.parentElement.requestFullscreen();
    });
    container.before(bar);
    document.addEventListener("fullscreenchange", () => setTimeout(() => cy.resize().fit(), 100));
    layout();
  }

  function start() {
    document.querySelectorAll(".cluster-graph").forEach((c) => {
      if (!c.dataset.ready) {
        c.dataset.ready = "1";
        const wrap = document.createElement("div");
        wrap.className = "cluster-graph-wrap";
        c.replaceWith(wrap);
        wrap.append(c);
        init(c);
      }
    });
  }

  if (typeof document$ !== "undefined") document$.subscribe(start);
  else document.addEventListener("DOMContentLoaded", start);
})();
