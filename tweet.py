import re
#helper methods to help with displayig the data or formating the data
class Tweet:

    def __init__(self, data):
        self.data = data

    #user link, when people click on user name they can go to users page
    def user_link(self):
        return "http://twitter.com/{}".format(self.data['username'])
    
    #runs 2 methods on text
    def filtered_text(self):
        return self.filter_brands(self.filter_urls(self.data['text']))

    #Adding a highlight to each studio name thats in the text
    def filter_brands(self, text):
        studios = ["StudioBones", "Madhouse", "@WIT_STUDIO", "Witstudio", "Studioghibli", 
            "sunrisestudio", "studiomappa", "MAPPA"]

        for studio in studios:
            if (studio in text):
                text = text.replace(studio, "<mark>{}</mark>".format(studio))
            else:
                continue

        return text
    #finds any links and replaces it with an a tag, making it a clickable link
    def filter_urls(self, text):
        return re.sub("(https?:\/\/\w+(\.\w+)+(\/[\w\+\-\,\%]+)*(\?[\w\[\]]+(=\w*)?(&\w+(=\w*)?)*)?(#\w+)?)", r'<a href="\1" target="_blank">\1</a>', text)