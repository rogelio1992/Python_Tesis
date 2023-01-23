#! /usr/bin/python
# -*- coding: utf-8 -*-
from .models import Datos_adinociales
import numpy as np
import datetime, random

from apps.tiempo.models import Estacion

currentDate = datetime.date.today()
meses = np.array(["Desconocido","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre" ,"Diciembre"])


#Sección 0 
#MiMiMjMj 
CODIGO_TIPO_ESTACION = {
    "AAXX": "Estación terrestre (FM 12)",
    "BBXX": "Estación maritima (FM 13)",
    "OOXX": "Estación terrestre móvil (FM 14)"
}

#IIiii



def get_stations():
    estaciones = Estacion.objects.all()
    stations = {}
    for estacion in estaciones:
        stations[estacion.code] = estacion.name
    
    return stations

def generar_color():
    return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

#YYGGIw
#Iw
indicador_del_viento = {
    '0': 'Estimada (en m/s)',
    '1': 'Obtenida con anemómetro (en m/s)',
    '3': 'Estimada (en nudos)',
    '4': 'Obtenida con anemómetro (en nudos)',
    '/' : 'No proporcionado' 
}



#Sección 1
#IrIxHVV

#Ir
ind_inclusio_omision_precipitacion = { 
    '0': 'En las secciones 1 y 3. Grupo 6RRR tR es incluido en ambas secciones',
    '1': 'Sección 1. Grupo 6RRR tR es incluido',
    '2': 'Sección 3. Grupo 6RRR tR es incluido',
    '3': 'Ninguno (ni en la sección 1 ni en la sección 3). Grupo 6RRR tR es omitido (La cantidad de precipitación = 0)',
    '4': 'Ninguno (ni en la sección 1 ni en la sección 3). Grupo 6RRR tR es omitido (No se dispone de datos de precipitación)',
    '/' : 'No proporcionado'
} 

#Ix
ind_operacion_tiempo_presente_pasado = {
    '1': 'Estación dotada de personal. El grupo 7wwW1W2 está incluido.',
    '2': 'Estación dotada de personal. El grupo 7wwW1W2 está omitido (nada importante)',
    '3': 'Estación dotada de personal. El grupo 7wwW1W2 está omitido (ninguna observación, datos no disponibles)',
    '4': 'Estación automática. El grupo 7wwW1W2 está incluido.',
    '5': 'Estación automática. El grupo 7wwW1W2 está omitido (ningún fenómeno importante por señalar)',
    '6': 'Estación automática. El grupo 7wwW1W2 está omitido (ninguna observación, datos no disponibles)',
    '/' : 'No proporcionado'
}
#H
altura ={
    "0": "0 a 49 m (0 a 166 pies)",
    "1": "50 a 99 m (167 - 333 pies)",
    "2": "100 a 199 m (334 - 666 pies)",
    "3": "200 a 299 m (667 - 999 pies)",
    "4": "300 a 599 m (1000 - 1999 pies)",
    "5": "600 a 999 m (2000 - 3333 pies)",
    "6": "1000 a 1499 m (3334 - 4999 pies)",
    "7": "1500 a 1999 m (5000 - 6666 pies)",
    "8": "2000 a 2499 m (6667 - 8333 pies)",
    "9": "2500 m o más (> 8334 pies) o sin nubes",
    "/": 'Altura de la base de la nube desconocida',
}

#VV
def calc_visivilidad(vis):
        visibilidad = int(vis)
        visib = 0

        if visibilidad <= 9:
            visib = f'{visibilidad * 100 } m'
        elif visibilidad <= 50:
            visib = f'{float(visibilidad)/10} km'
        elif visibilidad >= 56 and visibilidad <= 80 :
            visib = f'{visibilidad-50} km'
        elif visibilidad <= 88:
            visib = f'{(visibilidad-80)*5 + 30} km'
        elif visibilidad == 89:
            visib = f'> 70 km'
        elif visibilidad >= 90 and  visibilidad<=99:
            scale ={
                '90' : '< 50 m','91' : '50 m','92' : '200 m','93' : '500 m','94' : '1 km','95' : '2 km',
                '96' : '4 km','97' : '10 km','98' : '20 km','99' : '≥ 50 km', 
            }
            visib = scale[str(visibilidad)]
        else:
            visib = f'El valor de visibilidad no es valido'
        
        return visib



#Nddff (dd y ff se sacan de los numeros)
#N  
total_cielo_nublado = {
    "0": "0/8 (sin nubes)",
    "1": "1/8 o menos (casi claro)",
    "2": "2/8 (parcialmente nublado)",
    "3": "3/8",
    "4": "4/8 (nublado)",
    "5": "5/8",
    "6": "6/8 (muy nublado)",
    "7": "7/8 o más (casi nublado)",
    "8": "8/8 (nublado)",
    "9": "Cielo oscurecido, o no se puede estimar la nubosidad",
    "/": "no observado"
}

#dd Dirección de donde sopla el viento, en decenas de grados
direccion = {
    '00':'Viento en calma',
    '01': '5° a 14° N ¼ NE',
    '02': '15° a 24° NNE',
    '03': '25° a 34° NE ¼ N',
    '04': '35° a 44° NE',
    '05': '45° a 54° NE',
    '06': '55° a 64° NE ¼ E',
    '07': '65° a 74° ENE',
    '08': '75° a 84° E ¼ NE',
    '09': '85° a 94° E',
    '10': '95° a 104° E ¼ SE',
    '11': '105° a 114° ESE',
    '12': '115° a 124° SE ¼ E',
    '13': '125° a 134° SE',
    '14': '135° a 144° SE',
    '15': '145° a 154° SE ¼ S',
    '16': '155° a 164° SSE',
    '17': '165° a 174° S ¼ SE',
    '18': '175° a 184° S',
    '19': '185° a 194° S ¼ SW',
    '20': '195° a 204° SSW',
    '21': '205° a 214° SW ¼ S',
    '22': '215° a 224° SW',
    '23': '225° a 234° SW',
    '24': '235° a 244° SW ¼ S',
    '25': '245° a 254° WSW',
    '26': '255° a 264° W ¼ SW',
    '27': '265° a 274° W',
    '28': '275° a 284° W ¼ NW',
    '29': '285° a 294° WNW',
    '30': '295° a 304° NW ¼ W',
    '31': '305° a 314° NW',
    '32': '315° a 324° NW',
    '33': '325° a 334° NW ¼ N',
    '34': '335° a 344° NNW',
    '35': '345° a 354° N ¼ NW',
    '36': '355° a 4° N',
    '99': 'Viento variable',
}


