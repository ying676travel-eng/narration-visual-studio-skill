# Motion language

Motion should explain something. A line can show a route, a reveal can show an order, a split can show a state change, and stillness can give the result time to land. If the motion can be removed without changing the explanation, remove it.

## Time and seek behavior

Subtitle time is the authority. Give each scene an absolute start and end, then schedule its visual changes at relative points inside that interval. Keep the original cue meaning and time when the style changes.

Every visible state must be computable from the requested time alone. Think of seeking like moving a bookmark to any page: the reader should see the right page immediately, whether they arrived from the beginning, the end, or another page. Do not rely on a viewer having watched earlier frames. Avoid wall-clock timers, random motion, autoplay loops, or standalone tweens. In HyperFrames work, use its paused, seekable timeline contract and follow the installed version's animation rules.

For a browser-only illustration, a range slider can set an explicit progress value and derive the full visual state from it. The showcases use this approach: dragging backward restores earlier states, and repeating the same value produces the same frame.

## Match the action to the idea

- Reveal a phrase in speaking order when the idea unfolds clause by clause.
- Draw a connector when the narration names the relation between its real endpoints.
- Build or join parts when the narration describes assembly or cooperation.
- Split an object or frame when the narration explains a change in state.
- Reorder, branch, or focus nodes only when the underlying relationship changes.
- Change a value only when the source provides that value.
- Hold the resolved image after the explanation so viewers can read it.

Do not animate every object. Choose a few meaningful changes, let their order express importance, and leave stillness where the audience needs time. Keep entrances decisive and exits shorter. Vary motion only when the meaning changes; a new direction or speed should have a reason.

## Preserve the style's motion character

- **Cartesian:** quiet, exact reveals; a fine rule can draw the relation; a compass ring may resolve around a concept and then stop. Avoid big bounces or ambient drifting.
- **Code Editorial:** reveal a code mechanism in the order input → rule → result; use the coral spike for one restrained emphasis; keep the final code readable. Avoid a typewriter effect that hides words during speech.
- **BlockFrame:** use short, decisive placements, route drawing, and clear state changes; a tilt may settle once on entry. Avoid continuous wobble or repeated impacts.

These are tendencies, not a required effect in every scene. A still frame is correct when motion adds no explanation.

## Timing and review

Place each change near the spoken moment that explains it. Start with a short lead-in so the frame does not feel like an accidental flash, leave a readable hold after an important reveal, and shorten transitions that add no meaning. Check the opening, middle, ending, and at least one backward seek of every multi-step scene. Compare repeated seeks at the same time; the image should match exactly.
