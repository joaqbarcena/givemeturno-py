#!/usr/local/bin/python3
import requests
import sys
import re
import random
import string

user_id = sys.argv[1]
url = "http://comedor.unc.edu.ar/reserva"
app_path_rekey = r"/aplicacion\.php.*onsubmit"
cstoken_rekey = r"id='cstoken'.*/>"
alert_rekey = r"UD REGISTRA.*;</script></div>"
session = requests.Session()

def rand16chars():
	return ''.join(random.choice(string.ascii_uppercase + string.digits +  string.ascii_lowercase) for _ in range(16))

def generate_boundary():
	return "----WebKitFormBoundary" + rand16chars()

def login_data(token, boundary) : 
	return "--" + boundary + "\nContent-Disposition: form-data; name=\"cstoken\"\n\n" + token  + "\n--" + boundary + "\nContent-Disposition: form-data; name=\"form_2689_datos\"\n\n" + "ingresar" + "\n--" + boundary  + "\nContent-Disposition: form-data; name=\"form_2689_datos_implicito\"\n\n" + "\n--" + boundary  + "\nContent-Disposition: form-data; name=\"ef_form_2689_datosusuario\"\n\n" + user_id + "\n--" + boundary  + "--"

def process_data(token, boundary, user_data="") : 
	"""
	El user_data es porque en el navegador esta request la manda llena de toda la
	info del usuario, por lo que me imagine que luego del login era necesario scrapear
	los datos del usuarios para que le request sea la misma que envia el navegador
	pero por suerte NO ES NECESARIAMENTE ASI ya que solo necesita el token, y los
	campos ci_2695 (procesar, undefined) para que registre la accion de reserva
	"""
	if user_data in "":
		return "--" + boundary + "\nContent-Disposition: form-data; name=\"cstoken\"\n\n"+ token+ "\n--" + boundary + "\nContent-Disposition: form-data; name=\"ci_2695\"\n\n"+ "procesar"+ "\n--" + boundary + "\nContent-Disposition: form-data; name=\"ci_2695__param\"\n\n"+ "undefined" + "\n--" + boundary + "--"
	else:
		return "TODO"

def do_login(app_path, cstoken, boundary):
	post_data = login_data(cstoken, boundary)
	#print(post_data)
	response = session.request("POST",
		url + app_path, 
		data = post_data,
		headers = {'cache-control': "no-cache", 'Content-Type' : "multipart/form-data; boundary=" + boundary})
	data = response.text
	return data

def do_process(app_path, cstoken, boundary):
	#app_path = app_path[:-2] + "16" # en el login es 3614, pero en el menu es 3616 es solo una prueba
	post_data = process_data(cstoken, boundary)
	response = session.request("POST",
		url + app_path, 
		data = post_data,
		headers = {'cache-control': "no-cache", 'Content-Type' : "multipart/form-data; boundary=" + boundary})
	data = response.text
	return data

"""
Parse el aplicacion path, y el cstoken valores necesarios 
para hacer el submit del login
"""
def parse_web(lpage, get_alert_message=False):
	info = {}
	#<form  enctype='multipart/form-data' id='formulario_toba' name='formulario_toba' method='post' action='/reserva/aplicacion.php?ah=st5d557b56f3a1f2.33225400&ai=migestion%7C%7C3614' onsubmit='return false;'>
	app_paths = re.findall(app_path_rekey,lpage)
	#<input name='cstoken' id='cstoken' type='hidden' value='TG+bNQH1jb+1P9SAxjEDK2YywcvWN2/xOGioOICgeZk='  />
	cstokens = re.findall(cstoken_rekey,lpage)
	if len(app_paths) > 0 and len(cstokens) > 0:
		app_path = app_paths[0][:-len("' onsubmit")]
		cstoken = cstokens[0]
		cstoken = cstokens[0][cstoken.find("value='") + len("value='") : cstoken.rfind("'")]
		info["token"] = cstoken
		info["path"] = app_path
	else :
		print("Error en obtener el application path o cstoken")
		print(lpage)

	if get_alert_message :
		reslist = re.findall(alert_rekey,lpage)
		for res in reslist:
			idx = res.find("alert('")
			if idx >= 0:
				info["alert"] = res[idx + len("alert('") : res.find("');")]
				break
	return info

"""
Primer peticion a la pagina de login
"""
response = session.request("GET", url + "/", data="", headers={ 'cache-control': "no-cache" })
login = response.text
parsed = parse_web(login)
print("Before login => " + str(parsed))
"""
Empieza a preparar la request para el login
"""
boundary = generate_boundary()
profile = do_login(parsed["path"], parsed["token"], boundary)
#print(profile)
parsed = parse_web(profile)
print("After login => " + str(parsed))
"""
Empieza a preparar la request para la reservacion
#reserve_profile = do_process(app_path, cstoken, boundary)
"""
reserve_profile = do_process(parsed["path"], parsed["token"], boundary)
parsed = parse_web(reserve_profile, get_alert_message=True)
print("After reservation => " + str(parsed))

