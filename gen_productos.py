#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las paginas individuales de producto (SEO) a partir de PRODATA en index.html.
Una pagina por producto en /productos/<slug>.html, trilingue (ES/EN/PT) con selector,
JSON-LD Product y meta SEO en espanol. Fuente unica de la ficha rica: PRODATA."""
import json, re, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "index.html")
OUT  = os.path.join(ROOT, "productos")
SITE = "https://tega.com.ar"  # canonical base (ajustar si cambia el dominio definitivo)

# ── 1. Extraer PRODATA (JSON valido) de index.html ──
src = open(SRC, encoding="utf-8").read()
m = re.search(r"const PRODATA = (\{.*?\});\s*\n", src, re.S)
if not m:
    raise SystemExit("No se encontro PRODATA en index.html")
PRODATA = json.loads(m.group(1))

# ── 2. Metadatos por producto (orden = grid del landing) ──
# key, slug, nombre, imagen, logo submarca, tipo, n
PRODUCTS = [
    ("crane",     "tega-crane",     "Tega Crane",     "crane",     "struct",  1),
    ("powerlift", "power-lift",     "Power Lift",     "powerlift", "aparejo", 2),
    ("ultralift", "ultra-lift",     "Ultra Lift",     "powerlift", "aparejo", 3),
    ("antiex",    "anti-explosivo", "Anti Explosivo", "antiex",    "special", 4),
    ("chain",     "tega-chain",     "Tega Chain",     "chain",     "aparejo", 5),
    ("kit",       "tega-kit",       "Tega Kit",       "kit",       "access",  6),
    ("radio",     "radiolift",      "Radiolift",      "radio",     "access",  7),
    ("movicar",   "movicar",        "Movicar",        "movicar",   "special", 8),
]

# Etiqueta de categoria (numero / texto) por idioma
CAT = {
    "crane":     {"es":"01 / Puentes grúa & pórticos","en":"01 / Bridge cranes & gantries","pt":"01 / Pontes rolantes & pórticos"},
    "powerlift": {"es":"02 / Aparejos a cable","en":"02 / Wire rope hoists","pt":"02 / Talhas a cabo"},
    "ultralift": {"es":"03 / Aparejos alta capacidad","en":"03 / High-capacity hoists","pt":"03 / Talhas alta capacidade"},
    "antiex":    {"es":"04 / Áreas clasificadas Ex","en":"04 / Classified Ex areas","pt":"04 / Áreas classificadas Ex"},
    "chain":     {"es":"05 / Aparejos a cadena","en":"05 / Chain hoists","pt":"05 / Talhas a corrente"},
    "kit":       {"es":"06 / Kit para armado","en":"06 / Crane build kit","pt":"06 / Kit para montagem"},
    "radio":     {"es":"07 / Comando inalámbrico","en":"07 / Wireless control","pt":"07 / Comando sem fio"},
    "movicar":   {"es":"08 / Apiladoras","en":"08 / Stackers","pt":"08 / Empilhadeiras"},
}

PTYPE = {
    "struct":  {"es":"Estructuras","en":"Structures","pt":"Estruturas"},
    "aparejo": {"es":"Aparejos","en":"Hoists","pt":"Talhas"},
    "access":  {"es":"Accesorios","en":"Accessories","pt":"Acessórios"},
    "special": {"es":"Equipos especiales","en":"Special equipment","pt":"Equipamentos especiais"},
}

# Meta description SEO (espanol, ~150 car.)
SEO_DESC = {
    "crane":     "Puentes grúa, pórticos, semipórticos y plumas TEGA. La gama más completa, fabricada en Argentina bajo normas FEM, ASME y CMAA. Hasta 200 t y 40 m de luz.",
    "powerlift": "Power Lift: aparejo eléctrico a cable de acero TEGA. Robusto y versátil, freno WESTON-TEGA, control 24V, clasificación FEM 1Bm–3m. Fabricación argentina.",
    "ultralift": "Ultra Lift: aparejo eléctrico a cable de nueva generación. Izaje casi vertical, hasta 80.000 kg, tablero NEMA 4 y variador de frecuencia. Fabricación TEGA.",
    "antiex":    "Equipos de izaje antiexplosivos TEGA para áreas clasificadas (ATEX / NEC). La división Ex más importante de Sudamérica. Petroquímica, minería, oil & gas.",
    "chain":     "Tega Chain: aparejo eléctrico a cadena grado 80, compacto y eficiente. Hasta 10 t, doble freno y apto para ambientes agresivos. Fabricación argentina.",
    "kit":       "Tega Kit: componentes electromecánicos para armar tu propio puente grúa. De 0,5 a 20 t, normas FEM y CMAA, aparejo pre-cableado. Fabricación TEGA.",
    "radio":     "Radiolift: radiocomando inalámbrico TEGA (tecnología Telecrane) para puentes grúa y aparejos. Alcance hasta 300 m, compatible con todas las marcas.",
    "movicar":   "Movicar: apiladoras electrohidráulicas TEGA, silenciosas y sin emisiones. Hasta 1.000 kg y 3,2 m de elevación. Para fábricas, depósitos y expedición.",
}

# ── 3. Strings de interfaz (3 idiomas) ──
TXT = {
    "es": {
        "ptype.struct":"Estructuras","ptype.aparejo":"Aparejos","ptype.access":"Accesorios","ptype.special":"Equipos especiales",
        "nav.products":"Productos","nav.industries":"Industrias","nav.services":"Servicios",
        "nav.history":"Quiénes Somos","nav.contact":"Contacto","nav.requestConsult":"Solicitar consulta",
        "crumb.home":"Inicio","crumb.products":"Productos",
        "back":"← Volver a productos","cta.quote":"Solicitar cotización","cta.contact":"Contactar a un especialista",
        "lbl.caps":"Características principales","lbl.configs":"Configuraciones disponibles",
        "lbl.diffs":"Diferenciadores clave","lbl.sectors":"Sectores de aplicación",
        "lbl.components":"Componentes antideflagrantes","lbl.norms":"Normas y certificaciones",
        "band.title":"¿Necesita asesoramiento sobre este equipo?",
        "band.text":"Nuestro equipo técnico lo ayuda a definir la solución exacta para su operación.",
        "footer.rights":"Aparejos, Grúas y Apiladoras S.A. — Buenos Aires, Argentina.",
        "footer.privacy":"Política de Privacidad",
    },
    "en": {
        "ptype.struct":"Structures","ptype.aparejo":"Hoists","ptype.access":"Accessories","ptype.special":"Special equipment",
        "nav.products":"Products","nav.industries":"Industries","nav.services":"Services",
        "nav.history":"About Us","nav.contact":"Contact","nav.requestConsult":"Request a consultation",
        "crumb.home":"Home","crumb.products":"Products",
        "back":"← Back to products","cta.quote":"Request a quote","cta.contact":"Talk to a specialist",
        "lbl.caps":"Key specifications","lbl.configs":"Available configurations",
        "lbl.diffs":"Key differentiators","lbl.sectors":"Application sectors",
        "lbl.components":"Explosion-proof components","lbl.norms":"Standards & certifications",
        "band.title":"Need advice on this equipment?",
        "band.text":"Our engineering team helps you define the exact solution for your operation.",
        "footer.rights":"Aparejos, Grúas y Apiladoras S.A. — Buenos Aires, Argentina.",
        "footer.privacy":"Privacy Policy",
    },
    "pt": {
        "ptype.struct":"Estruturas","ptype.aparejo":"Talhas","ptype.access":"Acessórios","ptype.special":"Equipamentos especiais",
        "nav.products":"Produtos","nav.industries":"Indústrias","nav.services":"Serviços",
        "nav.history":"Quem Somos","nav.contact":"Contato","nav.requestConsult":"Solicitar consulta",
        "crumb.home":"Início","crumb.products":"Produtos",
        "back":"← Voltar aos produtos","cta.quote":"Solicitar cotação","cta.contact":"Falar com um especialista",
        "lbl.caps":"Características principais","lbl.configs":"Configurações disponíveis",
        "lbl.diffs":"Diferenciais-chave","lbl.sectors":"Setores de aplicação",
        "lbl.components":"Componentes antiexplosão","lbl.norms":"Normas e certificações",
        "band.title":"Precisa de assessoria sobre este equipamento?",
        "band.text":"Nossa equipe técnica ajuda você a definir a solução exata para sua operação.",
        "footer.rights":"Aparejos, Grúas y Apiladoras S.A. — Buenos Aires, Argentina.",
        "footer.privacy":"Política de Privacidade",
    },
}

LANGS = ["es","en","pt"]

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--y:#FFD200;--ink:#0A0A0A;--mid:#666662;--fog:#D4CFC4;--line:#E6E0D2;--bg:#F7F3E8;--card:#FFFDF5;--dark:#0E0E0C;--radius-btn:10px;--display:'Montserrat',sans-serif;--body:'DM Sans',sans-serif}
html{scroll-behavior:smooth}
body{font-family:var(--body);background:var(--bg);color:var(--ink);line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 32px}
/* nav */
nav{position:sticky;top:0;z-index:50;background:rgba(247,243,232,0.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.navin{max-width:1180px;margin:0 auto;padding:0 32px;height:66px;display:flex;align-items:center}
.nav-logo{display:flex;align-items:center;margin-right:38px;flex-shrink:0}
.nav-logo img{height:32px;width:auto}
.nav-links{display:flex;gap:26px;flex:1}
.nav-links a{font-size:15px;font-weight:500;color:var(--mid);text-decoration:none;transition:color .15s}
.nav-links a:hover{color:var(--ink)}
.nav-right{display:flex;align-items:center;gap:14px}
.nav-lang{display:flex;align-items:center;gap:2px}
.nav-lang button{background:none;border:none;padding:6px 9px;font-family:var(--body);font-size:13px;font-weight:500;color:var(--mid);cursor:pointer}
.nav-lang button.active{color:var(--ink);font-weight:700}
.nav-lang span{color:var(--fog)}
.btn-primary{background:var(--y);color:var(--ink);padding:11px 22px;border-radius:var(--radius-btn);border:none;font-family:var(--body);font-size:14px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:8px;transition:background .15s,transform .1s}
.btn-primary:hover{background:#FFDE3A;transform:translateY(-1px)}
.btn-ghost{background:none;border:1px solid var(--line);color:var(--ink);padding:11px 22px;border-radius:var(--radius-btn);font-family:var(--body);font-size:14px;font-weight:600;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:8px;transition:border-color .15s}
.btn-ghost:hover{border-color:var(--ink)}
/* breadcrumb */
.crumb{padding:22px 0 0;font-size:13px;color:var(--mid)}
.crumb a{color:var(--mid);text-decoration:none}.crumb a:hover{color:var(--ink)}
.crumb span{color:var(--fog);margin:0 8px}
.crumb b{color:var(--ink);font-weight:600}
/* hero */
.hero{display:grid;grid-template-columns:1fr 1fr;gap:54px;align-items:center;padding:40px 0 64px}
.h-tag{font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--mid)}
.h-type{display:inline-block;margin-bottom:16px;margin-top:14px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--ink)}
.h-titlerow{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
h1{font-family:var(--display);font-weight:800;font-size:clamp(34px,4.6vw,56px);letter-spacing:-0.02em;line-height:1.02}
.h-logo{height:54px;width:auto;border-radius:11px;box-shadow:0 4px 14px rgba(70,58,0,0.16);flex-shrink:0}
.h-lead{font-size:17px;color:#33332f;margin:20px 0 26px;max-width:560px}
.h-actions{display:flex;gap:12px;flex-wrap:wrap}
.h-img{border-radius:18px;overflow:hidden;box-shadow:0 24px 60px -24px rgba(40,33,0,0.4);background:var(--card);border:1px solid var(--line)}
.h-img img{width:100%;height:100%;object-fit:cover;object-position:center 30%;aspect-ratio:4/5}
/* caps */
.caps{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:36px 0 0}
.cap{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.cap-k{font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mid);margin-bottom:6px}
.cap-v{font-family:var(--display);font-weight:800;font-size:21px;letter-spacing:-0.01em}
/* sections */
section.blk{padding:18px 0}
.blk-label{font-family:var(--display);font-weight:800;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink);margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.list{display:flex;flex-direction:column;gap:11px}
.li{display:flex;gap:11px;align-items:flex-start;font-size:15.5px;color:#2c2c29}
.li-ic{flex-shrink:0;width:20px;height:20px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;margin-top:2px}
.li-ic.check{background:rgba(255,210,0,0.22);color:#7a6500}
.li-ic.star{background:var(--ink);color:var(--y)}
.chips{display:flex;flex-wrap:wrap;gap:9px}
.chip{font-size:13px;font-weight:600;padding:8px 14px;border-radius:999px;background:#fff;border:1px solid var(--line)}
.chip.red{border-color:#E2B4A6;background:#FBF1EC;color:#8a3a22}
.comps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.comp{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:16px 18px}
.comp-n{font-weight:700;font-size:15px;margin-bottom:4px}
.comp-s{font-size:13.5px;color:var(--mid)}
.norms{display:flex;flex-wrap:wrap;gap:9px}
.norm{font-size:12.5px;font-weight:600;padding:7px 13px;border-radius:8px;background:#EEF3F8;border:1px solid #D4E0EC;color:#2c4a66}
.norm.red{background:#FBF1EC;border-color:#E2B4A6;color:#8a3a22}
/* band */
.band{margin:56px 0 0;background:var(--dark);color:#fff;border-radius:22px;padding:48px 52px;display:flex;align-items:center;justify-content:space-between;gap:32px;flex-wrap:wrap}
.band h2{font-family:var(--display);font-weight:800;font-size:clamp(22px,2.6vw,30px);letter-spacing:-0.01em;line-height:1.15}
.band p{color:rgba(255,255,255,0.62);font-size:16px;margin-top:10px;max-width:520px}
/* footer */
footer{margin-top:64px;background:var(--dark);color:#fff;padding:40px 0}
.foot{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
.foot img{height:30px}
.f-copy{font-size:13px;color:rgba(255,255,255,0.4)}
.f-copy a{color:rgba(255,255,255,0.6);text-decoration:none}.f-copy a:hover{color:#fff}
@media(max-width:860px){
  .nav-links{display:none}
  .navin{height:60px}
  .nav-logo{margin-right:0}
  .nav-logo img{height:24px}
  .nav-lang span{display:none}
  .nav-lang button{padding:5px 7px;font-size:12px}
  .btn-primary{padding:9px 14px;font-size:13px}
  .hero{grid-template-columns:1fr;gap:30px;padding:24px 0 44px}
  .h-img{order:-1}
  .h-titlerow{gap:12px}
  h1{font-size:clamp(30px,8vw,44px)}
  .two{grid-template-columns:1fr;gap:26px}
  .band{padding:34px 28px}
  .wrap,.navin{padding:0 20px}
}
"""

