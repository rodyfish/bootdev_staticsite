import unittest
from StaticPageAgent import *

class TestStaticAgent(unittest.TestCase):

    def test_extract_title(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

#weirdly place wrong headling

# correctly headline

> Quote1
> Quote2

"""

        title = extract_title(md)
        self.assertEqual(
            title,
            "correctly headline",
        )


    pass





if __name__ == "__main__":
    unittest.main()