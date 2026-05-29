"""Generador de TAC básico para la gramática del proyecto."""


def generar_tac(tokens_lexer, tabla_simbolos):
    if tabla_simbolos is None:
        return [], "No se genero TAC porque no hay tabla de simbolos valida."

    tac = []
    etiqueta = 1
    temporal = 1

    def nuevo_temporal():
        nonlocal temporal
        nombre = f"t{temporal}"
        temporal += 1
        return nombre

    for i, (tipo, lexema) in enumerate(tokens_lexer):
        if (
            tipo == "while"
            and i + 4 < len(tokens_lexer)
            and tokens_lexer[i + 2][0] == "i"
            and tokens_lexer[i + 3][0] == "<"
            and tokens_lexer[i + 4][0] == "i"
        ):
            inicio = f"L{etiqueta}"
            salida = f"L{etiqueta + 1}"
            etiqueta += 2
            temporal_condicion = nuevo_temporal()
            tac.extend([
                f"{inicio}:",
                f"{temporal_condicion} = {tokens_lexer[i + 2][1]} < {tokens_lexer[i + 4][1]}",
                f"ifFalse {temporal_condicion} goto {salida}",
                "// cuerpo while",
                f"goto {inicio}",
                f"{salida}:",
            ])
        elif (
            tipo == "if"
            and i + 4 < len(tokens_lexer)
            and tokens_lexer[i + 2][0] == "i"
            and tokens_lexer[i + 3][0] == "<"
            and tokens_lexer[i + 4][0] == "i"
        ):
            salida = f"L{etiqueta}"
            etiqueta += 1
            temporal_condicion = nuevo_temporal()
            tac.extend([
                f"{temporal_condicion} = {tokens_lexer[i + 2][1]} < {tokens_lexer[i + 4][1]}",
                f"ifFalse {temporal_condicion} goto {salida}",
                "// cuerpo if",
                f"{salida}:",
            ])
        elif tipo == "i" and i + 1 < len(tokens_lexer) and tokens_lexer[i + 1][0] == ";":
            temporal_sentencia = nuevo_temporal()
            tac.append(f"{temporal_sentencia} = {lexema}")

    if not tac:
        return [], "El bloque fue aceptado, pero no contiene sentencias traducibles a TAC."
    return tac, "TAC generado correctamente."