def esc(s):
    return html.escape(s, quote=True)

def render_dynamic_html(d, lang, txt):
    """Bloques que dependen del idioma (se generan en ES por defecto y se re-renderizan por JS)."""
    parts = []
    # caps
    caps = d.get("caps") or []
    if caps:
        cap_html = "".join(f'<div class="cap"><div class="cap-k">{esc(k)}</div><div class="cap-v">{esc(v)}</div></div>' for k,v in caps)
        parts.append(f'<div class="caps" id="d-caps">{cap_html}</div>')
    else:
        parts.append('<div class="caps" id="d-caps" style="display:none"></div>')
    return "\n".join(parts)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="../assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="../assets/favicon-512.png">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="product">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{ogimage}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{jsonld}
</script>
<style>{css}</style>
</head>
<body>
<nav>
  <div class="navin">
    <a class="nav-logo" href="../index.html" aria-label="TEGA">
      <img src="../assets/tega-logo-header.png" alt="TEGA — Aparejos, Grúas y Apiladoras S.A." onerror="this.src='../assets/tega-logo.png'">
    </a>
    <div class="nav-links">
      <a href="../index.html#productos" data-i18n="nav.products">Productos</a>
      <a href="../index.html#industrias" data-i18n="nav.industries">Industrias</a>
      <a href="../index.html#servicios" data-i18n="nav.services">Servicios</a>
      <a href="../quienes-somos.html" data-i18n="nav.history">Quiénes Somos</a>
      <a href="../index.html#contacto" data-i18n="nav.contact">Contacto</a>
    </div>
    <div class="nav-right">
      <div class="nav-lang">
        <button data-lang="es" class="active" onclick="setLang('es')">ES</button>
        <span>/</span><button data-lang="en" onclick="setLang('en')">EN</button>
        <span>/</span><button data-lang="pt" onclick="setLang('pt')">PT</button>
      </div>
      <a class="btn-primary" href="../index.html#contacto" data-i18n="nav.requestConsult">Solicitar consulta</a>
    </div>
  </div>
