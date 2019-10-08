import unittest

from paypalhttp import File

class FileTest(unittest.TestCase):

    def testFromHandle(self):
        handle = open('CHANGELOG.md', 'rb')

        f = File.fromhandle(handle)
        self.assertEqual('rb', f.mode)
        self.assertEqual('CHANGELOG.md', f.name)

        f.close()
        handle.close()

    def testRead(self):
        f = File('CHANGELOG.md', 'r')

        handle = open('CHANGELOG.md')
        self.assertEqual(handle.read(), f.read())

        f.close()
        handle.close()

    def testRead_throwsIfClosed(self):
        f = File('CHANGELOG.md', 'r')

        f.read()
        f.close()

        try:
            f.read()
            self.fail('File.read() should have thrown an IOError after closing')
        except IOError as error:
            self.assertEqual('Open of closed file', str(error))

    def testRead_allowsMultipleReads(self):
        f = File('CHANGELOG.md', 'r')

        contents = f.read()
        self.assertEqual(contents, f.read())

    def testClose(self):
        f = File('CHANGELOG.md', 'r')

        f.open()
        self.assertFalse(f.closed)

        f.close()
        self.assertTrue(f.closed)

