from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import time

from urllib.request import urlopen
import html2text
from bs4 import BeautifulSoup
import requests, os


url = "https://www.craigslist.org/about/sites"
link_craigslist = '/d/software-qa-dba-ecc/search/sof'
category = 'Software'



root = Tk()
root.title('Search terms on Craiglist')
root.geometry('600x600')

#Panel 1
panel_1 = PanedWindow(bd=1, relief="flat", bg="grey")
panel_1.pack(fill=X)

panel_1_2 = PanedWindow(panel_1, orient=HORIZONTAL, bd=1, relief="flat", bg="grey")
panel_1.add(panel_1_2)

panel_1_3 = PanedWindow(panel_1, orient=HORIZONTAL, bd=1, relief="flat", bg="grey")
panel_1.add(panel_1_3)


#Panel 2
panel_2 = PanedWindow(bd=1, relief="flat", bg="grey")
panel_2.pack(fill=X)

panel_2_1 = PanedWindow(panel_2, orient=HORIZONTAL, bd=1, relief="flat", bg="grey")
panel_2.add(panel_2_1)


#Panel 3
panel_3 = PanedWindow(bd=1, relief="flat", bg="grey")
panel_3.pack(fill=X)

panel_3_1 = PanedWindow(panel_3, orient=HORIZONTAL, bd=1, relief="flat", bg="grey")
panel_3.add(panel_3_1)


tree = ttk.Treeview()
panel_3_1.add(tree)



headers = requests.utils.default_headers()
headers.update({ "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0" })

req = requests.get(url, headers)
soup = BeautifulSoup(req.content, "html.parser")

listCity = soup.find("div", {"class": "colmask"})

list_city_us = {}
city_selected = '- Select a city -'

linksCity = listCity.find_all("a")
for linkCity in linksCity:
    urlCity = linkCity.get("href")
    city = urlCity.split(".")[0].replace("https://","").capitalize()
    list_city_us[city] = urlCity 

list_city_us = dict(sorted(list_city_us.items(), key=lambda item: item[1]))


def select_city(selection):
    city_selected = list_city_us.get(selection)

def openLink(event):
    item = tree.selection()[0]
    
    import webbrowser
    webbrowser.open('{}'.format(tree.item(item,"text")))

def search():
    search_text = term_to_search_input.get()
    selected_city = list_city_us.get(city.get())

    if(search_text != '' and selected_city != '- Select -'):
            
        link_city_type_ad = selected_city + link_craigslist

        req = requests.get(link_city_type_ad, headers)
        soap = BeautifulSoup(req.content, "html.parser")

        link_ads = soap.findAll("a", {"class": "result-title"})

        for link_ad in link_ads:
            link_ad_text = link_ad.get("href")

            req = requests.get(link_ad_text)
            content = req.content
            txt = html2text.html2text(str(content))
            x = txt.find(search_text)
            if x != -1:
                tree.insert("", "end", text=link_ad_text)
        
        tree.bind("<Double-1>", openLink)


city = StringVar()
city.set("- Select -")

term_to_search = Label(panel_1_2, text="Term to search for(Category:" + category + ")")
term_to_search_input = Entry(root, width=40)

panel_1_2.add(term_to_search)
panel_1_2.add(term_to_search_input)

select_state = Label(root, text="Select City")
list_states = OptionMenu(root, city, *list_city_us.keys(), command=select_city)
panel_1_3.add(select_state)
panel_1_3.add(list_states)

search_button = Button(root, text="Search", command=search)
panel_2.add(search_button)

root.mainloop()