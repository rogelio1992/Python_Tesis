from pickle import TRUE
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator 
# Create your models here.


class Provincia(models.Model):

    name = models.CharField("Provincia", max_length=50)
   
    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"

    def __str__(self):
        return self.name

class Estacion(models.Model):

    name = models.CharField("Nombre", max_length=100)
    code = models.CharField("Código", max_length=50, unique=True)
    provincia = models.ForeignKey(Provincia, verbose_name="Provincia", on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "Estacion"
        verbose_name_plural = "Estaciones"

    def __str__(self):
        return f'{self.name} - {self.code}'


 


class Synop(models.Model):
    """Model definition for Synop."""

    # TODO: Define fields here
    estacion = models.ForeignKey(Estacion, verbose_name="Estacion", on_delete=models.CASCADE)
    synop_code = models.TextField("Código Synop")
    tipo_synop = models.CharField("Tipo de Synop", max_length=250 , default= "AAXX")
    fecha = models.DateField("Fecha", auto_now=False, auto_now_add=False)
    hora = models.IntegerField("Hora UTC", default= 0)
    indicador_viento_Iw = models.CharField("Indicador del Viento", max_length=250 , default="No proporcionado")
   
    var_Iy = models.CharField("Inclusión u omisión de precipitación", max_length=250 , default="No proporcionado")
    var_Ix = models.CharField("Tipo de operación de la estación", max_length=250 , default="No proporcionado")
    var_H = models.CharField("Altura por encima del suelo", max_length=250 , default="No proporcionado") 
    var_VV = models.CharField("Visibilidad horizontal en superficie", max_length=250 , default="No proporcionado")
    var_N = models.CharField("Cobertura nubosa total en octavos", max_length=250 , default="No proporcionado")
    var_dd = models.CharField("Dirección verdadera de donde sopla el viento en °", max_length=250 , default="No proporcionado")
    var_ff = models.CharField("Velocidad del viento en nudos", max_length=50 , default="No proporcionado")
    var_direccion = models.CharField("Dirección", max_length=250 , default="No proporcionado")
    

    #Seccion 1
    #1SnTTT
    vat_TTT = models.FloatField("Tempertura del Aire en °C", default= -999)
    #2SnTTT
    var_TTT_rocio = models.FloatField("Tempertura del Rocío en °C",default= -999)
    #29UUU
    var_UUU = models.IntegerField("Humedad relativa en porcentaje",default= -999)
    #3PPPP
    var_PPPP = models.FloatField("Presión a nivel de la estación en hPa", default= -999)
    #4PPPP
    var_PPPP_mar = models.FloatField("Presión a nivel medio del mar" , default= -999)
    #5appp
    var_a = models.CharField("Característica de la tendencia barométricas", max_length=250, default="No proporcionado")
    var_ppp = models.FloatField("Valor en hPa" , default= -999)
    #6RRRTr
    var_RRR = models.FloatField("Precipitaciones en mm", default= -999)
    var_Tr = models.CharField("Tiempo en el que a caido las Precipitaciones", max_length=250, default="No proporcionado")
    #7wwWW
    var_ww_presente = models.CharField("Tiempo presente desde una estación", max_length=250, default="No proporcionado")
    var_WW_pasado = models.CharField("Tiempo pasado desde una estación", max_length=250, default="No proporcionado")
    #8NCCC
    var_CCC = models.CharField("Cantidad de nubes", max_length=400, default="No proporcionado")
    #9GGgg
    var_GGgg = models.CharField("Hora con minutos", max_length=250, default="No proporcionado")

    #Seccion 3
    #0CsDlDmDh
    var_Cs = models.CharField("Estado del cielo en los trópicos", max_length=400, default="No proporcionado")
    

    #1SnTTT
    var_TTT_maxima = models.FloatField("Temperatura máxima de las últimas 12 horas", default=-999) 
    #2SnTTT
    var_TTT_minima = models.FloatField("Temperatura mínima de las últimas 12 horas", default=-999) 
    #3ESnTT
    var_E = models.CharField("Estado del suelo", max_length=250, default="No proporcionado")
    var_TT_suelo = models.FloatField("Temperatura mínima del suelo  entre las 00 y 12 UTC",default= -999) 
    #4E'sss
    var_E_hielo = models.CharField("Estado del suelo (nieve o con una capa de hielo medible)", max_length=250, default="No proporcionado")
    var_sss = models.CharField("Profundidad de la nieve", max_length=250, default="No proporcionado")
    
    #54g0dT
    var_g0 = models.CharField("Número de horas enteras que han transcurrido desde el momento del cambio", max_length=250, default="No proporcionado")
    var_dT = models.CharField("Cambio de temperatura ", max_length=250, default="No proporcionado")
    #5EEEiE
    var_EEE_evapo = models.FloatField("Cantidad de evaporación",default= -999)
    var_iE = models.CharField("Tipo de instrumento para medir la evaporación", max_length=250, default="No proporcionado")
    #55SSS
    var_SSS_insolacion = models.FloatField("Horas diarias de insolación",default= -999) 
    #56DDD
    var_Dl = models.CharField("Dirección y movimiento de las nubes Cl", max_length=250, default="No proporcionado")
    var_Dm = models.CharField("Dirección y movimiento de las nubes Cm", max_length=250, default="No proporcionado")
    var_Dh = models.CharField("Dirección y movimiento de las nubes Ch", max_length=250, default="No proporcionado")
    #57CDC
    var_C_genero = models.CharField("Género", max_length=250, default="No proporcionado")
    var_D = models.CharField("Dirección en la que se ven nubes", max_length=250, default="No proporcionado")
    var_C_angulo = models.CharField("Ángulo de elevación de la cima de la nube", max_length=250, default="No proporcionado")
    #58PPP - 59PPP
    var_PPP_presion = models.FloatField("Variación de la presión últimas 24 horas",default= -999) 
    #6RRRTr
    var_RRR_presipitacion = models.FloatField("Cantidad de precipitación acumulada",default= -999) 
    #7RRRR
    var_RRRR = models.FloatField("Precipitación 24 h antes de la observación en mm",default= -999) 
    #8NChh
    var_N_nubes = models.CharField("Cantidad de nubes individuales del género", max_length=250, default="No proporcionado")
    var_C_nube = models.CharField("Tipo de nubes", max_length=250, default="No proporcionado")
    var_hhh = models.CharField("Dirección en la que se ven nubes", max_length=250, default="No proporcionado")
   

    #Sección 5
    var_PhPh = models.CharField("QNH en hPa", max_length=250, default="No proporcionado")
    var_CCCC = models.CharField("Presencia de cenizas volcánicas", max_length=250, default="No hay cenizas volcánicas")
    var_FFFF = models.IntegerField("Nivel de la capa freática", default=-999)
    var_EEEE = models.FloatField("Evaporación diaria", default=-999)
    #5ddff
    var_dxdx = models.CharField("Dirección de la ráfaga", max_length=250, default="No proporcionado")
    var_fxfx = models.CharField("Velocidad en nudos de la ráfaga", max_length=250, default="No proporcionado")
    #6HeHeHeIv
    var_HeHeHe = models.CharField("Heliofanía efectiva del día civil anterior", max_length=250, default="No proporcionado")
    var_Iv = models.CharField(" Tipo de instrumento medidor de viento", max_length=250, default="No proporcionado")
    #64HHH 
    var_HHH_max = models.CharField("Horas en que se registraron las temperaturas máximas", max_length=250, default="No proporcionado")
    #65HHH
    var_HHH_min = models.CharField("Horas en que se registraron las temperatura mínimas", max_length=250, default="No proporcionado")

    #66TsTsTs 
    var_TTT_pos = models.CharField("Temperatura del suelo de cero grados o mayor", max_length=250, default="No proporcionado")
    #67TsTsTs
    var_HHH_neg = models.CharField("Temperatura del suelo inferior a cero grados", max_length=250, default="No proporcionado")
    #7ddff
    var_dd_ff = models.CharField("Dirección desde la que sopló la ráfaga - Velocidad", max_length=250, default="No proporcionado")
    #74HHH 
    var_HHH_rafaga = models.CharField("Hora de ocurrencia de la ráfaga", max_length=250, default="No proporcionado")
    #8HmHmHnHn
    var_HmHmHnHn = models.CharField("Valor de la humedad y minima en %", max_length=250, default="No proporcionado")
    #9RsRsRsR
    var_RRR_semana= models.FloatField("Precipitaciones de la semana en mm", default=-999)

    class Meta:
        """Meta definition for Synop."""

        verbose_name = 'Synop'
        verbose_name_plural = 'Synops'

    def __str__(self):
        return f'{self.estacion} -{self.fecha}'

class Datos_adinociales(models.Model):
    synop = models.ForeignKey(Synop, verbose_name="Synop", on_delete=models.CASCADE)
    value = models.CharField(("Grupo de fenómenos especiales"), max_length=50)
    descripcion = models.CharField(("Descripción"), max_length=250)

    var_SpSp = models.CharField("SpSp", max_length=250)
    var_ss = models.CharField("spsp", max_length=250)
    

    class Meta:
        verbose_name = "Dato adicional"
        verbose_name_plural = "Datos adicionales"

    def __str__(self):
        return self.value

    


tiempo = (
        ("PN", "PN"),
        ("PARCN", "PARCN"),
        ("N", "N"),
        ("AIS CHUB", "AIS CHUB"),
        ("ALG CHUB", "ALG CHUB"),
        ("NUM CHUB", "NUM CHUB"),
        ("ALG TORM", "ALG TORM"),
        ("NUM TORM", "NUM TORM"),
   )

viento = (
    ("VRB","VRB"),
    ("N","N"),
    ("NNE","NNE"),
    ("NE","NE"),
    ("ENE","ENE"),
    ("E","E"),
    ("ESE","ESE"),
    ("SE","SE"),
    ("SSE","SSE"),
    ("S","S"),
    ("SSW","SSW"),
    ("SW","SW"),
    ("WSW","WSW"),
    ("W","W"),
    ("WNW","WNW"),
    ("NW","NW"),
    ("NNW","NNW"),
)

luna = (
    ("Luna Llena","Luna Llena"),
    ("Cuarto Creciente","Cuarto Creciente"),
    ("Cuarto Menguante","Cuarto Menguante"),
    ("Luna Nueva","Luna Nueva"),
   
)

mar = (
    ("TQ","TQ"),
    ("PO","PO"),
    ("O","O"),
    ("MRJ","MRJ"),
    ("FMRJ","FMRJ"),
)


class Pronostico(models.Model):
    fecha = models.DateField("Fecha", auto_now=False, auto_now_add=False)
    provincia = models.ForeignKey(Provincia, verbose_name="Provincia", on_delete=models.CASCADE)
    n_temp_min = models.IntegerField("Mañana (Mín)")
    n_temp_max = models.IntegerField("Mañana (Máx)")
    n_temp_tarde_min = models.IntegerField("Tarde (Mín)")
    n_temp_tarde_max = models.IntegerField("Tarde (Máx)")
    n_temp_noche_min = models.IntegerField("Noche (Mín)")
    n_temp_noche_max = models.IntegerField("Noche (Máx)")
    
    i_temp_min = models.IntegerField("Mañana (Mín)")
    i_temp_max = models.IntegerField("Mañana (Máx)")
    i_temp_tarde_min = models.IntegerField("Tarde (Mín)")
    i_temp_tarde_max = models.IntegerField("Tarde (Máx)")
    i_temp_noche_min = models.IntegerField("Noche (Mín)")
    i_temp_noche_max = models.IntegerField("Noche (Máx)")
    
    
    s_temp_min = models.IntegerField("Mañana (Mín)")
    s_temp_max = models.IntegerField("Mañana (Máx)")
    s_temp_tarde_min = models.IntegerField("Tarde (Mín)")
    s_temp_tarde_max = models.IntegerField("Tarde (Máx)")
    s_temp_noche_min = models.IntegerField("Noche (Mín)")
    s_temp_noche_max = models.IntegerField("Noche (Máx)")
    
    
    n_tiempo_tarde = models.CharField("Tarde",choices=tiempo, max_length=250)
    n_tiempo_manana = models.CharField("Mañana",choices=tiempo, max_length=250)
    n_tiempo_noche = models.CharField("Noche",choices=tiempo, max_length=250)
    i_tiempo_tarde = models.CharField("Tarde",choices=tiempo, max_length=250)
    i_tiempo_manana = models.CharField("Mañana",choices=tiempo, max_length=250)
    i_tiempo_noche = models.CharField("Noche",choices=tiempo, max_length=250)
    s_tiempo_tarde = models.CharField("Tarde",choices=tiempo, max_length=250)
    s_tiempo_manana = models.CharField("Mañana",choices=tiempo, max_length=250)
    s_tiempo_noche = models.CharField("Noche",choices=tiempo, max_length=250)
    n_viento_dir_tarde = models.CharField("Tarde",choices=viento, max_length=250 , default="VRB")
    n_viento_dir_manana = models.CharField("Mañana",choices=viento, max_length=250 , default="VRB")
    n_viento_dir_noche = models.CharField("Noche",choices=viento, max_length=250 , default="VRB")
    i_viento_dir_tarde = models.CharField("Tarde",choices=viento, max_length=250 , default="VRB")
    i_viento_dir_manana = models.CharField("Mañana",choices=viento, max_length=250 , default="VRB")
    i_viento_dir_noche = models.CharField("Noche",choices=viento, max_length=250 , default="VRB")
    s_viento_dir_tarde = models.CharField("Tarde",choices=viento, max_length=250 , default="VRB")
    s_viento_dir_manana = models.CharField("Mañana",choices=viento, max_length=250 , default="VRB")
    s_viento_dir_noche = models.CharField("Noche",choices=viento, max_length=250 , default="VRB")
    n_viento_vel_tarde = models.CharField("Tarde", max_length=100 , default="VRB")
    n_viento_vel_manana = models.CharField("Mañana",max_length=100, default="VRB")
    n_viento_vel_noche = models.CharField("Noche",max_length=100, default="VRB" )
    i_viento_vel_tarde = models.CharField("Tarde",max_length=100, default="VRB")
    i_viento_vel_manana = models.CharField("Mañana",max_length=100, default="VRB")
    i_viento_vel_noche = models.CharField("Noche",max_length=100, default="VRB" )
    s_viento_vel_tarde = models.CharField("Tarde",max_length=100, default="VRB" )
    s_viento_vel_manana = models.CharField("Mañana",max_length=100, default="VRB")
    s_viento_vel_noche = models.CharField("Noche",max_length=100, default="VRB")

    d1_fecha = models.DateField("Fecha", auto_now=False, auto_now_add=False)
    d1_min = models.IntegerField("Mínima")
    d1_max = models.IntegerField("Máxima")
    d1_tiempo = models.CharField("Tiempo",choices=tiempo , max_length=250)

    d2_fecha = models.DateField("Fecha", auto_now=False, auto_now_add=False)
    d2_min = models.IntegerField("Mínima")
    d2_max = models.IntegerField("Máxima")
    d2_tiempo = models.CharField("Tiempo",choices=tiempo, max_length=250)

    d3_fecha = models.DateField("Fecha", auto_now=False, auto_now_add=False)
    d3_min = models.IntegerField("Mínima")
    d3_max = models.IntegerField("Máxima")
    d3_tiempo = models.CharField("Tiempo",choices=tiempo, max_length=250)

    fl_actual = models.CharField("Actual",choices=luna, max_length=250)
    fl_prox = models.CharField("Próxima",choices=luna, max_length=250)
    fl_fecha = models.DateField("Fecha")

    ss_actual = models.CharField("Actual", max_length=250)
    ss_prox = models.CharField("Próxima",max_length=50 ,blank=True,null=True)
    ss_fecha = models.DateField("Fecha",blank=True, null=True,auto_now=False, auto_now_add=False)

    ps_actual = models.CharField("Actual", max_length=250)
    ps_prox = models.CharField("Próxima",max_length=50 ,blank=True,null=True)
    ps_fecha = models.DateField("Fecha",blank=True, null=True,auto_now=False, auto_now_add=False)

    uv_actual = models.IntegerField("Actual", default=1 ,validators=[MinValueValidator(1), MaxValueValidator(10)])
    uv_prox = models.IntegerField("Próxima",default=1 ,validators=[MinValueValidator(1), MaxValueValidator(10)] ,blank=True,null=True)
    uv_fecha = models.DateField("Fecha",blank=True, null=True,auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = 'Pronostico'
        verbose_name_plural = 'Pronosticos'

    def __str__(self):
        return f'Pronostico - {self.fecha}'


