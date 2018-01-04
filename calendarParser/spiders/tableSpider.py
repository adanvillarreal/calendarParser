import datetime
from datetime import timedelta
import scrapy
from scrapy.spiders.init import InitSpider
from scrapy.utils.response import open_in_browser
from scrapy.http.cookies import CookieJar
from scrapy.utils.response import open_in_browser
from calendarParser.items import EventItem
from calendarParser.items import DayItem

semester_end_date = '20180518T235959Z'
class TableSpider(InitSpider):
    name = 'homepage'
    days = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']

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
        materias = response.xpath('//*[@id="detalles"]/table/tbody/tr/td/font/text()')
        tablesOld = response.xpath('//*[@class="texto4"]/text()').extract()
        tables = response.xpath('//*[@id="detalles"]/table')
        i = 4
        while i <= len(tables):
            event = EventItem()
            materia = response.xpath('//*[@id="detalles"]/table[%d]/tr/td/font/text()' % i).extract()[0]
            print (materia)
            event['summary'] = materia
            print("TABLA")
            print(i+2)
            horarios = response.xpath('//*[@id="detalles"]/table[%d]/tr' % (i+2))
            j = 2
            while j <= len(horarios):
                dias = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[2]/font/text()' % ((i+2), j)).extract()
                #print (dias)
                inicio = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[3]/font/text()' % ((i+2), j)).extract()[0][:5]
                #print(inicio)
                final = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[3]/font/text()' % ((i+2), j)).extract()[0][-10:-5]
                #print(final)
                edificio = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[4]/font/text()' % ((i+2), j)).extract()[0]
                #print(edificio)
                salon = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[5]/font/text()' % ((i+2), j)).extract()[0]
                #print(salon)
                event['location'] = '%s %s' % (edificio, salon)


                semester_start_date = datetime.date(2018, 1, 7)

                for numDay in range(0, 6):
                    dayTime = DayItem()
                    if dias[numDay] != '-':
                        dayTime['dateTime'] = '%sT%s:00.000-06:00' % (semester_start_date, inicio)
                        dayTime['timeZone'] = 'America/Monterrey'
                        event['start'] = dayTime
                        dayTime = DayItem()
                        dayTime['dateTime'] = '%sT%s:00.000-06:00' % (semester_start_date, final)
                        event['end'] = dayTime
                        dayTime['timeZone'] = 'America/Monterrey'
                        recurrence = ['RRULE:FREQ=WEEKLY;UNTIL=%s' % (semester_end_date),]
                        event['recurrence'] = recurrence
                        yield event
                    semester_start_date = semester_start_date + timedelta(days=1)

                j += 1
            #print(materia + dias + inicio + final + edificio + salon)
            i = i+3
        #int count = 0
        #for table in tables:
        #    if count == 3:
        #        materia = table.xpath('/text()')
