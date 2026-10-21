"""Portable behavior checks for the packer and bundled template."""
from pathlib import Path
import tempfile
import unittest
import zipfile
import shutil
from pack_tool import package


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / 'runtime'
        shutil.copytree(Path(__file__).resolve().parents[1] / 'assets' / 'bead-helper', self.source)

    def tearDown(self):
        self.tmp.cleanup()

    def test_root_entry_and_complete_template(self):
        result = package(self.source, self.root / 'tool.zip')
        self.assertEqual(result['platform_acceptance'], 'not-tested')
        with zipfile.ZipFile(self.root / 'tool.zip') as archive:
            self.assertIn('index.html', archive.namelist())
            self.assertEqual(len(archive.namelist()), 5)

    def test_missing_resource_fails_without_zip(self):
        (self.source / 'core.js').unlink()
        with self.assertRaises(ValueError):
            package(self.source, self.root / 'tool.zip')
        self.assertFalse((self.root / 'tool.zip').exists())

    def test_inline_script_rejected(self):
        entry = self.source / 'index.html'
        entry.write_text(entry.read_text(encoding='utf-8') + '<script>alert(1)</script>', encoding='utf-8')
        with self.assertRaises(ValueError):
            package(self.source, self.root / 'tool.zip')

    def test_prevent_source_contamination_and_overwrite(self):
        with self.assertRaises(ValueError):
            package(self.source, self.source / 'tool.zip')
        output = self.root / 'keep.zip'
        output.write_bytes(b'keep me')
        with self.assertRaises(ValueError):
            package(self.source, output)
        self.assertEqual(output.read_bytes(), b'keep me')

    def test_escape_resource_rejected(self):
        entry = self.source / 'index.html'
        entry.write_text(entry.read_text(encoding='utf-8').replace('./core.js', '../outside.js'), encoding='utf-8')
        (self.root / 'outside.js').write_text('var test=1;', encoding='utf-8')
        with self.assertRaises(ValueError):
            package(self.source, self.root / 'tool.zip')


if __name__ == '__main__':
    unittest.main()
