from html.parser import HTMLParser

class CardParser(HTMLParser):
    inside_p = False
    text = ''

    def clear(self):
        self.text = ''
        self.inside_p = False

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        if tag == "p":
            self.inside_p = True
    
    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        if (tag == "p") and self.inside_p:
            self.inside_p = False

    def handle_data(self, data):
        # print("Data     :", data)
        if self.inside_p:
            # print("***********")
            # print(data)
            # print("***********")
            self.text += ' ' + data