def blend_colors(base_hex: str, overlay_hex: str, opacity: float) -> str:
    """Mezcla un color de overlay (ej: onPrimary) sobre un color base (ej: primary).

    con una opacidad específica, simulando el 'State Layer' de Material Design 3.

    Retorna el color resultante en formato HEX.
    """
    if not base_hex or not overlay_hex:
        return base_hex

    base = base_hex.lstrip("#")
    overlay = overlay_hex.lstrip("#")

    # Si por alguna razón nos llega un hex de 8 caracteres (ARGB), ignoramos el alpha
    if len(base) == 8:
        base = base[2:]
    if len(overlay) == 8:
        overlay = overlay[2:]

    # Validar que al menos tenga 6 caracteres
    if len(base) != 6 or len(overlay) != 6:
        return base_hex

    r1, g1, b1 = int(base[0:2], 16), int(base[2:4], 16), int(base[4:6], 16)
    r2, g2, b2 = int(overlay[0:2], 16), int(overlay[2:4], 16), int(overlay[4:6], 16)

    # Fórmula de Alpha Compositing clásico sobre fondo sólido
    r = int((r2 * opacity) + (r1 * (1 - opacity)))
    g = int((g2 * opacity) + (g1 * (1 - opacity)))
    b = int((b2 * opacity) + (b1 * (1 - opacity)))

    # Asegurar que esten en rango 0-255
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))

    return f"#{r:02x}{g:02x}{b:02x}"
