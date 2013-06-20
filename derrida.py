from derrida_functions import *
import derrida_config
extraction_types = derrida_config.extraction_types


class Processor(object):
    def __init__(self, extraction_dict):
        self.__dict__.update(derrida_config.extraction_template)
        self.__dict__.update(extraction_dict)

    def extractInformation(self, rawtext):
        self.found_items = findType_AddToList(rawtext, self.regex)
        return self.found_items

    def outputFormat(self, kwargs):
        print kwargs
        if hasattr(self, 'format') and self.format is not "" and isinstance(kwargs, dict):
            return self.format.format(**kwargs)
        else:
            return kwargs

    def pullFromWeb(self):
        self.results = []
        for url in set(self.found_items):
            if self.tag_type == 'XML':
                result = extractFromURL_byXMLTag(url, self.tag, self.prefix, self.suffix)
                if result is not 0:
                    self.results.append(result)
            elif self.tag_type == 'HTML':
                result = (extractFromURL_byHTMLTag(url, self.tag, self.prefix, self.suffix))
                if result is not 0:
                    self.results.append(result)
        return self.results

def deconstruct_text(rawdata):
    total_results = []
    for item in extraction_types:
        extraction_type = Processor(extraction_types[item])
        total_results.append(extraction_type.extractInformation(rawdata))
        if hasattr(extraction_type, 'process'):
            results = extraction_type.pullFromWeb()
            print results
            total_results.append(results)
    return total_results

if __name__ == "__main__":
    rawdata = openRawFile('rawdata.txt')
    output_file = open("output.txt", "a")
    for item in extraction_types:
        extraction_type = Processor(extraction_types[item])
        output_file.write("\n" + extraction_type.name + "s\n-----\n")
        for found in extraction_type.extractInformation(rawdata):
            print repr(found)
            output_file.write(found.encode('utf-8') + "\n")
        if hasattr(extraction_type, 'process') and hasattr(extraction_type, 'found_items'):
            results = extraction_type.pullFromWeb()
            if len(results) is not 0:
                output_list = []
                output_file.write("\nProcessed " + extraction_type.name + "s\n-----\n")
                for result in results:
                    output_list.append(extraction_type.outputFormat(result))
                print output_list
                output_file.write(extraction_type.joiner.join(output_list)+"\n")
