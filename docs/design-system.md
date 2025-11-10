# Sistema de Diseño: Botones

Este documento describe el sistema de botones implementado, su paleta, estados, accesibilidad y uso.

## Paleta y tokens
- Variables (CSS): `--primary`, `--primary-700`, `--primary-800`, `--secondary`, `--secondary-700`, `--text`, `--outline`.
- Esquema formal: azules corporativos y grises neutros; contraste mínimo 4.5:1 (verificado para texto blanco sobre `--primary` y `--secondary`).

## Variantes
- `btn-primary`: acción principal.
- `btn-secondary`: acción secundaria.
- `btn-outline`: alternativa con borde, fondo transparente.

## Tamaños
- `btn-sm`, `btn` (por defecto), `btn-lg`. Altura táctil mínima 44px.

## Estados
- `hover`: cambio de color y realce.
- `active` / `is-pressed`: feedback táctil con `transform` (GPU friendly).
- `is-selected`: borde interno para indicar selección persistente.
- `disabled` / `is-disabled`: estilo atenuado y cursor desactivado.

## Accesibilidad
- `:focus-visible` con halo contrastado (box-shadow), sin afectar `outline` global.
- Respeto a `prefers-reduced-motion: reduce` desactivando transiciones.
- Colores con ratio mínimo 4.5:1.

## Rendimiento
- Transiciones de 220ms para suavidad óptima (200–300ms recomendado).
- `will-change: transform` en botones para mantener 60fps.
- Event delegation en `ui.js` para evitar listeners por elemento.

## Uso
```html
<button class="btn btn-primary">Guardar</button>
<button class="btn btn-secondary">Cancelar</button>
<button class="btn btn-outline">Más opciones</button>
```

## Integración
- Los botones se integran con el sistema existente de variables (`app/static/styles.css`).
- Se usan de forma consistente en plantillas (`.btn`). Añadir variantes según el contexto.

## Extensión futura
- Estados de carga (`is-loading`) con spinner (sin emojis), grupos segmentados y menús.