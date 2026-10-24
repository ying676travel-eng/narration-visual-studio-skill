# Importing a visual reference

Use this guide only for a local HTML/CSS reference the user has permission to use. The goal is a reviewable style description and local preview, not a clone of the page's content or behavior.

## Inspect without running unknown code

1. Preserve the original reference and note its local path and any user-provided license or permission details.
2. Read HTML, CSS, and asset references as text first. Identify inline scripts, event handlers, remote stylesheets, external fonts, images, iframes, and imports. Do not execute unknown scripts or open hidden remote dependencies.
3. Follow the cascade: record selectors that override one another, media-query differences, font fallbacks, and important computed-style uncertainty. Static source may not reveal what a browser would finally display.
4. Use a browser only for a reference the user has authorized and trusts. Disable network access where possible. Do not upload the source, download remote assets, or run a remote font service as part of import.

Treat the source like a sealed box until its contents are understood. If script execution or a remote asset is required to see the style, stop at a static description and explain what remains uncertain.

## Create a draft, then review it

Create a new, separate style directory; do not overwrite an existing pack. Produce:

- `frame.md` with a clearly marked token block, typography and local fallback stacks, geometry, composition guidance, motion tendencies, do/don't rules, and a source/license note;
- `style-preview.html`, a small standalone preview with local or original vector shapes and no copied remote behavior;
- `import-report.md` listing files inspected, observed cascade and media-query details, external references, missing assets, script risk, font uncertainty, inferred choices, and any unresolved questions;
- an asset list for any files the user authorized for reuse, with their source and license.

Separate observed values from inferred values. Record exact colors and font-family declarations where visible; mark approximations as approximations. A screenshot can help judge appearance but does not prove which CSS rule produced it. Use safe system-font fallbacks and avoid adding remote font dependencies.

## Keep brand separate from layout

Extract the visual voice—color, type, line, shape, density, and emphasis—not a mandate to repeat the source page's layout in every scene. Adapt each narration scene to its meaning. Do not imply that an imported design spec guarantees a faithful reproduction or finished visual quality; show the preview and leave the draft editable.