#1SnTTT 2SnTdTdTd 3PPPP 4PPPP (Se sacan de los numeros)



#5aPPP  (PPP se saca de los numeros)
#5a  
caracter_tendencia_barica = {
    '0': 'Subiendo, después bajando, la presión atmosférica está igual o más alta que 3 horas antes',
    '1': 'Subiendo, después fijo, subiendo, después subiendo más despacio. La presión atmosférica está más alta que 3 horas antes',
    '2': 'Subiendo estable o inestablemente. La presión atmosférica está más alta que 3 horas antes',
    '3': 'Bajando o fijo, después subiendo o subiendo, después más aprisa. La presión atmosférica está más alta que 3 horas antes',
    '4': 'Fijo, la presión atmosférica está igual que 3 horas antes',
    '5': 'Bajando, después subiendo, la presión atmosférica está igual o más baja que 3 horas antes',
    '6': 'Bajando, después fijo, o bajando, después bajando más despacio. La presión atmosférica está más baja que 3 horas antes',
    '7': 'Bajando estable o inestablemente. La presión atmosférica está más baja que 3 horas antes',
    '8': 'Fijo o subiendo, después bajando, o bajando y después bajando más rápidamente. La presión atmosférica está más baja que 3 horas antes',
    '/' : 'No proporcionado'
}


#6RRRTr (RRR se saca del codigo)
#Tr
tiempo = {
    "0": "período no indicado o que finaliza antes de la fecha límite",
    "1": "6 h anteriores.",
    "2": "12 h anteriores.",
    "3": "18 h anteriores.",
    "4": "24 h anteriores.",
    "5": "1 h o 30 minutos.",
    "6": "2 h anteriores",
    "7": "3 h anteriores",
    "8": "9 h anteriores",
    "9": "15 h anteriores",
    "/": "Medida especial",
}

#RRR
def calc_RRR(RRR):
    if RRR >= 0 and RRR <= 989:
        return RRR
    elif RRR == 990:
        return 990
    else:
        return (RRR%10)/10

#7wwWW
#ww
tiempo_presente = {
    "00": "Desarrollo de nubes no observado",
    "01": "Nubes disminuyendo",
    "02": "Nubosidad sin cambios",
    "03": "Creciente nubosidad",
    "04": "Visibilidad reducida por humo o ceniza",
    "05": "neblina seca (humedad relativa < 80%)",
    "06": "polvo común en el aire, no traído por el viento",
    "07": "Polvo o arena o spray, arrastrado por el viento",
    "08": "remolinos de polvo o arena bien desarrollados",
    "09": "Tormenta de polvo o arena a la vista, pero no en la estación",
    "10": "neblina húmeda (humedad relativa > 80%)",
    "11": "Caminos de niebla terrestre",
    "12": "niebla terrestre permanente",
    "13": "Tormentas visibles, no se escuchan truenos",
    "14": "Precipitación a la vista, que no llega al suelo",
    "15": "Lluvia en la distancia (> 5 km) pero no en la estación",
    "16": "Lluvia cerca (< 5 km) pero no en la estación",
    "17": "Tormenta (trueno audible), pero sin precipitaciones en la estación",
    "18": "Ráfagas significativas en el campo de visión, pero sin precipitaciones en la estación",
    "19": "Tromben (tubos nubosos en forma de embudo) en el campo de visión",
    "20": "después de una llovizna o una llovizna de nieve",


    "21": "después de la lluvia",
    "22": "después de la nevada",
    "23": "después de aguanieve o granos de hielo",
    "24": "después de la lluvia helada",
    "25": "después de la lluvia",
    "26": "después de la lluvia de nieve",
    "27": "después de aguanieve o granizadas",
    "28": "después de la niebla",
    "29": "después de la tormenta",
    "30": "tormenta de arena ligera o moderada, de intensidad decreciente",
    "31": "Tormenta de arena ligera o moderada, intensidad sin cambios",
    "32": "tormenta de arena de ligera a moderada, aumentando en intensidad",
    "33": "tormenta de arena severa, de intensidad decreciente",
    "34": "tormenta de arena fuerte, intensidad sin cambios",
    "35": "tormenta de arena severa, aumentando en intensidad",
    "36": "barrido de nieve ligero o moderado, por debajo del nivel de los ojos",
    "37": "barrido de nieve pesada, por debajo del nivel de los ojos",
    "38": "Nevada ligera o moderada, por encima del nivel de los ojos",
    "39": "fuertes nevadas, por encima del nivel de los ojos",
    "40": "Niebla en la distancia",
    "41": "Niebla en nubes o bancos",

    "42": "Niebla, cielo perceptible, adelgazamiento",
    "43": "Niebla, cielo no perceptible, adelgazamiento",
    "44": "Niebla, cielo visible, sin cambios",
    "45": "Niebla, cielo no visible, sin cambios",
    "46": "Niebla, cielo reconocible, cada vez más denso",
    "47": "Niebla, cielo no reconocible, cada vez más denso",
    "48": "Niebla con escarcha, cielo visible",
    "49": "Niebla con escarcha, cielo no visible",
    "50": "llovizna ligera interrumpida",
    "51": "Llovizna ligera todo el tiempo",
    "52": "llovizna moderada intermitente",
    "53": "Llovizna moderada constante",
    "54": "llovizna intensa intermitente",
    "55": "llovizna fuerte continua",
    "56": "ligera llovizna helada",
    "57": "llovizna helada moderada o fuerte",
    "58": "llovizna ligera con lluvia",
    "59": "llovizna moderada o fuerte con lluvia",
    "60": "lluvia ligera intermitente o gotas de lluvia sueltas",
    "61": "Lluvia ligera en todas partes",

    "62": "lluvia moderada intermitente",
    "63": "Lluvia moderada constante",
    "64": "lluvia intensa interrumpida",
    "65": "lluvia fuerte continua",
    "66": "lluvia helada ligera",
    "67": "lluvia helada moderada o fuerte",
    "68": "aguanieve ligera",
    "69": "aguanieve moderada o fuerte",
    "70": "nevadas ligeras interrumpidas o copos de nieve dispersos",
    "71": "Nevada ligera en todas partes",
    "72": "nevada moderada interrumpida",
    "73": "Nevadas moderadas constantes",
    "74": "fuertes nevadas interrumpidas",
    "75": "Intensas nevadas continuas",
    "76": "Agujas de hielo (nieve polar)",
    "77": "Grano de nieve",
    "78": "Cristales de nieve",
    "79": "Granos de hielo (gotas de lluvia congeladas)",
    "80": "chubasco ligero",
    "81": "chubasco moderado o fuerte",
    "82": "chubasco de lluvia extremadamente fuerte",

    "83": "chubasco ligero de aguanieve",
    "84": "aguanieve moderada o fuerte",
    "85": "lluvia de nieve ligera",
    "86": "chubascos de nieve moderados o intensos",
    "87": "chubasco ligero de aguanieve",
    "88": "aguanieve moderada o fuerte",
    "89": "tormenta de granizo ligera",
    "90": "granizada moderada o fuerte",
    "91": "Tormenta en la última hora, actualmente lluvia ligera",
    "92": "Tormenta en la última hora, lluvia moderada o intensa en la actualidad",
    "93": "Tormenta en la última hora, actualmente nevada ligera/aguanieve/aguanieve/granizo",
    "94": "Tormenta en la última hora, actualmente moderada o fuerte nevada/aguanieve/aguanieve/granizo",
    "95": "tormenta eléctrica ligera a moderada con lluvia o nieve",
    "96": "tormenta de ligera a moderada con aguanieve o granizo",
    "97": "tormenta fuerte con lluvia o nieve",
    "98": "fuerte tormenta con tormenta de arena",
    "99": "tormenta fuerte con aguanieve o granizo",
    "//": "No proporcionado"
                         
 }

