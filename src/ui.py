"""Interfaz HTML de CompyFI. La intención es mantener el diseño de las capturas."""
import html
from lexer import tokenizar_lista
from parser_lr0 import (
    analizar,
    construir_automata,
    formatear_item,
    formatear_produccion,
    obtener_no_terminales,
    obtener_producciones,
    obtener_terminales,
)
from sdt import explicar_resultado, validar_tipos
from tac import generar_tac

CODIGO_INICIAL = """{
    i;
    while ( i < i ) {
        i;
    }
    if ( i < i ) { }
}"""

EJEMPLOS = {
    "valido": {
        "titulo": "Bloque con while e if",
        "subtitulo": "Acepta parser, semantica y TAC",
        "codigo": CODIGO_INICIAL,
        "explicacion": "Acepta porque las sentencias cumplen S -> i ;, S -> while ( C ) B y S -> if ( C ) B.",
    },
    "vacio": {
        "titulo": "Bloque vacio",
        "subtitulo": "Acepta B -> { }",
        "codigo": "{ }",
        "explicacion": "Acepta porque la produccion B -> { } permite un bloque sin sentencias.",
    },
    "sin_punto_y_coma": {
        "titulo": "Falta punto y coma",
        "subtitulo": "Error sintactico",
        "codigo": "{\n    i\n}",
        "explicacion": "No acepta porque S -> i ; exige punto y coma. Si el parser falla, no se ejecuta semantica ni TAC.",
    },
    "condicion_incompleta": {
        "titulo": "Condicion incompleta",
        "subtitulo": "Error sintactico",
        "codigo": "{\n    while ( i < ) {\n        i;\n    }\n}",
        "explicacion": "No acepta porque C debe cumplir C -> i < i.",
    },
    "falta_llave": {
        "titulo": "Falta llave de cierre",
        "subtitulo": "Error sintactico",
        "codigo": "{\n    i;\n    while ( i < i ) {\n        i;\n    }",
        "explicacion": "No acepta porque B -> { W } requiere cerrar el bloque con }.",
    },
}

REFERENCIA_COMPILADORES = """
<section class="references">
    <p><strong>Referencia:</strong> [1] R. A. Dávila Pérez, “Compiladores: apuntes de clase proporcionados en pizarrón,” Facultad de Ingeniería, Universidad Nacional Autónoma de México, semestre 2026-2, 2026.</p>
</section>
"""

REFERENCIAS_ANTECEDENTES = """
<section class="references">
    <h3>Referencias IEEE</h3>
    <p>[1] L. P. Arellano Mendoza, “Lenguajes Formales y Autómatas: Introducción y Conceptos,” diapositivas de clase, n.d.</p>
    <p>[2] L. P. Arellano Mendoza, “Expresiones Regulares y Lenguajes,” diapositivas de clase, n.d.</p>
    <p>[3] L. P. Arellano Mendoza, “Gramáticas Regulares y Autómatas Finitos,” diapositivas de clase, n.d.</p>
    <p>[4] L. P. Arellano Mendoza, “Gramáticas de Contexto Libre,” diapositivas de clase, n.d.</p>
    <p>[5] R. A. Dávila Pérez, “Compiladores: análisis sintáctico y resolución de ambigüedad,” apuntes de clase proporcionados en pizarrón, Facultad de Ingeniería, Universidad Nacional Autónoma de México, semestre 2026-2, 2026.</p>
    <p>[6] L. P. Arellano Mendoza, “Autómatas Push Down,” diapositivas de clase, n.d.</p>
</section>
"""

CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#f4f8ff;color:#0f172a;font-family:'Poppins',Arial,Helvetica,sans-serif;overflow:hidden;font-size:14px}
.app-shell{display:grid;grid-template-columns:215px minmax(0,1fr);height:100vh}
.sidebar{height:100vh;background:rgba(255,255,255,.96);border-right:1px solid #dbeafe;padding:18px 12px;overflow:hidden;box-shadow:8px 0 26px rgba(15,23,42,.04);display:flex;flex-direction:column}
.brand{padding:4px 4px 14px;border-bottom:1px solid #dbeafe;margin-bottom:12px}.brand h1{margin:0;color:#4b63f0;font-size:23px;font-weight:700}.brand p{margin:4px 0 0;color:#64748b;font-size:11px}
.nav{overflow:auto;padding-right:2px}.nav-main{flex:1;min-height:0}.nav-bottom{border-top:1px solid #dbeafe;padding-top:10px;margin-top:10px}.nav-section-title{font-size:11px;color:#1e3a8a;font-weight:800;margin:16px 10px 8px;text-transform:uppercase}
.nav a{display:block;text-decoration:none;color:#334155;padding:10px 12px;border-radius:5px;margin:6px 0;font-weight:500;font-size:12px;transition:.2s}.nav a.primary{font-weight:700}.nav a.primary.active,.nav a.primary:hover{background:#4b63f0;color:white;box-shadow:0 8px 18px rgba(37,99,235,.18)}.nav a.active:not(.primary),.nav a:hover:not(.primary){background:#4b63f0;color:white;box-shadow:0 8px 18px rgba(37,99,235,.16)}
.sidebar-mascot{width:150px;margin:16px auto 8px;text-align:center;flex:0 0 auto}.sidebar-mascot img{display:block;width:100%;height:auto;max-height:210px;object-fit:contain}.bubble{border:1px solid #bfdbfe;background:#f8fbff;border-radius:5px;padding:11px;color:#1e3a8a;font-size:10px;line-height:1.35;text-align:center;font-weight:700;position:relative}.bubble:before{content:"";position:absolute;top:-8px;left:50%;width:14px;height:14px;background:#f8fbff;border-left:1px solid #bfdbfe;border-top:1px solid #bfdbfe;transform:translateX(-50%) rotate(45deg)}
.app-main{height:100vh;overflow:auto;padding:30px 34px 56px}.section-title{margin-bottom:22px}.section-title h2{font-size:36px;line-height:1.05;margin:0 0 10px;color:#0f172a}.section-title p{color:#64748b;font-size:13px;max-width:850px;line-height:1.65;margin:0}.eyebrow{display:inline-block;color:#2563eb;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px}
.panel,.split-panel,.unam-card,.info-card,.creator-card{background:white;border:1px solid #dbeafe;border-radius:5px;padding:18px;box-shadow:0 10px 24px rgba(15,23,42,.05)}.panel{margin:16px 0}.panel h3,.info-card h3{margin:0 0 12px;color:#1e3a8a;font-size:18px}.panel p,.info-card p{line-height:1.7;color:#334155;margin:0}.grammar-banner,.note{background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid #4b63f0;border-radius:4px;padding:14px 18px;margin:0 0 16px;line-height:1.55;color:#0f172a}.grammar-banner strong,.note strong{color:#1e3a8a}
.compiler-grid{display:grid;grid-template-columns:225px minmax(290px,1fr) minmax(480px,1.65fr);gap:18px;align-items:start}.code-card,.results-card,.examples{margin-top:0}.card-heading{display:flex;justify-content:space-between;gap:10px;align-items:center;border-bottom:1px solid #e5efff;margin:-18px -18px 18px;padding:16px 18px}.card-heading h3{margin:0}.card-heading span,.result-status{color:#2f7d32;font-size:11px}.card-heading span.bad{color:#b91c1c}.results-card{position:relative;overflow:hidden}.results-card>h3{margin-bottom:18px}.result-status{position:absolute;right:18px;top:20px}.result-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 -18px 0;padding:12px 18px;border-top:1px solid #e5efff;border-bottom:1px solid #e5efff;background:#f8fbff}.tab-btn{text-decoration:none;color:#4b63f0;border:1px solid #bfdbfe;background:white;border-radius:7px;padding:8px 12px;font-size:11px;font-weight:700;cursor:pointer;margin:0;box-shadow:none;transition:.18s}.tab-btn:hover{background:#eff6ff;transform:translateY(-1px)}.tab-btn.selected{background:#4b63f0;color:white;border-color:#4b63f0}.result-pane-shell{padding-top:14px}.tab-pane{display:none;animation:fadeIn .18s ease}.tab-pane.active{display:block}.pane-title{font-size:14px;font-weight:800;color:#1e3a8a;margin:0 0 12px}.pane-subtitle{font-size:14px;color:#1e3a8a;margin:18px 0 10px}.pane-help,.explain-text{font-size:12px;line-height:1.7;color:#475569;margin:0 0 12px}@keyframes fadeIn{from{opacity:.45;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}
.example{display:block;border:1px solid #dbeafe;border-radius:5px;padding:12px 12px;margin:9px 0;color:#334155;text-decoration:none;background:#f8fbff}.example strong{display:block;color:#4b63f0;font-size:12px}.example span{display:block;color:#64748b;font-size:11px;margin-top:4px;line-height:1.45}.example.active{border-color:#4b63f0;background:#eff6ff}.example-detail{background:white;border-radius:5px;margin-top:16px;padding:0 2px;color:#334155;line-height:1.65}.example-detail h4{font-size:15px;margin:10px 0 6px;color:#0f172a}.example-detail p{margin:0;color:#475569}.badge{display:inline-block;border-radius:5px;padding:6px 9px;font-weight:700;font-size:11px}.badge.ok{background:#dcfce7;color:#166534}.badge.bad{background:#fee2e2;color:#991b1b}
textarea{width:100%;min-height:220px;border:1px solid #bfdbfe;border-radius:5px;padding:14px;font-family:Consolas,'Courier New',monospace;font-size:13px;line-height:1.55;resize:vertical;background:#fbfdff;color:#0f172a}button{margin-top:14px;background:#4b63f0;color:white;border:0;border-radius:5px;padding:12px 20px;font-weight:700;cursor:pointer;font-family:inherit;box-shadow:0 8px 18px rgba(37,99,235,.2)}
.detail-output{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px;margin-top:18px}.detail-output .panel{margin:0}.split-panel{display:grid;grid-template-columns:minmax(300px,1fr) minmax(360px,1.1fr);gap:16px;align-items:start}.mini-card{background:#f8fbff;border:1px solid #dbeafe;border-radius:5px;padding:14px;line-height:1.65;color:#475569;margin-bottom:12px}
pre,.dark-code{background:#0f172a;color:#dbeafe;padding:16px;border-radius:5px;overflow:auto;line-height:1.7;font-size:13px;margin:0;font-family:Consolas,'Courier New',monospace}.table-scroll{overflow:auto;max-height:430px;border:1px solid #dbeafe;border-radius:6px;background:white}table{width:100%;border-collapse:collapse;font-size:12px;background:white}th,td{border-bottom:1px solid #dbeafe;padding:9px;text-align:left;vertical-align:top;white-space:pre-wrap;line-height:1.5}th{background:#eff6ff;color:#1e3a8a;font-weight:700;position:sticky;top:0;z-index:2}.notice{padding:14px;border-radius:5px;background:#eff6ff;border:1px solid #bfdbfe;color:#1e3a8a;line-height:1.65}.notice.ok{background:#f0fdf4;color:#14532d;border-color:#bbf7d0}.notice.bad{background:#fef2f2;color:#991b1b;border-color:#fecaca}.result-box{border-left:5px solid currentColor}.stop-note{color:#475569;line-height:1.6}
.graph-scroll{overflow:auto;max-height:460px;border:1px solid #dbeafe;border-radius:5px;background:#f8fbff;padding:16px}.canon-svg{display:block;min-width:1120px}.edge{fill:none;stroke:#2563eb;stroke-width:2;opacity:.78}.edge-label{fill:#1e3a8a;font-size:14px;font-weight:700;paint-order:stroke;stroke:white;stroke-width:5px;stroke-linejoin:round}.node circle{fill:white;stroke:#2563eb;stroke-width:3;filter:drop-shadow(0 8px 14px rgba(37,99,235,.18))}.state{text-anchor:middle;font-size:19px;font-weight:700;fill:#0f172a}
.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}.lexico-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:20px 0}.step-list{display:grid;gap:10px;margin:16px 0}.step-list article{background:white;border:1px solid #dbeafe;border-radius:5px;padding:12px 14px;box-shadow:0 8px 18px rgba(15,23,42,.04)}.step-list span{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:5px;background:#4b63f0;color:white;font-weight:700;margin-right:10px}.references{border-top:1px solid #bfdbfe;margin:22px 0 0;padding:14px;color:#334155;font-size:11px}.references p{line-height:1.6;margin:5px 0}.unam-card{margin:18px 0}.unam-card h3{font-size:20px;color:#4b63f0;margin:0 0 8px}.unam-card strong{display:block;margin:5px 0;color:#0f172a}.temario-grid{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}.concept-grid,.flow-diagram,.creator-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}.concept-grid article,.flow-diagram article{background:#f8fbff;border:1px solid #dbeafe;border-radius:5px;padding:14px}.concept-grid strong,.flow-diagram strong{display:block;color:#1e3a8a;margin-bottom:7px}.concept-grid p,.flow-diagram span{color:#475569;line-height:1.55;font-size:12px}.creator-card strong{display:block;color:#0f172a;margin-bottom:8px}.creator-card span{color:#475569;font-size:13px}
.route-row{display:grid;grid-template-columns:130px 1fr 130px 1fr 130px 1fr 130px;align-items:center;gap:8px;margin:16px 0}.route-box{background:#f8fbff;border:1px solid #bfdbfe;border-radius:5px;padding:12px;min-height:64px}.route-arrow{text-align:center;color:#4b63f0;font-size:20px;font-weight:700}.route-box strong{display:block;color:#1e3a8a;margin-bottom:4px}.route-box span{font-size:11px;color:#475569}

.grammar-mini-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:12px 0 16px}
.grammar-mini-card{background:#f8fbff;border:1px solid #dbeafe;border-radius:6px;padding:13px;line-height:1.55;color:#334155}
.grammar-mini-card strong{display:block;color:#1e3a8a;margin-bottom:6px}.grammar-list{margin:8px 0 0 18px;color:#334155;line-height:1.65;padding:0}
.canonical-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;max-height:520px;overflow:auto;padding-right:4px}.state-card{background:#ffffff;border:1px solid #dbeafe;border-radius:7px;padding:14px;box-shadow:0 8px 18px rgba(15,23,42,.04)}.state-card h4{margin:0 0 9px;color:#4b63f0;font-size:14px}.state-card pre{font-size:12px;line-height:1.6;padding:12px;max-height:180px}.state-transitions{font-size:11px;color:#475569;line-height:1.55;margin-top:9px}.state-transitions span{display:inline-block;background:#eff6ff;border:1px solid #bfdbfe;border-radius:999px;padding:4px 8px;margin:3px 4px 0 0;color:#1e3a8a;font-weight:700}
.tac-note{background:#0f172a;color:#dbeafe;border-radius:6px;padding:18px;margin:0;overflow:auto;font-family:Consolas,'Courier New',monospace;font-size:13px;line-height:1.75}.tac-note .tac-title{color:#bfdbfe;font-weight:700;margin-bottom:10px}.tac-note .tac-line{white-space:pre}.sdt-rules{background:#0f172a;color:#dbeafe;border-radius:6px;padding:18px;overflow:auto;font-family:Consolas,'Courier New',monospace;font-size:13px;line-height:1.75;margin:0 0 14px}.sdt-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-top:12px}.sdt-summary article{background:#f8fbff;border:1px solid #dbeafe;border-radius:6px;padding:12px;line-height:1.6;color:#334155}.sdt-summary strong{display:block;color:#1e3a8a;margin-bottom:5px}

@media(max-width:1100px){.compiler-grid,.split-panel,.lexico-grid{grid-template-columns:1fr}.detail-output{grid-template-columns:1fr}.route-row{grid-template-columns:1fr}.route-arrow{display:none}}
@media(max-width:720px){body{overflow:auto}.app-shell{display:block;height:auto}.sidebar{height:auto;overflow:visible}.app-main{height:auto;overflow:visible;padding:26px 18px}.section-title h2{font-size:32px}}
"""


def esc(valor):
    return html.escape(str(valor), quote=True)


def tabla_html(filas, encabezados):
    head = "".join(f"<th>{esc(celda)}</th>" for celda in encabezados)
    body = []
    for fila in filas:
        body.append("<tr>" + "".join(f"<td>{esc(celda)}</td>" for celda in fila) + "</tr>")
    return f"<div class='table-scroll'><table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"


def procesar_codigo(codigo):
    tokens, errores_lexicos = tokenizar_lista(codigo)
    automata = construir_automata()
    if errores_lexicos:
        return {"codigo": codigo, "tokens": tokens, "exito_parser": False, "traza": [{"stack": "0", "input": "UNKNOWN", "action": "error lexico"}], "automata": automata, "error_info": {"estado": 0, "token": "UNKNOWN", "lexema": errores_lexicos[0], "esperados": [], "mensaje": "El lexer encontro un token desconocido."}, "exito_semantico": False, "mensaje_semantico": "No se ejecuto semantica porque hubo error lexico.", "tabla_simbolos": [], "tac": [], "mensaje_tac": "No se genero TAC porque hubo error lexico."}
    exito_parser, traza, automata, error_info = analizar(tokens)
    if not exito_parser:
        return {"codigo": codigo, "tokens": tokens, "exito_parser": False, "traza": traza, "automata": automata, "error_info": error_info, "exito_semantico": False, "mensaje_semantico": "No se ejecuto semantica porque el parser no acepto la entrada.", "tabla_simbolos": [], "tac": [], "mensaje_tac": "No se genero TAC porque hubo error sintactico."}
    exito_semantico, mensaje_semantico, tabla_simbolos = validar_tipos(tokens)
    tac, mensaje_tac = generar_tac(tokens, tabla_simbolos) if exito_semantico else ([], "No se genero TAC porque hubo error semantico.")
    return {"codigo": codigo, "tokens": tokens, "exito_parser": True, "traza": traza, "automata": automata, "error_info": None, "exito_semantico": exito_semantico, "mensaje_semantico": mensaje_semantico, "tabla_simbolos": tabla_simbolos, "tac": tac, "mensaje_tac": mensaje_tac}


def render_gramatica():
    return "<pre>" + esc("\n".join(formatear_produccion(i) for i in range(len(obtener_producciones())))) + "</pre>"


def render_tokens(tokens):
    return tabla_html([(i + 1, tipo, lexema) for i, (tipo, lexema) in enumerate(tokens)], ["#", "Token", "Lexema"])


def render_estados(automata):
    return tabla_html([(f"I{i}", "\n".join(formatear_item(item) for item in sorted(estado))) for i, estado in enumerate(automata["estados"])], ["Estado", "Items LR(0)"])


def render_transiciones(automata):
    return tabla_html([(f"I{o}", s, f"I{d}") for (o, s), d in sorted(automata["transiciones"].items())], ["Estado", "Simbolo", "Destino"])


def render_tabla_lr0(automata):
    terminales = obtener_terminales()
    no_terminales = [nt for nt in obtener_no_terminales() if nt != "P'"]
    encabezados = ["Estado"] + terminales + no_terminales
    filas = []
    for i in range(len(automata["estados"])):
        fila = [f"I{i}"]
        fila.extend(automata["accion"].get((i, t), "") for t in terminales)
        fila.extend(f"I{automata['ir_a'][(i, nt)]}" if (i, nt) in automata["ir_a"] else "" for nt in no_terminales)
        filas.append(tuple(fila))
    return tabla_html(filas, encabezados)


def render_traza(traza):
    return tabla_html([(i + 1, p["stack"], p["input"], p["action"]) for i, p in enumerate(traza)], ["Paso", "Stack", "Input", "Action"])


def render_simbolos(tabla):
    if not tabla:
        return "<p class='notice bad'>No se genero tabla de simbolos.</p>"
    filas = [(s["nombre"], s["categoria"], s["tipo"], s["valor"], "si" if s["declarada"] else "no", "si" if s["usada"] else "no") for s in tabla]
    return tabla_html(filas, ["Nombre", "Categoria", "Tipo", "Valor", "Declarada", "Usada"])


def render_tac(tac, mensaje):
    if not tac:
        return f"<p class='notice'>{esc(mensaje)}</p>"
    lineas = ["Intermediate code TAC", ""]
    for i, linea in enumerate(tac, start=1):
        lineas.append(f"{i}: {linea}")
    return "<div class='tac-note'>" + "".join(
        f"<div class='tac-line'>{esc(linea)}</div>" for linea in lineas
    ) + "</div>"


def render_sdt_tab(datos):
    reglas = """Reglas semánticas SDT con place, newTemp() y gen()
{ P'.place = P.place }
{ P.place = B.place }
{ B.place = W.place }
{ B.place = "empty_block" }
{ W.place = S.place }
{ W.place = W.place + S.place }
{ S.place = newTemp(); gen(S.place = id.lexeme) }
{ C.place = newTemp(); gen(C.place = id.left < id.right) }
{ S.place = C.place; gen(ifFalse C.place goto L) }"""
    return f"""
    <p class='explain-text'>{esc(explicar_resultado(datos['exito_parser'], datos['exito_semantico'], datos['mensaje_semantico'], datos['tac']))}</p>
    <pre class='sdt-rules'>{esc(reglas)}</pre>
    <section class='sdt-summary'>
        <article><strong>place</strong>Es un atributo semántico que recuerda dónde quedó el resultado de una producción. En este compilador se usa para conservar el resultado de una sentencia, condición o bloque.</article>
        <article><strong>newTemp()</strong>Es una función que crea variables temporales como t1, t2 o t3. Sirve cuando una operación necesita guardar un resultado intermedio.</article>
        <article><strong>gen()</strong>Es una función que genera una instrucción de TAC, por ejemplo una asignación, una comparación o un salto.</article>
    </section>
    """


def render_gramatica_tab(automata):
    conflictos = len(automata.get('conflictos', []))
    return f"""
    <p class='explain-text'>La gramática activa del compilador describe bloques con sentencias simples, sentencias while, sentencias if y condiciones relacionales de la forma i &lt; i.</p>
    <pre>{esc("P' -> P\nP  -> B\nB  -> { W } | { }\nW  -> W S | S\nS  -> while ( C ) B | if ( C ) B | i ;\nC  -> i < i")}</pre>
    <section class='grammar-mini-grid'>
        <article class='grammar-mini-card'><strong>Terminales</strong>while, if, i, &lt;, (, ), {{, }}, ; y $.</article>
        <article class='grammar-mini-card'><strong>No terminales</strong>P', P, B, W, S y C.</article>
        <article class='grammar-mini-card'><strong>Símbolo inicial</strong>P es el símbolo inicial del lenguaje y P' se agrega para aumentar la gramática.</article>
    </section>
    <p class='explain-text'>Es una gramática libre de contexto porque el lado izquierdo de cada producción contiene un solo no terminal. Por ejemplo, P, B, W, S y C aparecen individualmente del lado izquierdo y cada uno produce una cadena formada por terminales y no terminales. Esta forma permite que el parser revise la estructura del bloque sin depender del contexto que rodea a cada producción.</p>
    <p class='explain-text'>Es adecuada para LR(0) porque, con esta gramática, los estados de la colección canónica permiten decidir entre shift, reduce, accept o error sin usar símbolo de anticipación. Además, la tabla ACTION/GOTO resultante no presenta conflictos shift/reduce ni reduce/reduce.</p>
    """


def render_coleccion_canonica(automata):
    trans_por_estado = {}
    for (origen, simbolo), destino in sorted(automata['transiciones'].items()):
        trans_por_estado.setdefault(origen, []).append((simbolo, destino))
    tarjetas = []
    for i, estado in enumerate(automata['estados']):
        items = "\n".join(formatear_item(item) for item in sorted(estado))
        transiciones = trans_por_estado.get(i, [])
        if transiciones:
            chips = "".join(f"<span>{esc(simbolo)} → I{destino}</span>" for simbolo, destino in transiciones)
        else:
            chips = "<span>sin salida</span>"
        tarjetas.append(f"<article class='state-card'><h4>I{i}</h4><pre>{esc(items)}</pre><div class='state-transitions'>{chips}</div></article>")
    return "<section class='canonical-grid'>" + "".join(tarjetas) + "</section>"


def render_conflictos(automata):
    conflictos = automata["conflictos"]
    if not conflictos:
        return "<p class='notice ok'>No hay conflictos LR(0) en esta gramatica.</p>"
    filas = [(c["estado"], c["simbolo"], c["existente"], c["nueva"], c["tipo"]) for c in conflictos]
    return tabla_html(filas, ["Estado", "Simbolo", "Existente", "Nueva", "Tipo"])


def render_grafo(automata):
    estados = automata["estados"]
    columnas, sx, sy, mx, my = 4, 285, 215, 110, 100
    filas = (len(estados) + columnas - 1) // columnas
    ancho = mx * 2 + (columnas - 1) * sx
    alto = my * 2 + max(0, filas - 1) * sy
    pos = {i: (mx + (i % columnas) * sx, my + (i // columnas) * sy) for i in range(len(estados))}
    edges = []
    for (origen, simbolo), destino in sorted(automata["transiciones"].items()):
        x1, y1 = pos[origen]
        x2, y2 = pos[destino]
        if origen == destino:
            path = f"M{x1 + 40} {y1 - 20} C{x1 + 130} {y1 - 115}, {x1 + 170} {y1 + 45}, {x1 + 45} {y1 + 45}"
            lx, ly = x1 + 120, y1 - 55
        else:
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 - 52
            path = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}"
            lx, ly = cx, cy - 10
        edges.append(f"<path d='{path}' class='edge' marker-end='url(#arrow)'/><text x='{lx}' y='{ly}' class='edge-label'>{esc(simbolo)}</text>")
    nodes = []
    for i, estado in enumerate(estados):
        x, y = pos[i]
        resumen = " | ".join(formatear_item(item) for item in sorted(estado)[:3])
        nodes.append(f"<g class='node'><circle cx='{x}' cy='{y}' r='42'/><text x='{x}' y='{y + 7}' class='state'>I{i}</text><title>{esc(resumen)}</title></g>")
    return f"<div class='graph-scroll'><svg class='canon-svg' viewBox='0 0 {ancho} {alto}' width='{ancho}' height='{alto}'><defs><marker id='arrow' markerWidth='12' markerHeight='12' refX='10' refY='4' orient='auto'><path d='M0,0 L0,8 L11,4 z' fill='#2563eb'/></marker></defs>{''.join(edges)}{''.join(nodes)}</svg></div>"


def render_resultado(datos):
    if datos["exito_parser"]:
        return f"""
        <div class="notice ok result-box"><strong>Parsing Success!</strong><br>
        La cadena fue aceptada por la tabla ACTION/GOTO LR(0).<br>
        Como el analisis sintactico fue exitoso, se ejecuta la validacion semantica basica y se habilita la generacion de TAC.<br>
        Estados generados: I0 a I{len(datos['automata']['estados']) - 1}.</div>
        """
    error = datos["error_info"]
    return f"""
    <div class="notice bad result-box"><strong>Parsing error...</strong><br>
    Estado actual: I{esc(error['estado'])}<br>
    Token recibido: {esc(error['token'])}<br>
    Lexema recibido: {esc(error['lexema'])}<br>
    Se esperaba uno de: {esc(' '.join(error.get('esperados', [])) or '(ninguno)')}<br>
    {esc(error['mensaje'])}</div>
    <p class="stop-note">No se ejecuta validacion semantica ni se genera TAC porque el parser no acepto la entrada.</p>
    """


def render_compilador(datos, codigo, ejemplo_id):
    links = []
    for clave, ejemplo in EJEMPLOS.items():
        active = "active" if clave == ejemplo_id else ""
        links.append(f"<a class='example {active}' href='/index.html?view=compilador&example={clave}'><strong>{esc(ejemplo['titulo'])}</strong><span>{esc(ejemplo['subtitulo'])}</span></a>")

    ejemplo = EJEMPLOS.get(ejemplo_id, {"titulo": "Entrada manual", "explicacion": "Código capturado por el usuario."})
    estado_clase = "ok" if datos["exito_parser"] else "bad"

    tabs = [
        ("resultado", "Resultado", render_resultado(datos)),
        ("gramatica", "Gramática", render_gramatica_tab(datos["automata"])),
        ("tokens", "Tokens", render_tokens(datos["tokens"])),
        ("estados", "Estados", render_estados(datos["automata"])),
        ("transiciones", "Transiciones", render_transiciones(datos["automata"])),
        ("coleccion", "Colección canónica", render_coleccion_canonica(datos["automata"])),
        ("tabla", "ACTION/GOTO", render_tabla_lr0(datos["automata"])),
        ("traza", "Traza", render_traza(datos["traza"])),
        ("tac", "TAC", render_tac(datos["tac"], datos["mensaje_tac"])),
        ("sdt", "SDT", render_sdt_tab(datos)),
    ]

    botones = "".join(
        f"<button class='tab-btn {'selected' if i == 0 else ''}' type='button' data-tab='{tab_id}'>{esc(label)}</button>"
        for i, (tab_id, label, _) in enumerate(tabs)
    )
    paneles = "".join(
        f"<section class='tab-pane {'active' if i == 0 else ''}' id='pane-{tab_id}'><div class='pane-title'>{esc(label)}</div>{contenido}</section>"
        for i, (tab_id, label, contenido) in enumerate(tabs)
    )

    return f"""
    <section class="section-title"><h2>Compilador</h2></section>
    <section class="compiler-grid">
        <aside class="panel examples">
            <h3>Ejemplos</h3>
            {''.join(links)}
            <div class="example-detail">
                <span class="badge {estado_clase}">{'Acepta' if datos['exito_parser'] else 'No acepta'}</span>
                <h4>{esc(ejemplo['titulo'])}</h4>
                <p>{esc(ejemplo['explicacion'])}</p>
            </div>
        </aside>
        <section class="panel code-card">
            <div class="card-heading"><h3>Código fuente</h3><span class="{estado_clase}">{'Aceptado' if datos['exito_parser'] else 'No aceptado'}</span></div>
            <form method="post" action="/index.html?view=compilador">
                <textarea name="codigo">{esc(codigo)}</textarea>
                <button type="submit">Analizar</button>
            </form>
        </section>
        <section class="panel results-card">
            <h3>Resultados LR(0)</h3>
            <span class="result-status">{'Parsing Success' if datos['exito_parser'] else 'Parsing error'}</span>
            <nav class="result-tabs" aria-label="Secciones del análisis LR(0)">{botones}</nav>
            <div class="result-pane-shell">{paneles}</div>
        </section>
    </section>
    """


def render_temario():
    return """
    <section class="section-title"><h2>Temario asignatura</h2><p>Programa de estudio de Compiladores para Ingeniería en Computación.</p></section>
    <section class="unam-card"><h3>UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO</h3><strong>FACULTAD DE INGENIERÍA</strong><strong>PROGRAMA DE ESTUDIO</strong><strong>COMPILADORES</strong></section>
    <section class="info-grid temario-grid">
        <article class="info-card"><h3>Datos generales</h3><p><strong>Asignatura:</strong> Compiladores<br><strong>Clave:</strong> 0434<br><strong>Semestre:</strong> 7<br><strong>Créditos:</strong> 8</p></article>
        <article class="info-card"><h3>Área académica</h3><p><strong>División:</strong> Ingeniería Eléctrica<br><strong>Departamento:</strong> Ingeniería en Computación<br><strong>Licenciatura:</strong> Ingeniería en Computación</p></article>
        <article class="info-card"><h3>Tipo de asignatura</h3><p><strong>Obligatoria:</strong> X<br><strong>Optativa:</strong><br><strong>Modalidad:</strong> Curso teórico</p></article>
        <article class="info-card"><h3>Horas/semana</h3><p><strong>Teóricas:</strong> 4.0<br><strong>Prácticas:</strong> 0.0<br><strong>Total:</strong> 4.0</p></article>
        <article class="info-card"><h3>Horas/semestre</h3><p><strong>Teóricas:</strong> 64.0<br><strong>Prácticas:</strong> 0.0<br><strong>Total:</strong> 64.0</p></article>
        <article class="info-card"><h3>Seriación</h3><p><strong>Seriación obligatoria antecedente:</strong> Lenguajes Formales y Autómatas<br><strong>Seriación obligatoria consecuente:</strong> Ninguna</p></article>
    </section>
    <section class="panel"><h3>Objetivo(s) del curso:</h3><p>El alumno diseñará los traductores como herramientas de uso y desarrollo de sistemas de software; como también diferenciará traductores existentes para elaborar software eficiente y adecuado al tipo de problema por resolver.</p></section>
    <section class="panel"><h3>Temario</h3><table><thead><tr><th>Núm.</th><th>Nombre</th><th>Horas</th></tr></thead><tbody><tr><td>1.</td><td>Panorama general</td><td>10.0</td></tr><tr><td>2.</td><td>Análisis léxico</td><td>8.0</td></tr><tr><td>3.</td><td>Análisis sintáctico</td><td>4.0</td></tr><tr><td>4.</td><td>Análisis sintáctico descendente</td><td>8.0</td></tr><tr><td>5.</td><td>Análisis sintáctico ascendente</td><td>10.0</td></tr><tr><td>6.</td><td>Traducción dirigida por sintaxis</td><td>8.0</td></tr><tr><td>7.</td><td>Organización de memoria en tiempo de corrida</td><td>4.0</td></tr><tr><td>8.</td><td>Generación de código intermedio y análisis semántico</td><td>8.0</td></tr><tr><td>9.</td><td>Optimización y generación de código</td><td>4.0</td></tr><tr><td></td><td><strong>Total</strong></td><td><strong>64.0</strong></td></tr></tbody></table></section>
    """


def render_detalle():
    return f"""
    <section class="section-title"><span class="eyebrow">Detalle</span><h2>Detalle gramática</h2><p>Clasificación de la gramática, terminales, no terminales y razón por la que el proyecto se comporta como un compilador didáctico.</p></section>
    <section class="split-panel"><div><h3>Gramática</h3>{render_gramatica()}</div><div><article class="mini-card"><strong>Gramática libre de contexto.</strong><br>Cada producción tiene un solo no terminal en el lado izquierdo.</article><article class="mini-card"><strong>Terminales.</strong><br>while, if, i, &lt;, (, ), {{, }}, ; y $.</article><article class="mini-card"><strong>No terminales.</strong><br>P', P, B, W, S y C.</article><article class="mini-card"><strong>Adecuada para LR(0).</strong><br>La colección canónica produce una tabla ACTION/GOTO sin conflictos.</article></div></section>
    """


def render_teoria(clave):
    contenidos = {
        "lexico": ("Análisis léxico", "Primera etapa formal del compilador: convierte texto fuente en tokens.", [("Ubicación en el compilador", "El análisis léxico pertenece a la fase de análisis. Recibe el código fuente de alto nivel y prepara la entrada para el parser, junto con el análisis sintáctico y el análisis semántico."), ("Qué reconoce", "El lexer clasifica lexemas como palabras reservadas, identificadores, operadores, símbolos de puntuación, constantes, literales y caracteres especiales. En este proyecto reconoce while, if, i, paréntesis, llaves, <, punto y coma y $."), ("Qué descarta", "Durante el escaneo se omiten elementos que no forman parte de la secuencia de tokens, como tabulaciones, saltos de línea, retornos de carro y comentarios.")], ["Leer el archivo de entrada como texto.", "Avanzar carácter por carácter o por grupos de caracteres.", "Identificar patrones de palabras reservadas, identificadores, números, operadores y símbolos.", "Generar tokens con tipo y lexema; por ejemplo (\"i\", \"main\").", "Reportar error léxico si aparece un carácter que no pertenece al lenguaje."]),
        "sintactico": ("Análisis sintáctico", "Verifica si los tokens aparecen en un orden válido según una gramática.", [("Entrada del parser", "El parser recibe la salida del lexer: tokens ya clasificados. Con ellos produce una validación estructural y puede construir un árbol de análisis."), ("Gramáticas", "Una gramática se define con terminales, no terminales, reglas de producción y un símbolo inicial. En compiladores se usan principalmente gramáticas libres de contexto."), ("Top-Down y Bottom-Up", "Los parsers Top-Down intentan derivar desde el símbolo inicial. Los Bottom-Up, como LR(0), parten de los tokens e intentan reducirlos hasta llegar al símbolo inicial.")], ["Calcular la cerradura del ítem inicial de la gramática aumentada.", "Aplicar GOTO con cada símbolo que aparezca después del punto.", "Crear nuevos estados cuando aparezcan conjuntos de ítems distintos.", "Construir ACTION con terminales y GOTO con no terminales.", "Usar pila, entrada y tabla para decidir shift, reduce, accept o error."]),
        "semantico": ("Análisis semántico y SDT", "Revisa que la estructura aceptada por el parser tenga significado válido.", [("Después del parser", "El análisis semántico se ejecuta después de una aceptación sintáctica. Su función es comprobar que la estructura reconocida cumpla reglas de significado, tipos y uso de identificadores."), ("SDT", "La Traducción Dirigida por Sintaxis combina una gramática libre de contexto con reglas semánticas asociadas a producciones. Puede actualizar tabla de símbolos, evaluar expresiones o generar código."), ("Bottom-Up", "En un parser LR(0), las acciones semánticas pueden ejecutarse durante las reducciones. Si se reduce una sentencia o una condición, se puede registrar su información para la tabla de símbolos o para TAC.")], ["Ejecutar semántica solo si el parser aceptó.", "Identificar función, variable, tipo declarado, valor asignado y valor de retorno.", "Crear o actualizar la tabla de símbolos.", "Validar compatibilidad de tipos.", "Si hay error semántico, detener la generación de TAC."]),
        "tac": ("Código intermedio y TAC", "Representación intermedia entre el análisis semántico y el código objetivo.", [("Propósito", "El código intermedio funciona como puente entre el Front End y el Back End del compilador. Permite analizar, optimizar y traducir el programa sin depender de una máquina específica."), ("Representaciones", "Puede aparecer como expresiones postfijas, árboles sintácticos, grafos acíclicos dirigidos o Código de Tres Direcciones."), ("TAC", "El TAC representa operaciones mediante instrucciones de tres direcciones. Esta forma facilita el análisis, la depuración y la optimización del programa.")], []),
        "backpatching": ("Backpatching", "Técnica para completar saltos pendientes durante la generación de código intermedio.", [("Por qué existe", "En estructuras como while, for o switch-case, no siempre se conoce desde el inicio la dirección final del salto. Se deja un espacio pendiente y se rellena después."), ("Ejemplo conceptual", "L1:\nifFalse condicion goto __\ncuerpo\ngoto L1\nL2:\n\nCuando se conoce L2, se completa el salto pendiente.")], ["Generar una instrucción de salto con destino vacío.", "Guardar esa instrucción en una lista de pendientes.", "Cuando se conoce el destino real, obtener la etiqueta o número de instrucción.", "Actualizar los saltos pendientes con la dirección correcta."]),
        "optimizacion": ("Optimización de código", "Mejora el código sin cambiar el significado del programa.", [("Objetivo", "La optimización busca mejorar velocidad, rendimiento o consumo de memoria, manteniendo un tiempo de compilación razonable y conservando el comportamiento original del programa."), ("Bloques básicos", "Para optimizar TAC se identifican líderes: la primera instrucción, destinos de saltos y la instrucción posterior a un salto. Con ellos se forman bloques básicos y un grafo de flujo."), ("Memoria en ejecución", "Las estrategias de almacenamiento pueden ser estáticas, en pila o en montículo. Aunque no son optimización directa, influyen en el código generado.")], []),
    }
    if clave == "flujo":
        pasos = [("Código fuente", "entrada escrita por el usuario."), ("Análisis léxico", "elimina espacios irrelevantes y genera tokens."), ("Análisis sintáctico LR(0)", "usa gramática, cerradura, GOTO, colección canónica, ACTION/GOTO y pila para decidir shift, reduce, accept o error."), ("Análisis semántico y SDT", "valida tipos, actualiza tabla de símbolos y prepara la traducción."), ("Código intermedio TAC", "genera instrucciones de tres direcciones, como asignaciones y sentencias return."), ("Backpatching", "completa saltos pendientes cuando existan estructuras de control."), ("Optimización", "mejora TAC o código objetivo sin cambiar el significado del programa.")]
        return "<section class='section-title'><h2>Orden completo del flujo</h2><p>Ruta completa que sigue el compilador del proyecto.</p></section><section class='step-list'>" + "".join(f"<article><span>{i}</span><strong>{esc(t)}</strong>: {esc(d)}</article>" for i, (t, d) in enumerate(pasos, 1)) + "</section><section class='note'>En la versión actual, el proyecto llega hasta parser LR(0), validación semántica, tabla de símbolos, código intermedio y TAC. Backpatching y optimización quedan como contexto teórico.</section>" + REFERENCIA_COMPILADORES
    titulo, intro, cards, pasos = contenidos[clave]
    html_cards = "".join(f"<article class='info-card'><h3>{esc(h)}</h3><p>{esc(t)}</p></article>" for h, t in cards)
    html_pasos = "".join(f"<article><span>{i}</span>{esc(p)}</article>" for i, p in enumerate(pasos, 1))
    extra = ""
    if clave == "sintactico":
        extra = f"<section class='note'><strong>LR(0)</strong> es un parser ascendente de tipo shift-reduce. No utiliza símbolo de anticipación para decidir reducciones, por lo que representa una de las formas básicas de la familia LR.</section><section class='split-panel'><div><h3>Gramática aumentada</h3>{render_gramatica()}</div><div><h3>Ítems LR(0)</h3><p>Un ítem es una producción con un punto que indica cuánto se ha reconocido.</p><pre>C -> i . &lt; i</pre><p>Significa que ya se reconoció el primer identificador de la condición y falta reconocer &lt; i.</p></div></section>"
    if clave == "tac":
        extra = "<section class='panel'><h3>Formas comunes de TAC</h3><table><thead><tr><th>Forma TAC</th><th>Uso en español</th></tr></thead><tbody><tr><td>x = y op z</td><td>Operación binaria seguida de asignación.</td></tr><tr><td>x = op z</td><td>Operación unaria seguida de asignación.</td></tr><tr><td>x = y</td><td>Asignación simple.</td></tr><tr><td>if x relop y goto L</td><td>Salto condicional hacia una etiqueta.</td></tr><tr><td>goto L</td><td>Salto incondicional hacia una etiqueta.</td></tr><tr><td>A[i] = x<br>y = A[i]</td><td>Acceso y asignación en arreglos.</td></tr><tr><td>x = *p<br>*p = y</td><td>Uso de apuntadores.</td></tr></tbody></table></section>"
    if clave == "optimizacion":
        extra = "<section class='split-panel'><div><h3>Independientes de máquina</h3><ul><li>Code motion.</li><li>Loop unrolling, jamming, unswitching y peeling.</li><li>Constant folding y constant propagation.</li><li>Strength reduction.</li><li>Dead code elimination.</li><li>Common subexpression elimination.</li><li>Algebraic simplification.</li></ul></div><div><h3>Dependientes de máquina</h3><p>Se aplican sobre código objetivo y dependen de la arquitectura física: asignación de registros, planificación de instrucciones y optimizaciones de mirilla.</p></div></section>"
    code = ""
    if clave == "lexico":
        code = "<pre class='lexico-code'>{ while ( i &lt; i ) { i; } }\n\nTokens esperados:\n{, while, (, i, &lt;, i, ), {, i, ;, }, }, $</pre><section class='note'>Si el lexer detecta un error, el análisis sintáctico no debe continuar, ya que el parser necesita recibir una secuencia de tokens válida y bien clasificada.</section>"
    return f"<section class='section-title'><h2>{esc(titulo)}</h2><p>{esc(intro)}</p></section><section class='info-grid lexico-grid'>{html_cards}</section>{extra}<section class='step-list'>{html_pasos}</section>{code}{REFERENCIA_COMPILADORES}"


def render_antecedentes():
    return """
    <section class="section-title"><h2>Antecedentes</h2><p>Fundamentos de lenguajes formales, autómatas y gramáticas relacionados con compiladores.</p></section>
    <section class="note">Los antecedentes se resumen en las siguientes relaciones: el código fuente se estudia como cadena de símbolos, el lexer se apoya en lenguajes regulares y autómatas finitos, y el parser se apoya en gramáticas libres de contexto y estructuras de pila.</section>
    <section class="panel"><h3>Ejemplos básicos de lenguaje formal</h3><div class="concept-grid"><article><strong>Símbolos</strong><p>Letras: a. Dígitos: 0, 1, 9. Reservadas: while, if. Operadores: &lt;.</p></article><article><strong>Alfabeto</strong><p>Σ = {a, b}. Σ = {0, 1}. En el compilador: {while, if, &lt;, ;, (, ), {, }}</p></article><article><strong>Cadenas</strong><p>Con Σ = {a, b}: ab, aab, bbb. Contienen longitud y la cadena vacía ε.</p></article><article><strong>Lenguaje</strong><p>L = {a, ab, abb}. En compiladores: conjunto de programas que cumplen las reglas del lenguaje.</p></article></div></section>
    <section class="panel"><h3>Gramática libre de contexto</h3><section class="note">Una gramática libre de contexto se define formalmente como G = (NT, T, P, S), donde NT es el conjunto de no terminales, T es el conjunto de terminales, P es el conjunto de producciones y S es el símbolo inicial. En este tipo de gramática, cada producción tiene la forma A → α, con A ∈ NT y α ∈ (NT ∪ T)* [4].</section><div class="concept-grid"><article><strong>Componentes en este compilador</strong><p>NT: P', P, B, W, S, C.<br>T: while, if, i, &lt;, (, ), {, }, ;, $.<br>S: P'.<br>P: reglas que forman bloques, sentencias y condiciones.</p></article><article><strong>Ejemplo de producciones</strong><p>P' → P<br>B → { W }<br>S → while ( C ) B<br>S → i ;<br>C → i &lt; i</p></article></div></section>
    <section class="panel"><h3>Clasificación de Chomsky</h3><div class="step-list"><article><strong>Tipo 0: no restringidas</strong><br>Máquinas de Turing [1].</article><article><strong>Tipo 1: sensibles al contexto</strong><br>Autómatas ligados linealmente [1].</article><article><strong>Tipo 2: libres de contexto</strong><br>Base del análisis sintáctico y parsers con pila [1], [4].</article><article><strong>Tipo 3: regulares</strong><br>Base del análisis léxico y autómatas finitos [1], [3].</article></div></section>
    <section class="panel"><h3>Ruta del análisis léxico</h3><div class="route-row"><div class="route-box"><strong>Patrón</strong><span>Expresión regular [2].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Reconocedor</strong><span>Autómata finito [3].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Lexema</strong><span>Fragmento reconocido.</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Token</strong><span>Entrada para el parser.</span></div></div><div class="concept-grid"><article><strong>Operaciones regulares</strong><p>Unión. Concatenación. Cerradura positiva. Cerradura de Kleene [2].</p></article><article><strong>Autómata finito</strong><p>Alfabeto de entrada. Estados. Estado inicial. Estados de aceptación. Función de transición [3].</p></article></div></section>
    <section class="panel"><h3>Ruta del análisis sintáctico</h3><div class="route-row"><div class="route-box"><strong>Tokens</strong><span>Salida del lexer.</span></div><div class="route-arrow">→</div><div class="route-box"><strong>GLC</strong><span>G = (NT, T, P, S) [4].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Parser</strong><span>LR(0) usa estados y pila.</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Resultado</strong><span>accept o error sintáctico.</span></div></div><div class="concept-grid"><article><strong>Árbol de derivación</strong><p>Raíz: símbolo inicial. Hojas: terminales. Nodos internos: no terminales [4].</p></article><article><strong>Ambigüedad</strong><p>Una cadena puede generar más de un árbol. La precedencia y asociatividad evitan interpretaciones incorrectas [5].</p></article></div></section>
    <section class="panel"><h3>Autómata de pila y LR(0)</h3><div class="route-row"><div class="route-box"><strong>Entrada</strong><span>Secuencia de tokens.</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Estado actual</strong><span>Control del análisis.</span></div><div class="route-arrow">+</div><div class="route-box"><strong>Pila</strong><span>Estados y símbolos [6].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Acción</strong><span>shift, reduce, accept o error.</span></div></div></section>
    <section class="panel"><h3>Conexión general con el compilador</h3><div class="route-row"><div class="route-box"><strong>Lenguajes formales</strong><span>Definen cadenas válidas.</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Expresiones regulares</strong><span>Describen patrones léxicos [2].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Autómatas finitos</strong><span>Reconocen tokens [3].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Gramáticas libres de contexto</strong><span>Definen la sintaxis [4].</span></div><div class="route-arrow">→</div><div class="route-box"><strong>Parser LR(0)</strong><span>Valida la estructura.</span></div></div></section>
    """ + REFERENCIAS_ANTECEDENTES


def render_creadores():
    creadores = [("Cano Vazquez, Axel Zaid", "canovazquezaxelzaid@gmail.com"), ("Carrasco Quinones, Diego Alexander", "alexnish1416@gmail.com"), ("Chacon Jaral, Hugo Emmanuel", "hugochaconjaral@gmail.com"), ("Mendoza Camacho, Estrella de Maria", "starmendozacamacho@gmail.com"), ("Sierra Garcia, Mariana", "mariana.gra18@gmail.com")]
    cards = "".join(f"<article class='creator-card'><strong>{esc(n)}</strong><span>{esc(c)}</span></article>" for n, c in creadores)
    return f"<section class='section-title'><span class='eyebrow'>Equipo 08</span><h2>Creadores</h2><p>Integrantes del proyecto CompyFI.</p></section><section class='creator-grid'>{cards}</section>"


def link_clase(view, actual):
    return "active" if view == actual else ""

def dialogo_mapache(view):
    dialogos = {
        "compilador": "Ayer aceptamos cadenas válidas.",
        "detalle": "La gramática primero.",
        "temario": "Esto explica por qué no dormimos en semestre.",
        "lexico": "El lexer separa todo, como amistad después de trabajo en equipo.",
        "sintactico": "Shift, reduce, accept… o terapia.",
        "semantico": "Si el parser dijo sí, semántica todavía puede decir amigo, no",
        "tac": "Tres direcciones :D",
        "backpatching": "Primero pongo el goto, luego veo a dónde. Planeación nivel semestre.",
        "optimizacion": "Si no cambia el significado y corre mejor, se queda.",
        "flujo": "Primero tokens, luego parser, luego semántica.",
        "antecedentes": "Lenguajes Formales y Autómatas… ni yo me acuerdo.",
        "creadores": "Créditos del equipo. Porque alguien debe hacerse responsable de esta belleza.",
    }
    return dialogos.get(view, "Listo, revisemos esta parte sin romper nada esta vez.")


def render_page(view, content):
    nav = f"""
    <aside class="sidebar"><div class="brand"><h1>CompyFI</h1><p>Compilador LR(0)</p></div>
    <nav class="nav nav-main"><a class="primary {link_clase(view,'compilador')}" href="/index.html?view=compilador">Compilador</a><a class="primary {link_clase(view,'temario')}" href="/index.html?view=temario">Temario asignatura</a><div class="nav-section-title">Teoría</div><a class="{link_clase(view,'lexico')}" href="/index.html?view=lexico">Análisis léxico</a><a class="{link_clase(view,'sintactico')}" href="/index.html?view=sintactico">Análisis sintáctico</a><a class="{link_clase(view,'semantico')}" href="/index.html?view=semantico">Análisis semántico y SDT</a><a class="{link_clase(view,'tac')}" href="/index.html?view=tac">Código intermedio y TAC</a><a class="{link_clase(view,'backpatching')}" href="/index.html?view=backpatching">Backpatching</a><a class="{link_clase(view,'optimizacion')}" href="/index.html?view=optimizacion">Optimización de código</a><a class="{link_clase(view,'flujo')}" href="/index.html?view=flujo">Flujo completo</a><a class="{link_clase(view,'antecedentes')}" href="/index.html?view=antecedentes">Antecedentes</a></nav>
    <div class="sidebar-mascot"><img src="/multimedia/mapache.gif" alt="CompyFI"></div><div class="bubble">{esc(dialogo_mapache(view))}</div><nav class="nav nav-bottom"><a class="{link_clase(view,'creadores')}" href="/index.html?view=creadores">Creadores</a></nav></aside>
    """
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>CompyFI LR(0)</title><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div class="app-shell">{nav}<main class="app-main">{content}</main></div><script>
document.querySelectorAll('.results-card').forEach(function(card){{
  const buttons = card.querySelectorAll('.tab-btn');
  const panes = card.querySelectorAll('.tab-pane');
  buttons.forEach(function(button){{
    button.addEventListener('click', function(){{
      const target = button.dataset.tab;
      buttons.forEach(function(btn){{ btn.classList.remove('selected'); }});
      panes.forEach(function(pane){{ pane.classList.remove('active'); }});
      button.classList.add('selected');
      const pane = card.querySelector('#pane-' + CSS.escape(target));
      if (pane) pane.classList.add('active');
    }});
  }});
}});
</script></body></html>"""


def render_view(view, ejemplo_id="valido", codigo_manual=None):
    if view == "temario":
        return render_temario()
    if view == "detalle":
        return render_detalle()
    if view in {"lexico", "sintactico", "semantico", "tac", "backpatching", "optimizacion", "flujo"}:
        return render_teoria(view)
    if view == "antecedentes":
        return render_antecedentes()
    if view == "creadores":
        return render_creadores()
    codigo = codigo_manual if codigo_manual is not None else EJEMPLOS.get(ejemplo_id, EJEMPLOS["valido"])["codigo"]
    return render_compilador(procesar_codigo(codigo), codigo, ejemplo_id if codigo_manual is None else "manual")
