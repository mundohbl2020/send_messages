import logging
from time import sleep
import requests
import time
import os 
import sched
import threading
import gspread
from oauth2client.service_account import ServiceAccountCredentials
os.environ['TZ']='Portugal'
time.tzset()
scheduler1 = sched.scheduler(time.time,time.sleep) 
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=0").sheet1
user_sheet=client.open_by_url("https://docs.google.com/spreadsheets/d/1PUVYTUywilJjJNuBHv06gJXEo8X8ddovJ232OgLYWOs/edit#gid=1831337301").get_worksheet(1)
TOKEN="1295514171:AAGGiqZHneD8REKvHVAg_k_XDBm2ti3t1dI"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
logger = logging.getLogger(__name__)
scheduler = sched.scheduler(time.time,time.sleep) 


















def send_message_to_all(message,userid="ALL"):
	print('oyyyyyyyyyyyyyyyyyyyyyyyyyyy')
	users = user_sheet.get_all_records()
	bot_url='https://api.telegram.org/bot' + TOKEN 
	try:

		message_obj= requests.get("https://herokumessaging.herokuapp.com/message?name="+message)
		message_obj=message_obj.json()
		for user in users:
			sleep(5)
			uid = str(user['USERID'])
			user_row = user_sheet.find(uid).row
			status = user_sheet.acell('C{}'.format(str(user_row))).value
			if  status == 'InActive':
				continue
			coachId = user_sheet.acell('B{}'.format(str(user_row))).value
			coach_row = sheet.find(coachId)
			coach_data=sheet.row_values(coach_row)
			text = message_obj['text']
			link = message_obj['link']
			image= message_obj['image']
			link_text =message_obj['link_text']
			order = message_obj['order']
			if 'COACH_MOBILE' in text:
				text = text.replace('COACH_MOBILE',"%2B"+coach_data[4])
			if 'COACH_NAME' in text:
				text = text.replace('COACH_NAME',coach_data[2])
			if 'PRODUCT_LINK' in text:
				text =  text.replace('PRODUCT_LINK',coach_data[6])
			if 'COACH_EMAIL' in text:
				text =  text.replace('COACH_EMAIL',coach_data[3])
			if 'BUSiNESS_LINK' in text:
				text =  text.replace('BUSiNESS_LINK',coach_data[5])
			if 'FACEBOOK_LINK' in text:
				text = text.replace('FACEBOOK_LINK',coach_data[7])
			if 'INSTAGRAM_LINK' in text:
				text = text.replace('INSTAGRAM_LINK',coach_data[8])
			if 'LEAD_NAME' in text:
				text=text.replace('LEAD_NAME',user_sheet.acell('Q{}'.format(str(user_row))).value)
			for i in order:
				sleep(3)
				print(i)
				if i == 'M':
					text = text.replace('&', '%26')
					res=requests.get(bot_url+'/sendMessage?chat_id='+ uid + '&parse_mode=HTML&text=' + text)
					print(res.json())
				elif i == 'P':
					res=requests.get(bot_url+'/sendPhoto?chat_id='+uid+'&photo='+image)
				elif i== 'L':
					link=link.replace('&','%26')
					link_text= link_text.replace('&','%26')
					msg= '<a href="'+link+'">'+link_text+'</a>'
					res=requests.get(bot_url+'/sendMessage?chat_id='+ uid + '&parse_mode=HTML&text=' + msg)
					print(res.json())
	except Exception as e:
		print(e)
		return e

	return "ok"


def send_message_to_user(message,user_id):
	print("hiiiiiiiiiiiiiiiiiiiii")
	bot_url='https://api.telegram.org/bot' + TOKEN 
	try:
		message_obj= requests.get("https://herokumessaging.herokuapp.com/message?name="+message)
		message_obj=message_obj.json()
		uid = str(user_id)
		user_row = user_sheet.find(uid).row
		coachId = user_sheet.acell('B{}'.format(str(user_row))).value
		coach_row = sheet.find(coachId)
		coach_data=sheet.row_values(coach_row)
		text = message_obj['text']
		link = message_obj['link']
		image= message_obj['image']
		link_text =message_obj['link_text']
		order = message_obj['order']
		if 'COACH_MOBILE' in text:
			text = text.replace('COACH_MOBILE',"%2B"+coach_data[4])
		if 'COACH_NAME' in text:
			text = text.replace('COACH_NAME',coach_data[2])
		if 'PRODUCT_LINK' in text:
			text =  text.replace('PRODUCT_LINK',coach_data[6])
		if 'COACH_EMAIL' in text:
			text =  text.replace('COACH_EMAIL',coach_data[3])
		if 'BUSiNESS_LINK' in text:
			text =  text.replace('BUSiNESS_LINK',coach_data[5])
		if 'FACEBOOK_LINK' in text:
			text = text.replace('FACEBOOK_LINK',coach_data[7])
		if 'INSTAGRAM_LINK' in text:
			text = text.replace('INSTAGRAM_LINK',coach_data[8])
		if 'LEAD_NAME' in text:
			text=text.replace('LEAD_NAME',user_sheet.acell('Q{}'.format(str(user_row))).value)
		for i in order:
			sleep(3)
			print(i)
			if i == 'M':
				text = text.replace('&', '%26')
				res=requests.get(bot_url+'/sendMessage?chat_id='+ uid + '&parse_mode=HTML&text=' + text)
				print(res.json())
			elif i == 'P':
				res=requests.get(bot_url+'/sendPhoto?chat_id='+uid+'&photo='+image)
			elif i== 'L':
				link=link.replace('&','%26')
				link_text= link_text.replace('&','%26')
				msg= '<a href="'+link+'">'+link_text+'</a>'
				res=requests.get(bot_url+'/sendMessage?chat_id='+ uid + '&parse_mode=HTML&text=' + msg)
				print(res.json())
	except Exception as e:
		print(e)
		return e

	return "ok"



def schedule_events(lead_id="123"):
	try:
		for event in scheduler.queue:
			scheduler.cancel(event)
		print("current time ",time.ctime(time.time()))
		url="https://herokumessaging.herokuapp.com/schedule"
		userid=lead_id
		event_exist=False
		url=url+"?user="+str(userid)
		response = requests.get(url)
		response=response.json()
		for event in response['events']:
			if str(event['user_id']) == '123':
				continue
			current_argument= (event['message_name'],event['user_id'])
			print(current_argument)
			if event['user_id'].lower() == 'all':
				function_name=send_message_to_all
			else:
				rowno=user_sheet.find(event['user_id']).row
				status = user_sheet.acell('C{}'.format(str(rowno))).value
				if  status == 'InActive':
					continue
				function_name=send_message_to_user

			for  planned_event in scheduler.queue:
				if int(planned_event[0]) == int(event['time']) and planned_event[3] == current_argument:
					event_exist =True
					break
			if event_exist == False:

				current_time = int(time.time())
				delay= int(event['time']) - current_time
				print("event time",time.ctime(event['time']))
				if delay >0:
					scheduler.enter(delay,1,function_name,current_argument)
		print("current queue",scheduler.queue)
		t = threading.Thread( target = scheduler.run )
		t.start()

	except Exception as e:
		print(e)
	return "ok"

def every_day():
	schedule_events()
	print("updating events")
	scheduler1.enter(900,1,every_day)
	t = threading.Thread( target = scheduler1.run )
	t.start()


scheduler1.enter(1,1,every_day)
t = threading.Thread( target = scheduler1.run )
t.start()