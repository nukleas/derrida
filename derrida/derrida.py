# Derrida
#
# A deconstructionist program.
#
# By Nader Heidari
#
#
# The purpose of this program is to act as a sort
# of "build system" for text articles. A majority
# of text in an article is not programmatically
# relevant, so what we want to do is extract stuff
# such as URLs, company names, DOIs, whatever, and
# present them in a clean form.
#
# I chose the name derrida since the program ought
# to deconstruct the articles with a touch of context,
# provided by the programmer/reader.
#
# Pretentious? Sure, but let's get to the code.
#
import re

extraction_template = {
}

class Extractor(object):
    def __init__(self, extraction_dict=None):
        # Load defaults as defined in extraction_template
        self.__dict__.update(extraction_template)
        # Override template defaults using provided dict
        if extraction_dict:
            self.__dict__.update(extraction_dict)

    def extractByRegexFrom(self,text, regex=None):
        output_list = []
        if regex is None:
            if hasattr(self, 'regex'):
                regex = self.regex
            else:
                raise KeyError("Regex is missing from extractor.")
        for found in re.finditer(regex, text):
            to_append = found.group()
            output_list.append(to_append)
        return output_list

class Test(object):
    def mockExtractor(self):
        # test if can instantiate
        derp = Extractor()
        # test if can extract
        print derp.extractByRegexFrom("THIS IS A TEST", "TEST")
        try:
            print derp.extractByRegexFrom("THIS IS A TEST")
        except KeyError:
            print "Perfect, it broke!"

test = Test()
test.mockExtractor()