import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

ch_options = webdriver.ChromeOptions()
print(ch_options)
# 不加载图片,加快访问速度
ch_options.add_experimental_option("prefs", {"profile.mamaged_default_content_settings.images": 2})

# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
#ch_options.add_argument('--proxy--server=127.0.0.1:8080')
ch_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
ch_options.add_argument('--incognito')
driver = webdriver.Chrome(options=ch_options) #使用Chrome開啟網頁

driver.get('https://www.nba.com/stats/players/hustle') #使用Chrome開啟url
print(driver.title)
#driver.execute_script("""document.getElementsByTagName('select')[0].value='4';""")
#driver.execute_script("""var aa = document.getElementsByTagName('select');aa[(aa.length-1)].value = "-1";""")

#js_blog = 'return document.getElementsByTagName("select")[(document.getElementsByTagName("select").length)-1].value;'
#blog = driver.execute_script(js_blog)
#print(blog)Pagination_button__sqGoH

#element = driver.find_elements(By.CSS_SELECTOR, '.Pagination_button__sqGoH')
#print(element[1])
#driver.execute_script("arguments[0].click();", element[1])


#element[1].click()
#driver.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()
#driver.find_element(:xpath, "//option[@value=#{-1}]").click()
#js.executeScript("document.getElementById('').checked=false;")
#key = driver.find_element('.DropDown_select__4pIg9')
#print(key)
#driver.execute_script("arguments[0].setAttribute('data-sitekey', 'somevalue');",key)
#js_blog = 'return document.getElementsByTagName("select")[(document.getElementsByTagName("select").length)-1].className;'
#blog = driver.execute_script(js_blog)
#print(blog)
#$("div.id_100 select").val("-1");
#driver.implicitly_wait(1000)

#print(html)

#取得網頁程式碼
soup = BeautifulSoup(driver.page_source, 'html.parser')
#print(soup.prettify())

#依html語法 搜尋每一階的class
div = soup.select_one('.Layout_base__6IeUC')
div = div.select_one('.Layout_mainContent__jXliI')
div = div.select_one('.MaxWidthContainer_mwc__ID5AG')
div = div.select_one('.nba-stats-content-block')
div = div.select_one('.Block_blockContent__6iJ_n')
div = div.select_one('.Crom_base__f0niE')
div2 = div.select_one('.Crom_cromSettings__ak6Hd')
div2 = div2.select('.Pagination_content__f2at7')
div2 = div2[0].find_all('div')
rows_str = div2[0].text.strip()
rows = rows_str.split(" ") #rows[0] 資料row數
pages_str = div2[6].text.strip()
pages = pages_str.split(" ") #pages[1] 網頁上記載的 有幾個分頁的UI
#print(rows_str)
div = div.select_one('.Crom_container__C45Ti')
table = div.select_one('.Crom_table__p1iZz')
thead = table.find('thead')
thead_tr = thead.select_one('.Crom_headers__mzI_m')
thead_tr_th = thead_tr.find_all('th') #資料標題
tbody = table.find('tbody')
tbody_tr = tbody.find_all('tr') #資料

out_table=[[0]*(len(thead_tr_th)) for i in range(int(rows[0])+1)] #宣告儲存資料用的二維陣列 txt輸出用
len_table=[0]*(len(thead_tr_th)+1) #宣告直欄長度的一維陣列 txt輸出排版使用

#print(len(out_table))
#print(len(out_table[0]))
#print(out_table[213][16])

#將標題儲存至輸出一維陣列
for i in range(0, len(thead_tr_th)):
    len_table[i] = len(thead_tr_th[i].text.strip())+1 #儲存每個標題長度
    out_table[0][i] = thead_tr_th[i].text.strip()+" " #將所有標題以空白間隔串接 寫至輸出資料的二維陣列
        

