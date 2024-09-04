import requests
import time
import random
import re
import os
from bs4 import BeautifulSoup

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

start_num=list(range(0,250,25))
for start in start_num:
    url="https://movie.douban.com/top250?start={}&filter=".format(start)
    response=requests.get(url,headers=headers)
    if response.ok:
        content=response.text
        soup=BeautifulSoup(content,'html.parser')

        titles=soup.findAll('span',attrs={'class':'title'})
        title = [t.string for t in titles if '/' not in t.string]

        texts=soup.find_all('p',attrs={'class':''})
        for i,text in enumerate(texts):
            parts=text.get_text().split('<br/>')
            for part in parts:
                part=part.strip()
                # 提取导演
                director_match = re.search(r"导演: (.+)(?<=主)", part)
                director = director_match.group(1) if director_match else "未知导演"
                director = director[:-1].strip()

                # 提取主演
                actors_match = re.search(r"主演: (.+)(?<=...)", part)
                actors = actors_match.group(1) if actors_match else "未知主演"

                # 提取年份
                year_match = re.search(r"\d{4}", part)
                year = year_match.group(0) if year_match else "未知年份"

                # 提取国家/地区
                country_pattern = re.compile(r'\d{4}\s*/\s*([^\n/]*)\s*/')
                country = country_pattern.findall(part)
                country = country[0] if country else "未知国家/地区"

                # 提取电影类型
                genre=part.split('/')[-1].strip()

                txt_name=f'txt_{i+start}.txt'
                txt_path=os.path.join('作业movie_list v1.0/scrapy/douban_txts',txt_name)
                with open(txt_path,'w',encoding='utf-8', errors='ignore') as fp:
                    fp.write(f"标题: {title[i]}<br>")
                    fp.write(f"导演: {director}<br>")
                    fp.write(f"主演: {actors}<br>")
                    fp.write(f"年份: {year}<br>")
                    fp.write(f"国家/地区: {country}<br>")
                    fp.write(f"类型: {genre}")
        
        imgs=soup.findAll('img')
        for i,img in enumerate(imgs):
            img_url=img.get('src')
            print(img_url)
            img_response=requests.get(img_url,headers=headers)
            img_response.raise_for_status()

            img_name=f'image_{i+start}.jpg'
            img_path=os.path.join('作业movie_list v1.0\scrapy\douban_images',img_name)

            with open(img_path,'wb') as fp:
                fp.write(img_response.content)
            
            print('----- 图 片 保 存 中... ({}/250) -----'.format(i+start))
            # time.sleep(random.randrange(0,0.2))

    
