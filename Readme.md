# 🍅 🥑 GiveMeTurno 🍔 🍗

## Update : 22/08 - 3:44 (jaja)
Se puede esquivar el captcha si uno guarda la session despues de hacer el primer
captcha, con la key `TOBA_SESSID` en la version ios esta mejor implementada, aca
en python luego voy a tratar de introducirlo, a meritos de prueba se puede copiar
el codigo (`give_me_turn.py`) y comentar la seccion quedando asi  
`give2.py`: 
```python
sess = {}
#Codigo del give_me_turn ...
...
"""
Primer peticion a la pagina de login
"""
"""
response = session.request("GET", url + "/", data="", headers={ 'cache-control': "no-cache" })
login = response.text
#print(login)
parsed = parse_web(login)
parsed["cookies"] = session.cookies.get_dict()
print("Before login => " + str(parsed))
print("Showing captcha ... ?")

img = None
captchas = re.findall(captcha_rekey,login)
for captcha in captchas :
	print(captcha[:-4])
	#response = requests.get(url + captcha[:-4]) el captcha que espera es de la misma session (cookies)
	response = session.get(url + captcha[:-4])
	img = Image.open(BytesIO(response.content))
	img.show()
	break
"""
parsed = sess
captcha_code = input("Enter captcha code:\n")
...
#parsed["cookies"] = session.cookies.get_dict() Cambiar esto 
parsed["cookies"] = {**sess["cookies"], **session.cookies.get_dict()}
...
```
donde sess es el diccionario que printea la primera ejecucion del captcha 
i.e.
```bash
$ python3 give_me_turno.py <ID de credencial>
Before login => {'token': '1YTKqIVTobemQbGKqC9eHny1RF8W5pb5fLc3nGHzYc4=', 'path': '/aplicacion.php?ah=st5d5eb2abb8c812.75088480&ai=migestion%7C%7C3614', 'cookies': {'idunc': 'rBAQyF1esquFthrvA2lYAg==', 'serverid': 'server_3|XV6yr|XV6yr', 'TOBA_SESSID': '9ep77f7hg0tu8mmjfiaqt8fei7'}}
Showing captcha ... ?
/aplicacion.php?ah=st5d5eb2abb8c812.75088480&ai=migestion%7C%7C3614&ts=mostrar_captchas_efs&tsd=migestion%7C%7C2689
Enter captcha code:
<Ctrl + c>
```
Aca copiar en `give2.py` el resultado del `beforeLogin`
```python
sess = {'token': '1YTKqIVTobemQbGKqC9eHny1RF8W5pb5fLc3nGHzYc4=', 'path': '/aplicacion.php?ah=st5d5eb2abb8c812.75088480&ai=migestion%7C%7C3614', 'cookies': {'idunc': 'rBAQyF1esquFthrvA2lYAg==', 'serverid': 'server_3|XV6yr|XV6yr', 'TOBA_SESSID': '9ep77f7hg0tu8mmjfiaqt8fei7'}}
```
Esto hace que `give2.py` comience con la session del anterior
luego (La primera vez que se ejecute hay que poner el captcha correctamente)
```bash
$ python3 give2.py <ID de credencial>
Enter captcha code:
XXXXX
...
```
Luego en las sucesivas corridas de `give2.py` con poner un captcha vacio (solo apretar enter) es suficiente ya que esa `TOBA_SESSID` ya esta logueada
```bash
$ python3 give2.py <ID de credencial>
Enter captcha code:

...
```

## Update : 20/08 
Cerca del mediodia en login pusieron un captcha(lo cual esta bien), la idea es en el paso intermedio del login traer el captcha para resolverlo y que conitnue igual
Tambien cambiaron partes de la pagina asi que hubieron modificaciones en el regex del parser

## Aun no ha sido completamente probado, hoy viernes (16/8) se hacen las pruebas finales ya que dependen del server de la UNC

Hace poco (la verdad no se cuando), cambiaron una vez mas el sistema de turnos del comedor de la UNC (Universidad Nacional de Cordoba) donde ahora hay que :  

- Sacar `reservacion` via web, (bien temprano)
- Imprimir la `reservacion` ahi mismo
- Ir a la cola con el turno ya impreso

No es una mala idea, agiliza bastante, pero es cierto que los
turnos desaparecen temprano en la mañana.  
Este script (por ahora) hace en un solo comando esa reservacion de turno.

### Requisitos
Este en particular esta hecho en `Python 3`, y requiere la lib `requests` 
```bash
$ pip3 install requests
```
### Uso
```bash
$ python3 give_me_turno.py <ID de credencial>
```
Y en caso que quisieras que corra bien pero bien bien bien
temprano asi te aseguras la reservacion, usa un cronjob, para evitar mandarlo
como parametro podes harcodearlo en el `user_id`
```bash
$ chmod +x /path/to/script/give_me_turno.py
$ JOB="1 8 * * 1-5 /usr/local/bin/python3 /path/to/script/give_me_turno.py"
$ (crontab -l ; echo "$JOB") | crontab -
```
☝🏽 Esto es 👇🏽  
`At 08:01 on every day-of-week from Monday through Friday`  
Aca lo explican/modificas re bien [Crontab.Guru](https://crontab.guru/#0_8_*_*_1-5)


