from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os

class AlbumCover():

    def __init__(self):
        # 请求网址
        self.init_url = "http://1024.qdldd.org/pw/thread.php?fid=16&page=1" # 14 15 16
        #想要存放的文件目录
        self.folder_path = "F:\PyCharm Community Edition 2018.1.4\data\data"

    def save_img(self, url, file_name):  ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功！')
        f.close()

    def request(self, url):
        # 封装的requests 请求# 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        r = requests.get(url)
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def get_files(self, path):  # 获取文件夹中的文件名称列表
        pic_names = os.listdir(path)
        return pic_names

    def spider(self):
        print("Start!")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver = webdriver.PhantomJS()
        driver.get(self.init_url)
        html = driver.page_source

        self.mkdir(self.folder_path)  # 创建文件夹
        print('开始切换文件夹')
        os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹

        file_names = self.get_files(self.folder_path)  # 获取文件夹中的所有文件名，类型是list

        all_h3 = BeautifulSoup(html, 'lxml').find_all('h3')
        # print(type(all_li))

        for h3 in all_h3:
            id = h3.find('a')['id']
            detail_url = h3.find('a')["href"]
            folder_name = h3.find('a').get_text()

            #进入详细页面
            if(id.startswith('a_ajax_') and detail_url.startswith('htm_data')):
                print('找到目标-->'+folder_name)
                self.spider_detail(detail_url , folder_name)

    def spider_detail(self,detail_url,folfer_name):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver = webdriver.PhantomJS()
        driver.get('http://1024.qdldd.org/pw/'+detail_url)
        html = driver.page_source
        all_imgs = BeautifulSoup(html, 'lxml').find(id='read_tpc').find_all('img')

        new_folder_path = self.folder_path +'\\'+folfer_name
        self.mkdir(new_folder_path)  # 创建文件夹
        print('开始切换文件夹')
        os.chdir(new_folder_path)  # 切换路径至上面创建的文件夹
        file_names = self.get_files(new_folder_path)  # 获取文件夹中的所有文件名，类型是list
        index = 1
        for img in all_imgs:
            img_url = img['src']
            img_path = str(index)+'.jpg'
            index = index +1
            if img_path in file_names:
                print('图片已经存在，不再重新下载')
            else:
                self.save_img(img_url, img_path)

album_cover = AlbumCover()
album_cover.spider()