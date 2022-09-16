from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, Image, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import re, fitz, glob
import io, os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont('Arial', 8)
        if self._pageNumber == 2:
            self.drawRightString(197*mm,23*mm, "%d" % (page_count))

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
                self.chapter = text
                key = 'h1-%s' % self.seq.nextf('Heading1')
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, 0, 0) 
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))
                self.chapter = text
                key = 'h2-%s' % self.seq.nextf('Heading2')
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, 0, 0) 

class docPDF():
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Arial', 'Data/Font/arial.ttf', 'UTF-8'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'Data/Font/arialbd.ttf', 'UTF-8'))
        pdfmetrics.registerFont(TTFont('Arial-Italic', 'Data/Font/ariali.ttf', 'UTF-8'))
        registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic')

        self.styleCenter = ParagraphStyle('Center', alignment=TA_CENTER, fontName='Arial', fontSize = 14, leading = 22)
        self.styleNormal = ParagraphStyle(name='Normal', fontName='Arial', alignment=TA_JUSTIFY, fontSize = 14, firstLineIndent = 24, wordWrap=True, bulletIndent = 24, leading = 22)
        self.styleNormalTable = ParagraphStyle(name='NormalTable', fontName='Arial', fontSize = 12)
        self.styleH1 = ParagraphStyle(name='Heading1', fontName='Arial', fontSize = 16, firstLineIndent = 20)
        self.styleH2 = ParagraphStyle(name='Heading2', fontName='Arial', alignment=TA_JUSTIFY, fontSize = 14, firstLineIndent = 24, wordWrap=True, bulletIndent = 24, leading = 22)
        self.styleH3 = ParagraphStyle(name='Heading3', fontName='Arial', fontSize = 14, firstLineIndent = 20)

        self.doc = MyDocTemplate('Data/Report/Report.pdf', pagesize=A4,
                                rightMargin=28,leftMargin=70,
                                topMargin=45,bottomMargin=70)

        frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width, self.doc.height, id='normal')
        template_large_frame = PageTemplate(id='template_large_frame', frames=frame, onPage=self.gost_large_frame)
        template_blank_frame = PageTemplate(id='template_blank_frame', frames=frame, onPage=self.gost_blank_frame)
        template_small_frame = PageTemplate(id='template_small_frame', frames=frame, onPage=self.gost_small_frame)

        self.doc.addPageTemplates([template_blank_frame, template_large_frame, template_small_frame])

        self.story = [] # словарь документа

    def gost_small_frame(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.drawInlineImage("Data/small_frame.png", x=0, y=0, width=width, height=height)
        canvas.setFont('Arial', 14)
        canvas.drawString(100*mm,13*mm,f"{self.data['code_project']}")
        canvas.setFont('Arial', 10)
        width_position = 196.5 if doc.page < 10 else 195.5
        height_position = 11
        canvas.drawString(width_position*mm, height_position*mm, " %d " % doc.page)
        canvas.setFont('Arial', 8)
        canvas.drawString(21.5*mm,8.5*mm,"Изм.")
        canvas.drawString(29.7*mm,8.5*mm,"Кол. уч.")
        canvas.drawString(41.5*mm,8.5*mm,"Лист")
        canvas.drawString(50.3*mm,8.5*mm,"№ док.")
        canvas.drawString(66.5*mm,8.5*mm,"Подп.")
        canvas.drawString(83.5*mm,8.5*mm,"Дата")
        canvas.drawString(195.3*mm,18*mm,"Лист")
        canvas.restoreState()

    def gost_large_frame(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.drawInlineImage("Data/large_frame.png", x=0, y=0, width=width, height=height)
        canvas.setFont('Arial', 12, leading = None)
        canvas.drawString(100*mm,38*mm,f"{self.data['code_project']}")
        canvas.setFont('Arial', 8)
        canvas.drawString(21*mm,33*mm,"Изм.")
        canvas.drawString(30*mm,33*mm,"Кол. уч.")
        canvas.drawString(42*mm,33*mm,"Лист")
        canvas.drawString(51*mm,33*mm,"№ док.")
        canvas.drawString(65*mm,33*mm,"Подп.")
        canvas.drawString(80*mm,33*mm,"Дата")
        canvas.drawString(178.5*mm,28*mm,"Лист")
        canvas.drawString(191*mm,28*mm,"Листов")
        canvas.drawString(161.5*mm,28*mm,"Стадия")
        # canvas.drawString(194.5*mm,23*mm,"?")
        canvas.drawString(163.5*mm,23*mm,"ОТР")
        canvas.drawString(181*mm,23*mm,"2")
        canvas.drawString(21*mm,28*mm,"Разраб.")
        canvas.drawString(21*mm,23*mm,"Нач. отдела")
        canvas.drawString(116*mm,18*mm,"Содержание")
        canvas.drawString(21*mm,13*mm,"Н. контр.")
        canvas.drawString(21*mm,8*mm,"ГИП")
        canvas.restoreState()
        
    def gost_blank_frame(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.drawInlineImage("Data/blank_frame.png", x=0, y=0, width=width, height=height)
        canvas.restoreState()
    
    def search_table_in_pdf(self, path_to_pvsyst):
        with fitz.open(path_to_pvsyst) as doc:
            for page in doc:
                text = page.search_for("January")
                if len(text) != 0:
                    num_page = page.number  
                    break
                
            text = doc[num_page].get_text()
            
            main_result = text.split('Production')[1].split('Normalized')[0].strip("\n").replace('\n', ' ').split(' ')
            int_main_result = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), main_result))
            
            balances_and_main_result = text.split('ratio')[-1].split('Legends')[0].strip("\n").split('\n')
        return balances_and_main_result, int_main_result

    def convert_to_pdf(self, file_svg, file_pdf):
        renderPDF.drawToFile(svg2rlg(file_svg), file_pdf, self.styleNormal)

    #титул  
    def title(self, data):
        self.story.append(Spacer(1, 50))
        self.story.append(Paragraph("<font size=12>Регистрационный номер – СРО № П-019-7701921436-01 от 24 июня 2015 (СРО <br/> \
                            Ассоциации ЭАЦП «Проектный портал» № Ростехнадзора: СРО-П-019-26082009)</font>", self.styleCenter))
        self.story.append(Spacer(1, 50))
        self.story.append(Paragraph(f"Заказчик: {data['client']}", self.styleNormalTable))
        self.story.append(Spacer(1, 70))
        self.story.append(Paragraph(f"<font size=16><b>«{data['title_project']}»</b></font>", self.styleCenter))
        self.story.append(Spacer(1, 100))
        self.story.append(Paragraph(f"<font size=12>Основные технические решения <br/> <b>{data['code_project']}</b></font>", self.styleCenter))
        self.story.append(NextPageTemplate('template_large_frame'))

    #Содержание 
    def table_of_content(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph('<b>Содержание</b>', self.styleCenter))

        toc = TableOfContents()
        toc.levelStyles = [self.styleH3]
        self.story.append(toc)
        self.story.append(NextPageTemplate('template_small_frame'))

    # Раздел 1
    def section_1(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>1 Термины и сокращения</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("В ОТР приняты следующие сокращения:", self.styleNormal))
        self.story.append(Spacer(1, 12))

        table_cut = Table(
        [
        [Paragraph('<b>Сокращение</b>', self.styleNormalTable), Paragraph('<b>Значение</b>', self.styleNormalTable)],
        [Paragraph('АКБ', self.styleNormalTable), Paragraph('Аккумуляторная батарея', self.styleNormalTable)],
        [Paragraph('ЗП', self.styleNormalTable), Paragraph('Задание на проектирование', self.styleNormalTable)],
        [Paragraph('КИУМ', self.styleNormalTable), Paragraph('Коэффициент использования установленной мощности', self.styleNormalTable)],
        [Paragraph('ОТР', self.styleNormalTable), Paragraph('Основные технические решения', self.styleNormalTable)],
        [Paragraph('СЭС', self.styleNormalTable), Paragraph('Солнечная электростанция', self.styleNormalTable)],
        [Paragraph('ОК', self.styleNormalTable), Paragraph('Опорные конструкции фотоэлектрических модулей', self.styleNormalTable)],
        [Paragraph('ПД', self.styleNormalTable), Paragraph('Проектная документация', self.styleNormalTable)],
        [Paragraph('РД', self.styleNormalTable), Paragraph('Рабочая документация', self.styleNormalTable)],
        [Paragraph('ФЭМ', self.styleNormalTable), Paragraph('Фотоэлектрические модули', self.styleNormalTable)]
        ]
        )

        table_cut.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'CENTRE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        self.story.append(table_cut)

    # Раздел 2
    def section_2(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>2 Исходные данные</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("Опросный лист переделанный под отчет:", self.styleNormal))
        self.story.append(Spacer(1, 170))
        self.story.append(Paragraph("<b>Переделанный опросный лист под отчет</b>", self.styleCenter))
        self.story.append(Spacer(1, 12))
        img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
        self.story.append(img)
        # Вставить готовый опросный лист

    # Раздел 3
    def section_3(self, data):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>3	Место размещения объекта</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        
        if data["block_3_1"] == False:
            self.story.append(Paragraph("<b>3.1	Описание границ участка</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            # Настроить отступы
            self.story.append(Paragraph(f"По данным предпроектного обследования и,согласно исходным данным, \
                                    объект – {'<b>многоквартирный жилой дом</b>'}, расположенный по адресу: {'<b>г. Екатеринбург, ул. Анатолия Мехренцева, 36.</b>'} \
                                    Координаты - {'<b>55.587562, 37.908986.</b>'}", self.styleNormal))
            self.story.append(Paragraph("<b>Вручную описать инфраструктуру территории или выписать данные из отчета ППО.</b>", self.styleNormal))
            self.story.append(Spacer(1, 24))
            
            if data['all_range'] != "Н/Д":
                data_range = data['all_range'].split(',')[0].split(' - ')
                start_range = data_range[0]
                end_range = data_range[1]
            else:
                start_range = "Н/Д"
                end_range = "Н/Д"
                
            
        if data["block_3_2"] == False:
            self.story.append(Paragraph("<b>3.2	Климатические условия</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph(f"<b>Климат Балаково - умеренно континентальный засушливый. \
                                    Характерной особенностью климата является преобладание в течение года ясных малооблачных дней, \
                                    умеренно холодная и малоснежная зима. Непродолжительная засушливая весна, жаркое и сухое лето. \
                                    Континентальный климат смягчён близостью реки Волги.</b> ИЗ ВИКИПЕДИИ", self.styleNormal))
            self.story.append(Paragraph(f"Общая климатическая характеристика площадки строительства (по данным метеостанции № {data['num_weather_station']}, \
                                    за срок наблюдения с {start_range} по {end_range} данные сайта https://rp5.ru ):", self.styleNormal))

            self.story.append(Spacer(1, 12))
            table_rp5 = Table(
            [
            [Paragraph('Средняя температура воздуха, °С', self.styleNormalTable), Paragraph(data['average_temp'], self.styleNormalTable)],
            [Paragraph('Минимальная температура воздуха, °С', self.styleNormalTable), Paragraph(data['min_temp'], self.styleNormalTable)],
            [Paragraph('Максимальная температура воздуха, °С', self.styleNormalTable), Paragraph(data['max_temp'], self.styleNormalTable)],
            [Paragraph('Среднее атмосферное давление, мм.рт.ст.', self.styleNormalTable), Paragraph(data['average_pressure'], self.styleNormalTable)],
            [Paragraph('Средняя влажность воздуха, %', self.styleNormalTable), Paragraph(data['average_humidity'], self.styleNormalTable)],
            [Paragraph('Преобладающий ветер ', self.styleNormalTable), Paragraph(data['main_wind'], self.styleNormalTable)],
            [Paragraph('Скорость ветра средняя, м/с ', self.styleNormalTable), Paragraph(data['average_speed_wind'], self.styleNormalTable)],
            [Paragraph('Скорость ветра максимальная, м/с', self.styleNormalTable), Paragraph(data['max_speed_wind'], self.styleNormalTable)],
            [Paragraph('Количество осадков, мм за 12 ч.', self.styleNormalTable), Paragraph(data['precipitation_on_12_hour'], self.styleNormalTable)],
            [Paragraph('Высота снежного покрова средняя, мм', self.styleNormalTable), Paragraph(data['average_height_snow'], self.styleNormalTable)],
            [Paragraph('Высота снежного покрова максимальная, мм', self.styleNormalTable), Paragraph(data['max_height_snow'], self.styleNormalTable)],
            [Paragraph('Самая ранняя дата появления снежного покрова', self.styleNormalTable), Paragraph(data['first_date_snow'], self.styleNormalTable)],
            [Paragraph('Самая поздняя дата наличия снежного покрова: ', self.styleNormalTable), Paragraph(data['last_date_snow'], self.styleNormalTable)]
            ]
            )

            table_rp5.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            self.story.append(table_rp5)
            
        if data["block_3_3"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>3.3 Топография площадки</b>", self.styleH2))
            self.story.append(Spacer(1, 12))

            # нет шаблона
            self.story.append(Spacer(1, 20))
            self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
            self.story.append(Spacer(1, 12))
            img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
            self.story.append(img)

            self.story.append(Spacer(1, 24))
        if data["block_3_4"] == False:
            self.story.append(Paragraph("<b>3.4	 Точка подключения объекта</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            # Настроить отступы
            self.story.append(Paragraph(f'Подключение инверторов производится в существующую сеть объекта на напряжение {data["u_dot_in"]} кВ согласно схеме присоединения:', self.styleNormal))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Удаленность инверторов от соответствующих точек присоединения представлено в таблице ниже:", self.styleNormal))

            self.story.append(Spacer(1, 12))
            table_invertor = Table(
            [
            [Paragraph('<b>Инвертор</b>', self.styleNormalTable), Paragraph('<b>Расстояние до точки подключения, м</b>', self.styleNormalTable)],
            [Paragraph(' ', self.styleNormalTable), ' '],
            [Paragraph(' ', self.styleNormalTable), ' '],
            [Paragraph(' ', self.styleNormalTable), ' '],
            ]
            )

            table_invertor.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            self.story.append(table_invertor)

    # Раздел 4
    def section_4(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>4 Анализ ресурсов (инсоляция)</b>", self.styleH1))
        self.story.append(Spacer(1, 170))
        self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
        self.story.append(Spacer(1, 12))
        img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
        self.story.append(img)

    # Раздел 5
    def section_5(self, data):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>5 Основные параметры СЭС</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        
        if data["block_5_1"] == False:
            self.story.append(Paragraph("<b>5.1 Назначение и состав СЭС</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph(f"Назначение СЭС – выработка электрической энергии путем фотоэлектрического преобразования \
                                    солнечной энергии поступающей на фотоэлектрические модули (ФЭМ) в электрическую с помощью инверторной установки, \
                                    выдача мощности во внутреннюю сеть {data['u_dot_in']} кВ, а также мониторинг работы СЭС, \
                                    и в случае необходимости, ограничение выработки СЭС.", self.styleNormal))
            self.story.append(Paragraph(f"СЭС имеет установленную мощность ФЭМ {'<b>____ кВт</b>'}. \
                                    Режим работы СЭС периодический – преобразование световой энергии солнца \
                                    в электрическую энергию будет производиться только в дневное время суток. \
                                    Работа оборудования СЭС осуществляется в автоматическом режиме.", self.styleNormal))
            self.story.append(Paragraph("Фотоэлектрическая система состоит из следующих элементов:", self.styleNormal))
            self.story.append(Paragraph("<bullet>&bull;</bullet> опорных конструкций, к которым крепятся ФЭМ;", self.styleNormal))
            self.story.append(Paragraph(f"<bullet>&bull;</bullet> инверторного оборудования, к которому подключены ФЭМ кабельными линиями постоянного тока. \
                                    Инвертор подключен кабелем переменного тока к ячейке {data['u_dot_in']} кВ;", self.styleNormal))
            self.story.append(Paragraph("<bullet>&bull;</bullet> оборудования для мониторинга выработки мощности;", self.styleNormal))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Массив ФЭМ состоит из _ цепочек, собранных суммарно из _ ФЭМ. \
                                    Цепочки подключаются к инвертору солнечным кабелем постоянного тока, \
                                    изоляция которого обладает повышенной стойкостью к воздействию ультрафиолета.", self.styleNormal))
            self.story.append(Paragraph("Информацию о работе системы и её состоянии обслуживающий персонал получает с помощью облачного сервиса.", self.styleNormal))
            self.story.append(Paragraph("Основные технико-экономические параметры работы СЭС представлены в таблице 5.1.", self.styleNormal))
            self.story.append(Paragraph("Таблица 5.1 — Основные технологические характеристики СЭС", self.styleNormal))
            print(len(data['specific_production']) is dict)
            if data['specific_production'] != 'Н/Д' and not len(data['specific_production']) is dict:
                use_set_power = round(8765 / int(data['specific_production']) * 100, 2)
            elif data['specific_production'] != 'Н/Д' and len(data['specific_production']) is dict:
                use_set_P = []
                for k, v in data['specific_production'].items():
                    use_set_P.append(k + f"{round(8765 / int(v) * 100, 2)}")
                use_set_power = ', '.join(use_set_P)
            else: 
                use_set_power = 'Н/Д'

            table_ses_params = Table(
            [
            [Paragraph('<b>Наименование показателя</b>', self.styleNormalTable), Paragraph('<b>Единица измерения</b>', self.styleNormalTable), Paragraph('<b>Величина</b>', self.styleNormalTable)],
            [Paragraph('Установленная мощность СЭС по ФЭМ', self.styleNormalTable), Paragraph('кВт', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Максимальная мощность СЭС по инверторам', self.styleNormalTable), Paragraph('кВт', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Количество устанавливаемых ФЭМ', self.styleNormalTable), Paragraph('шт', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Выработка электроэнергии в год (P50)*', self.styleNormalTable), Paragraph('МВт*ч', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Коэффициент использования установленной мощности (P50)*', self.styleNormalTable), Paragraph('%', self.styleNormalTable), 
                Paragraph(f'{use_set_power}', self.styleNormalTable)],
            ]
            )

            table_ses_params.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'CENTRE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            self.story.append(table_ses_params)
            self.story.append(Paragraph("* - модельное значение выработки электроэнергии с вероятностью 50%.", self.styleNormal))

        if data["block_5_1_1"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.1.1 ФЭМ</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Для преобразования энергии солнечного света в электрическую предусмотрено устройство массива фотоэлектрических модулей. \
                                    ФЭМ изготовлены в виде прямоугольных пластин размером ____х____х__ мм. ФЭМ состоит из нескольких основных элементов – \
                                    элементов каркаса, фоточувствительных ячеек, электрической коммутации элементов, подложки, ламинирующей пленки и закаленного стекла. \
                                    ФЭМ является комплектным изделием и не подлежит разборке и самостоятельному ремонту. \
                                    Световой поток при инсоляции проходит через закаленное стекло и прозрачную ламинирующую пленку и попадает на светочувствительные ячейки, \
                                    воздействуя на полупроводниковый материал, в результате воздействия возникает электрический ток, \
                                    который образует разность потенциалов на выводах полупроводникового элемента. С помощью электрической коммутации \
                                    (последовательного и параллельного соединения ячеек) значение напряжения в режиме холостого хода на выводах ФЭМ составляет __ В, \
                                    а ток в режиме короткого замыкания составляет __ А.", self.styleNormal))
            self.story.append(Paragraph("ФЭМ закрепляются на специальные несущие конструкции, заземляются и выставляются на определенные расчетом углы работы. \
                                    Данное закрепление позволяет выдерживать ветровые и снеговые нагрузки, \
                                    действующие на массив ФЭМ в течении всего срока эксплуатации станции. ", self.styleNormal))
            self.story.append(Paragraph("Основные технические характеристики панелей ФЭМ представлены в таблице 5.2.", self.styleNormal))
            self.story.append(Paragraph("Таблица 5.2 — Технические характеристики фотоэлектрических модулей", self.styleNormal))

            table_fem_params = Table(
            [
            [Paragraph('<b>Наименование показателя</b>', self.styleNormalTable), Paragraph('<b>Единица измерения</b>', self.styleNormalTable), Paragraph('<b>HJT 395 M2+</b>', self.styleNormalTable)],
            [Paragraph('Максимальная мощность', self.styleNormalTable), Paragraph('Вт', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Напряжение при номинальной мощности', self.styleNormalTable), Paragraph('В', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Сила тока при максимальной мощности', self.styleNormalTable), Paragraph('А', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Напряжение холостого хода', self.styleNormalTable), Paragraph('В', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Ток короткого замыкания', self.styleNormalTable), Paragraph('А', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Габариты', self.styleNormalTable), Paragraph('мм', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Площадь', self.styleNormalTable), Paragraph('м2', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Вес', self.styleNormalTable), Paragraph('кг', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            ]
            )

            table_fem_params.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'CENTRE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            self.story.append(table_fem_params)
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Характеристики даны при стандартных тестовых условиях: (удельный световой поток 1000Вт/м2, \
                                    температура модуля 25ºС, атмосферная масса 1,5).", self.styleNormal))
        if data["block_5_1_2"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.1.2 Опорные конструкции</b>", self.styleH2))
            self.story.append(Spacer(1, 12))

            path_to_image = "Data/Images/"

            if data["roof"] == 1:
                #1 плоская
                self.story.append(Paragraph("Способ крепления ФЭМ на кровле производится к опорной конструкции на пригрузах. \
                                        Монтаж ФЭМ ведется при помощи типовых металлоконструкций без крепления к поверхности кровли, \
                                        с применением пригруза (ж/б плит или аналогичного материала, не подверженного длительному разрушению \
                                        от воздействия климатических факторов окружающей среды).", self.styleNormal))
                self.story.append(Paragraph("Масса пригрузов в удельном эквиваленте (кг/м2) определяется результатом расчета отрывающей нагрузки \
                                        на конструкцию после проведения предпроектного обследования кровли и здания. ", self.styleNormal))
                self.story.append(Paragraph("Угол наклона ФЭМ на кровле здания принимается таким, чтобы обеспечить максимальную выработку электроэнергии.", self.styleNormal))
                self.story.append(Paragraph("Примерный вид опорных конструкций показан на рисунке __.", self.styleNormal))
                img = Image(path_to_image + "Кровля/плоская/Балласт З-В.jpg", 6*inch, 3*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 12))
                self.story.append(Paragraph("Рисунок __ - Опорные конструкции.", self.styleCenter))
            elif data["roof"] == 2:
                #2 скатная
                self.story.append(Paragraph("Крепление ФЭМ к кровле осуществляется посредством типовых металлоконструкций \
                                        с проникновением в несущие элементы кровли здания. Герметичность кровли не нарушается. ", self.styleNormal))
                self.story.append(Paragraph("Угол наклона и ориентация ФЭМ принимается по углу и ориентации ската кровли.", self.styleNormal))
                self.story.append(Paragraph("Примерный вид опорных конструкций показан на рисунке __.", self.styleNormal))
                img = Image(path_to_image + "Кровля/скатная/черепица.jpg", 6*inch, 3*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 12))
                self.story.append(Paragraph("Рисунок __ - Опорные конструкции.", self.styleCenter))
            elif data["roof"] == 3:
                #3 фикс
                self.story.append(Paragraph("ФЭМ устанавливаются на опорные столы в конфигурации __х__ (__ ряда по __модулей в ряду), \
                                        сориентированных по сторонам света на юг. Опорный стол состоит из стальных свай и набора \
                                        алюминиевого профиля с метизами для крепления ФЭМ. ", self.styleNormal))
                self.story.append(Paragraph("Примерный вид опорных конструкций показан на рисунке __.", self.styleNormal))
                img = Image(path_to_image + "Кровля/фиксы/Чертеж фикс 4 ряда.png", 3*inch, 4*inch)
                self.story.append(img)
                img = Image(path_to_image + "Кровля/фиксы/Вид фикс 4 ряда.png", 5*inch, 3*inch)
                self.story.append(img)
                self.story.append(Paragraph("Рисунок __ - Опорные конструкции.", self.styleCenter))
                self.story.append(Spacer(1, 12))
                self.story.append(Paragraph("На объекте предусматривается установка __ опорных конструкций. Шаг между двумя опорными \
                                        конструкциями в направлении север-юг (питч) составляет __ м.", self.styleNormal))
                self.story.append(Paragraph("Величина заглубления стоек опорной конструкции и конструктивное исполнение определены \
                                        поставщиком данного оборудования исходя из геологических условий и расчетных нагрузок.", self.styleNormal))
                self.story.append(Paragraph("Исходя из снегового района (__, по СП20.13330) принять расстояние от поверхности грунта\
                                        до нижней кромки ОК ФЭМ – __ мм.", self.styleNormal))
            
        if data["block_5_1_3"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.1.3 Инверторное оборудование</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph(f"На проектируемой солнечной электростанции для преобразования энергии постоянного тока (от ФЭМ) \
                                    в переменное {data['phase']}-х фазное напряжение, использованы инверторы. Для преобразования постоянного тока \
                                    в переменный к установке приняты инверторы {data['module']}.", self.styleNormal))
            self.story.append(Paragraph("Схемы объединения ФЭМ в цепочки и подключение к инвертору представлены на чертежах ___.", self.styleNormal))
            img = Image(path_to_image + "Инверторы/Sungrow_Invertor.png", 5*inch, 4*inch)
            self.story.append(img)
            self.story.append(Paragraph("Рисунок __ – Внешний вид инвертора", self.styleCenter))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Таблица __  – Параметры инверторов", self.styleNormal))

            table_invertor_params = Table(
            [
            [Paragraph('<b>Характеристики</b>', self.styleNormalTable), Paragraph(f'<b>Инвертор {data["module"]}</b>', self.styleNormalTable)],
            [Paragraph(f'Максимальная выходная мощность долговременной работы: <br/> \
                        - t окружающей среды: {data["tp_nom"]}°С <br/> \
                        - t окружающей среды: {data["tp_lim"]}°С <br/> \
                        - t окружающей среды: {data["tp_lim_abs"]}°С', self.styleNormalTable), 
                        Paragraph(f'{data["p_nom"]} кВА <br/> \
                                    {data["p_lim"]} кВА <br/> \
                                    {data["p_lim_abs"]} кВА', self.styleNormalTable)],
            [Paragraph('Диапазон выходного напряжения переменного тока', self.styleNormalTable), Paragraph(f'{data["phase"]} ф., {data["v_out"]} В', self.styleNormalTable)],
            [Paragraph('Максимальный выходной ток', self.styleNormalTable), Paragraph(f'≤ {data["i_out_max"]} В', self.styleNormalTable)],
            [Paragraph('Максимальный КПД преобразования', self.styleNormalTable), Paragraph(f'{data["kpd_max"]}%', self.styleNormalTable)],
            [Paragraph('Европейский показатель КПД', self.styleNormalTable), Paragraph(f'{data["kpd_euro"]}%', self.styleNormalTable)],
            [Paragraph('Диапазон выходной частоты', self.styleNormalTable), Paragraph('55 – 65 Гц', self.styleNormalTable)],
            [Paragraph('Минимальное напряжение цепочки ФЭМ', self.styleNormalTable), Paragraph(f'{data["v_mpp_min"]} В', self.styleNormalTable)],
            [Paragraph('Максимальное напряжение цепочки ФЭМ', self.styleNormalTable), Paragraph(f'{data["v_abs_max"]} В', self.styleNormalTable)],
            [Paragraph('Диапазон рабочего входного напряжения MPPT', self.styleNormalTable), Paragraph(f'{data["v_mpp_min"]}...{data["v_mpp_max"]} В', self.styleNormalTable)],
            [Paragraph('Количество МРРТ', self.styleNormalTable), Paragraph(f'{data["mppt"]} шт.', self.styleNormalTable)],
            [Paragraph('Суммарный коэф. гармонических искажений', self.styleNormalTable), Paragraph('<3% (номинальная мощность)', self.styleNormalTable)],
            [Paragraph('Коэффициент мощности', self.styleNormalTable), Paragraph('0,99 (при ном. мощности) <br/> 0,8 (регул. коэф. мощность)', self.styleNormalTable)],
            [Paragraph('Условия автоматического включения', self.styleNormalTable), Paragraph('Если напряжение на стороне постоянного тока и сеть переменного тока отвечают требованиям, \
                                                                                            инвертор автоматически переходит в режим работы', self.styleNormalTable)],
            [Paragraph('Размер инвертора', self.styleNormalTable), Paragraph(f'{data["height"]} х {data["width"]} х {data["depth"]} мм (Д х Ш х Г)', self.styleNormalTable)],
            [Paragraph('Степень защиты', self.styleNormalTable), Paragraph(f'{data["protect"]}', self.styleNormalTable)],
            [Paragraph('Вес', self.styleNormalTable), Paragraph(f'{data["weight"]} кг', self.styleNormalTable)],
            ]
            )

            table_invertor_params.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'CENTRE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            self.story.append(table_invertor_params)
            
        if data["block_5_1_4"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.1.4 Другое силовое оборудование</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Характеристики КТП представлены в таблице №__:", self.styleNormal))
            self.story.append(Paragraph("Таблица №__", self.styleNormal))

            table_ktp_params = Table(
            [
            [Paragraph('<b>Комплектная трансформаторная подстанция</b>', self.styleNormalTable), Paragraph('<b>Название КТП</b>', self.styleNormalTable)],
            [Paragraph('Мощность КТП, кВА', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Количество обмоток, шт	', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Напряжение первичной обмотки, кВ	', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Напряжение вторичной(-ых) обмотки(-ок), кВ	', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Номинальный ток обмоток, А', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Рабочая частота, Гц	', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            [Paragraph('Коэффициент полезного действия, %	', self.styleNormalTable), Paragraph('-', self.styleNormalTable)],
            ]
            )

            table_ktp_params.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'CENTRE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
            self.story.append(table_ktp_params)
            
        if data["block_5_2"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.2 Планировочное решение</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Территория     проектируемой     СЭС     расположена     на     территории  заказчика.", self.styleNormal))
            self.story.append(Paragraph("Территория проектируемой СЭС должна быть очищена от мусора и посторонних предметов.", self.styleNormal))
            self.story.append(Paragraph("Инженерной подготовкой предусматривается выравнивание площадки проектируемой СЭС без снятия почвенно – растительного слоя.", self.styleNormal))
            self.story.append(Paragraph("Решения по вертикальной планировке площадки проектируемой СЭС для отвода атмосферных осадков с территории, \
                                    а также защиту от подтопления поверхностными стоками будут рассмотрены на стадии рабочей документации.", self.styleNormal))

        if data["block_5_3"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.3 Электротехнические решения</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph("Размещение панелей ФЭМ предусматривается на опорных конструкциях. ", self.styleNormal))
            self.story.append(Paragraph("Для земных СЭС – закрепление металлоконструкций предусматривается при помощи стоек, погружаемых в грунт.", self.styleNormal))
            self.story.append(Paragraph("Для крышных СЭС без проникновения в кровлю – установка ФЭМ осуществляется при помощи типовых металлоконструкций \
                                    без крепления к поверхности кровли, с применением пригруза (ж/б плит или аналогичного материала, \
                                    не подверженного длительному разрушению от воздействия климатических факторов окружающей среды). \
                                    Масса пригруза – (определить проектом) кг. на один ФЭМ.", self.styleNormal))
            self.story.append(Paragraph("Для крышных СЭС с проникновения в кровлю – установка ФЭМ осуществляется при помощи типовых металлоконструкций \
                                    с крепления к поверхности кровли или металлоконструкций здания.", self.styleNormal))
            self.story.append(Paragraph("Для преобразования постоянного тока от массива ФЭМ в переменный, предусматривается установка инвертора/-ов (название инверторов).\
                                    Распределение панелей ФЭМ по инверторам представлена в таблице (номер таблицы). Выдача мощности с инверторов выполняется \
                                    на напряжение 0,4/6/10/35 кВ (выбрать нужное) на секции шин (указать), шкаф/щит (указать),\
                                    сущ./новый автоматический выключатель/ячейку (указать).", self.styleNormal))

        if data["block_5_4"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>5.4 Система заземления и молниезащиты</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph('Заземление СЭС выполнено согласно ГОСТ-12.1.030-81 "Элек-тробезопасность. Защитное заземление. \
                                    Зануление ", И-70 "Инструкция по устройству сетей заземления и молниезащиты", на основании ПУЭ изд.7 гл. 1.7., \
                                    и СП 76.13330.2016 "Электротехнические устройства. ', self.styleNormal))
            self.story.append(Paragraph('Актуализированная редакция СНиП 3.05.06-85", СТО 56947007-29.240.044-2010 \
                                    "Методические указания по обеспечению электромагнитной совместимости на объектах электросетевого хозяйства", \
                                    Технический циркуляр № 11/2006 "О заземляющих электродах и заземляющих проводниках", ГОСТ Р 50571.5.54-2013/МЭК 60364-5-54:2011 \
                                    «Электроустановки низковольтные. Часть 5-54. Выбор и монтаж электрооборудования. Заземляющие устройства, \
                                    защитные проводники и защитные проводники уравнивания потенциалов». ', self.styleNormal))
            self.story.append(Paragraph("Заземление ОК ФЭМ выполнено присоединением к заземляющему устройству оцинкованной полосовой сталью 5х40 мм. \
                                    Металлические опорные конструкции под установку фотоэлектрических модулей являются естественными заземлителями. \
                                    Заземляющие устройства запроектированы по норме на допустимое сопротивление растеканию тока. ", self.styleNormal))
            self.story.append(Paragraph("В качестве заземляющего устройства защитного заземления, молниезащиты, системы уравнивания потенциалов, \
                                    защиты от статического электричества применяются вертикальные заземлители, выполненные из оцинкованной \
                                    круглой стали диаметром 18 мм и длиной 5м, соединенные между собой горизонтальным заземлителем, \
                                    выполненным из оцинкованной полосовой стали 5х40 мм, проложенным в земле на глубине 1 м. ", self.styleNormal))
            self.story.append(Paragraph("Крайние опорные конструкции под установку фотоэлектрических модулей каждого ряда соединить оцинкованной \
                                    полосовой стали 5x40 мм с контуром заземления СЭС. В рядах все опорные конструкции соединить двумя перемычками \
                                    из провода ПВ-1 6 мм2,\ в прогонах ОК предусмотрены отверстия для перемычек. ", self.styleNormal))
            self.story.append(Paragraph("В рамках ФЭМ предусмотрены отверстия для присоединения провода заземления к прогонам ОК. \
                                    Соединение элементов заземляющего устройства ФЭМ выполнять болтовым соединением. ", self.styleNormal))
            self.story.append(Paragraph("Все металлические части оборудования, нормально не находящиеся под напряжением, заземлить путем присоединения \
                                    к заземляющему контуру стальной оцинкованной полосой 5x40 мм (не менее, чем в двух точках). ", self.styleNormal))
            self.story.append(Paragraph("Соединение элементов заземляющего устройства выполнять болтовым. Соединение элементов устройства уравнивания \
                                    потенциалов выполнять сварным. Сварные швы для полосовой стали выполнить по ГОСТ 5264-80*, для круглой стали - по ГОСТ 14098-91. \
                                    Катет шва принять по наименьшей толщине свариваемых элементов.", self.styleNormal))
        if data["block_5_5"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b> 5.5 Выбор оптимальных показателей сравнение вариантов</b>", self.styleH2))
            self.story.append(Spacer(1, 170))
            self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
            self.story.append(Spacer(1, 12))
            img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
            self.story.append(img)
            
        if data["block_5_6"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b> 5.6 Индикативный анализ стоимости</b>", self.styleH2))
            self.story.append(Spacer(1, 170))
            self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
            self.story.append(Spacer(1, 12))
            img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
            self.story.append(img)

    # Раздел 6
    def section_6(self, bamr, data):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>6 Выводы и результаты</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("Проект имеет высокий потенциал использования солнечной энергии, но на него могут влиять сезонные погодные изменения (таблица 6).", self.styleNormal))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("Таблица 6 – Основные результаты расчета выработки СЭС ", self.styleNormal))

        table_ses_output = Table(
        [
        [Paragraph(' ', self.styleNormalTable), Paragraph('Глобальная горизонталь- <br/> ная инсоляция <b>GHI</b>, кВтч/м2', self.styleNormalTable), 
            Paragraph('Рассеянная горизонталь- <br/> ная инсоляция, <b>DIF</b>, кВт/м2', self.styleNormalTable), Paragraph('Энергия, выработан- <br/> ная ФЭМ, <b>EArray</b>, МВтч', self.styleNormalTable),
            Paragraph('Энергии, отданная в сеть, <b>Egrid</b>, МВтч', self.styleNormalTable), Paragraph('Производи- <br/> тельность <b>PR</b> = Egrid/ <br/> Earray, о.е.', self.styleNormalTable)],
        [Paragraph('<b>Январь</b>', self.styleNormalTable),
            Paragraph(f"{bamr[1]}", self.styleNormalTable), Paragraph(f"{bamr[2]}", self.styleNormalTable), Paragraph(f"{bamr[6]}", self.styleNormalTable),
            Paragraph(f"{bamr[7]}", self.styleNormalTable), Paragraph(f"{bamr[8]}", self.styleNormalTable)],
        [Paragraph('<b>Февраль</b>', self.styleNormalTable),
            Paragraph(f"{bamr[10]}", self.styleNormalTable), Paragraph(f"{bamr[11]}", self.styleNormalTable), Paragraph(f"{bamr[15]}", self.styleNormalTable), 
            Paragraph(f"{bamr[16]}", self.styleNormalTable), Paragraph(f"{bamr[17]}", self.styleNormalTable)],
        [Paragraph('<b>Март</b>', self.styleNormalTable),
            Paragraph(f"{bamr[19]}", self.styleNormalTable), Paragraph(f"{bamr[20]}", self.styleNormalTable), Paragraph(f"{bamr[24]}", self.styleNormalTable), 
            Paragraph(f"{bamr[25]}", self.styleNormalTable), Paragraph(f"{bamr[26]}", self.styleNormalTable)],
        [Paragraph('<b>Апрель</b>', self.styleNormalTable),
            Paragraph(f"{bamr[28]}", self.styleNormalTable), Paragraph(f"{bamr[29]}", self.styleNormalTable), Paragraph(f"{bamr[33]}", self.styleNormalTable),
            Paragraph(f"{bamr[34]}", self.styleNormalTable), Paragraph(f"{bamr[35]}", self.styleNormalTable)],
        [Paragraph('<b>Май</b>', self.styleNormalTable),
            Paragraph(f"{bamr[37]}", self.styleNormalTable), Paragraph(f"{bamr[38]}", self.styleNormalTable), Paragraph(f"{bamr[42]}", self.styleNormalTable),
            Paragraph(f"{bamr[43]}", self.styleNormalTable), Paragraph(f"{bamr[44]}", self.styleNormalTable)],
        [Paragraph('<b>Июнь</b>', self.styleNormalTable),
            Paragraph(f"{bamr[46]}", self.styleNormalTable), Paragraph(f"{bamr[47]}", self.styleNormalTable), Paragraph(f"{bamr[51]}", self.styleNormalTable),
            Paragraph(f"{bamr[52]}", self.styleNormalTable), Paragraph(f"{bamr[53]}", self.styleNormalTable)],
        [Paragraph('<b>Июль</b>', self.styleNormalTable),
            Paragraph(f"{bamr[55]}", self.styleNormalTable), Paragraph(f"{bamr[56]}", self.styleNormalTable), Paragraph(f"{bamr[60]}", self.styleNormalTable),
            Paragraph(f"{bamr[61]}", self.styleNormalTable), Paragraph(f"{bamr[62]}", self.styleNormalTable)],
        [Paragraph('<b>Август</b>', self.styleNormalTable),
            Paragraph(f"{bamr[64]}", self.styleNormalTable), Paragraph(f"{bamr[65]}", self.styleNormalTable), Paragraph(f"{bamr[69]}", self.styleNormalTable),
            Paragraph(f"{bamr[70]}", self.styleNormalTable), Paragraph(f"{bamr[71]}", self.styleNormalTable)],
        [Paragraph('<b>Сентябрь</b>', self.styleNormalTable),
            Paragraph(f"{bamr[73]}", self.styleNormalTable), Paragraph(f"{bamr[74]}", self.styleNormalTable), Paragraph(f"{bamr[78]}", self.styleNormalTable),
            Paragraph(f"{bamr[79]}", self.styleNormalTable), Paragraph(f"{bamr[80]}", self.styleNormalTable)],
        [Paragraph('<b>Октябрь</b>', self.styleNormalTable),
            Paragraph(f"{bamr[82]}", self.styleNormalTable), Paragraph(f"{bamr[83]}", self.styleNormalTable), Paragraph(f"{bamr[87]}", self.styleNormalTable),
            Paragraph(f"{bamr[88]}", self.styleNormalTable), Paragraph(f"{bamr[89]}", self.styleNormalTable)],
        [Paragraph('<b>Ноябрь</b>', self.styleNormalTable),
            Paragraph(f"{bamr[91]}", self.styleNormalTable), Paragraph(f"{bamr[92]}", self.styleNormalTable), Paragraph(f"{bamr[96]}", self.styleNormalTable),
            Paragraph(f"{bamr[97]}", self.styleNormalTable), Paragraph(f"{bamr[98]}", self.styleNormalTable)],
        [Paragraph('<b>Декабрь</b>', self.styleNormalTable),
            Paragraph(f"{bamr[100]}", self.styleNormalTable), Paragraph(f"{bamr[101]}", self.styleNormalTable), Paragraph(f"{bamr[105]}", self.styleNormalTable),
            Paragraph(f"{bamr[106]}", self.styleNormalTable), Paragraph(f"{bamr[107]}", self.styleNormalTable)],
        [Paragraph('Год', self.styleNormalTable),
            Paragraph(f"{bamr[109]}", self.styleNormalTable), Paragraph(f"{bamr[110]}", self.styleNormalTable), Paragraph(f"{bamr[114]}", self.styleNormalTable),
            Paragraph(f"{bamr[115]}", self.styleNormalTable), Paragraph(f"{bamr[116]}", self.styleNormalTable)],
        ]
        )

        table_ses_output.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'CENTRE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        self.story.append(table_ses_output)

        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph(f"На основании расчета подтверждено, что годовая выработка составляет {data['produced_energy']} МВтч/ год \
                                и годовая удельная выработка СЭС составляет {data['specific_production']} кВтч / кВт / \
                                год при средней производительности {data['perf_ratio']}%.", self.styleNormal))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("После ввода в эксплуатацию СЭС поведение всех её компонентов, а также естественные \
                                и ускоренные изменения в их характеристиках можно отследить только путем проведения \
                                активного мониторинга и регулярной оценки производительности. Данная оценка должна \
                                подкрепляться численным анализом отслеживаемых характеристик с моделированием ожидаемых \
                                и справочных показателей эффективности на основе спутниковых и \
                                метеорологических наблюдений в реальном времени.", self.styleNormal))
        self.story.append(Paragraph("Такой подход обеспечивает устойчивую сохранность информации, позволяет быстро выявлять отказы \
                                и поддерживать эксплуатацию, контроль и техническое обслуживание.", self.styleNormal))
        self.story.append(Paragraph("Вычисления для этого отчета включают набор сложных операций, и в результате математического\
                                округления могут быть обнаружены незначительные несоответствия между числами.", self.styleNormal))

    # Раздел 7
    def section_7(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b>7 Перечень НТД</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("Разработка и оформление результатов работ должны соответствовать законам, правилам, СНиП и ГОСТ:", self.styleNormal))
        self.story.append(Spacer(1, 12))
        self.story.append(Paragraph("1. Технические регламент о безопасности зданий и сооружений 384-ФЗ от 30.12.2009 в редакции, действующей на момент проектирования;", self.styleNormal))
        self.story.append(Paragraph("2. ПУЭ (действующее издание);", self.styleNormal))
        self.story.append(Paragraph("3. ПТЭ (действующее издание);", self.styleNormal))
        self.story.append(Paragraph("4. Общие технические требования к микропроцессорным устройствам защиты и автоматики энергосистем (РД 34.35.310-97 с изм.1.1998);", self.styleNormal))
        self.story.append(Paragraph("5. Общие требования к системам противоаварийной и режимной автоматики, релейной защиты и автоматики, телеметрической информации, \
                                технологической связи в ЕЭС России, утверждённые Приказом ОАО РАО «ЕЭС России» №57 от 11.02.2008;", self.styleNormal))
        self.story.append(Paragraph("6. Правила технической эксплуатации электрических станций и сетей РФ, утверждённые приказом Минэнерго России №229 от 19.06.2003;", self.styleNormal))
        self.story.append(Paragraph("7. Приказ Министерства энергетики РФ от 23.06.2015 №380 «О Порядке расчета значений соотношения потребления активной \
                                и реактивной мощности для отдельных энергопринимающих устройств (групп энергопринимающих устройств) потребителей электрической энергии»;", self.styleNormal))
        self.story.append(Paragraph("8. Стандарт ОАО «СО ЕЭС» СТО 59012820.29.020.002-2012 «Релейная защита и автоматика. Взаимодействие субъектов электроэнергетики, \
                                потребителей электрической энергии при создании (модернизации) и организации эксплуатации», введенный в действие с 28 апреля 2012 года;", self.styleNormal))
        self.story.append(Paragraph("9. Положение о составе разделов проектной документации и требования к их содержанию, утвержденное Постановлением Правительства РФ №87 от 16.02.2008;", self.styleNormal))
        self.story.append(Paragraph("10. Градостроительный Кодекс РФ;", self.styleNormal))
        self.story.append(Paragraph("11. Земельный кодекс РФ;", self.styleNormal))
        self.story.append(Paragraph("12. Постановление Правительства РФ «О порядке организации и проведения государственной экспертизы проектной документации \
                                и результатов инженерных изысканий» от 05.03.2007 № 145;", self.styleNormal))
        self.story.append(Paragraph("13. Письмо Министерства регионального развития РФ от 22.06.2009 №19088-СК/08 «О применении положения о составе \
                                разделов проектной документации и требованиям к их содержанию»;", self.styleNormal))
        self.story.append(Paragraph("14. МДС 81-35.2004 «Методика определения сметной стоимости строительства на территории Российской Федерации»;", self.styleNormal))
        self.story.append(Paragraph("15. ГОСТ Р 21.1101-2013 «Основные требования к проектной и рабочей документации»;", self.styleNormal))
        self.story.append(Paragraph("16. Типовая инструкция по учету электроэнергии при ее производстве, передаче и распределении (СО 153-34.09.101-94);", self.styleNormal))
        self.story.append(Paragraph("17. Регламенты оптового рынка электроэнергии;", self.styleNormal))
        self.story.append(Paragraph("18. Инструкция по проектированию противопожарной защиты энергетических предприятий (СО 34.49.101-2003);", self.styleNormal))
        self.story.append(Paragraph('19. ФЗ РФ №123-ФЗ "Технический регламент о требованиях пожарной безопасности" от 22 июля 2008 г.;', self.styleNormal))
        self.story.append(Paragraph("20. Руководящие указания по проектированию электропитания технических средств диспетчерского и технологического управления» от 27.08.1987 № 11619ТМ-Т1;", self.styleNormal))
        self.story.append(Paragraph("21. ГОСТ Р 55105-2012 «Единая энергетическая система и изолированно работающие энергосистемы. \
                                Оперативно-диспетчерское управление. Автоматическое противоаварийное управление режимами энергосистем. \
                                Противоаварийная автоматика энергосистем. Нормы и требования»;", self.styleNormal))
        self.story.append(Paragraph("22. ГОСТ 32144-2013 «Электрическая энергия. Совместимость технических средств электромагнитная. \
                                Нормы качества электрической энергии в системах электроснабжения общего назначения»;", self.styleNormal))
        self.story.append(Paragraph("23. Методические указания по устойчивости энергосистем, утверждённые Приказом Министерства энергетики РФ от 30.06.2003 №277;", self.styleNormal))
        self.story.append(Paragraph("24. Методические указания по определению электромагнитной обстановки и совместимости на электрических станциях и подстанциях» (СО 34.35.311-2004);", self.styleNormal))
        self.story.append(Paragraph("25. Стандарт организации ОАО «СО ЕЭС» «Автоматическое противоаварийное управление режимами энергосистем. \
                                Противоаварийная автоматика энергосистем. Условия организации процесса. Условия создания объекта. \
                                Нормы и требования», СТО 59012820.29.240.001-2011; ГОСТ 2.601-2013. Межгосударственный стандарт.\
                                «Единая система конструкторской документации. Эксплуатационные документы»;", self.styleNormal))
        self.story.append(Paragraph("26. ГОСТ Р 53778-2010 «Здания и сооружения. Правила обследования и мониторинга технического состояния»", self.styleNormal))
        self.story.append(Paragraph("27. СТО 17230282.27.010.001-2007 «Здания и сооружения объектов энергетики. Методика оценки технического состояния»;", self.styleNormal))
        self.story.append(Paragraph("28. СО 153-34.20.501-2003 «Правила технической эксплуатации электрических станций и сетей РФ» \
                                (утверждены приказом Минэнерго России от 19.06.2003 №229, зарегистрированы Минюстом России 20.06.2003 №4799);", self.styleNormal))
        self.story.append(Paragraph("29. РД 03-606-03 «Инструкция по визуальному и измерительному контролю»;", self.styleNormal))
        self.story.append(Paragraph("30. СП 53-101-98 «Изготовление и контроль качества стальных строительных конструкций»;", self.styleNormal))
        self.story.append(Paragraph("31. СА 03-005-07 «Технологические трубопроводы нефтеперерабатывающей, нефтехимической и химической промышленности. \
                                Требования к устройству и эксплуатации». (рекомендованы к применению Ростехнадзором, \
                                письмо от 30.03.2007 №КЧ-45/500);", self.styleNormal))
        self.story.append(Paragraph("32. «Методические рекомендации по проектированию развития энергосистем» (утверждены приказом Минэнерго России от 30.06.2003 №281);", self.styleNormal))
        self.story.append(Paragraph("33. СН-11-101-95 «Порядок разработки, согласования, утверждения и состав обоснований инвестиций в строительство предприятий, зданий и сооружений»;", self.styleNormal))
        self.story.append(Paragraph("34. Федеральный закон от 20.06.1997 №116-ФЗ «О промышленной безопасности опасных производственных объектов», \
                                технические условия на ремонт указанного оборудования»;", self.styleNormal))
        self.story.append(Paragraph("35. СО 153-34.10.301 «Методические указания по разработке норм расхода материалов на ремонтно-эксплуатационные нужды в энергетике»;", self.styleNormal))
        self.story.append(Paragraph("36. ПТБ РД 34.03.201-97 «Правила техники безопасности при эксплуатации тепломеханического оборудования электростанций и тепловых сетей»;", self.styleNormal))
        self.story.append(Paragraph("37. СО 153-34.0-03.150-03 «Межотраслевые правила по охране труда (правила безопасности) при эксплуатации электроустановок»;", self.styleNormal))
        self.story.append(Paragraph("38. СанПиН 2.1.7.1322-03 «Гигиенические требования к размещению и обезвреживанию отходов производства и потребления»;", self.styleNormal))
        self.story.append(Paragraph("39. СО-34.03.301-00 «Правила пожарной безопасности для энергетических предприятий»;", self.styleNormal))
        self.story.append(Paragraph("40. Постановление Правительства РФ от 25.04.2012 № 390 «Правила противопожарного режима в РФ»;", self.styleNormal))
        self.story.append(Paragraph("41. Руководящие указания по расчету токов короткого замыкания и выбору электрооборудования, РД 153-34.0-20.527-98, РАО «ЕЭС России», 1998 г.", self.styleNormal))

    # Раздел 8
    def section_8(self, data):
        self.story.append(PageBreak())
        self.story.append(Paragraph("<b> 8 Приложения:</b>", self.styleH1))
        self.story.append(Spacer(1, 12))
        
        if data["block_8_1"] == False:
            self.story.append(Paragraph("<b>8.1 Отчет по выработке</b>", self.styleH2))
            self.story.append(Spacer(1, 12))
            if data["path_to_pvsyst"] != " ":
                patch_imgs_pvsyst = "Data/Images/PVsyst"
                img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]
                for i in range(len(img_files_pvsyst)):
                    i += 1
                    fname = open(f"Data/Images/PVsyst/page-{i}.png", 'rb')
                    img = Image(fname, 6*inch, 9*inch)
                    self.story.append(img)
                    self.images_pvsyst.append(fname)
                    if i != len(img_files_pvsyst):
                        self.story.append(PageBreak())
                    else:
                        break
                
        if data["block_8_2"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>8.2 Структурная схема</b>", self.styleNormal))
            self.story.append(Spacer(1, 12))
            # img = Image("Data/Images/1.png", 8*inch, 5*inch)
            # self.story.append(img)

        if data["block_8_3"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>8.3 Схема электрическая принципиальная</b>", self.styleNormal))
            self.story.append(Spacer(1, 12))
            # img = Image("Data/Images/2.png", 6*inch, 9*inch)
            # self.story.append(img)
            
        if data["block_8_4"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>8.4 Схема постоянного тока</b>", self.styleNormal))
            self.story.append(Spacer(1, 170))
            self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
            self.story.append(Spacer(1, 12))
            img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
            self.story.append(img)

        if data["block_8_5"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>8.5 План размещения</b>", self.styleNormal))
            self.story.append(Spacer(1, 170))
            self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
            self.story.append(Spacer(1, 12))
            img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
            self.story.append(img)

        if data["block_8_6"] == False:
            self.story.append(PageBreak())
            self.story.append(Paragraph("<b>8.6 Проект ТЗ на СЭС</b>", self.styleNormal))
            self.story.append(Spacer(1, 170))
            self.story.append(Paragraph("<b>Нет шаблона</b>", self.styleCenter))
            self.story.append(Spacer(1, 12))
            img = Image("Data/Images/flat,800x800,075,f.jpg", 3*inch, 3*inch)
            self.story.append(img)
    
    def build(self, **data):
        self.data = data
        self.images_pvsyst = []
        print("параметры", data)
        if data["path_to_pvsyst"] != " " and data["path_to_pvsyst"] != None:
            bamr = data['balances_and_main'] # balances_and_main_result таблица с pvsyst
            print(len(bamr))
        else:
            bamr = []
            for i in range(120):
                bamr.append('Н/Д')  
                  
        self.title(data)
        self.table_of_content()
        
        if data["block_1"] == False:
            self.section_1()
        else:
            print("Блок 1 отсутствует")
            
        if data["block_2"] == False:
            self.section_2()
        else:
            print("Блок 2 отсутствует")
            
        if data["block_3"] == False:
            self.section_3(data)
        else:
            print("Блок 3 отсутствует")
            
        if data["block_4"] == False:
            self.section_4()
        else:
            print("Блок 4 отсутствует")
            
        if data["block_5"] == False:
            self.section_5(data)
        else:
            print("Блок 5 отсутствует")
            
        if data["block_6"] == False:
            self.section_6(bamr, data)
        else:
            print("Блок 6 отсутствует")
            
        if data["block_7"] == False:
            self.section_7()
        else:
            print("Блок 7 отсутствует")
            
        if data["block_8"] == False:
            self.section_8(data)
        else:
            print("Блок 8 отсутствует")
            
        # self.schemes()
        self.doc.multiBuild(self.story, canvasmaker=NumberedCanvas)
        
        patch_imgs_pvsyst = "Data/Images/PVsyst"
        img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]
        if len(self.images_pvsyst) != 0:
            for img in self.images_pvsyst:
                img.close()
 