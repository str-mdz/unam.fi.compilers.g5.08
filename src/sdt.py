"""Validación semántica básica y explicación de resultados."""


def _obtener_identificadores(tokens_lexer):
    return [lexema for tipo, lexema in tokens_lexer if tipo == "i"]


def validar_tipos(tokens_lexer):
    identificadores = sorted(set(_obtener_identificadores(tokens_lexer)))

    if not identificadores:
        tabla_simbolos = [{
            "nombre": "bloque",
            "categoria": "bloque",
            "tipo": "B",
            "valor": "vacio",
            "declarada": True,
            "usada": True,
        }]
    else:
        tabla_simbolos = [{
            "nombre": nombre,
            "categoria": "identificador",
            "tipo": "id",
            "valor": "",
            "declarada": True,
            "usada": True,
        } for nombre in identificadores]

    mensaje = (
        "La estructura fue aceptada por el parser LR(0). La validacion semantica "
        "basica registro los identificadores usados en sentencias y condiciones."
    )
    return True, mensaje, tabla_simbolos


def explicar_resultado(exito_parser, exito_semantico=False, mensaje_semantico="", tac=None):
    tac = tac or []
    if not exito_parser:
        return "El analisis sintactico fallo. Por esa razon no se ejecuto la validacion semantica ni se genero codigo intermedio TAC."
    if not exito_semantico:
        return "El analisis sintactico fue exitoso, pero la validacion semantica fallo. Por esa razon no se genero TAC."
    if tac:
        return "El analisis sintactico fue exitoso porque la entrada coincide con la gramatica LR(0). Despues se valido semanticamente la estructura y se genero TAC para las sentencias y condiciones reconocidas."
    return "El analisis sintactico y la validacion semantica fueron exitosos. No se genero TAC porque el bloque aceptado no contiene sentencias traducibles."
