import unittest

from braintreehttp.testutils import TestHarness

from braintreehttp.serializers import FormPart

class FormPartTest(TestHarness):
    def test_init_lowercase_headers(self):
        form_part = FormPart({ "key": "value" }, { "content-type": "application/json" })

        self.assertTrue("Content-Type" in form_part.headers)
        self.assertEqual(len(form_part.headers), 1)

    def test_init_headers_collision(self):
        form_part = FormPart({ "key": "value" }, { "content-type": "application/json", "CONTENT-TYPE": "application/pdf"})

        self.assertTrue("Content-Type" in form_part.headers)
        self.assertEqual(len(form_part.headers), 1)

    def test_init_single_character_header(self):
        form_part = FormPart({ "key": "value" }, { "x": "application/json" })

        self.assertTrue("X" in form_part.headers)
        self.assertEqual(len(form_part.headers), 1)

    def test_init_multiple_headers(self):
        form_part = FormPart({ "key": "value" }, { "x": "application/json", "Content-type": "application/pdf", "CONTENT-ENCODING": "gzip" })

        self.assertTrue("X" in form_part.headers)
        self.assertTrue("Content-Type" in form_part.headers)
        self.assertTrue("Content-Encoding" in form_part.headers)
        self.assertEqual(len(form_part.headers), 3)
