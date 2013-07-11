import unittest
from xcolor.xparser import Xparser

class TestXcolorRegex(unittest.TestCase):

    # expected output for the tested patterns
    expected = dict(name='color5', value='aabbcc')

    def test_comments(self):
        line = ";*color5: rgb:aa/bb/cc"
        self.assertFalse(Xparser.valid(line))
        line = "#*color5: rgb:aa/bb/cc"
        self.assertFalse(Xparser.valid(line))

    def test_generic_rgb(self):
        line = "*color5: rgb:aa/bb/cc"
        self.assertTrue(Xparser.valid(line))
        output = Xparser.rgb(line)
        self.assertEqual(output, self.expected)

    def test_generic_hex(self):
        line = "*color5: #aabbcc"
        self.assertTrue(Xparser.valid(line))
        output = Xparser.hex(line)
        self.assertEqual(output, self.expected)

    def test_urxvt_rgb(self):
        line = "URxvt*color5: rgb:aa/bb/cc"
        self.assertTrue(Xparser.valid(line))
        output = Xparser.rgb(line)
        self.assertEqual(output, self.expected)

    def test_urxvt_hex(self):
        line = "URxvt*color5: #aabbcc"
        self.assertTrue(Xparser.valid(line))
        output = Xparser.hex(line)
        self.assertEqual(output, self.expected)

    def test_urxvt_dot_rgb(self):
        line = "URxvt.color5: rgb:aa/bb/cc"
        self.assertTrue(Xparser.valid(line))
        output = Xparser.rgb(line)
        self.assertEqual(output, self.expected)

    def test_urxvt_dot_hex(self):
        line = "URxvt.color5: #aabbcc"
        self.assertTrue(Xparser.valid(line))
        output = Xparser.hex(line)
        self.assertEqual(output, self.expected)

if __name__ == "__main__":
    unittest.main()
