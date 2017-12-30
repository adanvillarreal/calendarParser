import scrapy
from scrapy.spiders.init import InitSpider
from scrapy.utils.response import open_in_browser
from scrapy.http.cookies import CookieJar
from scrapy.utils.response import open_in_browser


class TableSpider(InitSpider):
    name = "homepage"
    handle_httpstatus_list = [301, 302]
    start_urls = ['http://alsvdbw01.itesm.mx/servesc/plsql/swghorario_itesm.cargado#']
    login_page = 'https://fs.itesm.mx/adfs/ls/?wa=wsignin1.0&wtrealm=urn%3asharepoint%3amitecbeta&wctx=https%3a%2f%2fmitecbeta.itesm.mx%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252F'
    def init_request(self):
        return scrapy.Request(meta={'dont_redirect': False}, url=self.login_page, callback=self.login)

    def login(self, response):
        return[scrapy.FormRequest.from_response(response,
                formdata={'ctl00$ContentPlaceHolder1$UsernameTextBox':'a01281312@itesm.mx',
                            'ctl00$ContentPlaceHolder1$PasswordTextBox':'',
                            'ctl00$ContentPlaceHolder1$ddlDomain':'TEC'},
                callback=self.after_login)]

    def after_login(self, response):
        print(response)
        open_in_browser(response)
        print("SOMETHING\n*******\n*******")
        return self.initialized()

    def parse(self, response):
        open_in_browser(response)
        url = 'http://alsvdbw01.itesm.mx/servesc/plsql/swghorario_itesm.cargado#'
        return scrapy.Request(url,
                          callback=self.parse_calendar_details)

    def parse_calendar_details(self, response):
        print(response.body)
        print("RERERERERER")
        count = 0
        tables = response.xpath('//*[@id="detalles"]/table');
        for result in tables:
            if count < 3:
                count+=1
                continue
            for x in range(0, 3):
                print(table[count])
                count +=1
