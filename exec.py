import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3 字型
from tkinter import ttk
import tkinter.messagebox
from motionless import CenterMap, DecoratedMap, AddressMarker
from PIL import Image, ImageTk
import requests
from io import BytesIO
import io
from urllib.request import urlopen
import datetime
from requests.auth import HTTPBasicAuth
import sys
from backend import Backend


#Sample Page
class Samplewin(tk.Tk):
    def __init__(self, data = sys.path[0]+'/database/1999_data.csv', *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) 
        self.data = data

        self.title('用數據看風水寶地')
        self.minsize(1000, 500)
        self.configure(background='#003377')
        self.title_font = tkfont.Font(family='Arial', size=12, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Startpage, Loginpage, Addresspage, Resultpage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Startpage")	

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
		
    #通往其他分頁(Class)的通道
    def get_page(self, page_class):
        return self.frames[page_class]

class Startpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
		
        #背景色塊
        self.bg_StartPage = tk.Canvas(self, bg = '#112F41', height = 500, width = 1000)
        self.bg_StartPage.place(x = 500, y = 250, anchor = 'center')
		
        self.img_house = tk.PhotoImage(file = sys.path[0] + '/image/image_house.gif')
        self.lable_house = tk.Label(self, image = self.img_house)
        self.lable_house.place(x = 500, y = 170, anchor = 'center')

        #標題
        self.label_windwater = tk.Label(self, text="用數據看風水寶地", fg = '#ED553B', bg = '#112F41', font= ('Noto Sans CJK TC Bold', 30, ))
        self.label_windwater.place(x = 500, y = 345, anchor = 'center')
        self.label_taipei = tk.Label(self, text="台北市住宅小體驗", fg = '#F49989', bg = '#112F41', font= ('Noto Sans CJK TC Regular', 16))
        self.label_taipei.place(x = 500, y = 390, anchor = 'center')
        #按鈕
        self.button_start = tk.Button(self, text="Start", bg = '#ED553B', fg = '#FFFFFF', font= ('Arial', 14, 'bold'), width=20, height=1, command=lambda: controller.show_frame("Loginpage"))
        self.button_start.place(x = 500, y = 450, anchor = 'center')


class Loginpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
		
        #背景色塊  #背景有偷偷長大
        self.bg_LoginPage = tk.Canvas(self, bg = '#112F41', height = 700, width = 1200)
        self.bg_LoginPage.place(x = 520, y = 250, anchor = 'center')
		
        self.bg_board_down = tk.Canvas(self, bg = '#55A4D3', height = 300, width = 500)
        self.bg_board_down.place(x = 450, y = 100, anchor = 'nw')		
		
        self.bg_board_up = tk.Canvas(self, bg = '#FFFFFF', height = 300, width = 500)
        self.bg_board_up.place(x = 430, y = 80, anchor = 'nw')
	
        #左邊標題/說明文
        self.label_googletitle = tk.Label(self, text="Google Maps API", bg = '#112F41', fg = '#FFFFFF', font= ('Noto Sans CJK TC Bold', 26))
        self.label_googletitle.place(x = 50, y = 150, anchor = 'nw')
		
        self.label_description1 = tk.Label(self, text="若您沒有Google Maps API Key", bg = '#112F41', fg = '#FFFFFF', font= ('Noto Sans CJK TC Regular', 12))
        self.label_description1.place(x = 52, y = 210, anchor = 'nw')
		
        self.label_description2 = tk.Label(self, text="請至此以下連結申請：", bg = '#112F41', fg = '#FFFFFF', font= ('Noto Sans CJK TC Regular', 12))
        self.label_description2.place(x = 52, y = 240, anchor = 'nw')		
		
        self.entry_googlelink = tk.Entry(self, width = 40)
        self.entry_googlelink.insert(tk.END,'https://cloud.google.com/maps-platform/')
        self.entry_googlelink.place(x = 55, y = 280, anchor = 'nw')
		
        #右邊輸入框
        self.label_enterkey = tk.Label(self, text="請輸入您的Google Maps API Key", bg = '#FFFFFF', fg = '#000000', font= ('Noto Sans CJK TC Bold', 16))
        self.label_enterkey.place(x = 450, y = 120, anchor = 'nw')

        self.entry_key = tk.Entry(self, width = 60)
        self.entry_key.place(x = 454, y = 190, anchor = 'nw')		

        #多指令按鈕：翻頁，同時記錄key
        self.button_enteraccount = tk.Button(self, text="Enter", bg = '#ED553B', fg = '#FFFFFF', font = ('Arial', 12, 'bold'), width=8, height=1, command = lambda: [controller.show_frame("Addresspage"), self.GetKey()])
        self.button_enteraccount.place(x = 850, y = 310, anchor = 'center')		
		
        self.button_back2StartPage = tk.Button(self, text="Back", bg = '#8497B0', fg = '#FFFFFF', font = ('Arial', 11, 'bold'), width=8, height=1, command = lambda: controller.show_frame("Startpage"))
        self.button_back2StartPage.place(x = 98, y = 450, anchor = 'center')
		
    def GetKey(self):
        self.input_key = self.entry_key.get()

        # print(self.input_key)  #先用print試試
        return self.input_key

today = datetime.datetime.now()
year, month = today.year, today.month
year = int(year) - 1911
today = str(year) + '.' + str(int(month))
del year, month

#彈跳視窗，等下會用到	
def Hit_loud():
    tk.messagebox.showinfo(title = '住宅吵鬧', message = '「住宅吵鬧」的定義為台北市 1999 市民服務，截至' + today +'，場所與設施噪音舉發通報案件數。')
def Hit_traffic():
    tk.messagebox.showinfo(title = '交通危險', message = '「交通危險」的定義為台北市 1999 市民服務，截至' + today +'，道路邊坡坍方／道路掏空／路面積淹水通報案件數。')	
def Hit_hygiene():
    tk.messagebox.showinfo(title = '鄰里髒亂', message = '「鄰里髒亂」的定義為台北市 1999 市民服務，截至' + today +'，鄰里無主垃圾清運／雨水下水道側溝清淤通報案件數。')
def Hit_residence():
    tk.messagebox.showinfo(title = '是否為海砂屋', message = '「是否為海砂屋」的定義為，截至' + today + '，依照臺北市高氯離子混凝土建築物列管名單，是否將您住宅地址。') 


class Addresspage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #背景色塊
        self.bg_AddressPage = tk.Canvas(self, bg = '#112F41', height = 500, width = 1000)
        self.bg_AddressPage.place(x = 500, y = 250, anchor = 'center')
		
        self.bg_board_down = tk.Canvas(self, bg = '#55A4D3', height = 300, width = 500)
        self.bg_board_down.place(x = 450, y = 100, anchor = 'nw')		
		
        self.bg_board_up = tk.Canvas(self, bg = '#FFFFFF', height = 300, width = 500)
        self.bg_board_up.place(x = 430, y = 80, anchor = 'nw')

        self.img_board = tk.PhotoImage(file = sys.path[0] + '/image/image_board.gif')
        self.lable_board = tk.Label(self, image = self.img_board)
        self.lable_board.place(x = 50, y = 100, anchor = 'nw')	
        #右邊輸入框
        self.label_enteraddress = tk.Label(self, text="請輸入要查詢的地址", bg = '#FFFFFF', fg = '#ED553B', font= ('Noto Sans CJK TC Bold', 16))
        self.label_enteraddress.place(x = 450, y = 120, anchor = 'nw')		

        #行政區
        self.label_district = tk.Label(self, text="行政區：", bg = '#FFFFFF', fg = '#000000', font= ('Noto Sans CJK TC Regular', 12))
        self.label_district.place(x = 450, y = 160, anchor = 'nw')
        self.entry_district = tk.Entry(self, width = 15)
        self.entry_district.place(x = 530, y = 167, anchor = 'nw')	
		
        #路/街
        self.label_road = tk.Label(self, text="道路或街名：", bg = '#FFFFFF', fg = '#000000', font= ('Noto Sans CJK TC Regular', 12))
        self.label_road.place(x = 450, y = 195, anchor = 'nw')
        self.entry_road = tk.Entry(self, width = 20)
        self.entry_road.place(x = 560, y = 202, anchor = 'nw')
        #巷
        self.entry_alley = tk.Entry(self, width = 7)
        self.entry_alley.place(x = 560, y = 240, anchor = 'nw')	
        self.label_alley = tk.Label(self, text="巷", bg = '#FFFFFF', fg = '#000000', font= ('Noto Sans CJK TC Regular', 12))
        self.label_alley.place(x = 625, y = 233, anchor = 'nw')
        #弄
        self.entry_nong = tk.Entry(self, width = 7)
        self.entry_nong.place(x = 660, y = 240, anchor = 'nw')	
        self.label_nong = tk.Label(self, text="弄", bg = '#FFFFFF', fg = '#000000', font= ('Noto Sans CJK TC Regular', 12))
        self.label_nong.place(x = 725, y = 233, anchor = 'nw')
        #號
        self.entry_number = tk.Entry(self, width = 7)
        self.entry_number.place(x = 760, y = 240, anchor = 'nw')	
        self.label_number = tk.Label(self, text="號", bg = '#FFFFFF', fg = '#000000', font= ('Noto Sans CJK TC Regular', 12))
        self.label_number.place(x = 825, y = 233, anchor = 'nw')
        #跨class取值：self.controller.get_page('LoginPage').entry_key.get()
        #多指令按鈕：翻頁，同時記錄address，建立map(ResultPage)，建立分數按鈕(ResultPage)。
        self.button_enteraddress = tk.Button(self, text="Enter", bg = '#ED553B', fg = '#FFFFFF', font = ('Arial', 12, 'bold'), width=8, height=1, command= lambda: [controller.show_frame("Resultpage"), self.GetMap(self.GetAddress(), self.controller.get_page('Loginpage').entry_key.get()), self.GetPoint(self.GetAddress(),self.controller.get_page('Loginpage').entry_key.get() )])
        self.button_enteraddress.place(x = 830, y = 310, anchor = 'center')		
        self.button_back2LoginPage = tk.Button(self, text="Back", bg = '#8497B0', fg = '#FFFFFF', font = ('Arial', 12, 'bold'), width=8, height=1, command=lambda: controller.show_frame("Loginpage"))
        self.button_back2LoginPage.place(x = 98, y = 450, anchor = 'center')	

    def GetAddress(self):
        a_district = '' if (self.entry_district.get() == '') else (self.entry_district.get())
        a_road = '' if (self.entry_road.get() == '') else (self.entry_road.get())
        a_alley = '' if (self.entry_alley.get() == '') else (self.entry_alley.get() + '巷')
        a_nong = '' if (self.entry_nong.get() == '') else (self.entry_nong.get() + '弄')
        a_number = '' if (self.entry_number.get() == '') else (self.entry_number.get() + '號')		

        self.input_address = '台北市' + a_district + a_road + a_alley + a_nong + a_number

        # print(self.input_address)  #先用print試試
        return self.input_address	
		
		
    def GetMap(self, address, key):  
        road_styles = [{
        'feature': 'road.highway',
        'element': 'geomoetry',
        'rules': {
            'visibility': 'simplified',
            'color': '#c280e9'
            }
        }, {
            'feature': 'transit.line',
            'rules': {
                'visibility': 'simplified',
                'color': '#bababa'
            }
        }]

        cmap = DecoratedMap(style = road_styles, key=key)
        cmap.add_marker(AddressMarker(address,label='A'))
        url = cmap.generate_url()
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))  
		
        # 儲存圖片到Github，再下載圖片，丟到下一頁(ResultPage)
        # 可先用自己的電腦試試
        img.save(sys.path[0] + '/image/mymap.gif')
        self.img_map = tk.PhotoImage(file = sys.path[0] + '/image/mymap.gif')  
        self.lable_map = tk.Label(self.controller.get_page('Resultpage'), image = self.img_map)
        self.lable_map.place(x = 54, y = 80, anchor = 'nw')			
		
        # 測試用
        # img.show()	

        # (捨棄)另法，直接放圖片 >> 出不來，但可以再試試	
        # img = ImageTk.PhotoImage(img)
        # panel = tk.Label(self.controller.get_page('ResultPage'), image=img)
        # panel.place(x = 54, y = 80, anchor = 'nw')	

		
        '''import 外部函數 cal_point'''
    def GetPoint(self, address, API_KEY):
        dict_point = Backend().exec(address, API_KEY)
        point_loud = dict_point.get('住宅安寧')
        point_traffic = dict_point.get('交通安全')
        point_hygiene = dict_point.get('衛生')		
        point_residence = dict_point.get('住宅安全')
        if point_residence == True:
            str_residence = "是"	
        else:
            str_residence = "否"			

        # 跨class取值：self.controller.get_page('ResultPage')，放到另一頁ResultPage
        # 這些按紐隨address變動，按下Enter後，才會在ResultPage建立有分數的按鈕。
        button_index_loud = tk.Button(self.controller.get_page('Resultpage'), text=("%s" % point_loud), bg = '#112F41', fg = '#ED553B', font= ('Noto Sans CJK TC Bold', 40), width = 5, command=Hit_loud)
        button_index_loud.place(x = 630, y = 165, anchor = 'center')

        button_index_traffic = tk.Button(self.controller.get_page('Resultpage'), text=("%s" % point_traffic), bg = '#112F41', fg = '#ED553B', font= ('Noto Sans CJK TC Bold', 40), width = 5, command=Hit_traffic)
        button_index_traffic.place(x = 850, y = 165, anchor = 'center')	

        button_index_hygiene = tk.Button(self.controller.get_page('Resultpage'), text=("%s" % point_hygiene), bg = '#112F41', fg = '#ED553B', font= ('Noto Sans CJK TC Bold', 40), width = 5, command=Hit_hygiene)
        button_index_hygiene.place(x = 630, y = 340, anchor = 'center')		

        button_index_residence = tk.Button(self.controller.get_page('Resultpage'), text=("%s" % str_residence), bg = '#112F41', fg = '#ED553B', font= ('Noto Sans CJK TC Bold', 40),  width = 5, command=Hit_residence)
        button_index_residence.place(x = 850, y = 340, anchor = 'center')		
		
	
