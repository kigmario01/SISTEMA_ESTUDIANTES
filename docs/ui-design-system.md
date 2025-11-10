# Sistema de Diseño UI/UX Moderno

## 🎨 Paleta de Colores

### Colores Primarios
- **Primary 50**: `#f0f9ff` - Fondo muy claro
- **Primary 100**: `#e0f2fe` - Fondo claro
- **Primary 500**: `#0ea5e9` - Color principal
- **Primary 600**: `#0284c7` - Hover principal
- **Primary 700**: `#0369a1` - Color activo
- **Primary 900**: `#0c4a6e` - Texto oscuro

### Colores Neutrales
- **Neutral 0**: `#ffffff` - Blanco puro
- **Neutral 50**: `#f8fafc` - Fondo muy claro
- **Neutral 100**: `#f1f5f9` - Fondo claro
- **Neutral 200**: `#e2e8f0` - Borde claro
- **Neutral 300**: `#cbd5e1` - Borde medio
- **Neutral 600**: `#475569` - Texto secundario
- **Neutral 700**: `#334155` - Texto principal
- **Neutral 800**: `#1e293b` - Texto oscuro
- **Neutral 900**: `#0f172a` - Texto más oscuro

### Colores de Estado
- **Success**: `#22c55e` - Verde éxito
- **Warning**: `#f59e0b` - Amarillo advertencia
- **Error**: `#ef4444` - Rojo error

## 📱 Tipografía

### Familia de Fuentes
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'Fira Code', 'Monaco', 'Consolas', monospace;
```

### Tamaños de Fuente
- **text-xs**: 12px
- **text-sm**: 14px
- **text-base**: 16px (base)
- **text-lg**: 18px
- **text-xl**: 20px
- **text-2xl**: 24px
- **text-3xl**: 30px
- **text-4xl**: 36px

### Pesos de Fuente
- **font-light**: 300
- **font-normal**: 400
- **font-medium**: 500
- **font-semibold**: 600
- **font-bold**: 700

## 🎯 Componentes

### Botones

#### Botón Primario
```html
<button class="btn-modern btn-primary">Botón Principal</button>
```
- Color de fondo: `--primary-600`
- Color de texto: Blanco
- Hover: `--primary-700` con sombra
- Active: `--primary-800`

#### Botón Secundario
```html
<button class="btn-modern btn-secondary">Botón Secundario</button>
```
- Color de fondo: `--secondary-100`
- Color de texto: `--secondary-700`
- Hover: `--secondary-200`

#### Botón Outline
```html
<button class="btn-modern btn-outline">Botón Outline</button>
```
- Fondo transparente
- Borde: `--neutral-300`
- Hover: `--neutral-50`

### Formularios

#### Input Moderno
```html
<div class="form-group">
  <label class="form-label">Label</label>
  <input type="text" class="form-input" placeholder="Placeholder">
</div>
```

#### Select Moderno
```html
<select class="form-input form-select">
  <option>Opción 1</option>
  <option>Opción 2</option>
</select>
```

#### Checkbox Moderno
```html
<label class="flex items-center">
  <input type="checkbox" class="form-checkbox">
  <span class="ml-2">Checkbox</span>
</label>
```

### Tarjetas (Cards)
```html
<div class="card">
  <h3 class="text-lg font-semibold mb-2">Título</h3>
  <p class="text-gray-600">Contenido de la tarjeta</p>
</div>
```
- Fondo blanco con sombra suave
- Bordes redondeados: `--radius-lg`
- Hover: Elevación con sombra aumentada

### Tablas
```html
<table class="table-modern">
  <thead>
    <tr>
      <th>Encabezado 1</th>
      <th>Encabezado 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dato 1</td>
      <td>Dato 2</td>
    </tr>
  </tbody>
