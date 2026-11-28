# Language Coach — Design System Specification

This specification documents the visual design tokens, glassmorphic surfaces, color palettes, UI components, and accessibility standards implemented in `app/static/css/style.css`.

---

## 1. Visual Design Philosophy

- **Aesthetic:** Modern, calm, premium SaaS appearance inspired by high-end educational software.
- **Surface Elevation:** Translucent glassmorphism cards (`backdrop-filter: blur(16px)`), subtle layered borders, and soft glowing drop shadows.
- **Ambient Lighting:** Subtle radial gradients (`var(--bg-gradient)`) creating atmospheric depth behind UI components.
- **Typography:** Modern clean system font stack supporting Latin, Devanagari (Hindi/Sanskrit), and European diacritics without external font CDNs:
  ```css
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto,
    "Nirmala UI", "Noto Sans Devanagari", "Helvetica Neue", Arial, sans-serif;
  ```

---

## 2. Color Palette & Design Tokens

### Accent Palette
- **Primary Violet:** `#7c3aed` (`--accent-1`)
- **Vibrant Pink:** `#ec4899` (`--accent-2`)
- **Bright Cyan:** `#06b6d4` (`--accent-3`)
- **Primary Gradient:** `linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #06b6d4 100%)`
- **Reverse Gradient:** `linear-gradient(135deg, #06b6d4 0%, #ec4899 50%, #7c3aed 100%)`

### Semantic Feedback Tokens
- **Success (Green):** `#10b981` (Light) / `#34d399` (Dark) &rarr; Score $\ge 70\%$, matched phonemes.
- **Warning (Amber):** `#f59e0b` (Light) / `#fbbf24` (Dark) &rarr; Score $40\%\le x < 70\%$, quiet mic warning.
- **Danger (Red):** `#ef4444` (Light) / `#f87171` (Dark) &rarr; Score $< 40\%$, substituted/missing phonemes, stop button.

---

## 3. Light vs. Dark Theme Variables

The application supports instant theme switching. A synchronous inline script in `<head>` applies the `data-theme` attribute before the first paint to eliminate Flash of Unstyled Theme (FOUT):

| CSS Variable | Light Theme (`:root`) | Dark Theme (`[data-theme="dark"]`) |
|---|---|---|
| `--bg-body` | `#f4f1fa` | `#0c0a16` |
| `--glass-bg` | `rgba(255, 255, 255, 0.65)` | `rgba(22, 18, 40, 0.70)` |
| `--glass-border` | `rgba(255, 255, 255, 0.45)` | `rgba(255, 255, 255, 0.08)` |
| `--surface` | `#ffffff` | `#1a1530` |
| `--surface-subtle` | `#f5f3ff` | `#221d3a` |
| `--surface-border` | `#e5e1f0` | `#2e2850` |
| `--text-primary` | `#1e1b2e` | `#f0eef8` |
| `--text-secondary` | `#4a4564` | `#c4bfdb` |
| `--text-muted` | `#7c7893` | `#8d87a8` |
| `--primary` | `#7c3aed` | `#a78bfa` |
| `--accent-glow` | `rgba(124, 58, 237, 0.25)` | `rgba(167, 139, 250, 0.30)` |

---

## 4. Reusable UI Components

### 1. Glass Cards (`.card`, `.glass-card`)
- Backdrop blur: `16px`.
- Border radius: `24px` (`--radius-lg`).
- Subtle 1px translucent border with soft elevation shadow.

### 2. Buttons (`.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger`)
- Border radius: `9999px` (pill shape).
- Primary button features gradient background with soft glow hover elevation (`transform: translateY(-1px)`).
- Secondary button features translucent glass surface with subtle border.

### 3. Microphone Action Button (`.btn-mic`)
- 96px circular trigger with vibrant gradient fill.
- Ambient radial pulse box-shadow.
- Scales to `1.06` on hover.

### 4. Phonetic Sound Chips (`.phone-chip`)
- Monospace font (`monospace`) for precise IPA glyph rendering.
- Correct sound: `.chip-correct` &rarr; translucent green background with green border.
- Substituted sound: `.chip-wrong` &rarr; translucent red background displaying `/expected/ → /spoken/`.

### 5. Circular Score Ring (`.score-ring`)
- SVG 120px ring with animated `stroke-dashoffset` transition (`0.8s cubic-bezier(0.4, 0, 0.2, 1)`).
- Dynamically colored: Green ($\ge 70\%$), Amber ($40\text{--}69\%$), Red ($< 40\%$).

---

## 5. Accessibility & Motion Guidelines

- **Focus Outlines:** Custom focus ring (`0 0 0 3px rgba(124,58,237,0.35)`) on all interactive buttons and dropdowns.
- **ARIA Live Regions:** Screen-reader announcements on recording status (`aria-live="polite"` on `#status`) and error banners (`role="alert"`).
- **Reduced Motion Compliance:** Respects user's operating system preferences:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
