import re


class CustomTools:

    def CleanHtml(self):
        clean_re = re.compile('<.*?>')
        clean_text = re.sub(clean_re, '', self)
        return clean_text