</table>
```

## ✨ Animaciones

### Transiciones
- **Duración 150ms**: Para micro-interacciones
- **Duración 200ms**: Para cambios de estado
- **Duración 300ms**: Para transiciones de página
- **Duración 500ms**: Para animaciones complejas

### Efectos de Hover
- **Botones**: Elevación de 1px con sombra
- **Tarjetas**: Elevación de 4px con sombra aumentada
- **Enlaces**: Cambio de color suave

### Ripple Effect
Los botones modernos incluyen un efecto ripple al hacer clic:
```html
<button class="btn-modern btn-primary" data-ripple="true">
  Botón con Ripple
</button>
```

### Animaciones de Entrada
- **fadeIn**: Opacidad de 0 a 1 (0.5s)
- **slideUp**: Desliza desde abajo (0.4s)
- **scaleIn**: Escala desde 95% a 100% (0.3s)

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Adaptaciones Mobile
- Botones de ancho completo
- Navegación colapsable
- Tablas scrollables horizontalmente
- Espaciado reducido

## ♿ Accesibilidad (WCAG AA)

### Contraste de Color
- Todos los colores cumplen con WCAG AA
- Ratio mínimo 4.5:1 para texto normal
- Ratio mínimo 3:1 para texto grande

### Navegación por Teclado
- Todos los elementos interactivos son accesibles por teclado
- Estados de foco visibles con outline de 2px
- Orden lógico de tabulación

### Soporte para Lectores de Pantalla
- Etiquetas semánticas apropiadas
- Textos alternativos para iconos
- Estados anunciados correctamente

### Preferencias del Usuario
- **prefers-reduced-motion**: Desactiva animaciones
- **prefers-color-scheme**: Soporte para modo oscuro
- **prefers-contrast**: Aumenta contraste cuando sea necesario

## 🌙 Modo Oscuro

El sistema incluye soporte automático para modo oscuro basado en `prefers-color-scheme`:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --neutral-0: #0f172a;
    --neutral-50: #1e293b;
    /* ... más variables invertidas */
  }
}
```

## 🔧 Implementación

### 1. Incluir el CSS
```html
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
```

### 2. Incluir el JavaScript
```html
<script src="{{ url_for('static', filename='ui.js') }}"></script>
```

### 3. Usar Componentes
```html
<!-- Botón con ripple y loading -->
<button class="btn-modern btn-primary" data-auto-loading="true">
  Enviar
</button>

<!-- Formulario moderno -->
<form class="space-y-4">
  <div class="form-group">
    <label class="form-label">Email</label>
    <input type="email" class="form-input" placeholder="tu@email.com">
  </div>
  <button type="submit" class="btn-modern btn-primary w-full">
    Enviar
  </button>
</form>
```

## 📊 Rendimiento

### Optimizaciones
- CSS minimizado y sin dependencias
- JavaScript ligero (~3KB)
- Animaciones con `transform` y `opacity`
- Uso de `will-change` cuando es apropiado

### Métricas Objetivo
- Tiempo de carga < 100ms para CSS
- Tiempo de carga < 50ms para JavaScript
- Animaciones a 60fps
- CLS (Cumulative Layout Shift) < 0.1

## 🚀 Mejores Prácticas

### 1. Consistencia
- Usar las variables CSS para mantener consistencia
- Seguir la jerarquía de tipografía establecida
- Mantener espaciado uniforme

### 2. Accesibilidad
- Siempre incluir etiquetas para formularios
- Usar contraste adecuado
- Probar con teclado
- Verificar con lectores de pantalla

### 3. Rendimiento
- No sobre-utilizar animaciones
- Optimizar imágenes
- Usar `prefers-reduced-motion`
- Minimizar reflows y repaints

### 4. Responsive
- Mobile-first approach
- Probar en dispositivos reales
- Usar unidades relativas
- Considerar touch targets (mínimo 44px)

## 📋 Checklist de Implementación

- [ ] Variables CSS implementadas
- [ ] Tipografía configurada
- [ ] Componentes base creados
- [ ] Animaciones implementadas
- [ ] Responsive design aplicado
- [ ] Accesibilidad verificada
- [ ] Modo oscuro probado
- [ ] Rendimiento optimizado
- [ ] Documentación completa
- [ ] Pruebas en múltiples navegadores

## 🔗 Recursos

- [Inter Font](https://rsms.me/inter/)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [ prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)