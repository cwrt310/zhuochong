"""Run the installer against isolated homes, never the user's Codex settings."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHELL = os.environ.get('XIAOBA_TEST_POWERSHELL', 'powershell.exe')


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='xiaoba-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / 'package'
        self.package.mkdir()
        shutil.copy2(ROOT / 'work' / '安装小巴.ps1', self.package / 'install.ps1')
        shutil.copy2(ROOT / 'work' / 'Update-XiaobaConfig.ps1', self.package)
        shutil.copytree(ROOT / 'work/xiaoba/native', self.package / 'xiaoba/native')
        self.home = self.root / 'home with spaces'
        self.home.mkdir()
        self.config = self.home / 'config.toml'

    def install(self, *, relative=False, success=True, error=None):
        env = os.environ.copy()
        env['CODEX_HOME'] = self.home.name if relative else str(self.home)
        result = subprocess.run(
            [SHELL, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', str(self.package / 'install.ps1')],
            cwd=self.root, env=env, capture_output=True, timeout=30,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(error.encode('ascii'), result.stderr)
        return result

    def check(self, original, *, relative=False):
        if original is not None:
            self.config.write_bytes(original.encode('utf-8'))
        self.install(relative=relative)
        written = self.config.read_bytes()
        parsed = tomllib.loads(written.decode('utf-8'))
        self.assertEqual(parsed['desktop']['selected-avatar-id'], 'xiaoba')
        self.assertIs(parsed['desktop']['avatar-overlay-pet-visible'], True)
        backup = self.home / 'config.before-xiaoba.toml'
        if original is not None:
            self.assertEqual(backup.read_bytes(), original.encode('utf-8'))
        else:
            self.assertFalse(backup.exists())
        copied = self.home / 'pets/xiaoba'
        self.assertEqual((copied / 'spritesheet.webp').read_bytes(), (self.package / 'xiaoba/native/spritesheet.webp').read_bytes())
        self.assertEqual(json.loads((copied / 'pet.json').read_text(encoding='utf-8'))['name'], '小巴')
        self.install(relative=relative)
        self.assertEqual(self.config.read_bytes(), written, 'Reinstall must leave config bytes unchanged')
        if original is not None:
            self.assertEqual(backup.read_bytes(), original.encode('utf-8'))
        return parsed

    def test_new_home(self):
        self.check(None)

    def test_empty_config(self):
        self.check('')

    def test_header_at_end_of_file(self):
        self.check('[desktop]')

    def test_commented_header_and_quoted_keys(self):
        parsed = self.check('[desktop] # personal\n  "selected-avatar-id" = "codex"\n  \'avatar-overlay-pet-visible\' = false\n\n[other]\nselected-avatar-id = "leave me"\n')
        self.assertEqual(parsed['other']['selected-avatar-id'], 'leave me')

    def test_quoted_table_and_crlf(self):
        self.check('["desktop"] # note\r\nselected-avatar-id = "codex"\r\n')
        self.assertNotIn(b'\n', self.config.read_bytes().replace(b'\r\n', b''))

    def test_value_case_and_inline_comment(self):
        self.check('[desktop]\nselected-avatar-id = "XIAOBA" # keep comment\navatar-overlay-pet-visible = true\n')
        self.assertIn('# keep comment', self.config.read_text())

    def test_multiline_string_with_fake_desktop(self):
        original = 'note = """\n[desktop]\nselected-avatar-id = \\"not a setting\\"\n"""\n[desktop] # real table\n'
        before = tomllib.loads(original)
        parsed = self.check(original)
        self.assertEqual(parsed['note'], before['note'])

    def test_comments_and_literal_multiline(self):
        original = '# """ in comment\nnote = \'\'\'\n[desktop]\n\'\'\'\n[\'desktop\']\n'
        self.assertEqual(self.check(original)['note'], tomllib.loads(original)['note'])

    def test_relative_codex_home(self):
        self.check('[desktop]\n', relative=True)

    def test_rejects_duplicate_table_before_copying(self):
        original = b'[desktop]\n[desktop]\n'
        self.config.write_bytes(original)
        target = self.home / 'pets/xiaoba'
        target.mkdir(parents=True)
        (target / 'pet.json').write_text('existing pet')
        self.install(success=False, error='Duplicate desktop tables')
        self.assertEqual(self.config.read_bytes(), original)
        self.assertEqual((target / 'pet.json').read_text(), 'existing pet')
        self.assertFalse((self.home / 'config.before-xiaoba.toml').exists())

    def test_rejects_wrong_manifest_before_writing(self):
        manifest = self.package / 'xiaoba/native/pet.json'
        data = json.loads(manifest.read_text(encoding='utf-8'))
        data['spritesheetPath'] = 'missing.webp'
        manifest.write_text(json.dumps(data), encoding='utf-8')
        self.install(success=False, error='Invalid Xiaoba pet manifest')
        self.assertFalse(self.config.exists())
        self.assertFalse((self.home / 'pets').exists())

    def test_dotted_desktop_does_not_corrupt_config(self):
        original = b'desktop.selected-avatar-id = "codex"\n'
        self.config.write_bytes(original)
        self.install(success=False, error='Desktop uses root dotted keys')
        self.assertEqual(self.config.read_bytes(), original)
        self.assertFalse((self.home / 'pets').exists())


if __name__ == '__main__':
    unittest.main()
