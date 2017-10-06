# Scrapy

## Installation & Setup

```shell
mkdir rfef && cd rfef
virtualenv .
source bin/activate
pip install scrapy
scrapy startproject rfef
scrapy shell "http://actas.rfef.es/actas/RFEF_CmpJornada?cod_primaria=1000144&CodCategoria=100&CodTemporada=100&CodJornada=1"
```

## Crawling

```shell
scrapy crawl acta_rfef -o actas.json -t json
```

## Notes


Include encoding option in settings.py

```shell
FEED_EXPORT_ENCODING = 'utf-8'
```

# Approach

## URL structure

Understanding how the URLs change for different seasons,etc.


Temporada 2003/2004 / Jornada 1

http://actas.rfef.es/actas/RFEF_CmpJornada?cod_primaria=1000144&CodCategoria=100&CodTemporada=100&CodJornada=1

Temporada 2004/2005 / Jornada 13

http://actas.rfef.es/actas/RFEF_CmpJornada?cod_primaria=1000144&CodCategoria=100&CodTemporada=101&CodJornada=13

Temporada 2017/2018 / Jornada 7

http://actas.rfef.es/actas/RFEF_CmpJornada?cod_primaria=1000144&CodCategoria=100&CodTemporada=114&CodJornada=7


## Acta

For a given match, we need to access its "Acta" (consists of 2 different pages)

Temporada 2017/2018 / Jornada 7

http://actas.rfef.es/actas/RFEF_CmpPartido?cod_primaria=1000144&CodActa=44378

Acta del Partido

http://actas.rfef.es/actas/RFEF_CmpActa1?cod_primaria=1000144&CodActa=44378
http://actas.rfef.es/actas/RFEF_CmpActa2?cod_primaria=1000144&CodActa=44378


## JSON desired output

For each match, we want to scrape the following info.

