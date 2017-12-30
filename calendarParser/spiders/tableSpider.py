import scrapy
from scrapy.spiders.init import InitSpider
from scrapy.utils.response import open_in_browser
from scrapy.http.cookies import CookieJar
from scrapy.utils.response import open_in_browser


class TableSpider(InitSpider):
    name = "homepage"
    #handle_httpstatus_list = [301, 302]
    start_urls =['http://alsvdbw01.itesm.mx/servesc/plsql/swghorario_itesm.cargado#']
    login_page = 'https://mail.itesm.mx/'
    def init_request(self):
        return scrapy.Request(meta={'dont_redirect': False}, url='https://mitecbeta.itesm.mx/', callback=self.adfs_request)

    def adfs_request(self, response):
        print("ADFS REQUEST++++++++++++++")
        return scrapy.FormRequest.from_response(response,
                formdata={'ctl00$ContentPlaceHolder1$UsernameTextBox':'a01281312@itesm.mx',
                            'ctl00$ContentPlaceHolder1$PasswordTextBox':'password',
                            'ctl00$ContentPlaceHolder1$ddlDomain':'TEC',
                            '__db':'15'},
                callback=self.trust)

    def trust(self, response):
        print("TRUST++++++++++++")
        print(response)
        return [scrapy.FormRequest.from_response(response, url='https://mitecbeta.itesm.mx/_trust',
                              meta={'dont_redirect': False},
                              callback = self.credentials,
                              dont_filter=True
                              )]

    def credentials(self, response):
        print("CREDENTIALS++++++++")
        print(response)
        return scrapy.Request(url='https://mitecbeta.itesm.mx/SiteAssets/ProfesionalLanding/WorkingonitAlumni.aspx', callback=self.after_login)


    def after_login(self, response):
        print(response)
        print("SOMETHING\n*******\n*******")
        #return [scrapy.Request(meta={'dont_redirect': False}, url='https://mitecbeta.itesm.mx/_trust/default.aspx?trust=ADFSProd&ReturnUrl=%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252F&Source=%2F', callback=self.after_login2)]
        return self.initialized()

    def parse(self, response):
        print(response.body)
        print("RERERERERER")
        count = 0
        tables = response.xpath('//*[@id="detalles"]/table/text()');
        for table in tables:
            print(table)