#WW
tiempo_pasado = {
    "0": "Cubierta de nubes siempre menor o igual a la mitad (0-4/8)",
    "1": "Cubierta de nubes a veces menor o igual, a veces cubriendo más de la mitad (</> 4/8)",
    "2": "Cubierta de nubes siempre más de la mitad cubierta (5-8/8)",
    "3": "Tormenta de polvo, tormenta de arena o ventisca de nieve",
    "4": "Niebla o neblina densa",
    "5": "llovizna",
    "6": "Lluvia",
    "7": "Nieve o aguanieve",
    "8": "Chubasco(s)",
    "9": "Tormenta(s), con o sin precipitación",
    '/' : 'No proporcionado'                 
}


#8NClCmCh
#Cl
LOW_CLOUDS_CODE = {"0": "sin nubes bajas",
                   "1": "Cumulus humilis o fractus (sin desarrollo vertical)",
                   "2": "Cumulus mediocris o congestus (desarrollo vertical moderado)",
                   "3": "Cumulonimbus calvus (sin contorno ni yunque)",
                   "4": "Stratocumulus cumulogenitus (creado por la propagación de cúmulos)",
                   "5": "Estratocúmulo",
                   "6": "Stratus nebulosus o fractus (área nubosa continua)",
                   "7": "Stratus fractus o Cumulus fractus (nubes irregulares con mal tiempo)",
                   "8": "Cumulus y Stratocumulus (a diferentes alturas)",
                   "9": "Cumulonimbus capillatus (con yunque)",
                   "/": "nubes bajas no visibles debido a niebla, oscuridad u ocultación",
                  
                  }
#Cm
MEDIUM_CLOUDS_CODE = {"0": "sin nubes de nivel medio",
                      "1": "Altostratus translucidus (principalmente transparente)",
                      "2": "Altostratus opacus o Nimbostratus",
                      "3": "Altocumulus translucidus (mayormente transparente)",
                      "4": "Bancos de Altocúmulos (irregulares, lenticulares)",
                      "5": "Bandas de altocúmulos (cubriendo progresivamente el cielo)",
                      "6": "Altocumulus cumulogenitus (creado por la propagación de cúmulos)",
                      "7": "Altocumulus (en capas o junto con Altostratus/Nimbostratus)",
                      "8": "Altocumulus castellanus o floccus (con mechones cumuliformes)",
                      "9": "Altocumulus de un cielo de aspecto desordenado",
                      "/": "Nubes de nivel medio no perceptibles debido a niebla, oscuridad u ocultación",
                      
                     }
#Ch
HIGH_CLOUDS_CODE = {"0": "sin nubes altas",
                    "1": "Cirrus fibratus o uncinus (copetudo)",
                    "2": "Cirrus spissatus, castellanus o floccus (denso, en penachos)",
                    "3": "Cirrus spissatus cumulogenitus (surgido de un yunque)",
                    "4": "Cirrus uncinus o fibratus (cubriendo el cielo de forma creciente o progresiva)",
                    "5": "Bandas de cirros o cirroestratos crecientes (a no más de 45 grados sobre el horizonte)",
                    "6": "Bandas de cirros o cirrostratos crecientes (más de 45 grados sobre el horizonte, que no cubren completamente el cielo)",
                    "7": "Cirrostratos (siempre cubriendo completamente el cielo)",
                    "8": "Cirrostratos (que no cubo completamente el cielo, pero tampoco aumenta)",
                    "9": "Cirrocúmulos",
                    "/": "nubes altas no visibles debido a niebla, oscuridad u ocultación",
                   
                    }

def calc_NCCC (NCCC):
    clouds = total_cielo_nublado[NCCC[0]]
  
    clouds = clouds + f', {LOW_CLOUDS_CODE[NCCC[1]]}, ' 
    clouds = clouds + f', {MEDIUM_CLOUDS_CODE[NCCC[2]]}, ' 
    clouds = clouds + f', {HIGH_CLOUDS_CODE[NCCC[3]]} ' 
  
    
    return clouds


