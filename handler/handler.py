import requests as req
import urllib.request
import re
import os
import json
import sys
import shutil

def getClienId():
	try:
	  grab = req.get("https://m.soundcloud.com")
	  client_id = re.search(r'&client_id=(.*?)",', grab.text).group(1)
	  return client_id
	except:
	  print("An exception occurred")
	  sys.exit()

def downloadHandler(track_link):
	if track_link != '':
		resp = req.get("https://w.soundcloud.com/player/?url="+track_link)
		data = re.search(r'var c=\[(.*?)}]}]', resp.text).group(1)
		data = data+"}]}"
		data = json.loads(data)
		stream_url = data['data'][0]['media']['transcodings'][0]['url']+"?client_id="+getClienId()
		title = data['data'][0]['title']
		stream_resp = req.get(stream_url)
		stream_resp = stream_resp.json()
		stream_mp3 = req.get(stream_resp['url'])
		dirName = "temp"
		if not os.path.exists(dirName):
		    os.mkdir(dirName)
		    print("Directory " , dirName ,  " Created ")
		result = re.findall(r',(.*?)#', stream_mp3.text, re.DOTALL)
		result = [i.replace('\n','') for i in result]
		result = [urllib.request.urlretrieve(result[i],  'temp/'+str("{:04d}".format(i)) +'.mp3') for i in range(len(result))]
		cmd = "cat temp/*.mp3 | \"tools\\ffmpeg\"  -i pipe: -c:a copy -c:v copy \""+title+".mp3\""
		os.system(cmd)
		shutil.rmtree('temp/')  #remove no empty directory
		# output.config(text='Success: The track is located in '+os.getcwd())
		return 'Success: The track is located in '+os.getcwd()
	else:
		# output.config(text='Erroor')
		return "Erroor"

# def getInput(track_url):
# 	if track_url != '':
# 		downloadHandler(track_url)
# 		output_label.config(text='Success: The track is located in '+os.getcwd())
# 		# output_label.config(text=getClienId())
# 	else:
# 		output_label.config(text='Erroor')

	