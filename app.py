from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#classes
class Shop:
    def __init__(self, name = "", discount_name = "", locations = "", discount_list = [], type = "", first_type = ""):
        self.name = name
        self.locations = locations
        self.discount_list = discount_list
        self.type = type
        self.first_type = first_type

    def extractData(self, data):
        containers = data.findAll(str(self.first_type), {str(self.type): str(self.locations)})
        for x in containers:
            #extracting the promocode itself from the html
            self.discount_list.append(x.get_text())



class Url_Controll:
    def __init__(self, id = '', url = ''):
        self.id = id
        self.url = url

    def connectClient(self):
        #connecting up to the server of the shop
        uClient = uReq(self.url)
        html_page = uClient.read()
        uClient.close()
        #adjusting html_page to html standards
        soup_page = soup(html_page, "html.parser")
        return soup_page

#functions
def RTVspecialExtract(data):
    for x in range(0, len(data)):
        #extracting this way due to the specific website design
        first_letter = data[x].find('\nTwój kod rabatowy\r\n                ') + len('\nTwój kod rabatowy\r\n                ')
        data[x] = data[x][first_letter:]
        last_letter = data[x].find('\r\n              ')
        data[x] = data[x][:last_letter]

    return data

def main():
    s1 = Shop(name = 'MediaMarkt',locations = 'promoCode', type = "class", first_type = "div", discount_list= [])
    s2 = Shop(name = 'RTV Euro AGD', locations = "voucherC code", type = "class", first_type = "div", discount_list= [])
    u1 = Url_Controll(id = 'MM', url = 'https://mediamarkt.pl/kody-rabatowe?cd=2073544986&ad=79353350627&kd=mediamarkt%20kod%20rabatowy&gclid=CjwKCAjw_uDsBRAMEiwAaFiHazGWiUzE5sZWDQQBqS_FnkLOEoJPJFPN1Cm0jcH13J7_drv_3XI2QBoCl_0QAvD_BwE')
    u2 = Url_Controll(id = 'MM', url = 'https://www.euro.com.pl/cms/aktualne-kupony-rabatowe.bhtml?link=lp-agregator')
    s1.extractData(u1.connectClient())
    s2.extractData(u2.connectClient())
    s2.discount_list = RTVspecialExtract(s2.discount_list)
    print(s1.discount_list)
    print(s2.discount_list)


if __name__ == "__main__":
    main()