#9GGgg
def calc_GGgg (GGgg):
    return f'{GGgg[0:2]}:{GGgg[2:5]}'



#Seccion 3

#0CsDlDmDh
tropicos = {
    '0': 'Las nubes Cúmulus son pequeñas, cubren menos de 2/8 del cielo, excepto en las laderas de las montañas, la anchura promedio de la nube es al menos tan grande como su desarrollo vertical.',
    '1': 'Los Cúmulus son de tamaño mediano y cubren menos de 5/8, la anchura media de la nube es mayor que su espesor vertical, las torres son verticales con ninguna o poca evidencia de precipitación, excepto en las laderas de las montañas, en general no existen nubes medias o altas.',
    '2': 'Cúmulus en estado de rápido desarrollo con torres altas que crecen en tamaño con altura y sus topes tienden a separarse de la nube principal y a evaporarse a los pocos minutos de su separación.',
    '3': 'Cúmulus crecientes con torres que tienen marcada inclinación en la misma dirección del flujo, el desarrollo vertical de la nube excede de 1.5 veces su anchura promedio.',
    '4': 'Cúmulus crecientes con torres que tienen marcada inclinación en la dirección opuesta a la del flujo, el desarrollo vertical de la nube excede de 1.5 veces su altura promedio.',
    '5': 'Cúmulus potentes con desarrollo vertical que excede el doble de la anchura promedio, no existe organización en líneas o agrupamientos de estos Cúmulus, uno o más niveles de nube se extienden a partir de las torres, sin embargo, estas nubes no forman capas continuas.',
    '6': 'Cumulonimbus aislados o grupos aislados de torres cumuliformes, las bases de las nubes se presentan generalmente oscuras y se observan chubascos asociados a la mayoría de las torres, algunas nubes medias y altas pueden estar presentes, el desarrollo vertical de los Cúmulus individuales es entre uno y dos veces la anchura de los mismos.',
    '7': 'Cúmulus numerosos que penetran bien la tropósfera media y existen en presencia de capas continuas o semi-continuas de nubes medias y/o cirrostratos, las torres cumuliformes generalmente no decrecen en tamaño con la altura, las bases oscuras de las nubes se presentan irregularmente y se observan algunos chubascos.',
    '8': 'Capas densas y continuas de nubes medias y/o Cs con algunos Cu grandes o Cu potentes que penetran estas capas, ocasionalmente se observa lluvia ligera procedente de As, las bases de los Cb son oscuras e irregulares con chubascos visibles.',
    '9': 'Capas continuas de nubes medias y Cirrostratus o Cirrostratus con Cumulonimbus y Cúmulus Congestus dispuestos en líneas o bandas nubosas, las capas de Altostratus generalmente producen lluvia y los Cumulonimbus chubascos fuertes, la índole del viento es rafagoso.',
    '/': 'Estado del cielo desconocido.',

}

#3EsTT
ESTT_GROUND_CONDITIONS_CODE = {
    "0": "Superficie del suelo seca (sin grietas y sin polvo o arena suelta en cantidad apreciable)",
    "1": "Superficie del suelo húmedo c/o",
    "2": "Superficie del suelo mojado (agua estancada en charcos grandes o pequeños sobre la superficie)",
    "3": "Suelo inundado",
    "4": "Superficie del suelo helado",
    "5": "Cencellada (hielo liso) transparente sobre el suelo",
    "6": "Polvo o arena secos sueltos que no cubren completamente el suelo",
    "7": "Fina capa de polvo o arena secos sueltos que cubren el suelo completamente",
    "8": "Capa media o espesa de polvo o arena secos sueltos que cubren el suelo completamente",
    "9": "Suelo extremadamente seco con grietas",
    '/' : 'No proporcionado'
}




#4E'sss
#E'
medida_cubierta_nieve_o_hielo = {
    '0' : 'Superficie predominantemente cubierta por hielo.',
    '1' : 'Nieve compacta o húmeda (con o sin hielo) cubriendo menos de la mitad del suelo.',
    '2' : 'Nieve compacta o húmeda (con o sin hielo) cubriendo mas de la mitad del suelo.',
    '3' : 'Cubierta homogénea compacta de nieve húmeda cubre el suelo completamente.',
    '4' : 'Cubierta no homogénea compacta de nieve húmeda cubre el suelo completamente.',
    '5' : 'Nieve seca suelta cubre menos de la mitad del suelo.',
    '6' : 'Nieve seca suelta cubre mas de la mitad del suelo (pero no completamente).',
    '7' : 'Nieve suelta en una cubierta homogénea cubre completamente el suelo.',
    '8' : 'Nieve suelta en una cubierta no homogénea cubre completamente el suelo.',
    '9' : 'Nieve cubre completamente el suelo. Ventisca grande.',
    '/' : 'No proporcionado'
}
#sss
def calc_sss(sss):
    int_sss = int(sss)
    if int_sss < 997:
        return f'{int_sss} cm'
    elif int_sss == 997:
        return f'Menos de 0.5 cm'
    elif int_sss == 998:
        return f'Cubierta de nieve no continua'
    else:
        return f'Medida imposible o inexacta.'

#54g0dT
tiempo_cambio_temperatura = {
    '0':' ',
    '1':'0. 30',
    '2':'1. 30',
    '3':'2. 30',
    '4':'3. 30',
    '5':'4. 30',
    '/': 'No proporcionado'
} 

