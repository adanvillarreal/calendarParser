import datetime
from datetime import timedelta
import scrapy
from scrapy.spiders.init import InitSpider
from scrapy.utils.response import open_in_browser
from scrapy.http.cookies import CookieJar
from scrapy.utils.response import open_in_browser
from calendarParser.items import EventItem
from calendarParser.items import DayItem
from calendarParser.items import ReminderItem
import argparse

semester_end_date = '20181202T235959Z'

class TableSpider(InitSpider):
    name = 'homepage'
    start_urls =['http://alsvdbw01.itesm.mx/servesc/plsql/swghorario_itesm.cargado#']

    def __init__(self, category='', domain=None, *args, **kwargs):
        super(TableSpider, self).__init__(*args, **kwargs)
        self.pswd = kwargs.get('pswd')
        self.userId = kwargs.get('mail')


    def init_request(self):
        return scrapy.Request(meta={'dont_redirect': False}, url='https://mitecbeta.itesm.mx/', callback=self.adfs_request)

    def adfs_request(self, response):
        return scrapy.FormRequest.from_response(response,
                formdata={'ctl00$ContentPlaceHolder1$UsernameTextBox':self.userId,
                            'ctl00$ContentPlaceHolder1$PasswordTextBox':self.pswd,
                            'ctl00$ContentPlaceHolder1$ddlDomain':'TEC',
                            '__db':'15'},
                callback=self.trust)

    def trust(self, response):
        return [scrapy.FormRequest.from_response(response, url='https://mitecbeta.itesm.mx/_trust',
                              meta={'dont_redirect': False},
                              callback = self.credentials,
                              dont_filter=True
                              )]

    def credentials(self, response):
        return scrapy.Request(url='https://mitecbeta.itesm.mx/SiteAssets/ProfesionalLanding/WorkingonitAlumni.aspx', callback=self.after_login)


    def after_login(self, response):
        return self.initialized()

    def parse(self, response):
        reminder = ReminderItem()
        reminder['useDefault'] = False
        tables = response.xpath('//*[@id="detalles"]/table')
        i = 4
        while i <= len(tables):
            event = EventItem()
            materia = response.xpath('//*[@id="detalles"]/table[%d]/tr/td/font/text()' % i).extract()[0]
            event['summary'] = materia
            horarios = response.xpath('//*[@id="detalles"]/table[%d]/tr' % (i+2))
            j = 2
            while j <= len(horarios):
                semester_start_date = datetime.date(2018, 8, 5)
                dias = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[2]/font/text()' % ((i+2), j)).extract()
                inicio = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[3]/font/text()' % ((i+2), j)).extract()[0][:5]
                final = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[3]/font/text()' % ((i+2), j)).extract()[0][-10:-5]
                edificio = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[4]/font/text()' % ((i+2), j)).extract()[0]
                salon = response.xpath('//*[@id="detalles"]/table[%d]/tr[%d]/td[5]/font/text()' % ((i+2), j)).extract()[0]
                event['location'] = '%s %s' % (edificio, salon)
                for numDay in range(0, 6):
                    dayTime = DayItem()
                    if dias[numDay] != '-':
                        dayTime['dateTime'] = '%sT%s:00.000-05:00' % (semester_start_date, inicio)
                        dayTime['timeZone'] = 'America/Monterrey'
                        event['start'] = dayTime
                        dayTime = DayItem()
                        dayTime['dateTime'] = '%sT%s:00.000-05:00' % (semester_start_date, final)
                        event['end'] = dayTime
                        dayTime['timeZone'] = 'America/Monterrey'
                        recurrence = ['RRULE:FREQ=WEEKLY;UNTIL=%s' % (semester_end_date),]
                        event['recurrence'] = recurrence
                        event['reminders'] = reminder
                        yield event
                    semester_start_date = semester_start_date + timedelta(days=1)
                j += 1
            i = i+3
