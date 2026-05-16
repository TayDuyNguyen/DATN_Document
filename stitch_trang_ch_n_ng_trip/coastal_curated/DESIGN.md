# Design System Document: The Coastal Curated Editorial

## 1. Overview & Creative North Star

### The Creative North Star: "The Digital Curator"
This design system is not a utility; it is a lens. To capture the essence of Da Nang—a city where the Marble Mountains meet the Han River and the East Sea—we move away from "app-like" density toward a high-end editorial experience. 

The goal is to break the "template" look. We achieve this through **Intentional Asymmetry** (overlapping elements), **Breathable Composition** (generous whitespace mimicking the coastline), and **Tonal Depth**. This system treats the screen like a premium travel magazine where photography is the hero, and the UI is the sophisticated, quiet guide.

---

## 2. Colors & The Coastal Tonal Rules

The palette is derived from the transition of dawn over the water to the neon pulse of the Dragon Bridge. 

### Core Palette
- **Primary (Da Nang Azure):** `#004E9F` to `#0066CC`. Use this for brand authority and navigational anchors.
- **Secondary (Dragon Bridge Orange):** `#AB3500` to `#FF6B35`. This is our "Heat." Use it sparingly for high-intent CTAs and vital status indicators.
- **Neutral Surface:** A sophisticated range of whites and slates (`#F6FAFE` to `#171C1F`) that provide the "canvas."

### The "No-Line" Rule
**Explicit Instruction:** Prohibit 1px solid borders for sectioning. In this design system, boundaries are defined by background color shifts or subtle tonal transitions. 
- *Instead of a border:* Use a `surface-container-low` section sitting against a `surface` background.
- *Why:* Borders create visual "noise" that interrupts the breezy, coastal flow.

### Surface Hierarchy & Nesting
Treat the UI as physical layers—stacked sheets of fine paper. 
- Use the `surface-container` tiers (Lowest to Highest) to define importance. 
- An inner card should use `surface-container-lowest` when placed on a `surface-container-high` background to create a "lifted" feel without artificial shadows.

### Glassmorphism & Signature Textures
To escape the "flat" web look:
- **Floating Elements:** Use semi-transparent `surface` colors with a 20px-40px backdrop-blur for navigation bars and overlays.
- **Tonal Gradients:** For Hero backgrounds and Primary CTAs, use a subtle linear gradient from `primary` (#004E9F) to `primary_container` (#0066CC). This adds "soul" and mimics the depth of the sea.

---

## 3. Typography: Editorial Rhythm

We use **Inter** exclusively. Its neutrality allows our photography to speak, but our *scale* is what provides the editorial voice.

- **The Hook (Display LG/MD):** `3.5rem` to `2.75rem`. Use these for destination names (e.g., "Mỹ Khê Beach"). Tighten letter-spacing by -2% for a premium, tucked-in look.
- **The Narrative (Body LG/MD):** `1rem` to `0.875rem`. Use generous line heights (1.6+) to ensure the "breathable" quality is maintained in long-form travel descriptions.
- **The Metadata (Label MD/SM):** `0.75rem` to `0.68rem`. Use all-caps with increased letter-spacing (+5% to +10%) for categories or tags (e.g., "GASTRONOMY," "NIGHTLIFE").

---

## 4. Elevation & Depth

We convey hierarchy through **Tonal Layering** rather than traditional structural lines.

### The Layering Principle
Depth is achieved by "stacking." 
- **Level 0 (Base):** `surface` (#F6FAFE).
- **Level 1 (Sections):** `surface-container-low`.
- **Level 2 (Interactive Cards):** `surface-container-lowest` (Pure white).

### Ambient Shadows
When a "floating" effect is required (e.g., a modal or a floating action button):
- **Formula:** Extra-diffused blur (20px-40px) at 4%-8% opacity.
- **Tone:** The shadow color must be a tinted version of `on-surface` (#171C1F), never pure black. This mimics natural light reflecting off Da Nang’s white sands.

### The "Ghost Border" Fallback
If a border is required for accessibility:
- Use the `outline-variant` token at **15% opacity**.
- **Forbid:** 100% opaque, high-contrast borders.

---

## 5. Components

### Buttons
- **Primary:** `primary` background with `on-primary` text. Use `xl` (1.5rem) corner radius for a modern, inviting feel.
- **Secondary:** `secondary_container` background. This is for secondary actions that still require "warmth" (e.g., "Book Now").
- **Tertiary:** No background. Use `primary` text with an icon.

### Editorial Cards
- **Constraint:** Forbid divider lines. 
- **Separation:** Use vertical white space (32px or 48px) and `surface-container-highest` backgrounds for "nested" content like price details or amenities.
- **Imagery:** Cards should always feature a high-quality image with a `DEFAULT` (8px) or `lg` (16px) radius.

### Signature Component: The "Curated Highlight"
A custom layout pattern where a `display-md` headline overlaps the edge of a high-resolution image by 24px. This intentional asymmetry breaks the grid and creates an editorial magazine feel.

### Input Fields
- Background: `surface-container-highest`.
- Active State: Transition background to `surface-container-lowest` and add a `primary` ghost border.

---

## 6. Do's and Don'ts

### Do
- **Do** use asymmetrical margins. Allow images to bleed off the edge of the screen on mobile to suggest "more to explore."
- **Do** lean into the Spacing Scale. If you think there is enough whitespace, add 16px more.
- **Do** use `secondary` (Orange) only for the most important conversion points.

### Don't
- **Don't** use pure black (#000000) for text. Use `on-surface` (#171C1F) to maintain visual softness.
- **Don't** use 1px dividers to separate list items. Use 16px of vertical padding and a background color shift instead.
- **Don't** use sharp 0px corners. This design system is "Coastal"—it should feel eroded and smooth, like a sea pebble.