</nav>

<div class="wrap">
  <div class="crumb">
    <a href="../index.html" data-i18n="crumb.home">Inicio</a><span>/</span>
    <a href="../index.html#productos" data-i18n="crumb.products">Productos</a><span>/</span>
    <b>{name}</b>
  </div>

  <header class="hero">
    <div class="hero-txt">
      <div class="h-tag" id="d-cat" data-dyn="cat">{cat}</div>
      <span class="h-type" data-i18n="ptype.{ptype}">{ptype_label}</span>
      <div class="h-titlerow">
        <h1>{name}</h1>
        <img class="h-logo" src="../assets/submarcas/{logo}.png" alt="{name}">
      </div>
      <p class="h-lead" id="d-desc" data-dyn="desc">{desc_body}</p>
      <div class="h-actions">
        <a class="btn-primary" href="../index.html#contacto" data-i18n="cta.quote">Solicitar cotización</a>
        <a class="btn-ghost" href="../index.html#productos" data-i18n="back">← Volver a productos</a>
      </div>
    </div>
    <div class="h-img"><img src="../assets/prod/{key}.jpg" alt="{name} — TEGA" loading="eager"></div>
  </header>

  {caps_html}

  <main id="dyn-main">{dyn_sections}</main>

  <div class="band">
    <div>
      <h2 data-i18n="band.title">¿Necesita asesoramiento sobre este equipo?</h2>
      <p data-i18n="band.text">Nuestro equipo técnico lo ayuda a definir la solución exacta para su operación.</p>
    </div>
    <a class="btn-primary" href="../index.html#contacto" data-i18n="cta.contact">Contactar a un especialista</a>
  </div>
