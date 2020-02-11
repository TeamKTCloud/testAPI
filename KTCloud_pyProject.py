import sys
import os
import hashlib
import hmac
import base64
import urllib
import urllib.parse
import time
import requests
import json

s_api_url = 'https://api.ucloudbiz.olleh.com/server/v1/client/api'
w_api_url = 'https://api.ucloudbiz.olleh.com/watch/v1/client/api'
n_api_url = 'https://api.ucloudbiz.olleh.com/nas/v1/client/api'
l_api_url = 'https://api.ucloudbiz.olleh.com/loadbalancer/v1/client/api'
wa_api_url = 'https://api.ucloudbiz.olleh.com/waf/v1/client/api'
c_api_url = 'https://api.ucloudbiz.olleh.com/cdn/v1/client/api'
p_api_url = 'https://api.ucloudbiz.olleh.com/packaging/v1/client/api'
apiKey = 'apikey'
secretKey = 'secretkey'.encode()

job_id = ""

#인증정보 생성
def generateSig(request):
	print(">>generateSig Parameter(request) : ")
	print(request)
	sig_str = '&'.join(['='.join([k.lower(),urllib.parse.quote_plus(request[k]).replace('+','%20').lower()])for k in sorted(request.keys())])
	#sig_str = ""
	#for k in sorted(request.keys()):
	#	sig_str = sig_str + '&' + str(k) + '=' + str(request[k])
	#sig_str = sig_str.replace('+','%20').lower()[1:]
	print(">>generateSig sig_str : ")
	print(sig_str)
	digest = hmac.new(key=secretKey,msg=sig_str.lower().encode('utf-8'),digestmod=hashlib.sha1).digest()
	signature = base64.b64encode(digest)
	signature = urllib.parse.quote_plus(signature)
	print(">>generateSig Return(signature) : ")
	print(signature)
	return signature

#api request링크 완성
def generateReq(request, token):
	print(">>generateReq Parameter(request) : ")
	print(request)
	print(type(request))
	print("@@@")
	print(request.keys())
	request_str = '&'.join(['='.join([k,urllib.parse.quote_plus(request[k])]) for k in request.keys()])
	#request_str = ""
	#for k in request.keys():
	#	request_str = request_str + '&' + str(k) + '=' + str(request[k])
	#request_str = request_str[1:]
	print(">>generateReq request_str : ")
	print(request_str)
	signature = generateSig(request)
	request_str = request_str + '&signature=' + signature
	if token == 0 : 
		api_url = w_api_url
	elif token == 1 :
		api_url = s_api_url
	elif token == 2 :
		api_url = n_api_url
	elif token == 3 :
		api_url = l_api_url
	elif token == 4 :
		api_url = wa_api_url
	elif token == 5 :
		api_url = c_api_url
	elif token == 6 :
		api_url = p_api_url
	req = api_url + '?' + request_str
	print(">>generateReq Return(reqest) : ")
	print(req)
	return req


#apikey, command, response타입 설정
def generateRequire(button, request, id):
	request = {}
	request['apikey'] = apiKey
	request['response'] = 'json'
	if button == 1:#m존 고정
		request['command'] = 'listAvailableProductTypes'
		request['zoneid'] = '95e2f517-d64a-4866-8585-5177c256f7c7'
	elif button == 2:
		request['command'] = 'listVirtualMachines'
		#request['name'] = 'VM'
		#request['state'] = 'Running'
	elif button == 3:
		request['command'] = 'listMetrics'
	elif button == 4:
		request['command'] = 'crateTopic'
		request['name'] = 'myTopic'
	elif button == 5:
		request['command'] = 'listZones'
	elif button == 6:#1x1 고정
		if id == None:
			request['templateid'] = '60b1376f-c576-440e-b36f-9b8b39b05104'
		else:
			request['templateid'] = id
		request['command'] = 'deployVirtualMachine'
		request['serviceofferingid'] = 'f86f09f6-9acf-4b30-936c-cfb409a89e68'
		request['zoneid'] = '95e2f517-d64a-4866-8585-5177c256f7c7'
		request['usageplantype'] = 'hourly'#monthly
		request['name'] = 'JTpyTest'
		request['displayname'] = 'JTpyTest'
	elif button == 7:#고정
		request['command'] = 'queryAsyncJobResult'
		request['jobid'] = input()
	elif button == 8:
		request['command'] = 'stopVirtualMachine'
		request['id'] = id
	elif button == 9:
		request['command'] = 'startVirtualMachine'
		request['id'] = id
	elif button == 10:
		request['command'] = 'createPackage'
		request['packagename'] = input("packagename : ")
		if id[0] == 0:
			request['templateid'] = id[1]
		elif id[0] == 1:
			request['templatebody'] = id[1]
		#request['templateid'] = id
	elif button == 11:
		request['command'] = 'deletePackage'
		request['packagename'] = id
	elif button == 12:
		request['command'] = 'listPackages'
	elif button == 13:
		request['command'] = 'listVolumes'
	elif button == 14:
		request['command'] = 'createSnapshot'
		request['volumeid'] = id
	elif button == 15:
		request['command'] = 'listSnapshots'
	elif button == 16:
		request['command'] = 'createTemplate'
		request['name'] = id[0]
		request['displaytext'] = id[1]
		request['ostypeid'] = id[2]
		request['snapshotid'] = id[3]
	elif button == 17:
		request['command'] = 'listTemplates'
		request['templatefilter'] = 'self'
	elif button == 18:
		request['command'] = 'validateTemplate'
		request['templatebody'] = id
	elif button == 19:
		request['command'] = 'uploadTemplate'
		request['templatebody'] = id
		request['templatename'] = input("TemplateName : ")
	return request