class Resultpage(tk.Frame):
	
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
		
        #背景色塊
        self.bg_ResultPage = tk.Canvas(self, bg = '#112F41', height = 500, width = 1000)
        self.bg_ResultPage.place(x = 500, y = 250, anchor = 'center')

        #左邊標題/說明文
        self.label_resulttitle = tk.Label(self, text="Results", bg = '#112F41', fg = '#FFFFFF', font= ('Noto Sans CJK TC Bold', 26))
        self.label_resulttitle.place(x = 50, y = 30, anchor = 'nw')
	
        self.label_radius = tk.Label(self, text="資料以住宅周圍500公尺內案件為基準", bg = '#112F41', fg = '#F2B134', font= ('Noto Sans CJK TC Regular', 10))
        self.label_radius.place(x = 200, y = 55, anchor = 'nw')	
		
	
        #右邊指數區
        #跨class取值：self.controller.get_page('AddressPage').pointlist
		
        #吵鬧指數_標示	
        label_index_loud = tk.Label(self, text="住宅吵鬧(件數)", bg = '#112F41', fg = '#F2B134', font= ('Noto Sans CJK TC Bold', 12))
        label_index_loud.place(x = 630, y = 80, anchor = 'center')		

        #交通安全_標示	
        label_index_traffic = tk.Label(self, text="交通危險(件數)", bg = '#112F41', fg = '#F2B134', font= ('Noto Sans CJK TC Bold', 12))
        label_index_traffic.place(x = 850, y = 80, anchor = 'center')	
	
        #衛生_標示	
        label_index_hygiene = tk.Label(self, text="鄰里髒亂(件數)", bg = '#112F41', fg = '#F2B134', font= ('Noto Sans CJK TC Bold', 12))
        label_index_hygiene.place(x = 630, y = 255, anchor = 'center')	
	
        #住宅安全_標示
        label_index_residence = tk.Label(self, text="是否為海砂屋", bg = '#112F41', fg = '#F2B134', font= ('Noto Sans CJK TC Bold', 12))
        label_index_residence.place(x = 850, y = 255, anchor = 'center')		

        #按鈕
        self.button_back2StartPage = tk.Button(self, text="Main Page", bg = '#ED553B', fg = '#FFFFFF', font = ('Arial', 12, 'bold'), width=15, height=1, command=lambda: controller.show_frame("Startpage"))
        self.button_back2StartPage.place(x = 644, y = 460, anchor = 'center')	

        self.button_back2AddressPage = tk.Button(self, text="New Address", bg = '#ED553B', fg = '#FFFFFF', font = ('Arial', 12, 'bold'), width=15, height=1, command=lambda: controller.show_frame("Addresspage"))
        self.button_back2AddressPage.place(x = 846, y = 460, anchor = 'center')	
	
	
root = Samplewin()
root.mainloop()