</div>

<footer>
  <div class="wrap foot">
    <img src="https://www.tega.com.ar/img/tega-logo-y-texto.png" alt="TEGA" style="filter:brightness(0) invert(1)" onerror="this.style.display='none'">
    <span class="f-copy">© 2026 TEGA <span data-i18n="footer.rights">Aparejos, Grúas y Apiladoras S.A. — Buenos Aires, Argentina.</span> · <a href="../privacidad.html" data-i18n="footer.privacy">Política de Privacidad</a></span>
  </div>
</footer>

<script>
const TXT = {txt_json};
const DATA = {data_json};
const CAT = {cat_json};
const LBL = {lbl_json};
let lang = 'es';

function buildSections(lang){{
  const d = DATA[lang] || DATA.es;
  const L = TXT[lang] || TXT.es;
  let h = '';
  // Sectores (chips rojos)
  if((d.sectors||[]).length){{
    h += '<section class="blk"><div class="blk-label">'+L['lbl.sectors']+'</div><div class="chips">'+
      d.sectors.map(s=>'<span class="chip red">'+s+'</span>').join('')+'</div></section>';
  }}
  // Componentes
  if((d.components||[]).length){{
    h += '<section class="blk"><div class="blk-label">'+L['lbl.components']+'</div><div class="comps">'+
      d.components.map(c=>'<div class="comp"><div class="comp-n">'+c[0]+'</div><div class="comp-s">'+c[1]+'</div></div>').join('')+'</div></section>';
  }}
  // Configuraciones + Diferenciadores (dos columnas)
  const hasCfg=(d.configs||[]).length, hasDiff=(d.diffs||[]).length;
  if(hasCfg||hasDiff){{
    h += '<section class="blk"><div class="two">';
    if(hasCfg){{
      h += '<div><div class="blk-label">'+L['lbl.configs']+'</div><div class="list">'+
        d.configs.map(x=>'<div class="li"><span class="li-ic check">✓</span><span>'+x+'</span></div>').join('')+'</div></div>';
    }}
    if(hasDiff){{
      h += '<div><div class="blk-label">'+L['lbl.diffs']+'</div><div class="list">'+
        d.diffs.map(x=>'<div class="li"><span class="li-ic star">★</span><span>'+x+'</span></div>').join('')+'</div></div>';
    }}
    h += '</div></section>';
  }}
  // Normas
  if((d.norms||[]).length){{
    h += '<section class="blk"><div class="blk-label">'+L['lbl.norms']+'</div><div class="norms">'+
      d.norms.map(n=>'<span class="norm'+(n[1]==='red'?' red':'')+'">'+n[0]+'</span>').join('')+'</div></section>';
  }}
  return h;
}}

