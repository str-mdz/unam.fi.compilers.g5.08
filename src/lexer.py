"""Analizador léxico para CompyFI LR(0)."""
from pathlib import Path

PALABRAS_RESERVADAS = {"while", "if"}
SIMBOLOS = {"{", "}", "(", ")", "<", ";"}


def leer_archivo(ruta):
    return Path(ruta).read_text(encoding="utf-8")


def tokenizar_lista(codigo):
    tokens = []
    errores = []
    i = 0

    while i < len(codigo):
        c = codigo[i]

        if c.isspace():
            i += 1
            continue

        if c.isalpha() or c == "_":
            inicio = i
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == "_"):
                i += 1
            lexema = codigo[inicio:i]
            tipo = lexema if lexema in PALABRAS_RESERVADAS else "i"
            tokens.append((tipo, lexema))
            continue

        if c in SIMBOLOS:
            tokens.append((c, c))
            i += 1
            continue

        errores.append(c)
        tokens.append(("UNKNOWN", c))
        i += 1

    tokens.append(("$", "$"))
    return tokens, errores


def imprimir_tokens(tokens):
    for tipo, lexema in tokens:
        print(f"{tipo:10} {lexema}")
