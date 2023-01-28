from PIL import Image, ImageFont, ImageDraw
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView
from django.shortcuts import redirect, render

from core.settings import STATICFILES_DIRS, BASE_DIR
from apps.tiempo.models import Pronostico
import locale
import os
import base64


def url(file, option="fondo"):
    statics = STATICFILES_DIRS[0]
    root = statics + "/assets/img/pronostico/"
    if option == "luna":
        return f"{root}fase_luna/{file}.png"
    elif option == "dia":
        return f"{root}tiempo/{file}.png"
    elif option == "noche":
        return f"{root}tiempo/noche/{file}.png"
    return root + file


def format_12(value):
    val = value.split(":")
    if int(val[0]) > 12:
        return f"{int(val[0])-12}:{val[1]} PM"
    else:
        return f"{value} AM"


def parse(val):
    return str(val) + "°C"


def dia_semana(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return f"{dias[fecha.weekday()]} {fecha.day}"


def pronosticoImage(request, pk):

    with Image.open(url("fondo.png")).convert("RGBA") as fondo:

        pronostico = Pronostico.objects.get(id=pk)

        # Imagen luna
        fase_lunar = (
            Image.open(url(pronostico.fl_actual, "luna"))
            .resize((120, 120))
            .convert("RGBA")
        )

        # Imagen viento manin
        viento_main = Image.open(url("viento.png")).resize((80, 80)).convert("RGBA")
        viento = Image.open(url("viento.png")).resize((40, 40)).convert("RGBA")

        # Imagenes clima.convert("RGBA")
        tiempo_main_norte = (
            Image.open(url(pronostico.n_tiempo_manana, "dia"))
            .resize((110, 110))
            .convert("RGBA")
        )
        tiempo_tarde_norte = (
            Image.open(url(pronostico.n_tiempo_tarde, "dia"))
            .resize((60, 60))
            .convert("RGBA")
        )
        tiempo_noche_norte = (
            Image.open(url(pronostico.n_tiempo_noche, "noche"))
            .resize((60, 60))
            .convert("RGBA")
        )
        tiempo_main_centro = (
            Image.open(url(pronostico.i_tiempo_manana, "dia"))
            .resize((110, 110))
            .convert("RGBA")
        )
        tiempo_tarde_centro = (
            Image.open(url(pronostico.i_tiempo_tarde, "dia"))
            .resize((60, 60))
            .convert("RGBA")
        )
        tiempo_noche_centro = (
            Image.open(url(pronostico.i_tiempo_noche, "noche"))
            .resize((60, 60))
            .convert("RGBA")
        )
        tiempo_main_sur = (
            Image.open(url(pronostico.s_tiempo_manana, "dia"))
            .resize((110, 110))
            .convert("RGBA")
        )
        tiempo_tarde_sur = (
            Image.open(url(pronostico.s_tiempo_tarde, "dia"))
            .resize((60, 60))
            .convert("RGBA")
        )
        tiempo_noche_sur = (
            Image.open(url(pronostico.s_tiempo_noche, "noche"))
            .resize((60, 60))
            .convert("RGBA")
        )
        tiempo_d1 = (
            Image.open(url(pronostico.d1_tiempo, "dia"))
            .resize((50, 50))
            .convert("RGBA")
        )
        tiempo_d2 = (
            Image.open(url(pronostico.d2_tiempo, "dia"))
            .resize((50, 50))
            .convert("RGBA")
        )
        tiempo_d3 = (
            Image.open(url(pronostico.d3_tiempo, "dia"))
            .resize((50, 50))
            .convert("RGBA")
        )

        # Colores
        negro = (0, 0, 0)
        blanco = (255, 255, 255)
        rojo = (203, 1, 1)

        # Fuentes
        font = ImageFont.truetype("arial.ttf", 22)
        font_extras = ImageFont.truetype("arial.ttf", 25)
        viento_font = ImageFont.truetype("arial.ttf", 35)
        temp_main = ImageFont.truetype("arial.ttf", 50)
        temp = ImageFont.truetype("arial.ttf", 30)
        fecha_font = ImageFont.truetype("arial.ttf", 40)

        # annadiendo luna
        fondo.paste(fase_lunar, (90, 730), fase_lunar)

        # annadiendo viento
        fondo.paste(viento_main, (70, 400), viento_main)
        fondo.paste(viento_main, (400, 400), viento_main)
        fondo.paste(viento_main, (730, 400), viento_main)
        fondo.paste(viento, (60, 590), viento)
        fondo.paste(viento, (210, 590), viento)
        fondo.paste(viento, (400, 590), viento)
        fondo.paste(viento, (540, 590), viento)
        fondo.paste(viento, (730, 590), viento)
        fondo.paste(viento, (870, 590), viento)

        # annadiendo tiempo
        # norte
        fondo.paste(tiempo_main_norte, (210, 260), tiempo_main_norte)
        fondo.paste(tiempo_tarde_norte, (135, 500), tiempo_tarde_norte)
        fondo.paste(tiempo_noche_norte, (280, 500), tiempo_noche_norte)

        # centro
        fondo.paste(tiempo_main_centro, (540, 260), tiempo_main_centro)
        fondo.paste(tiempo_tarde_centro, (465, 500), tiempo_tarde_centro)
        fondo.paste(tiempo_noche_centro, (610, 500), tiempo_noche_centro)
        # sur
        fondo.paste(tiempo_main_sur, (870, 260), tiempo_main_sur)
        fondo.paste(tiempo_tarde_sur, (795, 500), tiempo_tarde_sur)
        fondo.paste(tiempo_noche_sur, (940, 500), tiempo_noche_sur)

        # d1,d2,d3
        fondo.paste(tiempo_d1, (630, 730), tiempo_d1)
        fondo.paste(tiempo_d2, (760, 730), tiempo_d2)
        fondo.paste(tiempo_d3, (900, 730), tiempo_d3)

        image_editable = ImageDraw.Draw(fondo)

        # norte main
        image_editable.text(
            (750, 30), pronostico.fecha.strftime("%d/%m/%Y"), negro, font=fecha_font
        )

        # Textos
        # norte main
        image_editable.text(
            (80, 260), parse(pronostico.n_temp_min), blanco, font=temp_main
        )
        image_editable.text(
            (80, 310), parse(pronostico.n_temp_max), rojo, font=temp_main
        )

        # norte tarde
        image_editable.text(
            (65, 500), parse(pronostico.n_temp_tarde_min), blanco, font=temp
        )
        image_editable.text(
            (65, 535), parse(pronostico.n_temp_tarde_max), rojo, font=temp
        )
        # norte noche
        image_editable.text(
            (205, 500), parse(pronostico.n_temp_noche_min), blanco, font=temp
        )
        image_editable.text(
            (205, 535), parse(pronostico.n_temp_noche_max), rojo, font=temp
        )

        # centr main
        image_editable.text(
            (410, 260), parse(pronostico.i_temp_min), blanco, font=temp_main
        )
        image_editable.text(
            (410, 310), parse(pronostico.i_temp_max), rojo, font=temp_main
        )

        # centro tarde
        image_editable.text(
            (395, 500), parse(pronostico.i_temp_tarde_min), blanco, font=temp
        )
        image_editable.text(
            (395, 535), parse(pronostico.i_temp_tarde_max), rojo, font=temp
        )
        # centro noche
        image_editable.text(
            (535, 500), parse(pronostico.i_temp_noche_min), blanco, font=temp
        )
        image_editable.text(
            (535, 535), parse(pronostico.i_temp_noche_max), rojo, font=temp
        )

        # sur main
        image_editable.text(
            (740, 260), parse(pronostico.s_temp_min), blanco, font=temp_main
        )
        image_editable.text(
            (740, 310), parse(pronostico.s_temp_max), rojo, font=temp_main
        )

        # centro tarde
        image_editable.text(
            (725, 500), parse(pronostico.s_temp_tarde_min), blanco, font=temp
        )
        image_editable.text(
            (725, 535), parse(pronostico.s_temp_tarde_max), rojo, font=temp
        )
        # centro noche
        image_editable.text(
            (865, 500), parse(pronostico.s_temp_noche_min), blanco, font=temp
        )
        image_editable.text(
            (865, 535), parse(pronostico.s_temp_noche_max), rojo, font=temp
        )

        # luna
        image_editable.text((70, 690), pronostico.fl_actual, negro, font=font)

        # viento norte
        if (
            pronostico.n_viento_dir_manana == "VRB"
            or pronostico.n_viento_vel_manana == "VRB"
        ):
            image_editable.text((170, 430), "Variable", blanco, font=viento_font)
        else:
            image_editable.text(
                (210, 400), pronostico.n_viento_dir_manana, blanco, font=viento_font
            )
            image_editable.text(
                (170, 440),
                (pronostico.n_viento_vel_manana + " km/h"),
                blanco,
                font=viento_font,
            )

        # viento norte tarde
        if (
            pronostico.n_viento_dir_tarde == "VRB"
            or pronostico.n_viento_vel_tarde == "VRB"
        ):
            image_editable.text((105, 600), "Variable", blanco, font=font)
        else:
            image_editable.text(
                (130, 590), pronostico.n_viento_dir_tarde, blanco, font=font
            )
            image_editable.text(
                (105, 610), (pronostico.n_viento_vel_tarde + " km/h"), blanco, font=font
            )

        # viento norte noche
        if (
            pronostico.n_viento_dir_noche == "VRB"
            or pronostico.n_viento_vel_noche == "VRB"
        ):
            image_editable.text((260, 600), "Variable", blanco, font=font)
        else:
            image_editable.text(
                (270, 590), pronostico.n_viento_dir_noche, blanco, font=font
            )
            image_editable.text(
                (260, 610), (pronostico.n_viento_vel_noche + " km/h"), blanco, font=font
            )

        # viento centro
        if (
            pronostico.i_viento_dir_manana == "VRB"
            or pronostico.i_viento_vel_manana == "VRB"
        ):
            image_editable.text((500, 430), "Variable", blanco, font=viento_font)
        else:
            image_editable.text(
                (520, 400), pronostico.i_viento_dir_manana, blanco, font=viento_font
            )
            image_editable.text(
                (500, 440),
                (pronostico.i_viento_vel_manana + " km/h"),
                blanco,
                font=viento_font,
            )

        # viento centro tarde
        if (
            pronostico.i_viento_dir_tarde == "VRB"
            or pronostico.i_viento_vel_tarde == "VRB"
        ):
            image_editable.text((445, 600), "Variable", blanco, font=font)
        else:
            image_editable.text(
                (460, 590), pronostico.i_viento_dir_tarde, blanco, font=font
            )
            image_editable.text(
                (450, 610), (pronostico.i_viento_vel_tarde + " km/h"), blanco, font=font
            )

        # viento centro noche
        if (
            pronostico.i_viento_dir_noche == "VRB"
            or pronostico.i_viento_vel_noche == "VRB"
        ):
            image_editable.text((585, 600), "Variable", blanco, font=font)
        else:
            image_editable.text(
                (600, 590), pronostico.i_viento_dir_noche, blanco, font=font
            )
            image_editable.text(
                (590, 610), (pronostico.i_viento_vel_noche + " km/h"), blanco, font=font
            )

        # viento sur
        if (
            pronostico.s_viento_dir_manana == "VRB"
            or pronostico.s_viento_vel_manana == "VRB"
        ):
            image_editable.text((830, 430), "Variable", blanco, font=viento_font)
        else:
            image_editable.text(
                (850, 400), pronostico.s_viento_dir_manana, blanco, font=viento_font
            )
            image_editable.text(
                (830, 440),
                (pronostico.s_viento_vel_manana + " km/h"),
                blanco,
                font=viento_font,
            )

        # viento sur tarde
        if (
            pronostico.s_viento_dir_tarde == "VRB"
            or pronostico.s_viento_vel_tarde == "VRB"
        ):
            image_editable.text((775, 600), "Variable", blanco, font=font)
        else:
            image_editable.text(
                (790, 590), pronostico.s_viento_dir_tarde, blanco, font=font
            )
            image_editable.text(
                (780, 610), (pronostico.s_viento_vel_tarde + " km/h"), blanco, font=font
            )

        # viento sur noche
        if (
            pronostico.s_viento_dir_noche == "VRB"
            or pronostico.s_viento_vel_noche == "VRB"
        ):
            image_editable.text((915, 600), "Variable", blanco, font=font)
        else:
            image_editable.text(
                (930, 590), pronostico.s_viento_dir_noche, blanco, font=font
            )
            image_editable.text(
                (920, 610), (pronostico.s_viento_vel_noche + " km/h"), blanco, font=font
            )

        # extras
        image_editable.text((310, 700), "Salida Sol:", negro, font=font_extras)
        image_editable.text(
            (440, 700), format_12(pronostico.ss_prox), negro, font=font_extras
        )

        image_editable.text((300, 750), "Puesta Sol:", negro, font=font_extras)
        image_editable.text(
            (440, 750), format_12(pronostico.ps_prox), negro, font=font_extras
        )

        image_editable.text((313, 800), "Índice UV:", negro, font=font_extras)
        image_editable.text(
            (440, 800), str(pronostico.uv_prox), negro, font=font_extras
        )

        # dia de la semana d1
        image_editable.text(
            (610, 690), dia_semana(pronostico.d1_fecha), negro, font=font
        )

        # temp d1
        image_editable.text((630, 790), parse(pronostico.d1_min), blanco, font=font)
        image_editable.text((630, 815), parse(pronostico.d1_max), rojo, font=font)

        # dia de la semana d2
        image_editable.text(
            (750, 690), dia_semana(pronostico.d2_fecha), negro, font=font
        )

        # temp d2
        image_editable.text((760, 790), parse(pronostico.d2_min), blanco, font=font)
        image_editable.text((760, 815), parse(pronostico.d2_max), rojo, font=font)

        # dia de la semana d3
        image_editable.text(
            (880, 690), dia_semana(pronostico.d3_fecha), negro, font=font
        )

        # temp d3
        image_editable.text((900, 790), parse(pronostico.d3_min), blanco, font=font)
        image_editable.text((900, 815), parse(pronostico.d3_max), rojo, font=font)

        # fondo.show()

        fondo.save(
            f"{os.getcwd()}/Pronosticos/Pronostico {pronostico.fecha}.png", "png"
        )
        # fondo.save(f"D:/Proyectos/Tiempo/Tiempo/Pronosticos/Pronostico {pronostico.fecha}.png",'png')

        with open(
            f"{os.getcwd()}/Pronosticos/Pronostico {pronostico.fecha}.png", "rb"
        ) as archivo_imagen:
            imagen = base64.b64encode(archivo_imagen.read()).decode("utf-8")

        context = {"imagen": imagen}

        return render(request, "tiempo/render_img.html", context)
