# Tsumiki Color System

A guide to using colors consistently across the application.

---

## Background Colors

| Variable | Usage |
|----------|-------|
| `$background` | Primary/main background for the application |
| `$background-alt` | Secondary background, elevated surfaces, popovers |
| `$background-dark` | Darkest background for dropdowns, tooltips, overlays |
| `$bar-background` | Status bar background |

---

## Text Colors

| Variable | Usage |
|----------|-------|
| `$text-main` | Primary text, headings, important content |
| `$text-secondary` | Secondary text, descriptions, subtitles |
| `$text-muted` | Placeholder text, hints, less important info |
| `$text-disabled` | Disabled/inactive text elements |

---

## Surface Colors

| Variable | Usage |
|----------|-------|
| `$surface-disabled` | Background for disabled buttons/inputs |
| `$surface-neutral` | Cards, panels, input fields, containers |
| `$surface-highlight` | Hover states, selections, focus rings |

---

## Accent Colors

### Primary Accents
| Variable | Usage |
|----------|-------|
| `$accent-blue` | **Primary accent** - Links, buttons, active states, CTAs |
| `$accent-light-blue` | Secondary blue - Toggles, switches, progress bars |
| `$accent-purple` | Tertiary accent - Tags, badges, special highlights |
| `$accent-lavender` | Subtle highlights - Borders, dividers, soft accents |

### Decorative Accents
| Variable | Usage |
|----------|-------|
| `$accent-pink` | Decorative - Workspace hover, special interactions |
| `$accent-light` | Lightest accent - Soft highlights, backgrounds |

---

## Semantic Colors

Use these for their specific meaning - don't use them decoratively!

| Variable | Meaning | Usage |
|----------|---------|-------|
| `$accent-green` | **Success** | Success messages, confirmations, completed states |
| `$accent-teal` | **Info** | Informational messages, tips, neutral notifications |
| `$accent-yellow` | **Warning** | Warnings, caution states, attention needed |
| `$accent-orange` | **Alert** | Alerts, important notices, elevated warnings |
| `$accent-red` | **Error/Danger** | Errors, destructive actions, critical warnings |

---

## UI Element Colors

| Variable | Usage |
|----------|-------|
| `$shadow-color` | Drop shadows, elevation effects |
| `$ws-active` | Active workspace indicator |
| `$ws-hover` | Workspace hover state |

---

## Usage Examples

### Buttons
```scss
// Primary button
background: $accent-blue;
color: $background;

// Secondary button
background: $surface-neutral;
color: $text-main;

// Danger button
background: $accent-red;
color: $background;

// Disabled button
background: $surface-disabled;
color: $text-disabled;
```

### Cards & Panels
```scss
background: $surface-neutral;
border: 1px solid $surface-highlight;
color: $text-main;

.subtitle {
  color: $text-secondary;
}
```

### Notifications
```scss
// Success notification
background: color.mix($accent-green, $background, 15%);
border-left: 3px solid $accent-green;

// Error notification
background: color.mix($accent-red, $background, 15%);
border-left: 3px solid $accent-red;
```

### Interactive States
```scss
// Default
background: $surface-neutral;

// Hover
background: $surface-highlight;

// Active/Pressed
background: $accent-blue;

// Disabled
background: $surface-disabled;
opacity: 0.6;
```

---

## Best Practices

1. **Use semantic colors for their meaning** - Don't use `$accent-red` for decoration
2. **Maintain contrast** - Ensure text is readable against backgrounds
3. **Be consistent** - Use the same color for the same purpose everywhere
4. **Limit accent usage** - Too many colors = visual noise
5. **Use muted colors for secondary content** - Draw attention to what matters