function renderDynamic(lang){{
  const d = DATA[lang] || DATA.es;
  // caps
  const capsEl = document.getElementById('d-caps');
  if(capsEl){{
    const caps = d.caps||[];
    capsEl.innerHTML = caps.map(c=>'<div class="cap"><div class="cap-k">'+c[0]+'</div><div class="cap-v">'+c[1]+'</div></div>').join('');
    capsEl.style.display = caps.length? '' : 'none';
  }}
  const descEl = document.getElementById('d-desc'); if(descEl) descEl.textContent = d.desc||'';
  const catEl = document.getElementById('d-cat'); if(catEl) catEl.textContent = CAT[lang]||CAT.es;
  document.getElementById('dyn-main').innerHTML = buildSections(lang);
}}

function setLang(code){{
  if(!TXT[code]) return;
  lang = code;
  document.documentElement.lang = code;
  document.querySelectorAll('[data-i18n]').forEach(el=>{{
    const v = TXT[code][el.dataset.i18n];
    if(v!==undefined) el.textContent = v;
  }});
  document.querySelectorAll('.nav-lang button').forEach(b=>b.classList.toggle('active', b.dataset.lang===code));
  renderDynamic(code);
  try{{ localStorage.setItem('tega-lang', code); }}catch(e){{}}
}}
try{{ const s=localStorage.getItem('tega-lang'); if(s&&TXT[s]&&s!=='es') setLang(s); }}catch(e){{}}
</script>
</body>
</html>
"""

os.makedirs(OUT, exist_ok=True)

def build_jsonld(name, desc, img, cat_es):
    obj = {
        "@context":"https://schema.org/",
        "@type":"Product",
        "name": name,
        "image": img,
        "description": desc,
        "category": cat_es,
        "brand": {"@type":"Brand","name":"TEGA"},
        "manufacturer": {
            "@type":"Organization",
            "name":"TEGA Aparejos, Grúas y Apiladoras S.A.",
            "url": SITE,
            "address":{"@type":"PostalAddress","addressLocality":"Buenos Aires","addressCountry":"AR"}
        }
    }
    return json.dumps(obj, ensure_ascii=False, indent=2)

for key, slug, name, logo, ptype, n in PRODUCTS:
    pd = PRODATA[key]
    # DATA por idioma: desc, caps, configs, diffs, sectors, components, norms
    data = {}
    for lg in LANGS:
        b = pd.get(lg, pd.get("es", {}))
        data[lg] = {
            "desc": b.get("desc",""),
            "caps": b.get("caps",[]),
            "configs": b.get("configs",[]),
            "diffs": b.get("diffs",[]),
            "sectors": b.get("sectors",[]),
            "components": b.get("components",[]),
            "norms": b.get("norms",[]),
        }
    cat_map = {lg: CAT[key][lg] for lg in LANGS}
    desc_es = pd["es"]["desc"]
    seo = SEO_DESC[key]
    canonical = f"{SITE}/productos/{slug}"
    ogimage = f"{SITE}/assets/prod/{key}.jpg"
    title = f"{name} — {PTYPE[ptype]['es']} TEGA | Aparejos, Grúas y Apiladoras"
    jsonld = build_jsonld(name, seo, ogimage, CAT[key]["es"])

    caps_html = render_dynamic_html(data["es"], "es", TXT["es"])
    dyn_sections = ""  # se rellena por JS en carga; pero generamos ES para SEO/no-JS:
    # generar secciones ES estaticas para crawlers (se sobreescriben por JS identico)
    import types
    d_es = data["es"]
    def static_sections(d, L):
        h=""
        if d["sectors"]:
            h+='<section class="blk"><div class="blk-label">'+esc(L["lbl.sectors"])+'</div><div class="chips">'+"".join('<span class="chip red">'+esc(s)+'</span>' for s in d["sectors"])+'</div></section>'
        if d["components"]:
            h+='<section class="blk"><div class="blk-label">'+esc(L["lbl.components"])+'</div><div class="comps">'+"".join('<div class="comp"><div class="comp-n">'+esc(c[0])+'</div><div class="comp-s">'+esc(c[1])+'</div></div>' for c in d["components"])+'</div></section>'
        if d["configs"] or d["diffs"]:
            h+='<section class="blk"><div class="two">'
            if d["configs"]:
                h+='<div><div class="blk-label">'+esc(L["lbl.configs"])+'</div><div class="list">'+"".join('<div class="li"><span class="li-ic check">✓</span><span>'+esc(x)+'</span></div>' for x in d["configs"])+'</div></div>'
            if d["diffs"]:
                h+='<div><div class="blk-label">'+esc(L["lbl.diffs"])+'</div><div class="list">'+"".join('<div class="li"><span class="li-ic star">★</span><span>'+esc(x)+'</span></div>' for x in d["diffs"])+'</div></div>'
            h+='</div></section>'
        if d["norms"]:
            h+='<section class="blk"><div class="blk-label">'+esc(L["lbl.norms"])+'</div><div class="norms">'+"".join('<span class="norm'+(' red' if nrm[1]=="red" else '')+'">'+esc(nrm[0])+'</span>' for nrm in d["norms"])+'</div></section>'
        return h
    dyn_sections = static_sections(d_es, TXT["es"])

    page = PAGE.format(
        title=esc(title),
        desc=esc(seo),
        canonical=canonical,
        ogtitle=esc(f"{name} — TEGA"),
        ogimage=ogimage,
        jsonld=jsonld,
        css=CSS,
        name=esc(name),
        cat=esc(cat_map["es"]),
        ptype=ptype,
        ptype_label=esc(PTYPE[ptype]["es"]),
        desc_body=esc(desc_es),
        key=key,
        logo=logo,
        caps_html=caps_html,
        dyn_sections=dyn_sections,
        txt_json=json.dumps(TXT, ensure_ascii=False),
        data_json=json.dumps(data, ensure_ascii=False),
        cat_json=json.dumps(cat_map, ensure_ascii=False),
        lbl_json=json.dumps({lg:{k:TXT[lg][k] for k in TXT[lg] if k.startswith("lbl.")} for lg in LANGS}, ensure_ascii=False),
    )
    out_path = os.path.join(OUT, slug + ".html")
    open(out_path, "w", encoding="utf-8").write(page)
    print("escrito:", os.path.relpath(out_path, ROOT))

print("OK -", len(PRODUCTS), "paginas")
