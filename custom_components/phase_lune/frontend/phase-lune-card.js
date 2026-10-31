/* Carte Lovelace « Phase de la Lune » — livrée avec l'intégration phase_lune. */
(() => {
  const DEFAULTS = {
    title: "Phase de la Lune",
    entity: "sensor.phase_lune",
    image_path: "/phase_lune/moon_phases",
    language: "fr",
    show_illumination: true,
    show_anecdote: true,
  };
  const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const HEX = "data:image/svg+xml;utf8," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="56" height="97" viewBox="0 0 56 97">' +
    '<path d="M28 66L0 50V17L28 1l28 16v33L28 66zm0 31L0 81V66l28 16 28-16v15L28 97z" fill="none" stroke="#5a5470" stroke-width="2" opacity=".55"/></svg>');
  const L = {
    fr: { cur: "Phase actuelle", ill: "Illumination", know: "Anecdote du jour" },
    en: { cur: "Current phase", ill: "Illumination", know: "Fact of the day" },
  };
  const LABELS = { title: "Titre", entity: "Entité", image_path: "Chemin des images", language: "Langue", show_illumination: "Afficher l’illumination", show_anecdote: "Afficher l’anecdote du jour" };
  let ANEC = null;
  const loadAnec = (cb) => { if (ANEC || loadAnec.p) return; loadAnec.p = fetch("/phase_lune/anecdotes.json").then((r) => r.json()).then((j) => { ANEC = j; cb(); }).catch(() => {}); };
  const EN = { new_moon: "New moon", waxing_crescent: "Waxing crescent", first_quarter: "First quarter", waxing_gibbous: "Waxing gibbous", full_moon: "Full moon", waning_gibbous: "Waning gibbous", last_quarter: "Last quarter", waning_crescent: "Waning crescent" };

  class PhaseLuneCard extends HTMLElement {
    static getConfigForm() {
      return { schema: [
        { name: "title", selector: { text: {} } },
        { name: "entity", selector: { entity: { domain: "sensor" } } },
        { name: "image_path", selector: { text: {} } },
        { name: "language", selector: { select: { options: ["fr", "en"] } } },
        { name: "show_illumination", selector: { boolean: {} } },
        { name: "show_anecdote", selector: { boolean: {} } },
      ], computeLabel: (x) => LABELS[x.name] || x.name };
    }
    static getStubConfig() { return { ...DEFAULTS }; }
    setConfig(c) {
      const cfg = { ...DEFAULTS, ...(c || {}) };
      cfg.image_path = DEFAULTS.image_path; // chemin forcé : PNG servies par l'intégration
      if (cfg.show_anecdote === undefined || cfg.show_anecdote === null) cfg.show_anecdote = true;
      this._c = cfg; this._render();
    }
    set hass(h) { this._h = h; this._render(); }
    getCardSize() { return 9; }
    _render() {
      if (!this._c || !this._h) return;
      if (!this.shadowRoot) this.attachShadow({ mode: "open" });
      const c = this._c, st = this._h.states, s = st[c.entity] || st["sensor.phase_lune"] || st["sensor.phase_de_la_lune"];
      if (!s) { this.shadowRoot.innerHTML = `<ha-card><div style="padding:16px">Entité introuvable : ${esc(c.entity)}</div></ha-card>`; return; }
      const a = s.attributes || {}, en = c.language === "en", t = L[en ? "en" : "fr"];
      const slug = a.phase_slug || st["sensor.phase_lune_slug"]?.state || "full_moon";
      const img = a.image_slug || slug;
      const label = en ? EN[slug] || slug : (a.phase_fr || s.state);
      const pick = (k) => { for (const o of [s, st["sensor.phase_lune_anecdote"], st["sensor.phase_lune"], st["sensor.phase_lune_slug"]]) { const v = o?.attributes?.[k]; if (v) return v; } return ""; };
      const poetic = en ? (pick("poetic_en") || pick("poetic")) : pick("poetic");
      let anec = en ? (pick("anecdote_en") || pick("anecdote")) : pick("anecdote");
      if (!anec) {
        const d = new Date(), doy = Math.min(365, Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 864e5));
        if (ANEC) { const x = ANEC[doy - 1] || ANEC[0]; anec = en ? x.en : x.fr; } else loadAnec(() => this._render());
      }
      const ill = a.illumination ?? st["sensor.phase_lune_illumination"]?.state ?? pick("illumination");
      const [head, ...rest] = String(poetic || "").split(/(?<=\.)\s/);
      this.shadowRoot.innerHTML = `
<style>
 ha-card{overflow:hidden;color:#fff;background:#2b2838 url("${HEX}") repeat;background-size:56px 97px;
  box-shadow:inset 0 0 120px rgba(0,0,0,.6);padding:20px 22px;font-family:var(--ha-font-family-body,Roboto,sans-serif)}
 h2{margin:0 0 14px;font-size:1.7em;font-weight:700;text-shadow:0 2px 6px #000}
 img{width:min(48%,220px);aspect-ratio:1;border-radius:50%;display:block;margin:4px 0 18px;filter:drop-shadow(0 0 18px rgba(255,255,255,.18))}
 p{margin:10px 0;font-size:1.08em;line-height:1.4;text-shadow:0 1px 4px #000}
 .anec{background:rgba(255,255,255,.08);border-left:3px solid #f5d76e;padding:10px 12px;border-radius:6px;font-size:1em}
 b{font-weight:700} .s{opacity:.85;font-size:.95em}
</style>
<ha-card>
 <h2>🌙 ${esc(c.title)}</h2>
 <img src="${esc(c.image_path)}/${esc(img)}.png" alt="${esc(label)}" onerror="this.style.display='none'">
 <p>🌕 <b>${t.cur} : ${esc(label)}</b></p>
 ${poetic ? `<p>🌗 <b>${esc(head)}</b> ${esc(rest.join(" "))}</p>` : ""}
 ${c.show_anecdote !== false && anec ? `<p class="anec">✨ <b>${t.know} :</b> ${esc(anec)}</p>` : ""}
 ${c.show_illumination !== false && ill !== "" && ill != null ? `<p class="s">💡 ${t.ill} : ${esc(ill)} %</p>` : ""}
</ha-card>`;
    }
  }
  if (!customElements.get("phase-lune-card")) customElements.define("phase-lune-card", PhaseLuneCard);
  window.customCards = window.customCards || [];
  if (!window.customCards.some((x) => x.type === "phase-lune-card"))
    window.customCards.push({ type: "phase-lune-card", name: "Phase de la Lune", description: "Phase lunaire, texte poétique et anecdote du jour (365).", preview: true });
})();