#button==1
def listAvailableProductType(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==2
def listVirtualMachines(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==3
def listMetrics(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request,0)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==4
def crateTopic(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request,6)####################################################################
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==5
def listZones(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==6
def deployVirtualMachine(button):
	request = {}
	token = input("템플릿을 사용하려면 id 입력, 사용하지 않으려면 -1 입력")
	if token == "-1":
		request = generateRequire(button, request, None)
	else:
		request = generateRequire(button, request, token)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	print("save jobid? (Y:1 / N:0)")
	user_cmd = int(input())
	print("Your jobid is :")
	print(root['deployvirtualmachineresponse']['jobid'])
	job_id = root['deployvirtualmachineresponse']['jobid']
	return root
	

#button==7
def queryAsyncJobResult(button, j_id):
	request = {}
	request = generateRequire(button, request, j_id)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==8
def stopVirtualMachine(button, ldid):
	request = {}
	l_did = ldid
	print(l_did)
	if len(l_did) == 0:
		print("Running VM not exist")
		return
	tmp = int(input("index 입력 (ex.0,2,4...)"))
	id = l_did[tmp]['id']
	
	request = generateRequire(button, request, id)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==9
def startVirtualMachine(button, ldid):
	request = {}
	l_did = ldid
	print(l_did)
	if len(l_did) == 0:
		print("Stopped VM not exist")
		return
	tmp = int(input("index 입력 (ex.0,2,4...)"))
	id = l_did[tmp]['id']
	
	request = generateRequire(button, request, id)
	api = generateReq(request,1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==10
#def createPackage(button, tid):
def createPackage(button,t_t):
	request = {}
	request = generateRequire(button, request, t_t)
	#request = generateRequire(button, request, tid)
	api = generateReq(request,6)
	response = requests.get(api)
	print(response)
	root = response.json()
	print(root)
	return root

#button==11
def deletePackage(button, tname):
	request = {}
	request = generateRequire(button, request, tname)
	api = generateReq(request,6)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==12
def listPackages(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request, 6)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==13
def listVolumes(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request, 1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==14
def createSnapshot(button, vid):
	request = {}
	request = generateRequire(button, request, vid)
	api = generateReq(request, 1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root
	
#button==15
def listSnapshots(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request, 1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==16
def createTemplate(button, name, displayText, osTypeId, snapshotId):
	request = {}
	request = generateRequire(button, request, [name, displayText, osTypeId, snapshotId])
	api = generateReq(request, 1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==17
def listTemplates(button):
	request = {}
	request = generateRequire(button, request, None)
	api = generateReq(request, 1)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==18
def validateTemplate(button, tbody):
	request = {}
	request = generateRequire(button, request, tbody)
	api = generateReq(request, 6)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#button==19
def uploadTemplate(button, tbody):
	request = {}
	request = generateRequire(button, request, tbody)
	api = generateReq(request, 6)
	response = requests.get(api)
	root = response.json()
	print(root)
	return root

#JSON Control
def getDataWithJson(jsonData, token):#0 : stopped // 1: running
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	listDataInDict = list()
	dictData = dict()
	if token == 0:
		str_state = 'Stopped'
	elif token == 1:
		str_state = 'Running'
	for k in jsonData['listvirtualmachinesresponse']['virtualmachine']:
		if k['state'] == str_state:
			for kk in k:
				if kk == 'id' or kk == 'name':
					#print("kk : ",kk," kk.value : ",k[kk])
					dictData[kk] = k[kk]
					listDataInDict.append({kk : k[kk]})
	print(listDataInDict)
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	return listDataInDict

def main():
	while(1):
		print("===========================")
		print("1(S) : listAvailableProductTypes # 신청가능 상품 조회")
		print("2(S) : listVirtualMachines # 서비스 이용중인 VM 조회")
		print("3(W) : listMetrics #")
		print("4() : crateTopic # 패키지 생성 (미완)")
		print("5(S) : listZones # 신청가능 Zone 조회")
		print("---------------------------")
		print("6(S) : deployVirtualMachine # VM 생성")
		print("7(S) : queryAsyncJobResult # 비동기 jobid 상태 조회")
		print("8(S) : stopVirtualMachine # VM 중지")
		print("9(S) : startVirtualMachine # VM 시작")
		print("---------------------------")
		print("10(P) : createPackage # PACKAGE 생성")
		print("11(P) : deletePackage # PACKAGE 삭제")
		print("12(P) : listPackages # PACKAGE 조회")
		print("---------------------------")
		print("13(S) : listVolumes # Volume 조회")
		print("14(S) : createSnapshot # Volume id로 스냅샷 생성")
		print("15(S) : listSnapshots # 스냅샷 id 조회")
		print("16(S) : createTemplate # 스냅샷 id로 템플릿 생성")
		print("17(S) : listTemplates # 템플릿 조회")
		print("18(P) : validateTemplate # 템플릿 유효성 검사")
		print("19(P) : uploadTemplate # 템플릿 저장")
		print("0 : EXIT")
		print("===========================")
		button = 0
		try:
			button = int(input())
		except:
			button = -1

		if button == 0:
			break
		elif button == 1:
			listAvailableProductType(button)
		elif button == 2:
			listVirtualMachines(button)
		elif button == 3:
			listMetrics(button)
		elif button == 4:
			crateTopic(button)
		elif button == 5:
			listZones(button)
		elif button == 6:
			deployVirtualMachine(button)
		elif button == 7:
			queryAsyncJobResult(button. job_id)
		elif button == 8:
			rtn_json = listVirtualMachines(2)
			rtn_lst = getDataWithJson(rtn_json, 1)
			stopVirtualMachine(button, rtn_lst)
		elif button == 9:
			rtn_json = listVirtualMachines(2)
			rtn_lst = getDataWithJson(rtn_json, 0)
			startVirtualMachine(button, rtn_lst)
		elif button == 10:
			tid = ""
			tbody = ""
			token = int(input("0: templateid // 1: templatebody"))
			if token == 0:
				tid = input("templateid : ")
				createPackage(button, [token,tid])
			elif token == 1:
				with open("shortsample.json",encoding='utf-8') as json_file:
					json_data = json.load(json_file)
					print(json_data)
					json_data = json.dumps(json_data)
					tbody = json_data
					createPackage(button, [token,tbody])
			#createPackage(button,tid)
		elif button == 11:
			tname = input("insert template name to delete : ")
			deletePackage(button,tname)
		elif button == 12:
			listPackages(button)
		elif button == 13:
			listVolumes(button)
		elif button == 14:
			vid = input("insert volume id : ")
			createSnapshot(button, vid)
		elif button == 15:
			listSnapshots(button)
		elif button == 16:
			name = input("insert template name : ")
			displayText = input("insert template displayText : ")
			osTypeId = input("insert ostypeid : ")
			snapshotId = input("insert snapshotId : ")
			createTemplate(button, name, displayText, osTypeId, snapshotId)
		elif button == 17:
			listTemplates(button)
		elif button == 18:
			with open("shortsample.json", encoding='utf-8') as json_file:
				json_data = json.load(json_file)
				print(json_data)
				json_data = json.dumps(json_data)
				
				tbody = json_data
				validateTemplate(button, tbody)
		elif button == 19:
			with open("lbsample.json", encoding='utf-8') as json_file:
				json_data = json.load(json_file)
				print(json_data)
				json_data = json.dumps(json_data)
				tbody = json_data
				uploadTemplate(button, tbody)
		else:
			pass
	

if __name__ == '__main__':
	main()