cambio_temperatura = {
    '0':'10',
    '1':'11',
    '2':'12',
    '3':'13',
    '4':'14 o más',
    '5':'5',
    '6':'6',
    '7':'7',
    '8':'8',
    '9':'9',
    '/': 'No proporcionado'
}
#55EEEiE
instrumento_evaporacion = {
    '0': 'Evaporímetro estadounidense de recipiente abierto (sin tapa)',
    '1': 'Evaporímetro estadounidense de recipiente abierto (con tapa)',
    '2': 'Evaporímetro GG1-3000 (hundido)',
    '3': 'Tanque de 20m²',
    '4': 'Otros',
    '5': 'Arroz',
    '6': 'Trigo',
    '7': 'Maíz',
    '8': 'Sorgo',
    '9': 'Otros cultivos',
    '/': 'No proporcionado'
}
#56DDD
#D
direccion_nuves = {
    '0' : 'Estacionario o sin nubes',
    '1' : '23°-67° (NE)',
    '2' : '68°-112° (E)',
    '3' : '113°-157° (SE)',
    '4' : '158°-202° (S)',
    '5' : '203°-247° (SW)',
    '6' : '248°-292° (W)',
    '7' : '293°-337° (NW)',
    '8' : '338°-22° (N)',
    '9' : 'Desconocida o nubes no visibles',
    '/' : 'No proporcionado'
}
#57CDC

angulo_elevacion = {
    '0' : 'Cimas de la nube no visibles ',
    '1' : '45º aproximadamente ',
    '2' : '30º aproximadamente ',
    '3' : '20º aproximadamente ',
    '4' : '15º aproximadamente ',
    '5' : '12º aproximadamente',
    '6' : '9º aproximadamente',
    '7' : '7º aproximadamente',
    '8' : '6º aproximadamente',
    '9' : 'menor que 5º',
    '/' : 'No proporcionado'
}

#8NChh
#C
CLOUD_TYPE_CODE = {"0": "Cirrus (Ci)",
                   "1": "Cirrocúmulus (Cc)",
                   "2": "Cirrostratus (Cs)",
                   "3": "Altocúmulus (Ac)",
                   "4": "Altostratus (As)",
                   "5": "Nimbostratus (Ns)",
                   "6": "Stratocúmulus (Sc)",
                   "7": "Stratus (St)",
                   "8": "Cúmulus (Cu)",
                   "9": "Cumulunimbus (Cb)",
                   "/": "Nubes no visibles a causa de oscuridad, niebla, tempestad de polvo o arena, u otro fenómeno."
}
                   
CLOUD_HEIGHT_CLASSES = {
    '90' : '0 a 50 m',
    '91' : '50 a 99 m',
    '92' : '100 a 199 m',
    '93' : '200 a 299 m',
    '94' : '300 a 599 m',
    '95' : '600 a 999 m',
    '96' : '1000 a 1499 m',
    '97' : '1500 a 1999 m',
    '98' : '2000 a 2499 m',
    '99' : '2500 m o más, o sin nubes',
    '//' : 'No proporcionado.'
}
def calc_hh(hh):
    if hh == '//':
        return CLOUD_HEIGHT_CLASSES[hh]
    else:
        int_hh = int(hh)
        if int_hh == 0 :
            return f'menor a 30 m (100 ft)'
        elif int_hh <= 50:
            return f'{int_hh*30} m ({int_hh*100} ft)' 
        elif int_hh >= 56 and int_hh <= 80:
            return f'{(int_hh - 50)* 300} m'
        elif int_hh >= 81 and int_hh <= 89:
            return f'{(int_hh - 80)* 1500 + 9000} m'
        else:
            return CLOUD_HEIGHT_CLASSES[hh]


def calc_dir_vient(grado):
    if grado == 0:
        return '--'
    elif grado < 23:
        return 'N'
    elif grado < 45:
        return 'NNE'
    elif grado < 67:
        return 'NE'
    elif grado < 90:
        return 'ENE'
    elif grado < 112:
        return 'E'
    elif grado < 135:
        return 'ESE'
    elif grado < 157:
        return 'SE'
    elif grado < 180:
        return 'SSE'
    elif grado < 202:
        return 'S'
    elif grado < 225:
        return 'SSO'
    elif grado < 247:
        return 'SO'
    elif grado < 270:
        return 'OSO'
    elif grado < 292:
        return 'O'
    elif grado < 315:
        return 'ONO'
    elif grado < 337:
        return 'NO'
    elif grado <= 360:
        return 'NNO'
    return '--'


def mayor(lista):
    max = lista[0]
    for x in lista:
        if x > max:
            max = x
    return max    
 
def menor(lista):
    min = lista[0]
    for x in lista:
        if x < min:
            min = x
    return min