```json

{
   "jornada":1,
   "temporada":"Temporada 2016/2017",
   "club_local":{
      "entrenador_2":"Unzue Labiano, Juan Carlos",
      "tarjetas":[
      ],
      "suplentes":[
         [
            13,
            "Cillessen , Jacobus Antonius Peter Johannes"
         ],
         [
            4,
            "Rakitic , Ivan"
         ],
         [
            7,
            "Turan , Arda"
         ],
         [
            12,
            "Alcantara Do Nascimento, Rafael"
         ],
         [
            17,
            "Alcacer Garcia, Francisco"
         ],
         [
            19,
            "Digne , Lucas"
         ],
         [
            23,
            "Um Titi , Samuel Yves"
         ]
      ],
      "alineacion":[
         [
            1,
            "Ter Stegen , Marc Andre"
         ],
         [
            3,
            "Pique Bernabeu, Gerard"
         ],
         [
            5,
            "Busquets Burgos, Sergio"
         ],
         [
            6,
            "Suarez Fernandez, Denis"
         ],
         [
            8,
            "Iniesta Lujan, Andres"
         ],
         [
            9,
            "Suarez Diaz, Luis Alberto"
         ],
         [
            10,
            "Messi Cuccittini, Lionel Andres"
         ],
         [
            11,
            "Da Silva Santos J, Neymar"
         ],
         [
            14,
            "Mascherano , Javier Alejandro"
         ],
         [
            18,
            "Alba Ramos, Jorge"
         ],
         [
            20,
            "Roberto Carnicer, Sergi"
         ]
      ],
      "sustituciones_count":2,
      "sustituciones":[
         {
            "entra":"Alcantara Do Nascimento, Rafael",
            "minuto":64,
            "sale":"Suarez Fernandez, Denis"
         },
         {
            "entra":"Um Titi , Samuel Yves",
            "minuto":74,
            "sale":"Busquets Burgos, Sergio"
         }
      ],
      "entrenador":"Martinez Garcia, Luis Enrique",
      "nombre":"FC Barcelona",
      "tarjetas_count":0,
      "goles_count":4,
      "goles":[
         {
            "goleador":"Suarez Diaz, Luis Alberto",
            "minuto":17,
            "tipo_gol":"Gol"
         },
         {
            "goleador":"Suarez Diaz, Luis Alberto",
            "minuto":66,
            "tipo_gol":"Gol"
         },
         {
            "goleador":"Alba Ramos, Jorge",
            "minuto":68,
            "tipo_gol":"Gol"
         },
         {
            "goleador":"Messi Cuccittini, Lionel Andres",
            "minuto":86,
            "tipo_gol":"Gol"
         }
      ]
   },
   "campo":"Camp Nou",
   "fecha":"2016-12-18 20:45:00",
   "club_visitante":{
      "entrenador_2":"Giraldez Diaz, Alberto",
      "tarjetas":[
         {
            "tarjeta":"Amarilla",
            "minuto":9,
            "jugador":"Piatti , Pablo Daniel"
         },
         {
            "tarjeta":"Amarilla",
            "minuto":12,
            "jugador":"Martin Caricol, Aaron"
         },
         {
            "tarjeta":"Amarilla",
            "minuto":64,
            "jugador":"Caicedo Corozo, Felipe Salvador"
         }
      ],
      "suplentes":[
         [
            1,
            "Jimenez Gago, Roberto"
         ],
         [
            3,
            "Duarte Sanchez, Ruben"
         ],
         [
            6,
            "Duarte Gaitan, Oscar Esau"
         ],
         [
            9,
            "Reyes Calderon, Jose Antonio"
         ],
         [
            22,
            "Vazquez Garcia, Alvaro"
         ],
         [
            28,
            "Roca Junqué, Marc"
         ],
         [
            30,
            "Melendo Jimenez, Oscar"
         ]
      ],
      "alineacion":[
         [
            13,
            "Lopez Rodriguez, Diego"
         ],
         [
            7,
            "Moreno Balagueró, Gerard"
         ],
         [
            10,
            "Caicedo Corozo, Felipe Salvador"
         ],
         [
            14,
            "Jurado Marin, Jose Manuel"
         ],
         [
            15,
            "Lopez Silva, David"
         ],
         [
            16,
            "Lopez Rodriguez, Javier"
         ],
         [
            18,
            "Fuego Martinez, Javier"
         ],
         [
            19,
            "Piatti , Pablo Daniel"
         ],
         [
            20,
            "Diop , Papa Kouly"
         ],
         [
            23,
            "Reyes Rosales, Diego Antonio"
         ],
         [
            29,
            "Martin Caricol, Aaron"
         ]
      ],
      "sustituciones_count":3,
      "sustituciones":[
         {
            "entra":"Jimenez Gago, Roberto",
            "minuto":51,
            "sale":"Lopez Rodriguez, Diego"
         },
         {
            "entra":"Melendo Jimenez, Oscar",
            "minuto":70,
            "sale":"Caicedo Corozo, Felipe Salvador"
         },
         {
            "entra":"Reyes Calderon, Jose Antonio",
            "minuto":79,
            "sale":"Piatti , Pablo Daniel"
         }
      ],
      "entrenador":"Sanchez Flores, Enrique",
      "nombre":"RCD spanyol de Barcelona SAD",
      "tarjetas_count":3,
      "goles_count":1,
      "goles":[
         {
            "goleador":"Lopez Silva, David",
            "minuto":78,
            "tipo_gol":"Gol"
         }
      ]
   },
   "urls":[
      "http://actas.rfef.es/actas/RFEF_CmpActa1?cod_primaria=1000144&CodActa=38657",
      "http://actas.rfef.es/actas/RFEF_CmpActa2?cod_primaria=1000144&CodActa=38657"
   ],
   "campeonato":"Campeonato de Liga 1ª División",
   "arbitros":{
      "arbitro_asistente_1":[
         "D. Martinez Munuera, Miguel",
         "Comité Valencia"
      ],
      "arbitro_asistente_2":[
         "D. Díaz Pérez Del Palomar, Roberto",
         "Comité Vasco"
      ],
      "arbitro":[
         "D. Mateu Lahoz, Antonio Miguel",
         "Comité Valencia"
      ],
      "cuarto_arbitro":[
         "D. Miralles Selma, Francisco",
         "Comité Valencia"
      ],
      "delegado":[
         "D. Segura García, Ricardo A.",
         "Comité Catalán"
      ]
   }
}
```