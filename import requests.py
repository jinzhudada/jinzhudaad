import requests
import re
import json
from pprint import pprint
import subprocess

def Getrequest(url):
    headers = {
        "Cookie": "buvid3=9C705C8D-CE0F-41A2-5155-500F3413CA0A19284infoc; b_nut=1732111119; _uuid=2103B69B8-425F-7D37-D65A-33DC2CF168EA56500infoc; buvid_fp=1693694ae6aeca40f339aedc5232506f; enable_web_push=DISABLE; buvid4=DDB699F7-7A4F-AB23-E04D-5986E18FC50720562-024112013-xWnmn9AnehJnQoCa38Q3Ww%3D%3D; CURRENT_FNVAL=4048; rpdid=|(YYJ~m)J|u0J'u~Jkuuumuu; b_lsid=3BB88543_1936BD50C02; bsource=search_bing; header_theme_version=CLOSE; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI5NDAwOTksImlhdCI6MTczMjY4MDgzOSwicGx0IjotMX0.DsF23m2WpgfrIWeyy58rVTK7mhlOJb8xoXXus6JrmlM; bili_ticket_expires=1732940039; SESSDATA=9ccbc8a0%2C1748232920%2C908d8%2Ab2CjCBkqzIn-GZ6uJtH5bYf6rY5l_UUS0U8RJbK_M1LseDRbg61CwvpXSxkrWa1neusv8SVnBHclowY1RXVXpObTRqUjZtWldOMGlEOEtQTmJCNHFaQWJnX0IyV1R0WUdhdXJ1RUl0TG9KalBnd003dWoxUnJIOVB0UTJoT1o2ZlNET3VIZmVyNjJnIIEC; bili_jct=91becbd5b3016d9f819be8c8e59990e5; DedeUserID=1612644696; DedeUserID__ckMd5=a7d65640e9ba2e21; bp_t_offset_1612644696=1004346061713571840; home_feed_column=5; browser_resolution=1659-945; sid=6cgwlbci",
        "Referer":"https://www.bilibili.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        
    }
    response = requests.get(url=url, headers=headers)
    return response

def Getviodinfo():
    link = 'https://www.bilibili.com/video/BV1VwUXYAEtH/?spm_id_from=333.1007.tianma.3-1-7.click&vd_source=e394ee30e256611d933493150d1ebbed'
    response = Getrequest(link)
    html = response.text
    info = re.findall('<script>window.__playinfo__=(.*?)</script>', html)[0]
    json_info = json.loads(info)
    title = re.findall('<title data-vue-meta="true">(.*?)</title>',html)[0]
    audio_url = json_info['data']['dash']['audio'][0]['baseUrl']
    video_url = json_info['data']['dash']['video'][0]['baseUrl']
    
    return title,audio_url,video_url


def Save(title,audio_url,video_url):

    audio_content = requests.get(audio_url).content
    video_content = requests.get(video_url).content
    with open(f'{title}.mp3', 'wb') as audio_file:
        audio_file.write(audio_content)
    with open(f'{title}.mp4', 'wb') as video_file:
        video_file.write(video_content)
    """合并音频和视频"""
    cmd = f"ffmpeg -hint_banner -i video\\{title}.mp4 -i video\\{title}.mp3 -c:v copy -c:a aac -strict experimental code.-c\\{title}output.mp4"
    subprocess.run(cmd)


if __name__ == '__main__':
    title,audio_url,video_url = Getviodinfo()
    Save(title,audio_url,video_url)