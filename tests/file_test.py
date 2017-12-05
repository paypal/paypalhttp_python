import unittest

from braintreehttp import File

class FileTest(unittest.TestCase):

    def testFromHandle(self):
        handle = open('CHANGELOG.md', 'rb')

        f = File.fromhandle(handle)
        self.assertEquals('rb', f.mode)
        self.assertEquals('CHANGELOG.md', f.name)

    def testRead(self):
        f = File('CHANGELOG.md', 'r')

        self.assertEquals(open('CHANGELOG.md').read(), f.read())

    def testRead_throwsIfClosed(self):
        f = File('CHANGELOG.md', 'r')

        f.read()
        f.close()

        try:
            f.read()
            self.fail('File.read() should have thrown an IOError after closing')
        except IOError as error:
            self.assertEquals('Open of closed file', error.message)

    def testClose(self):
        f = File('CHANGELOG.md', 'r')

        f.open()
        self.assertFalse(f.closed)

        f.close()
        self.assertTrue(f.closed)

