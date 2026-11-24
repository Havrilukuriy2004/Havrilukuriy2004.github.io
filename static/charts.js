/* Interactive charts for posts. Each .ichart-box has data-chart (JSON spec) and data-lang.
   Spec: {type, x, series:[{name:{uk,en}, y, kind, dash, axis, fill, band:{lo,hi}}], yaxis:{uk,en}, ...} */
(function () {
  const PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#7a5cc4", "#5b6b7a"];
  const T = (v, lang) => (v && typeof v === "object" && !Array.isArray(v)) ? (v[lang] ?? v.uk ?? "") : (v ?? "");
  function layout(spec, lang) {
    const base = {
      margin: {l: 58, r: 18, t: 10, b: 46}, height: spec.height || 380,
      font: {family: "Arial, Helvetica, sans-serif", size: 12.5, color: "#222"},
      paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
      legend: {orientation: "h", y: -0.18, x: 0},
      hovermode: spec.hovermode || "x unified",
      xaxis: {gridcolor: "#eee", linecolor: "#bbb", title: {text: T(spec.xaxis, lang)}, type: spec.xtype || undefined,
              zeroline: false, tickformat: spec.xtickformat || undefined},
      yaxis: {gridcolor: "#eee", linecolor: "#bbb", title: {text: T(spec.yaxis, lang)}, zerolinecolor: "#999",
              ticksuffix: spec.ysuffix || "", tickformat: spec.ytickformat || undefined},
      barmode: spec.barmode || undefined, shapes: [], annotations: []
    };
    (spec.vlines || []).forEach(v => {
      base.shapes.push({type: "line", x0: v.x, x1: v.x, yref: "paper", y0: 0, y1: 1, line: {color: "#999", width: 1, dash: "dot"}});
      if (v.label) base.annotations.push({x: v.x, yref: "paper", y: 1, text: T(v.label, lang), showarrow: false, font: {size: 11, color: "#666"}, xanchor: "left"});
    });
    if (spec.hline !== undefined) base.shapes.push({type: "line", xref: "paper", x0: 0, x1: 1, y0: spec.hline, y1: spec.hline, line: {color: "#999", width: 1}});
    return base;
  }
  function traces(spec, lang) {
    const out = [];
    spec.series.forEach((s, i) => {
      const color = s.color || PAL[i % PAL.length];
      const x = T(s.x || spec.x, lang);
      const name = T(s.name, lang);
      if (s.band) {
        out.push({x, y: s.band.hi, type: "scatter", mode: "lines", line: {width: 0}, hoverinfo: "skip", showlegend: false});
        out.push({x, y: s.band.lo, type: "scatter", mode: "lines", line: {width: 0}, fill: "tonexty",
                  fillcolor: (s.bandcolor || color) + "2e", hoverinfo: "skip", showlegend: false});
      }
      const kind = s.kind || spec.type || "line";
      if (kind === "bar") {
        out.push({x, y: s.y, type: "bar", name, marker: {color}, hovertemplate: "%{y:.2f}" + (spec.ysuffix || "") + "<extra>" + name + "</extra>"});
      } else if (kind === "scatter") {
        out.push({x, y: s.y, type: "scatter", mode: "markers", name, marker: {color, size: 8, line: {color: "#fff", width: 1}},
                  text: s.text, hovertemplate: (s.text ? "%{text}<br>" : "") + "%{x:.1f}; %{y:.1f}<extra>" + name + "</extra>"});
      } else {
        out.push({x, y: s.y, type: "scatter", mode: s.markers ? "lines+markers" : "lines", name,
                  line: {color, width: s.width || 2, dash: s.dash || "solid"}, marker: {size: 6},
                  fill: s.fill || undefined, stackgroup: s.stack || undefined,
                  hovertemplate: "%{y:.2f}" + (spec.ysuffix || "") + "<extra>" + name + "</extra>"});
      }
    });
    return out;
  }
  function draw(el) {
    const lang = el.dataset.lang || document.documentElement.lang || "uk";
    fetch(el.dataset.chart).then(r => r.json()).then(spec => {
      Plotly.newPlot(el, traces(spec, lang), layout(spec, lang), {displaylogo: false, responsive: true,
        modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d"]});
    }).catch(() => { el.innerHTML = "<p class='muted'>" + (lang === "en" ? "Chart data could not be loaded." : "Не вдалося завантажити дані графіка.") + "</p>"; });
  }
  function init() {
    if (!window.Plotly) { setTimeout(init, 150); return; }
    document.querySelectorAll(".ichart-box").forEach(draw);
  }
  document.addEventListener("DOMContentLoaded", init);
})();
