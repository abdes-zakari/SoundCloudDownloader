import requests as req
import urllib.request
import re
import os
import json
import sys
import shutil
import progressbar



def getClienId():
	try:
	  data = req.get("https://m.soundcloud.com")
	  client_id = re.search(r'&client_id=(.*?)",', data.text).group(1)
	  return client_id
	except:
	  print("An exception occurred")
	  sys.exit()


# print(getClienId())
print("Welcome to Python Soundcloud downloader using stream/hls (chnuk not progressive)")
track_link = input("Please give a track url:") 

respa = req.get("https://w.soundcloud.com/player/?url="+track_link)
# print(respa.text)
resulta = re.search(r'var c=\[(.*?)}]}]', respa.text).group(1)
resulta = resulta+"}]}"
resulta = json.loads(resulta)
stream_url = resulta['data'][0]['media']['transcodings'][0]['url']+"?client_id="+getClienId()
print(resulta['data'][0]['media']['transcodings'][0]['url'])
title = resulta['data'][0]['title']
print(resulta['data'][0]['title'])
stream_resp = req.get(stream_url)
stream_resp = stream_resp.json()
stream_mp3 = req.get(stream_resp['url'])
dirName = "temp"
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")

result = re.findall(r',(.*?)#', stream_mp3.text, re.DOTALL)
result = [i.replace('\n','') for i in result]
bar = progressbar.ProgressBar(maxval=len(result), \
widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

bar.start()
for i in range(len(result)):
	urllib.request.urlretrieve(result[i],  'temp/'+str("{:04d}".format(i)) +'.mp3')
	bar.update(i+1)
bar.finish()

cmd = "cat temp/*.mp3 | \"tools\\ffmpeg\"  -i pipe: -c:a copy -c:v copy \""+title+".mp3\""
os.system(cmd)
shutil.rmtree('temp/')  #remove no empty directory








	