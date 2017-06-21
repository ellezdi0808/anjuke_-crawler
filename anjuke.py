import requests
from bs4 import BeautifulSoup
import pprint
from openpyxl import Workbook




def get_url(n):

    urls = []
    for i in range(1,n):
        url = "https://sh.fang.anjuke.com/loupan/all/p{}/".format(i)
        urls.append(url)

    return urls

def do_resp(urls):
    data = [['楼盘名', '户型', '区域', '板块', '地址', '销售状态'], ]

    headers = {"Host": "sh.fang.anjuke.com",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 Firefox/52.0",
               "Cookie": "ctid=11; aQQ_ajkguid=BE9644B0-A469-E7CE-FFBC-SX0619144635; sessid=BACDB4E4-D4C0-9C03-B9B8-SX0619144635; tuangou_list_ids=3%3A4; isp=true; isp=true; lps=http%3A%2F%2Fwww.anjuke.com%2Fajax%2Fchecklogin%2F%3Fr%3D0.08280191185563313%26callback%3DjQuery1113012894280179972784_1497854837891%26_%3D1497854837892%7Chttps%3A%2F%2Fsh.fang.anjuke.com%2F%3Ffrom%3Dnavigation; twe=2; 58tj_uuid=bacf6c49-b90e-485b-a23f-33157215c93f; new_session=1; init_refer=; new_uv=1; __xsptplusUT_8=1; __xsptplus8=8.1.1497854876.1497854876.1%234%7C%7C%7C%7C%7C%23%23jQwMHxZPBZWC8nFP6SHmGN4fGyeFpUze%23; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1497854877; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1497854877; als=0"}
    for url in urls:

        resp = requests.get(url,headers=headers).text

        soup = BeautifulSoup(resp, "html.parser")

        new_house_list = soup.find_all(class_="item-mod")


        print (len(new_house_list))
        for n,st in enumerate(new_house_list):

            data_get = []

            if st.div == None:
                continue
            else :

                plot_name = st.find("a",class_="items-name")
                pname = st.find("div",class_="lp-name").h3

                url_pic = st.img.attrs["src"]
                respon = requests.get(url_pic)

                if plot_name:
                    with open('./picture/{}.png'.format(plot_name.text), 'wb') as f:
                        f.write(respon.content)
                    data_get.append(plot_name.text)
                    # print (plot_name.text)
                else:
                    data_get.append(pname.text)
                    with open('./picture/{}.png'.format(pname.text), 'wb') as f:
                        f.write(respon.content)
                    # print (pname.text)




                huxing = st.find_all('p')[1].text.split()


                if huxing[0] == "户型：":
                    data_get.append(huxing[1])
                    # print (huxing[1])
                else:
                    data_get.append(huxing[0])
                    # print (huxing[0])

                address = st.find("a",class_="list-map")

                if address:
                    get_address = address.text
                    split_result = get_address.split('[')
                    split_res = split_result[1].split(']')
                    split_district = split_res[0].split()
                    data_get.append(split_district[0])
                    data_get.append(split_district[1])
                    data_get.append(split_res[1])
                    # print (split_district[0],split_district[1],split_res[1])


                forsale = st.find('i',class_="status-icon forsale")
                sale = st.find('i', class_="status-icon onsale")
                haiwai = st.find('i', class_="status-icon haiwai")
                soldout = st.find('i',class_="status-icon soldout")


                if forsale:
                    data_get.append(forsale.text)
                    # print (forsale.text)
                elif sale:
                    data_get.append(sale.text)
                    # print (sale.text)
                elif soldout:
                    data_get.append(soldout.text)
                    # print (soldout.text)

                else:
                    data_get.append(haiwai.text)
                    # print (haiwai.text)
            data.append(data_get)

    return data


def write_excel(data):
    wb = Workbook()
    ws = wb.active
    ws.title = '房源'
    for line in data:
        ws.append(line)

    wb.save("房源表.xlsx")


urls = get_url(26)
data = do_resp(urls)
write_excel(data)