TABLA_28_a = {
    '00': 'En la Observación',
    '01': '0 hora 6 minutos',
    '02': '0 hora 12 minutos',
    '03': '0 hora 18 minutos',
    '04': '0 hora 24 minutos',
    '05': '0 hora 30 minutos',
    '06': '0 hora 36 minutos',
    '07': '0 hora 42 minutos',
    '08': '0 hora 48 minutos',
    '09': '0 hora 54 minutos',
    '10': '1 hora 0 minutos',
    '11': '1 hora 6 minutos',
    '12': '1 hora 12 minutos',
    '13': '1 hora 18 minutos',
    '14': '1hora 24 minutos',
    '15': '1 hora 30 minutos',
    '16': '1 hora 36 minutos',
    '17': '1 hora 42 minutos',
    '18': '1 hora 48 minutos',
    '19': '1hora 54 minutos',
    '20': '2 horas 0 minutos',
    '21': '2 horas 6 minutos',
    '22': '2 horas 12 minutos',
    '23': '2 horas 18 minutos',
    '24': '2 horas 24 minutos',
    '25': '2 horas 30 minuto',
    '26': '2 horas 36 minutos',
    '27': '2 hora 42 minutos',
    '28': '2 horas 48 minutos',
    '29': '2 horas 54 minutos',
    '30': '3 horas 0 minutos',
    '31': '3 horas 6 minutos',
    '32': '3 horas 12 minutos',
    '33': '3 horas 18 minutos',
    '34': '3 horas 24 minutos',
    '35': '3 horas 30 minutos',
    '36': '3 horas 36 minutos',
    '37': '3 horas 42 minutos',
    '38': '3 horas 48 minutos',
    '39': '3 horas 54 minutos',
    '40': '4 horas 0 minutos',
    '41': '4 horas 6 minutos',
    '42': '4 horas 12 minutos',
    '43': '4 hora 18 minuto',
    '44': '4 horas 24 minutos',
    '45': '4 horas 30 minutos',
    '46': '4 horas 36 minutos',
    '47': '4 horas 42 minutos',
    '48': '4 horas 48 minutos',
    '49': '4 horas 54 minutos',
    '50': '5 horas 0 minutos',
    '51': '5 horas 6 minutos',
    '52': ' 5 horas 12 minutos',
    '53': '5 horas 18 minutos',
    '54': '5 horas 24 minutos',
    '55': '5 horas 30 minutos',
    '56': '5 horas 36 minutos',
    '57': '5 horas 42 minutos',
    '58': '5 horas 48 minutos',
    '59': '5 horas 54 minutos',
    '60': '6 horas 0 minutos',
    '61': '6 horas a 7 horas',
    '62': '7 horas a 8 horas',
    '63': '8horas  a 9 horas',
    '64': '9 horas a 10 horas',
    '65': '10 horas a 11 horas',
    '66': '11 horas a 12 horas',
    '67': '12 horas a 18 horas',
    '68': 'Más de 18 horas',
    '69': 'Hora desconocida',
    '70': 'Comienzo durante la Observación',
    '71': 'Terminación durante la Observación',
    '72': 'Comienzo y terminación durante la Observación',
    '73': 'Cambio considerable durante la Observación',
    '74': 'Comienzo después de la Observación',
    '75': 'Terminación después de la Observación',
    '76': 'En la Estación',
    '77': 'En la Estación pero no a distancia',
    '78': 'En todas las direcciones',
    '79': 'En todas las direcciones, pero no en la Estación',
    '80': 'Aproximación a la Estación',
    '81': 'Alejamiento de la Estación',
    '82': 'Pasa a distancia de la Estación',
    '83': 'Observación a distancia',
    '84': 'Observación en la cercanía pero no en la Estación',
    '85': 'En lo alto, pero no cerca del suelo',
    '86': 'Cerca del suelo, pero no en lo alto',
    '87': 'Ocasional, ocasionalmente',
    '88': 'Intermitente, intermitentemente',
    '89': 'Frecuente, frecuentemente, a intervalos frecuentes',
    '90': 'Estable, estable en intensidad, establemente, sin cambios apreciables',
    '91': 'En aumento, intensidad en aumento, ha aumentado',
    '92': 'En descenso, intensidad en descenso, ha disminuido',
    '93': 'Fluctuante, variable',
    '94': 'Continuo, continuamente',
    '95': 'Muy ligera, muy débil, muy por debajo de lo normal, muy fina, muy escasa',
    '96': 'Ligero, débil, por debajo de lo normal, fina, escasa',
    '97': 'Moderada, normal, densidad media, mediana gradualmente',
    '98': 'Fuerte, severa, densa, sobre la normal, mediana, repentina',
    '99': 'Muy fuerte, cruda, muy rigurosa, densa muy por encima de la normal, muy densa, muy buena',

}
HORA_Y_VARIABILIDAD = {
    '00tt': 'Hora de comienzo del fenómeno meteorológico comunicado mediante WW en el grupo 7wwW1W2',
    '00zz': 'Variabilidad, localización e intensidad del fenómeno meteorológico comunicado mediante WW en el grupo 7wwW1W2 ',
    '01tt': 'Hora de terminación del fenómeno meteorológico comunicado mediante el grupo 7wwW1W2',
    '02tt': 'Hora de comienzo del fenómeno meteorológico comunicado en el grupo 9SpSpSpSp siguiente',
    '02zz': 'Variabilidad, localización e intensidad del fenómeno meteorológico comunicado mediante WW en el grupo 7wwW1W2',
    '03tt': 'Hora de terminación del fenómeno meteorológico comunicado en el grupo 9SpSpSpSp anterior',
    '04tt': 'Hora en que se produce el fenómeno meteorológico comunicado en el grupo 9SpSpSpSp anterior',
    '05tt': 'Duración de un fenómeno meteorológico no persistente u hora de comienzo de un fenómeno meteorológico persistente, comunicado mediante WW en el grupo 7wwW1W2',
    '06tt': 'Duración de un fenómeno meteorológico no persistente u hora de comienzo de un fenómeno meteorológico persistente, comunicado en el grupo 9SpSpSpSp siguiente',
    '07tt': 'Duración de período de referencia que termina a la Hora de la Observación de un fenómeno meteorológico comunicado en el grupo 9SpSpSpSp siguiente',
    '08tt': 'No utilizada',
    '09Rt': 'Hora en que comenzó o terminó la precipitación indicada por RRR y duración y carácter de la precipitación',

}
TABLA_28_b = {
    '1': 'Menos de 1 hora antes de la Hora de la Observación',
    '2': 'De 1 a 2horas antes de la Hora de la Observación',
    '3': 'De 2 a 3 horas antes de la Hora de la Observación',
    '4': 'De 3 a 4 horas antes de la Hora de la Observación',
    '5': 'De 4 a 5 horas antes de la Hora de la Observación',
    '6': 'De 5 a 6 horas antes de la Hora de la Observación',
    '7': 'De 6 a 12 horas antes de la Hora de la Observación',
    '8': 'Más de 12 horas antes de la Hora de la Observación',
    '9': 'No se conoce',
    '/': 'No proporcionado'
}
TABLA_28_c ={
    '0': 'Duración inferior a 1 hora',
    '1': 'Duración de 1 a 3 horas',
    '2': 'Duración de 3 a 6 horas',
    '3': 'Duración más de 6 horas',
    '4': 'Duración menos de 1 hora',
    '5': 'Duración de 1 a 3 horas',
    '6': 'Duración de 3 a 6 horas',
    '7': 'Duración más de 6 horas',
    '9': 'No se conoce',
    '/': 'No proporcionado',
}
VIENTO_Y_TURBONADAS = {
    '10ff': 'Ráfaga máxima durante los 10 minutos inmediatamente anteriores a la Hora de la Observación',
    '11ff': 'Ráfaga máxima',
    '12ff': 'Velocidad media máxima del viento',
    '13ff': 'Velocidad media del viento',
    '14ff': 'Velocidad media mínima del viento',
    '15dd': 'Dirección del viento',
    '16tt': 'Cambio pronunciado de la dirección del viento en el sentido de las agujas del reloj (destrogiro) (Tabla 28 a)',
    '17tt': 'Cambio pronunciado de la dirección del viento en el sentido contrario a las agujas del reloj (levogiro) ) (Tabla 28 a)',
    '19MwDa': 'Tromba(s) máxima(s), tornados, torbellinos, remolinos de polvo.',

} 
TABLA_28_d = {
    '0': 'Tromba(s) marina(s) a 3 km como máxima de la Estación',
    '1': 'Tromba(s) marina(s) a más de 3 km de la Estación',
    '2': 'Nubes de tornado a 3 km como máximo de la Estación',
    '3': 'Nubes de tornado a más de 3 km de la Estación',
    '4': 'Torbellinos de poca intensidad',
    '5': 'Torbellinos de intensidad moderada',
    '6': 'Torbellinos de gran intensidad',
    '7': 'Remolinos de polvo de poca intensidad',
    '8': 'Remolinos de polvo de intensidad moderada',
    '9': 'Remolinos de polvo de gran intensidad   ',

}
TABLA_26 = {
    '0': 'En la Estación',
    '1': 'NE',
    '2': 'E',
    '3': 'SE',
    '4': 'S',
    '5': 'SW',
    '6': 'W',
    '7': 'NW',
    '8': 'N',
    '9': 'Todas las direcciones',
} 
Estado_del_mar = {
    '20':'Estado del mar y fuerza máxima del viento (Fx ≤ 9 Beaufort)',
    '21':'Estado del mar y fuerza máxima del viento (Fx > Beaufort)',
    '23':'Estado del mar en la zona de amarizaje y en alta mar',
    '24':'Estado del mar y visibilidad mar adentro (desde una Estación costera)',
} 
TABLA_28_e = {
    '0': 'Calma (como un espejo), 0m',
    '1': 'Calma (con rizos), 0 a 0,1m',
    '2': 'Ondulada, 0,1 a 0,5m',
    '3': 'Ligeramente agitado, 0,5 a 1,25m',
    '4': 'Agitada, 1,25 a 2,5m',
    '5': 'Gruesa, 2,5 a 4m',
    '6': 'Muy gruesa, 4 a 6m',
    '7': 'Alta, 6 a 9m',
    '8': 'Muy alta, 9 a 14m',
    '9': 'Montañoso, Más de 14m',

}
TABLA_28_f = {
    '0': 'Inferior a 50 metros',
    '1': 'De 50 a 200 metros',
    '2': 'De 200 a 500 metros',
    '3': 'De 500 a 1000 metros',
    '4': 'De 1 a 2 km',
    '5': 'De 2 a 4 km',
    '6': 'De 4 a 6 km',
    '7': 'De 10 a 20 km',
    '8': 'De 20 a 50 km',
    '9': '50 km o más',

}
TABLA_28_g ={
    '00': '0',
    '01': '1',
    '02': '2',
    '03': '3',
    '04': '4',
    '05': '5',
    '06': '6',
    '07': '7',
    '08': '8',
    '09': '9',
    '10': '10',
    '11': '11',
    '12': '12',
    '13': '13',
    '14': '14',
    '15': '15',
    '16': '16',
    '17': '17',
    '18': '18',
    '19': '19',
    '20': '20',
    '21': '21',
    '22': '22',
    '23': '23',
    '24': '24',
    '25': '25',
    '26': '26',
    '27': '27',
    '28': '28',
    '29': '29',
    '30': '30',
    '31': '31',
    '32': '32',
    '33': '33',
    '34': '34',
    '35': '35',
    '36': '36',
    '37': '37',
    '38': '38',
    '39': '39',
    '40': '40',
    '41': '41',
    '42': '42',
    '43': '43',
    '44': '44',
    '45': '45',
    '46': '46',
    '47': '47',
    '48': '48',
    '49': '49',
    '50': '50',
    '51': '51',
    '52': '52',
    '53': '53',
    '54': '54',
    '55': '55',
    '56': '60',
    '57': '70',
    '58': '80',
    '59': '90',
    '60': '100',
    '61': '110',
    '62': '120',
    '63': '130',
    '64': '140',
    '65': '150',
    '66': '160',
    '67': '170',
    '68': '180',
    '69': '190',
    '70': '200',
    '71': '210',
    '72': '220',
    '73': '230',
    '74': '240',
    '75': '250',
    '76': '260',
    '77': '270',
    '78': '280',
    '79': '290',
    '80': '300',
    '81': '310',
    '82': '320',
    '83': '330',
    '84': '340',
    '85': '350',
    '86': '360',
    '87': '370',
    '88': '380',
    '89': '390',
    '90': '400',
    '91': '0,1',
    '92': '0,2',
    '93': '0,3',
    '94': '0,4',
    '95': '0,5',
    '96': '0,6',
    '97': 'Precipitación escasa no mensurable',
    '98': 'Más de 400 ',
    '99': 'Medición imposible',

}
Tabla_28_h = {
    '0': 'Todas las montañas despejadas, solo se ven unas pocas nubes',
    '1': 'Montañas parcialmente cubiertas por nubes dispersas (se ve menos de la mitad de las cimas)',
    '2': 'Todas las laderas de las montañas cubiertas, cimas y pasos despejados',
    '3': 'Montañas despejadas del lado del Operador (solo se ven unas pocas nubes) pero existe una cortina de nubes homogéneas del otro lado',
    '4': 'Nubes rasantes a las montañas, pero todas las laderas y montañas despejadas (solo se ven unas pocas nubes en las laderas)',
    '5': 'Nubes rasantes a las montañas, cimas cubiertas parcialmente por la cortina de la precipitación o las nubes',
    '6': 'Todas las cimas cubiertas pero los pasos despejados, las laderas despejadas o cubiertas',
    '7': 'Montañas cubiertas por lo general, pero algunas cimas despejadas, las laderas total o parcialmente cubiertas',
    '8': 'Todas las cimas, pasos y laderas cubiertas',
    '9': 'No se ven las montañas debido a la oscuridad, la niebla, la nevada, la precipitación, etc.',

}
TABLA_28_i = {
    '0': 'Sin cambios',
    '1': 'Toma forma de cúmulo',
    '2': 'Se eleva lentamente',
    '3': 'Se eleva rápidamente',
    '4': 'Se eleva y estratifica',
    '5': 'Desciende lentamente',
    '6': 'Desciende rápidamente',
    '7': 'Se estratifica',
    '8': 'Se estratifica y desciende',
    '9': 'Varía rápidamente',

}
TABLA_28_j = {
    '0': 'Ni nubes, ni neblina',
    '1': 'Neblina, por encima, claro',
    '2': 'Bancos de niebla dispersos',
    '3': 'Capa de niebla ligera',
    '4': 'Capa de niebla densa',
    '5': 'Algunas nubes aisladas',
    '6': 'Nubes aisladas, por encima, claro',
    '7': 'Muchas nubes aisladas',
    '8': 'Mar de nubes',
    '9': 'Mala visibilidad hacia abajo',

}
TABLA_28_k ={
    '0': 'Sin cambios',
    '1': 'Disminución y elevación',
    '2': 'Disminución',
    '3': 'Elevación',
    '4': 'Disminución y descenso',
    '5': 'Aumento y elevación',
    '6': 'Descenso',
    '7': 'Aumento',
    '8': 'Aumento y descenso',
    '9': 'Niebla intermitente en la Estación',

}
def create_9SSss(synop,value):
    obj = Datos_adinociales()
    obj.synop = synop
    obj.value = value
    aux = 'tt'
    obj.descripcion = 'HORA Y VARIABILIDAD'

    if value[1:3]!='//'and int(value[1:3]) <= 9 :
        obj.descripcion = 'HORA Y VARIABILIDAD'
        if value[3:5]!='//'and int(value[3:5]) >=76 and int(value[3:5]) <= 99:
            aux = 'zz'
        if value[1:3] == '00' or value[1:3] == '02':
            obj.var_SpSp = HORA_Y_VARIABILIDAD[f'{value[1:3]}{aux}']
            obj.var_ss = TABLA_28_a[value[3:5]]
        elif value[1:3] == '09':
            obj.var_SpSp = HORA_Y_VARIABILIDAD['09Rt']
            obj.var_ss = f'{TABLA_28_b[value[3]]}, {TABLA_28_c[value[4]]}'
        elif value[3:5]!='//'and int(value[1:3]) <= 9 :
            obj.var_SpSp = HORA_Y_VARIABILIDAD[f'{value[1:3]}{aux}']
            obj.var_ss = TABLA_28_a[value[3:5]]
    elif value[1:3]!='//'and int(value[1:3]) <= 19 and int(value[1:3])>=10:
        obj.descripcion = 'VIENTO Y TURBONADAS'
        if int(value[1:3])>=10 and int(value[1:3])<=14:
            obj.var_SpSp = VIENTO_Y_TURBONADAS[f'{value[1:3]}ff']
            obj.var_ss = value[3:5]
        elif value[1:3] == '15':
            obj.var_SpSp = VIENTO_Y_TURBONADAS[f'15dd']
            obj.var_ss = direccion[value[3:5]]
        elif value[1:3] == '16' or value[1:3] == '17':
            obj.var_SpSp = VIENTO_Y_TURBONADAS[f'{value[1:3]}tt']
            obj.var_ss = TABLA_28_a[value[3:5]]
        elif value[1:3] == '19':
            obj.var_SpSp = VIENTO_Y_TURBONADAS['19MwDa']
            obj.var_ss = f'{TABLA_28_d[value[3]]} - {TABLA_26[value[4]]}'
    elif value[1:3]!='//'and int(value[1:3]) >= 20 and int(value[1:3])<=29:
        obj.descripcion = 'Estado del mar'
        if value[1:3] == '20':
            obj.var_SpSp = Estado_del_mar[value[1:3]]
            obj.var_ss = TABLA_28_e[value[3]]
        elif value[1:3] == '21':
            obj.var_SpSp = Estado_del_mar[value[1:3]]
            obj.var_ss = TABLA_28_e[value[3]]
        elif value[1:3] == '23':
            obj.var_SpSp = Estado_del_mar[value[1:3]]
            obj.var_ss = TABLA_28_e[value[4]]
        elif value[1:3] == '24':
            obj.var_SpSp = Estado_del_mar[value[1:3]]
            obj.var_ss = f'{TABLA_28_e[value[3]]} - {TABLA_28_f[value[4]]}'
    elif value[1:3]!='//'and int(value[1:3]) >= 30 and int(value[1:3])<=39:
        obj.descripcion = 'Cantidad de precipitación o depósito '
        if value[1:3] == '30':
            obj.var_SpSp = f'Cantidad de precipitación'
            obj.var_ss = TABLA_28_g[value[3:5]]
        elif value[1:3] == '32':
            obj.var_SpSp = f'Diámetro máximo de las piedras de granizo'
            obj.var_ss = TABLA_28_g[value[3:5]]
    elif value[1:3]!='//'and int(value[1:3]) >= 50 and int(value[1:3])<=59:
        obj.descripcion = 'Condiciones de nubosidad en montañas y pasos o en valles o llanuras observadas desde más alto nivel'
        if value[1:3] == '50':
            obj.var_SpSp = f'Condiciones de nubosidad sobre montañas y pasos'
            obj.var_ss = TABLA_28_g[value[3:5]]
        elif value[1:3] == '51':
            obj.var_SpSp = f'Niebla, neblina o nubes bajas en valles o llanuras, observadas desde una Estación situada a más alto nivel'
            obj.var_ss = F'{TABLA_28_j[value[3]]} - {TABLA_28_k[value[4]]}'

    elif value[1:3]!='//'and int(value[1:3]) >= 90 and int(value[1:3])<=99:
        obj.descripcion = 'Fenómenos ópticos y de otro tipo '
        if value[1:3] == '95':
            obj.var_SpSp = f'Presión atmosférica mínima reducida al nivel medio del mar durante el período abarcado por W1W2 '
            obj.var_ss = value[3:5]
    return obj