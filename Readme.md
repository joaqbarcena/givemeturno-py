# 🍅 🥑 GiveMeTurno 🍔 🍗
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


