# Visual quality review

Review the actual rendered frames as well as the source. A clean code check cannot tell whether a diagram explains the narration, and a beautiful static start frame cannot prove that a later seek works.

## Scene review

For each scene, confirm:

- Its main visual expresses the scene's stated idea, rather than repeating the spoken paragraph as text.
- One primary focal point leads to a clear secondary reading step; labels remain secondary to the explanation.
- Every drawn connection has meaningful endpoints and a clear purpose.
- Any data, UI, screenshot, or code is either supplied evidence or plainly marked as illustrative.
- The composition fits this scene's relationship. Neighboring scenes can vary in structure while still sharing the pack's visual voice.
- Motion clarifies a reveal, route, build, comparison, or state change, then settles into a readable hold.

## Style-pack review

Read the selected `frame.md` as the source of truth. Compare the output with its exact token block and rules:

- **Cartesian:** warm-stone palette, Playfair 400 sentence case, Inter labels/body, one-pixel taupe structure, flat surfaces, and at most two restrained compass rings.
- **Code Editorial:** cream / ink / single coral accent, EB Garamond 400 display, Inter body, JetBrains Mono technical voice, and warm navy only for code or terminal surfaces.
- **BlockFrame:** exact pastel set, black outlines, square corners, hard shadow offsets coupled to border weight, and heavy uppercase Inter display.

The pack showcase should demonstrate at least four visibly different scene structures. Do not count four color changes or four copies of one card layout as structural variety. A production work should also vary its composition according to content rather than copying the showcase.

## Legibility and technical inspection

Inspect scene starts, major reveals, resolved frames, and scene boundaries. Seek directly into a scene, jump backward, and repeat the same time. Each sample should show the state expected for that instant, without a flash, missing object, or dependence on playback history.

Check the actual target sizes, including 1920×1080 and 1280×720 where applicable. Read the smallest load-bearing text at normal viewing scale. Confirm that Chinese text uses available local font fallbacks, fits its measure, and does not split into unnatural single-character columns. Check overlap, crop, contrast, asset loading, console errors, and the HTML frame bounds.

## Report what was observed

Record the file, time or state, screenshot path, observation, and repair for every issue. Distinguish automated checks from human visual review. If a browser or rendering check did not run, report it as blocked or pending. If visual review is still due, say so; internal checks do not equal user approval.

## V3.1 layout check

Use composition-system.md. Inspect grouping, alignment, safe areas, type roles and natural Chinese line breaks in real frames. Remove repeated conclusions, stray notes and decorative connections. For a layout iteration, a compact set of before/after examples plus new-content proof is enough; no per-page approval or additional scoring/gate system. Preserve timing and verify playback/seek.