now_row = 0 #儲存總共所有分頁總共跑了幾個row
for k in range(0, (int(pages[1]))): #幾個分頁 loop幾次

    #因刷新分頁 需重新抓取資料table
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.select_one('.Layout_base__6IeUC')
    div = div.select_one('.Layout_mainContent__jXliI')
    div = div.select_one('.MaxWidthContainer_mwc__ID5AG')
    div = div.select_one('.nba-stats-content-block')
    div = div.select_one('.Block_blockContent__6iJ_n')
    div = div.select_one('.Crom_base__f0niE')
    div = div.select_one('.Crom_container__C45Ti')
    table = div.select_one('.Crom_table__p1iZz')
    thead = table.find('thead')
    thead_tr = thead.select_one('.Crom_headers__mzI_m')
    thead_tr_th = thead_tr.find_all('th') #table資料標題
    tbody = table.find('tbody')
    tbody_tr = tbody.find_all('tr') #table資料

    #將資料儲存至輸出一維陣列
    for j in range(0, len(tbody_tr)):
        tbody_tr_td = tbody_tr[j].find_all('td') #找到table UI中所有的td UI
        for k in range(0, len(tbody_tr_td)): #loop 直欄數
            if len(tbody_tr_td[k].text.strip()) > len_table[k]: #如果資料長度 > 已儲存的長度 則 寫入
                len_table[k] = len(tbody_tr_td[k].text.strip())
            out_table[j+1+now_row][k] = tbody_tr_td[k].text.strip() #資料寫入二維陣列

    now_row += len(tbody_tr) #儲存每個分頁總共跑了幾個row
    #儲存完一個分頁資料後 切換至下一頁
    element = driver.find_elements(By.CSS_SELECTOR, '.Pagination_button__sqGoH') #抓取下一頁UI
    driver.execute_script("arguments[0].click();", element[1]) #執行click

#輸出txt檔案
'''
with open('index.txt', 'w', encoding='utf-8',) as file:
    for i in range(0, len(out_table)):
        for j in range(0, len(out_table[0])):
            null_str = ""
            if len_table[j] > len(out_table[i][j]):
                for k in range(0, (len_table[j]-len(out_table[i][j]))):
                    null_str += " "
            file.write(str(out_table[i][j])+null_str)
            
        file.write("\n")
'''

#整理成dataframe 輸出xlsx檔案
data = {}
col = []
for j in range(0, len(out_table[0])): #loop 二維陣列
    for i in range(1, len(out_table)):
        col.append(str(out_table[i][j])) #所有資料寫入col陣列
    data[str(out_table[0][j])] = col #col再已json格式寫入data
    col = []

df = pd.DataFrame(data) #轉成dataframe格式

#print(df)
df.to_excel('index.xlsx', index=False) #輸出xlsx

driver.quit() #關閉瀏覽器


'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

r = requests.get('https://www.nba.com/stats/players/hustle?dir=D&sort=CHARGES_DRAWN', headers=headers)
if r.status_code == 200:
    print(f'請求成功：{r.status_code}')
    #soup = BeautifulSoup(r.text, 'html.parser')
    #table = soup.select_one('.Crom_table__p1iZz')
    #print(len(table))
    #th = soup.select_one('.Crom_text__NpR1_')
    #test = soup.select_one('.Block_blockContent__6iJ_n')
    #test = soup.select('.Block_blockContent__6iJ_n')
    #div = soup.select_one('.MaxWidthContainer_mwc__ID5AG > .nba-stats-content-block > .Block_blockContent__6iJ_n')
    #div = soup.select('.MaxWidthContainer_mwc__ID5AG > .Block_block__62M07 ')
    #div2 = div[0].select_one('.Block_blockContent__6iJ_n > .LoadingOverlay_loader__iZ0Nm')
    #test2 = test.select('.Crom_table__p1iZz')
    #test = soup.select_one('.Layout_base__6IeUC')
    #test = test.select_one('.Layout_mainContent__jXliI')
    #test = test.select_one('.MaxWidthContainer_mwc__ID5AG')
    #test = test.select('.Block_block__62M07')
    #test = test.select('.Block_blockContent__6iJ_n')
    #arr = r.text.split('<table')

    #print(arr[1])
else:
    print(f'請求失敗：{r.status_code}')
'''
'''
r = requests.get('https://ani.gamer.com.tw/', headers=headers)
if r.status_code == 200:
    print(f'請求成功：{r.status_code}')
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    newanime_item = soup.select_one('.timeline-ver > .newanime-block')
    anime_items = newanime_item.select('.newanime-date-area')
    print(len(anime_items))
else:
    print(f'請求失敗：{r.status_code}')
'''