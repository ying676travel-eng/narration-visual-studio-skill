import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_project import audit, load_tokens

class AuditTests(unittest.TestCase):
    def fixture(self, root):
        tokens={'bg':'#eee8df','ink':'#171717','accent':'#bb3300','muted':'#555555','line':'#777777','display_font':'serif','body_font':'sans-serif','mono_font':'monospace'}
        (root/'frame.md').write_text('```json\n'+json.dumps(tokens)+'\n```')
        (root/'input.json').write_text(json.dumps({'duration':5,'cues':[{'id':1,'start':0,'end':5,'text':'test'}]}))
        (root/'scenes.json').write_text(json.dumps({'scenes':[{'scene_id':'one','start':0,'end':5,'cue_ids':[1],'reveal_times':[1]}]}))
        for f in ['source-map.md','scene-plan.md','visual-storyboard.md']: (root/f).write_text('test')
        (root/'index.html').write_text('<div data-composition-id="main" data-width="1920" data-height="1080" data-duration="5"><section class="clip" data-start="0" data-duration="5"></section></div>')
    def test_coverage_and_durations(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            self.assertEqual(audit(root)['errors'],[])
            data=json.loads((root/'scenes.json').read_text());data['scenes'][0]['cue_ids']=[2]
            (root/'scenes.json').write_text(json.dumps(data))
            self.assertEqual(audit(root)['status'],'BLOCKED')
    def test_missing_style_and_remote_media_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            with (root/'index.html').open('a') as f: f.write('<img src="https://untrusted.invalid/x.png">')
            self.assertTrue(any('local' in x for x in audit(root)['errors']))
            (root/'frame.md').write_text('```json\n{}\n```')
            with self.assertRaises(ValueError):load_tokens(root/'frame.md')
    def test_duplicate_dom_ids_report_both_locations(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            (root/'index.html').write_text('''<div id="composition-root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="5">
<section id="scene-one" class="clip" data-start="0" data-duration="5">
<h1 id="el-one-title">Title</h1><p id="el-one-title">Copy</p>
</section></div>''')
            result=audit(root)
            self.assertEqual(result['status'],'BLOCKED')
            self.assertTrue(any('Duplicate DOM id "el-one-title"' in x and 'lines 3 and 3' in x for x in result['errors']))
    def test_unique_ids_and_script_text_do_not_false_positive(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            (root/'index.html').write_text('''<div id="composition-root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="5">
<section id="scene-one" class="clip" data-start="0" data-duration="5"><h1 id="el-one-title">Title</h1>
<img id="el-one-image" src="data:image/png;base64,AA"/><p id="EL-one-title">Copy</p></section></div>
<script>const example = '<p id="el-one-title">';</script>''')
            self.assertEqual(audit(root)['errors'],[])
    def test_unknown_style(self):
        # Keep import lazy: module also loads the input preparation tool.
        from new_project import resolve_style
        with self.assertRaises(ValueError):resolve_style('style-that-does-not-exist')
    def test_style_pack_fonts_are_packed(self):
        from new_project import resolve_style, pack_style_assets
        frame, style_dir = resolve_style('code-editorial')
        self.assertEqual(frame.name, 'frame.md')
        self.assertTrue((style_dir/'upstream'/'FRAME.md').is_file())
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)/'proj'
            out.mkdir()
            packed = pack_style_assets(style_dir, out)
            self.assertIn('assets/fonts/Inter-400.woff2', packed)
            self.assertTrue((out/'assets'/'fonts'/'OFL-inter.txt').is_file())
    def test_styles_without_fonts_stay_clean(self):
        from new_project import pack_style_assets
        with tempfile.TemporaryDirectory() as d:
            style = Path(d)/'unfonted-style'
            style.mkdir()
            out = Path(d)/'proj'
            out.mkdir()
            self.assertEqual(pack_style_assets(style, out), [])
            self.assertFalse((out/'assets').exists())
    def test_style_snapshot_keeps_official_guidance_and_reading_links(self):
        from new_project import resolve_style, pack_style_guidance
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            style_dir = resolve_style('code-editorial')[1]
            pack_style_guidance(style_dir, out)
            text = (out/'frame.md').read_text(encoding='utf-8')
            self.assertEqual(load_tokens(out/'frame.md')['id'], 'code-editorial')
            self.assertTrue((out/'upstream'/'FRAME.md').is_file())
            self.assertTrue((out/'upstream'/'SOURCE.md').is_file())
            self.assertTrue((out/'references'/'code-editorial-execution.md').is_file())
            self.assertIn('(references/code-editorial-execution.md)', text)
            self.assertIn('(assets/fonts/)', text)
            self.assertNotIn('(upstream/frame-showcase.html)', text)
            guide = (out/'references'/'code-editorial-execution.md').read_text(encoding='utf-8')
            self.assertIn('(../upstream/FRAME.md)', guide)
            self.assertNotIn('../styles/code-editorial/', guide)
    def test_seven_official_styles_keep_tokens_and_authority(self):
        from new_project import resolve_style, pack_style_guidance
        names = ('cartesian','code-editorial','blockframe','broadside',
                 'cobalt-grid','daisy-days','editorial-forest')
        with tempfile.TemporaryDirectory() as d:
            for name in names:
                with self.subTest(style=name):
                    out = Path(d)/name
                    out.mkdir()
                    pack_style_guidance(resolve_style(name)[1], out)
                    self.assertEqual(load_tokens(out/'frame.md')['id'], name)
                    self.assertTrue((out/'upstream'/'FRAME.md').is_file())
                    self.assertNotIn('(upstream/frame-showcase.html)',
                                     (out/'frame.md').read_text(encoding='utf-8'))
    def test_custom_style_keeps_its_own_showcase(self):
        from new_project import pack_style_guidance
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            style = root/'custom-style'
            (style/'upstream').mkdir(parents=True)
            tokens = {'id':'custom-style','bg':'#eee8df','ink':'#171717',
                      'accent':'#bb3300','muted':'#555555','line':'#777777',
                      'display_font':'serif','body_font':'sans-serif','mono_font':'monospace'}
            (style/'frame.md').write_text('```json\n'+json.dumps(tokens)+'\n```\n'
                                          '[showcase](upstream/frame-showcase.html)', encoding='utf-8')
            (style/'upstream'/'FRAME.md').write_text('Custom authority', encoding='utf-8')
            (style/'upstream'/'frame-showcase.html').write_text('<p>Custom showcase</p>', encoding='utf-8')
            out = root/'project'
            out.mkdir()
            pack_style_guidance(style, out)
            self.assertEqual((out/'upstream'/'frame-showcase.html').read_text(encoding='utf-8'),
                             '<p>Custom showcase</p>')
            self.assertIn('(upstream/frame-showcase.html)',
                          (out/'frame.md').read_text(encoding='utf-8'))
            self.assertNotIn('hyperframes/blob/',
                             (out/'frame.md').read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
