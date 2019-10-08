from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#classes
class Shop:
    def __init__(self, name = "", discount_name = "", promotion_info = "", data_storage = "", discount_list = [], discount_info_list = []):
        self.name = name
        self.discount_list = discount_list
        self.data_storage = data_storage
        self.promotion_info = promotion_info
        self.discount_info_list = discount_info_list

    def extractData(self, data, f_type, typ, loc):
        containers = data.findAll(str(f_type), {str(typ) : str(loc)})
        if self.data_storage == 'text':
            for x in containers:
                #extracting the promocode itself from the html
                self.discount_list.append(x.get_text())
        elif self.data_storage == 'value':
            for x in containers:
                #extracting the promocode itself from the html
                self.discount_list.append(x['value'])

    def extractInfoProm(self, data, f_type_first, typ_first, loc_first):
        containers = data.findAll(str(f_type_first), {str(typ_first) : str(loc_first)})
        for x in containers:
            self.discount_info_list.append(x.get_text())


class Url_Controll:
    def __init__(self, id = '', url = '', first_type = "", type = "", location = "", first_type_info = "", type_info = "", location_info = ""):
        self.id = id
        #url with coupons and informations
        self.url = url
        self.first_type = first_type
        self.type = type
        self.location = location
        #information about each promotion
        self.first_type_info = first_type
        self.type_info = type_info
        self.location_info = location_info

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
    s1 = Shop(name = 'MediaMarkt', discount_list= [], discount_info_list = [], data_storage= "text")
    s2 = Shop(name = 'RTV Euro AGD',  discount_list= [], discount_info_list = [], data_storage= "text")
    s3 = Shop(name = 'Homme & You', discount_list= [], data_storage= "value")
    u1 = Url_Controll(id = 'MM', location = 'promoCode', type = "class", first_type = "div", first_type_info = 'div', type_info = 'class',location_info = 'txt1' ,url = 'https://mediamarkt.pl/kody-rabatowe')
    u2 = Url_Controll(id = 'MM', location = "voucherC code", type = "class", first_type = "div", first_type_info = 'div', type_info = 'class', location_info = 'desc', url = 'https://www.euro.com.pl/cms/aktualne-kupony-rabatowe.bhtml?link=lp-agregator')
    u3 = Url_Controll(id = 'H&Y', location = "couponcode", type = "class", first_type = "input", url = 'https://www.kupujzrabatem.pl/nowe-kody.html?gclid=EAIaIQobChMIw8K375eM5QIVB-aaCh2ybw7bEAAYASABEgJBQfD_BwE')
    s1.extractData(u1.connectClient(), u1.first_type, u1.type, u1.location)
    s1.extractInfoProm(u1.connectClient(), u1.first_type_info, u1.type_info, u1.location_info)
    s2.extractData(u2.connectClient(), u2.first_type, u2.type, u2.location)
    s2.extractInfoProm(u2.connectClient(), u2.first_type_info, u2.type_info, u2.location_info)
    s2.discount_list = RTVspecialExtract(s2.discount_list)
    s3.extractData(u3.connectClient(), u3.first_type, u3.type, u3.location)

    prom = []
    print(s1.name + " = " + str(s1.discount_list))
    print(s1.name + " = " + str(s1.discount_info_list))
    print(s2.name + " = " + str(s2.discount_list))
    print(s2.name + " = " + str(s2.discount_info_list))
    print(s3.name + ' = ' + str(s3.discount_list))




if __name__ == "__main__":
    main()
