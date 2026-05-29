"""Parser LR(0) para una gramática pequeña de bloques, if, while y sentencias i;."""
from collections import deque

producciones = [
    ("P'", ["P"]),
    ("P", ["B"]),
    ("B", ["{", "W", "}"]),
    ("B", ["{", "}"]),
    ("W", ["W", "S"]),
    ("W", ["S"]),
    ("S", ["while", "(", "C", ")", "B"]),
    ("S", ["if", "(", "C", ")", "B"]),
    ("S", ["i", ";"]),
    ("C", ["i", "<", "i"]),
]

terminales = ["while", "if", "i", "<", "(", ")", "{", "}", ";", "$"]
no_terminales = ["P'", "P", "B", "W", "S", "C"]


def obtener_no_terminales():
    return no_terminales.copy()


def obtener_terminales():
    return terminales.copy()


def obtener_producciones():
    return producciones.copy()


def formatear_produccion(numero, produccion=None):
    if produccion is None:
        produccion = producciones[numero]
    izquierda, derecha = produccion
    return f"{numero}. {izquierda} -> {' '.join(derecha)}"


def formatear_item(item):
    numero, punto = item
    izquierda, derecha = producciones[numero]
    derecha_con_punto = derecha.copy()
    derecha_con_punto.insert(punto, ".")
    return f"{izquierda} -> {' '.join(derecha_con_punto)}"


def formatear_estado(numero_estado, estado):
    lineas = [f"I{numero_estado}:"]
    for item in sorted(estado):
        lineas.append(f"  {formatear_item(item)}")
    return "\n".join(lineas)


def formatear_stack(stack):
    return " ".join(str(elemento) for elemento in stack)


def formatear_input(entrada, posicion):
    return " ".join(token["tipo"] for token in entrada[posicion:])


def cerradura(items):
    resultado = set(items)
    cambio = True
    while cambio:
        cambio = False
        nuevos_items = set()
        for numero, punto in resultado:
            _, derecha = producciones[numero]
            if punto >= len(derecha):
                continue
            simbolo = derecha[punto]
            if simbolo not in no_terminales:
                continue
            for i, (izquierda, _) in enumerate(producciones):
                nuevo = (i, 0)
                if izquierda == simbolo and nuevo not in resultado:
                    nuevos_items.add(nuevo)
        if nuevos_items:
            resultado.update(nuevos_items)
            cambio = True
    return frozenset(resultado)


def closure(items):
    return cerradura(items)


def mover(items, simbolo):
    resultado = set()
    for numero, punto in items:
        _, derecha = producciones[numero]
        if punto < len(derecha) and derecha[punto] == simbolo:
            resultado.add((numero, punto + 1))
    return cerradura(resultado) if resultado else frozenset()


def goto(items, simbolo):
    return mover(items, simbolo)


def construir_coleccion_lr0():
    estados = []
    transiciones = {}
    cola = deque()
    simbolos = terminales[:-1] + no_terminales[1:]
    estado_inicial = cerradura({(0, 0)})
    estados.append(estado_inicial)
    cola.append(estado_inicial)

    while cola:
        estado = cola.popleft()
        numero_estado = estados.index(estado)
        for simbolo in simbolos:
            destino = mover(estado, simbolo)
            if not destino:
                continue
            if destino not in estados:
                estados.append(destino)
                cola.append(destino)
            transiciones[(numero_estado, simbolo)] = estados.index(destino)
    return estados, transiciones


def detectar_tipo_conflicto(existente, nueva):
    if existente.startswith("s") and nueva.startswith("r"):
        return "shift/reduce"
    if existente.startswith("r") and nueva.startswith("s"):
        return "shift/reduce"
    if existente.startswith("r") and nueva.startswith("r"):
        return "reduce/reduce"
    if existente == "acc" or nueva == "acc":
        return "accept/conflict"
    return "conflict"


def registrar_accion(accion, conflictos, estado, simbolo, nueva):
    clave = (estado, simbolo)
    existente = accion.get(clave)
    if existente is not None and existente != nueva:
        conflictos.append({
            "estado": estado,
            "simbolo": simbolo,
            "existente": existente,
            "nueva": nueva,
            "tipo": detectar_tipo_conflicto(existente, nueva),
        })
        return
    accion[clave] = nueva


