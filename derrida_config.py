# -*- coding: utf-8 -*-
# Rederrida config
# Currently an effort to make extraction types modular
# Explanation:
# Now, you can set types as entries in a dict.
# The structure is as follows:
#   'Type name':
#   {
#       "name": 'Type name',
#       "regex": "what to look for in the file",
#       "tag_type": "If you want to pull data from web, HTML or XML",
#       "tag": "XML or HTML tag",
#       "prefix": "stuff to add before the found text for a URL"
#       "suffix": "stuff to add after the found text for a URL"
#   }
extraction_template = {
        "name": "",
        "regex": "",
        "tag_type": "",
        "tag": "",
        "tag2": "",
        "tag2_type": "",
        "format": "",
        "joiner": "\n",
        "prefix": "",
        "suffix": "",
        "process": 0
}
extraction_types = {
    'DOI':
    {
        "name": 'DOI',
        "regex": "(10\.(\d)+/([^(\s\>\"\<\,);])+)",
        "tag_type": "XML",
        "tag": "(?i)(dc|article|citation)..itle",
        "prefix": "http://dx.doi.org/",
        "process": 1
    },
    'URL':
    {
        "name": 'URL',
        "regex": "(((ht|f)tp(s?))\://)?(www.|[a-zA-Z].)[a-zA-Z0-9\-\.]+\.(com|edu|gov|mil|net|org|biz|info|name|museum|us|ca|uk|ie|de|eu|cn)(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\;\?\'\\\+&amp;%\$#\=~_\-]+))*",
        "tag_type": "HTML",
        "tag": "title",
        "format": "{url}|{page_title}",
        "granulate": "yes",
        "process": 1
    },
    'Quote':
    {
        "name": "Quote",
        "regex": "[“\"].*?[\"”]"
    },
    'Keyword':
    {
        "name": "Keyword",
        "regex": "\S*?~.*"
    }#,
    #'Capped Word':
    #{
    #    "name": "Capitalized Words",
    #    "regex": "([A-Z][a-zA-Z0-9-]*)([\ ][A-Z][\.a-zA-Z0-9-]*)+[^\:\s\)\'\.\,\?\!]?"
    #}
}
print "config loaded"