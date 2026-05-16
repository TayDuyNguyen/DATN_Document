# Design System Strategy: The Azure Explorer

## 1. Overview & Creative North Star
This design system is built upon a Creative North Star we define as **"The Coastal Curated Editorial."** 

Da Nang is a city where the river meets the sea and modern architecture meets organic nature. To reflect this, we move away from the "standard travel portal" look. Instead of rigid grids and heavy borders, we embrace **Fluid Asymmetry** and **Tonal Depth**. The goal is to make the user feel they are flipping through a premium travel magazine—one that is breathable, sophisticated, and intentionally layered. We break the "template" feel by using overlapping elements, staggered image placements, and high-contrast typography scales that guide the eye through a narrative rather than a list of features.

---

## 2. Colors
Our palette is anchored by "Da Nang Blue" and "Dragon Bridge Orange," but used with surgical precision to ensure a premium feel.

### Core Palette
*   **Primary (Da Nang Blue):** `#004e9f` (Deep Trust), `#0066cc` (The Vitality of the Sea).
*   **Secondary (Dragon Bridge Orange):** `#ab3500` (Foundational Heat), `#fe6a34` (The Energetic Accent).
*   **Neutral/Surface:** `#f8f9ff` (Background), `#ffffff` (Surface Container Lowest).

### The "No-Line" Rule
Traditional 1px solid borders are strictly prohibited for sectioning. To separate content, designers must use **Background Color Shifts**. 
*   *Example:* A `surface-container-low` section sitting directly on a `background` surface.
*   *The Logic:* Lines create visual "noise" and feel clinical. Tonal shifts create a sense of landscape and natural horizons.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. We use the Material surface tiers to define importance:
1.  **Level 0 (Background):** `#f8f9ff` – The canvas.
2.  **Level 1 (Surface Container Low):** `#eff4ff` – Subtle grouping for secondary content.
3.  **Level 2 (Surface Container Highest):** `#d3e4fe` – To highlight interactive zones or sidebars.

### The "Glass & Gradient" Rule
To add "soul," avoid flat colors for high-impact areas.
*   **Hero Sections:** Use a subtle linear gradient from `primary` (`#004e9f`) to `primary_container` (`#0066cc`) at a 135-degree angle.
*   **Floating Navigation:** Use Glassmorphism—apply `surface` color at 70% opacity with a `backdrop-blur` of 12px. This integrates the UI into the photography of Da Nang.

---

## 3. Typography
We use **Inter** not as a utility font, but as an editorial voice.

*   **Display (L/M/S):** 3.5rem to 2.25rem. Used for destination names and impactful "hooks." Letter-spacing is set to -0.02em to create a dense, authoritative feel.
*   **Headline (L/M/S):** 2rem to 1.5rem. Bold. Used for section starts.
*   **Title (L/M/S):** 1.375rem to 1rem. Semibold. Used for card titles and sub-headers.
*   **Body (L/M/S):** 1rem to 0.75rem. Regular. We prioritize line heights of 1.6 to ensure the "Editorial" breathability.
*   **Labels:** 0.75rem. All-caps for "Must-See" or "Featured" tags to create high-contrast hierarchy.

---

## 4. Elevation & Depth
In this design system, depth is a feeling, not a structure.

### The Layering Principle
Avoid "Drop Shadows" on standard cards. Instead, achieve lift by placing a `surface-container-lowest` (#ffffff) card on a `surface-container-low` (#eff4ff) background. This "Tonal Layering" feels modern and high-end.

### Ambient Shadows
When an element must float (e.g., a "Book Now" floating action button):
*   **Color:** Use a tinted version of `on-surface` (approx 8% opacity).
*   **Blur:** High diffusion (24px - 32px) to mimic natural, soft daylight rather than a harsh artificial light source.

### The "Ghost Border" Fallback
If a border is required for accessibility in input fields:
*   Use `outline-variant` (`#c1c6d5`) at **20% opacity**.
*   **Strict Rule:** 100% opaque borders are forbidden as they "trap" the content.

---

## 5. Components

### Buttons (The "Call to Action")
*   **Primary:** Solid `primary` background with `on_primary` text. Radius: `8px`. No border.
*   **Secondary:** Glass-style. `primary_container` at 10% opacity with `primary` text. This creates a "watery" feel suitable for a coastal brand.
*   **States:** On hover, primary buttons should shift to a subtle gradient rather than a darker flat color.

### Cards & Lists
*   **Forbid Divider Lines:** Use vertical white space (Spacing `8` or `12`) or a subtle background shift to separate items in a list.
*   **Image Integration:** Cards should use the `xl` (1.5rem) roundedness scale. For an editorial look, images within cards should occasionally "break" the container or use asymmetrical aspect ratios (e.g., 4:5 for portraits).

### Inputs & Fields
*   **Surface:** Use `surface_container_low`. 
*   **Focus State:** Instead of a heavy border, use a 2px outer "glow" using the `primary` color at 30% opacity.

### Featured Components
*   **The "Experience" Chip:** A high-contrast chip using `secondary` (`#fe6a34`) to highlight "Dragon Bridge Fire Show" or "Night Market"—adds a pop of heat to the cool blue palette.
*   **Floating Navigation Bar:** A glassmorphic bar that sits 24px from the top, using the "Ghost Border" at 10% to define its shape without cutting off the background imagery.

---

## 6. Do's and Don'ts

### Do:
*   **Use Intentional White Space:** If you think a section needs more room, double the padding. White space is a luxury in design.
*   **Layer Imagery:** Overlap a small image over a larger one to create a "scrapbook editorial" feel.
*   **Use Tonal Shifts:** Always check if a background color change can replace a border.

### Don't:
*   **Don't use #000000:** Always use `on_surface` (`#0b1c30`) for text to maintain the "Midnight Blue" sophisticated depth.
*   **Don't use standard drop shadows:** Avoid the "2010 web" look; if it's not ambient and diffused, don't use it.
*   **Don't crowd the edges:** This design system requires breathing room to feel "High-End." Maintain a minimum of 24px (Spacing `6`) for inner container padding.