def construir_tabla_lr0(estados, transiciones):
    accion = {}
    ir_a = {}
    conflictos = []

    for numero_estado, estado in enumerate(estados):
        for numero_produccion, punto in estado:
            izquierda, derecha = producciones[numero_produccion]
            if punto < len(derecha):
                simbolo = derecha[punto]
                destino = transiciones.get((numero_estado, simbolo))
                if destino is None:
                    continue
                if simbolo in terminales:
                    registrar_accion(accion, conflictos, numero_estado, simbolo, f"s{destino}")
                elif simbolo in no_terminales:
                    ir_a[(numero_estado, simbolo)] = destino
                continue
            if izquierda == "P'":
                registrar_accion(accion, conflictos, numero_estado, "$", "acc")
            else:
                for terminal in terminales:
                    registrar_accion(accion, conflictos, numero_estado, terminal, f"r{numero_produccion}")
    return accion, ir_a, conflictos


def construir_automata():
    estados, transiciones = construir_coleccion_lr0()
    accion, ir_a, conflictos = construir_tabla_lr0(estados, transiciones)
    return {"estados": estados, "transiciones": transiciones, "accion": accion, "ir_a": ir_a, "conflictos": conflictos}


def obtener_entrada(tokens_lexer):
    entrada = [{"tipo": tipo, "lexema": lexema} for tipo, lexema in tokens_lexer]
    if not entrada or entrada[-1]["tipo"] != "$":
        entrada.append({"tipo": "$", "lexema": "$"})
    return entrada


def tokens_esperados(accion, estado):
    return [terminal for terminal in terminales if (estado, terminal) in accion]


def crear_error_info(accion, estado, token_actual):
    tipo = token_actual["tipo"]
    lexema = token_actual["lexema"]
    return {
        "estado": estado,
        "token": tipo,
        "lexema": lexema,
        "esperados": tokens_esperados(accion, estado),
        "mensaje": f"No existe accion en ACTION[{estado}, {tipo}].",
    }


def analizar(tokens_lexer):
    automata = construir_automata()
    accion = automata["accion"]
    ir_a = automata["ir_a"]
    entrada = obtener_entrada(tokens_lexer)
    stack = [0]
    posicion = 0
    traza = []

    while True:
        estado = stack[-1]
        token_actual = entrada[posicion]
        simbolo_entrada = token_actual["tipo"]
        accion_actual = accion.get((estado, simbolo_entrada))

        if accion_actual is None:
            error_info = crear_error_info(accion, estado, token_actual)
            traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": "error"})
            return False, traza, automata, error_info

        if accion_actual == "acc":
            traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": "acc"})
            return True, traza, automata, None

        if accion_actual.startswith("s"):
            estado_destino = int(accion_actual[1:])
            traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": f"shift {simbolo_entrada} -> {estado_destino}"})
            stack.append(simbolo_entrada)
            stack.append(estado_destino)
            posicion += 1
            continue

        if accion_actual.startswith("r"):
            numero_produccion = int(accion_actual[1:])
            izquierda, derecha = producciones[numero_produccion]
            traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": f"reduce r{numero_produccion}: {izquierda} -> {' '.join(derecha)}"})
            for _ in range(2 * len(derecha)):
                stack.pop()
            estado_superior = stack[-1]
            destino = ir_a.get((estado_superior, izquierda))
            if destino is None:
                error_info = {"estado": estado_superior, "token": simbolo_entrada, "lexema": token_actual["lexema"], "esperados": [izquierda], "mensaje": f"No existe transicion en GOTO[{estado_superior}, {izquierda}]."}
                traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": "goto error"})
                return False, traza, automata, error_info
            traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": f"goto {izquierda} -> {destino}"})
            stack.append(izquierda)
            stack.append(destino)
            continue

        error_info = {"estado": estado, "token": simbolo_entrada, "lexema": token_actual["lexema"], "esperados": tokens_esperados(accion, estado), "mensaje": f"Accion desconocida en ACTION[{estado}, {simbolo_entrada}]: {accion_actual}."}
        traza.append({"stack": formatear_stack(stack), "input": formatear_input(entrada, posicion), "action": "error"})
        return False, traza, automata, error_info
