from cProfile import label
from logging import warning
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import *
from .code_descriptions import *

import numpy as np
import re
import datetime, statistics, calendar


"""
Estas vistas se usan para listar(ListView), crear(CreateView), actualizar(UpdateView),
eliminar(DeleteView) sea cual sea el modelo al que ahcen reperencia

LoginRequiredMixin -> Indica que esa vista requuire estar registrado para cceder a ella

"""

# Vista que interpreta los synosp
class Parser(LoginRequiredMixin, View):
    """Vista que interpreta los synops"""

    def get(self, request):

        return render(
            request, "tiempo/synop.html", context={"segment": "suynop_parser"}
        )

    def post(self, request):
        context = {}
        msg = ""
        msge = "Asegúrese de que haya introducido un formato de synop válido."
        warnings = []
        codigo = 1
        synops_obje = []
        ESTACION = get_stations()
        try:
            # elimino lso espacios enter y otros caracteres de mas
            synop = request.POST.get("codigo_synom")
            synop = str(synop).replace("\r\n", " ")
            synop = synop.replace("\r", " ")
            synop = synop.replace("\n", " ")
            synop = synop.replace("\t", " ")

            elements = synop.split("=")
            for element in elements:
                if element.lower().count("aaxx") > 1:
                    context["msg"] = {
                        "type": "error",
                        "title": "Error",
                        "msg": f"Asegurese de que todos los códigos teminen en el singno =.",
                    }
                    context["segment"] = "suynop_parser"
                    return render(request, "tiempo/synop.html", context=context)

                obj = Synop()
                obj.synop_code = element
                fenomenos_especiales = []

                synop = str(element).split(" ")

                pos = 1
                etapa = 0
                for val in synop:
                    warning = False

                    # a continuacion se determina cual es el valor que se esta procesando y se almacena en la variable respectiva
                    value = re.sub(r"[^a-zA-Z0-9]", "/", val)

                    if len(value) <= 1:
                        continue

                    if value == "222":
                        etapa = 2
                        continue
                    if value == "333":
                        etapa = 3
                        continue
                    if value == "444":
                        etapa = 4
                        continue
                    if value == "555":
                        etapa = 5
                        continue

                    if etapa == 0:
                        if pos == 1:
                            obj.tipo_synop = CODIGO_TIPO_ESTACION[str(value).upper()]
                            warning = True

                        elif pos == 2:
                            obj.fecha = datetime.datetime(
                                currentDate.year,
                                currentDate.month,
                                int(value[0:2]),
                                int(value[2:4]),
                                0,
                                0,
                            )
                            obj.hora = int(value[2:4])
                            obj.indicador_viento_Iw = indicador_del_viento[value[4]]
                            warning = True
                            etapa = 1

                    if etapa == 1:
                        if pos == 3:
                            estacion = Estacion.objects.filter(code=value).first()
                            obj.estacion = estacion

                            warning = True

                        elif pos == 4:
                            obj.var_Iy = ind_inclusio_omision_precipitacion[value[0]]
                            obj.var_Ix = ind_operacion_tiempo_presente_pasado[value[1]]
                            obj.var_H = altura[value[2]]
                            obj.var_VV = calc_visivilidad(value[3:5])
                            warning = True

                        elif pos == 5:
                            warning = True
                            obj.var_N = total_cielo_nublado[value[0]]
                            if value[1:3] != "//":
                                obj.var_dd = direccion[value[1:3]]

                            if value[3:5] != "//":
                                obj.var_ff = value[3:5]
                            if value[1:3] != "//":
                                obj.var_direccion = calc_dir_vient(int(value[1:3]) * 10)

                        if value[0] == "1" and pos > 5:
                            if value[2:5] != "///":
                                obj.vat_TTT = (
                                    float(value[2:5]) / 10
                                    if value[1] == "0"
                                    else float(value[2:5]) / 10 * -1
                                )
                            warning = True
                        elif value[0] == "2" and pos > 5:
                            warning = True
                            if value[1] == "9":
                                obj.var_UUU = int(value[2:5])

                            else:
                                if value[2:5] != "///":
                                    obj.var_TTT_rocio = (
                                        float(value[2:5]) / 10
                                        if value[1] == "0"
                                        else float(value[2:5]) / 10 * -1
                                    )

                        elif value[0] == "3" and pos > 5:
                            if value[1:5] != "////" and value[2:5] != "///":
                                if value[1] == "0":
                                    obj.var_PPPP = float(value[1:5]) / 10 + 1000
                                else:
                                    obj.var_PPPP = float(value[1:5]) / 10
                            warning = True
                        elif value[0] == "4" and pos > 5:
                            if value[1:5] != "////" and value[2:5] != "///":
                                if value[1] == "0":
                                    obj.var_PPPP_mar = float(value[1:5]) / 10 + 1000
                                else:
                                    obj.var_PPPP = float(value[1:5]) / 10
                            warning = True
                        elif value[0] == "5" and pos > 5:
                            warning = True
                            obj.var_a = caracter_tendencia_barica[value[1]]
                            if value[2:5] != "///":
                                obj.var_ppp = float(value[2:5]) / 10

                        elif value[0] == "6" and pos > 5:
                            # en caso de que sea 990 es (inapreciable (trazas, no medible))
                            obj.var_RRR = calc_RRR(float(value[1:4]))
                            obj.var_Tr = tiempo[value[4]]
                            warning = True
                        elif value[0] == "7" and pos > 5:
                            obj.var_ww_presente = tiempo_presente[value[1:3]]
                            obj.var_WW_pasado = tiempo_pasado[value[3]]
                            warning = True
                        elif value[0] == "8" and pos > 5:
                            obj.var_CCC = calc_NCCC(value[1:5])
                            warning = True
                        elif value[0] == "9" and pos > 5:
                            obj.var_GGgg = calc_GGgg(value[1:5])
                            warning = True

                    elif etapa == 3:
                        if value[0] == "0":
                            warning = True
                            obj.var_Cs = tropicos[value[1]]
                            obj.var_Dl = direccion_nuves[value[2]]
                            obj.var_Dm = direccion_nuves[value[3]]
                            obj.var_Dh = direccion_nuves[value[4]]

                        elif value[0] == "1":
                            if value[2:5] != "///":
                                obj.var_TTT_maxima = (
                                    float(value[2:5]) / 10
                                    if value[1] == "0"
                                    else float(value[2:5]) / 10 * -1
                                )
                            warning = True
                        elif value[0] == "2":
                            if value[2:5] != "///":
                                obj.var_TTT_minima = (
                                    float(value[2:5]) / 10
                                    if value[1] == "0"
                                    else float(value[2:5]) / 10 * -1
                                )
                            warning = True
                        elif value[0] == "3":
                            obj.var_E = ESTT_GROUND_CONDITIONS_CODE[value[1]]
                            warning = True
                            if value[2:5] != "///":
                                obj.var_TT_suelo = (
                                    float(value[3:5])
                                    if value[2] == "0"
                                    else float(value[3:5]) * -1
                                )

                        elif value[0] == "4":
                            obj.var_E_hielo = medida_cubierta_nieve_o_hielo[value[1]]
                            if value[2:5] != "///":
                                obj.var_sss = calc_sss(value[2:5])
                            warning = True

                        elif value[0] == "5":
                            warning = True
                            if value[1] == "4":
                                obj.var_g0 = tiempo_cambio_temperatura[value[2]]
                                obj.var_dT = (
                                    cambio_temperatura[value[4]]
                                    if value[3] == "0"
                                    else f"-{cambio_temperatura[value[4]]}"
                                )

                            elif value[1] == "5":
                                if value[2:5] != "///":
                                    obj.var_SSS_insolacion = float(value[2:5]) / 10
                            elif value[1] == "6":
                                obj.var_Dl = direccion_nuves[value[2]]
                                obj.var_Dm = direccion_nuves[value[3]]
                                obj.var_Dh = direccion_nuves[value[4]]

                            elif value[1] == "7":
                                obj.var_C_genero = CLOUD_TYPE_CODE[value[2]]
                                obj.var_D = direccion_nuves[value[3]]
                                obj.var_C_angulo = angulo_elevacion[value[4]]

                            elif value[1] == "8":
                                if value[2:5] != "///":
                                    obj.var_PPP_presion = float(value[2:5])

                            elif value[1] == "9":
                                if value[2:5] != "///":
                                    obj.var_PPP_presion = float(value[2:5]) * -1
                            else:
                                if value[1:4] != "///" and value[2:5] != "///":
                                    obj.var_EEE_evapo = float(value[1:4]) / 10
                                    obj.var_iE = instrumento_evaporacion[value[4]]
                        elif value[0] == "6":
                            if value[1:4] != "///":
                                obj.var_RRR_presipitacion = calc_RRR(float(value[1:4]))
                            warning = True
                        elif value[0] == "7" and value[1:5] != "////":
                            obj.var_RRRR = float(value[1:5]) / 10
                            warning = True
                        elif value[0] == "8":
                            obj.var_N_nubes = total_cielo_nublado[value[1]]
                            obj.var_C_nube = CLOUD_TYPE_CODE[value[2]]
                            if value[3:5] != "//":
                                obj.var_hhh = calc_hh(value[3:5])
                            warning = True
                        elif value[0] == "9":
                            fenomenos_especiales.append(value)
                            warning = True

                    elif etapa == 5:
                        if value[0] == "1":
                            warning = True
                            if value[1:5] != "////":
                                if value[1] == "0":
                                    obj.var_PhPh = float(value[1:5]) / 10 + 1000
                                else:
                                    obj.var_PhPh = float(value[1:5]) / 10
                        elif value[0] == "2":
                            warning = True
                            if value[1:5] == "9999":
                                obj.var_CCCC = "Si hay cenizas volcánicas"

                        elif value[0] == "3" and value != "31///":
                            warning = True
                            obj.var_FFFF = float(value[1:5]) / 100
                        elif value[0] == "4":
                            warning = True
                            if value[1:5] != "////" and value[2:5] != "///":
                                obj.var_EEEE = float(value[1:5]) / 10

                        elif value[0] == "5":
                            warning = True
                            if value[1:5] != "////" and value[1] != "5":
                                obj.var_dxdx = value[1:3]
                                obj.var_fxfx = value[3:5]
                            elif value[1] == "5":
                                obj.var_fxfx = value[2:5]
                        elif value[0] == "6":
                            warning = True
                            if value[1:4] != "///":
                                if int(value[1]) < 4 and int(value[1]) > 8:
                                    obj.var_HeHeHe = f"{value[1:3]}:{int(value[3])*6}"
                                    if value[4] != "/":
                                        if value[4] == "1":
                                            obj.var_Iv = "anemógrafo"
                                        elif value[4] == "2":
                                            obj.var_Iv = "anemómetro"
                                elif value[1] == "4":
                                    obj.var_HHH_max = f"{value[2:4]}:{int(value[4])*6}"
                                elif value[1] == "5":
                                    obj.var_HHH_min = f"{value[2:4]}:{int(value[4])*6}"
                                elif value[1] == "6":
                                    obj.var_TTT_pos = float(value[2:5]) / 10
                                elif value[1] == "7":
                                    obj.var_HHH_neg = float(value[2:5]) / 10
                        elif value[0] == "7":
                            warning = True
                            aux = ""
                            if value[1:5] != "////":
                                if value[1] != "4" and value[1] != "7":
                                    aux = value
                                    obj.var_dd_ff = (
                                        f"{direccion[value[1:3]]} - {value[3:5]}kn"
                                    )
                                elif value[1] == "4":
                                    obj.var_HHH_rafaga = (
                                        f"{value[2:4]}:{int(value[4])*6}"
                                    )
                                elif value[1] == "7":
                                    obj.var_dd_ff = (
                                        f"{direccion[aux[1:3]]} - {value[2:5]}kn"
                                    )
                        elif value[0] == "8":
                            warning = True
                            if value[1:5] != "////":
                                max = "100" if value[1:3] == "00" else value[1:3]
                                min = "100" if value[3:5] == "00" else value[3:5]
                                obj.var_HmHmHnHn = f"Max:{max} % - Min:{min} %"
                        elif value[0] == "9":
                            warning = True
                            if value[1:5] != "////" and value[1:4] != "9///0":
                                obj.var_RRR_semana = float(value[1:5]) / 10

                    if warning == False:
                        warnings.append(
                            f"Código {codigo} - sección {etapa} - valor {value}"
                        )
                    msg = f"Código {codigo} - sección {etapa} - valor {value}"
                    pos = pos + 1
                if len(obj.synop_code) > 5:
                    obj.save()
                    synops_obje.append(obj)

                    for fenomeno in fenomenos_especiales:
                        fenome = create_9SSss(obj, fenomeno)
                        fenome.save()

                    codigo = codigo + 1
            if len(warnings) >= 1:
                x = ""
                for warnin in warnings:
                    x = x + f"{warnin},"
                context["msg"] = {
                    "type": "warning",
                    "title": "Advertencia",
                    "msg": f"El código synop se interpretó pero no en su totalidad. Faltó por desconocer su codificación: { x }",
                }
            else:
                context["msg"] = {
                    "type": "success",
                    "title": "Correcto",
                    "msg": "El código synop se interpretó correctamente.",
                }

            context["segment"] = "suynop_parser"
            return render(request, "tiempo/synop.html", context=context)
        except Exception as e:
            context["msg"] = {
                "type": "error",
                "title": "Error",
                "msg": f"{msge} Codigo {codigo} - sección {etapa} - valor: {value}, no es correcto.",
            }
            context["segment"] = "suynop_parser"
            for val in synops_obje:
                record = Synop.objects.get(id=val.id)
                record.delete()
            print(e)

            return render(request, "tiempo/synop.html", context=context)


class SynopListView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context["segment"] = "gestionar_synop"
        context["synops"] = (
            Synop.objects.all().order_by("-id").select_related("estacion")
        )
        context["estaciones"] = Estacion.objects.all()
        return render(request, "tiempo/synop_list.html", context=context)

    def post(self, request):
        context = {}

        estacion_code = request.POST.get("estaciones")

        context["segment"] = "gestionar_synop"
        fecha_inicio = request.POST.get("fecha_inicio")  # .strftime("%Y %M %d")
        fecha_fin = request.POST.get("fecha_fin")  # .strftime("%Y %M %d ")
        if fecha_fin < fecha_inicio:
            context["msg"] = "La fecha final tiene que ser mayor o igual a la inicial"
            context["synops"] = Synop.objects.all().order_by("-id").values()
            return render(request, "tiempo/synop_list.html", context=context)

        station = Estacion.objects.filter(code=estacion_code).first()

        context["synops"] = Synop.objects.filter(
            estacion=station, fecha__gte=fecha_inicio, fecha__lte=fecha_fin
        )
        context["estaciones"] = Estacion.objects.all()
        return render(request, "tiempo/synop_list.html", context=context)


class SynopDeleteView(LoginRequiredMixin, DeleteView):
    model = Synop
    fields = "__all__"
    success_url = reverse_lazy("synop_list")
    template_name = "tiempo/synop_delete.html"


class SynopUpdateView(LoginRequiredMixin, UpdateView):
    model = Synop
    fields = "__all__"
    success_url = reverse_lazy("synop_list")
    template_name = "tiempo/synop_update.html"


class SynopDetailView(LoginRequiredMixin, DetailView):
    model = Synop
    fields = "__all__"
    template_name = "tiempo/synop_detail.html"


class DatosAdinocialesListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["segment"] = "gestionar_synop"
        code = Synop.objects.get(id=kwargs["id"])
        context["datos_adinociales"] = Datos_adinociales.objects.filter(
            synop=code
        ).values()
        context["code"] = code
        context["synop_id"] = kwargs["id"]
        return render(request, "tiempo/datos_adinociales_list.html", context=context)


class DatosAdinocialesUpdateView(LoginRequiredMixin, UpdateView):
    model = Datos_adinociales
    fields = "__all__"
    template_name = "tiempo/datos_adinociales_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["synop_id"] = self.kwargs["id"]
        context["dato_id"] = self.kwargs["pk"]
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("datos_adinociales_list", kwargs={"id": self.kwargs["id"]})


class DatosAdinocialesDetailView(LoginRequiredMixin, DetailView):
    model = Datos_adinociales
    fields = "__all__"
    template_name = "tiempo/synop_detail.html"


class PronosticoListView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        context["segment"] = "gestionar_pronostico"
        context["pronosticos"] = (
            Pronostico.objects.all().order_by("-id").select_related("provincia")
        )
        return render(request, "tiempo/pronostico_list.html", context=context)


class PronosticoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pronostico
    fields = "__all__"
    success_url = reverse_lazy("pronostico_list")
    template_name = "tiempo/pronostico_delete.html"


class PronosticoDetailView(LoginRequiredMixin, DetailView):
    model = Pronostico
    fields = "__all__"
    template_name = "tiempo/pronostico_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "gestionar_pronostico"
        return context


class PronosticoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pronostico
    fields = "__all__"
    success_url = reverse_lazy("pronostico_list")
    template_name = "tiempo/pronostico_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "gestionar_pronostico"
        return context


class PronosticoCreateView(LoginRequiredMixin, CreateView):
    model = Pronostico
    fields = "__all__"
    success_url = reverse_lazy("pronostico_list")
    template_name = "tiempo/pronostico_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "gestionar_pronostico"
        return context


# Muestra lo que sale en la pagina de estadisticas
class Resumen(LoginRequiredMixin, View):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = calendar.monthrange(year, month)
    pronostico_general = []
    ESTACION = ""
    colores = [
        "#F66868",
        "#1020F5",
        "#68C7F6",
        "#68F68E",
        "#E8F668",
        "#0D0D0C",
        "#D610F5",
    ]
    datos_estaciones = {}

    def init(self):
        self.ESTACION = get_stations()
        self.datos_estaciones = {}
        i = 0
        for val in self.ESTACION:
            self.datos_estaciones[self.ESTACION[val]] = {
                "label": self.ESTACION[val],
                "code": val,
                "data": [],
                "color": generar_color(),
                "temp_date": [],
                "last_synops_day": {"day": "", "synops": []},
            }
            i = i + 1

        synops = (
            Synop.objects.filter(
                fecha__gte=f"{self.year}-{self.month}-{1}",
                fecha__lte=f"{self.year}-{self.month}-{self.day[1]}",
            )
            .order_by("-fecha", "-hora")
            .select_related("estacion")
        )
        self.pronostico_general = []
        for element in self.datos_estaciones:
            self.datos_estaciones[element]["data"] = [
                0 for _ in range(1, self.day[1] + 1)
            ]
            self.datos_estaciones[element]["temp_date"] = [
                [] for _ in range(1, self.day[1] + 1)
            ]
            self.datos_estaciones[element]["last_synops_day"]["day"] = ""
            self.datos_estaciones[element]["last_synops_day"]["synops"] = []

        for synop in synops:
            self.datos_estaciones["Varadero"]
            synop_date = int(str(synop.fecha).split("-")[2]) - 1
            if synop.vat_TTT != -999:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.vat_TTT)
            if (
                self.datos_estaciones[synop.estacion.name]["last_synops_day"]["day"]
                == ""
            ):
                self.datos_estaciones[synop.estacion.name]["last_synops_day"][
                    "day"
                ] = synop_date
                self.datos_estaciones[synop.estacion.name]["last_synops_day"][
                    "synops"
                ].append(synop)
            elif (
                self.datos_estaciones[synop.estacion.name]["last_synops_day"]["day"]
                == synop_date
            ):
                self.datos_estaciones[synop.estacion.name]["last_synops_day"][
                    "synops"
                ].append(synop)

        for elemen in self.datos_estaciones:
            valores = {}
            (
                temp,
                temp_min,
                temp_max,
                temp_rocio,
                min_12,
                humedad,
                viento,
                v_direccion,
                precipitacion,
                acumulada,
                ante_24,
                presion,
                mar,
                variasion,
            ) = ([], [], [], [], [], [], [], [], [], [], [], [], [], [])

            for synop in self.datos_estaciones[elemen]["last_synops_day"]["synops"]:
                valores["var_IIiii"] = synop.estacion.name
                valores["var_IIiii_code"] = synop.estacion.code
                valores["fecha"] = synop.fecha

                if synop.vat_TTT != -999.0:
                    temp.append(synop.vat_TTT)
                if synop.var_TTT_minima != -999:
                    temp_min.append(synop.var_TTT_minima)
                if synop.var_TTT_maxima != -999:
                    temp_max.append(synop.var_TTT_maxima)
                if synop.var_TTT_rocio != -999:
                    temp_rocio.append(synop.var_TTT_rocio)
                if synop.var_TT_suelo != -999:
                    min_12.append(synop.var_TT_suelo)
                if synop.var_UUU != -999:
                    humedad.append(synop.var_UUU)
                if synop.var_ff != "No proporcionado":
                    if "m/s" in synop.indicador_viento_Iw:
                        viento.append(round((float(synop.var_ff) * 1.943), 2))
                    else:
                        viento.append(float(synop.var_ff))
                if synop.var_dd != "No proporcionado":
                    if (
                        synop.var_dd != "Viento en calma"
                        and synop.var_dd != "Viento variable"
                    ):
                        v_direccion.append(synop.var_dd)

                if synop.var_RRR != -999 and synop.var_RRR != 990:
                    precipitacion.append(synop.var_RRR)
                if (
                    synop.var_RRR_presipitacion != -999
                    and synop.var_RRR_presipitacion != 990
                ):
                    acumulada.append(synop.var_RRR_presipitacion)
                if synop.var_RRRR != -999 and synop.var_RRR_presipitacion != 990:
                    ante_24.append(synop.var_RRRR)
                if synop.var_PPPP != -999:
                    presion.append(synop.var_PPPP)
                if synop.var_PPPP_mar != -999:
                    mar.append(synop.var_PPPP_mar)
                if synop.var_PPP_presion != -999:
                    variasion.append(synop.var_PPP_presion)

            valores["vat_TTT"] = (
                round(statistics.mean(temp), 2) if len(temp) > 0 else "--"
            )
            valores["var_TTT_maxima"] = mayor(temp_max) if len(temp_max) > 0 else "--"
            valores["var_TTT_minima"] = menor(temp_min) if len(temp_min) > 0 else "--"
            valores["var_TTT_rocio"] = (
                round(statistics.mean(temp_rocio), 2) if len(temp_rocio) > 0 else "--"
            )
            valores["var_TT_suelo"] = (
                round(statistics.mean(min_12), 2) if len(min_12) > 0 else "--"
            )
            valores["var_UUU"] = (
                round(statistics.mean(humedad), 2) if len(humedad) > 0 else "--"
            )

            valores["var_ff"] = (
                round(statistics.mean(viento), 2) if len(viento) > 0 else "--"
            )
            # valores['var_dd'] = round(statistics.mean(v_direccion),2) if len(v_direccion) > 0 else  '--'
            # valores['var_direccion'] =  calc_dir_vient(statistics.mean(v_direccion)) if len(v_direccion) > 0 else  '--'
            valores["var_ff_ms"] = (
                round(statistics.mean(viento) * 0.514, 2) if len(viento) > 0 else "--"
            )
            valores["var_ff_km"] = (
                round(statistics.mean(viento) * 1.85, 2) if len(viento) > 0 else "--"
            )
            valores["var_RRR"] = (
                round(statistics.mean(precipitacion), 2)
                if len(precipitacion) > 0
                else "--"
            )
            valores["var_RRR_presipitacion"] = (
                round(mayor(acumulada), 2) if len(acumulada) > 0 else "--"
            )
            valores["var_RRR_in"] = (
                round((statistics.mean(precipitacion) * 0.039), 2)
                if len(precipitacion) > 0
                else "--"
            )
            valores["var_RRRR"] = (
                round(statistics.mean(ante_24), 2) if len(ante_24) > 0 else "--"
            )
            valores["var_PPPP"] = (
                round(statistics.mean(presion), 2) if len(presion) > 0 else "--"
            )
            valores["var_PPPP_mar"] = (
                round(statistics.mean(mar), 2) if len(mar) > 0 else "--"
            )
            valores["var_PPP_presion"] = (
                round(statistics.mean(variasion), 2) if len(variasion) > 0 else "--"
            )

            self.pronostico_general.append(valores)

    def get(self, request):
        context = {}
        context["segment"] = "resumen-estadisticas"
        elements = []

        self.init()

        context["xvalues"] = {"values": [i for i in range(1, self.day[1] + 1)]}

        for value in self.datos_estaciones:
            for i in range(len(self.datos_estaciones[value]["data"])):
                list = self.datos_estaciones[value]["temp_date"][i]
                self.datos_estaciones[value]["data"][i] = (
                    round(statistics.mean(list), 2) if len(list) > 0 else 0
                )
            elements.append(
                {
                    "label": value,
                    "data": self.datos_estaciones[value]["data"],
                    "color": self.datos_estaciones[value]["color"],
                }
            )
        context["estaciones"] = self.ESTACION

        context["pronostico_general"] = self.pronostico_general
        context["elements"] = elements
        context["title"] = "Temperatura"

        return render(request, "tiempo/resumen.html", context=context)

    def post(self, request):
        context = {}
        context["estaciones"] = self.ESTACION

        self.init()
        context["pronostico_general"] = self.pronostico_general
        context["segment"] = "resumen-estadisticas"

        titulos = {
            "temp": "Temperatura",
            "temp_min": "Temperatura minima",
            "temp_max": "Temperatura maxima",
            "temp_rocio": "Temperatura rocio",
            "humedad": "Humedad",
            "presion": "Presión",
            "viento": "Velocidad Viento",
            "precip": "Precipitaciones",
        }
        variable = request.POST.get("variable")
        fecha_inicio = request.POST.get("fecha_inicio")  # .strftime("%Y %M %d")
        fecha_fin = request.POST.get("fecha_fin")  # .strftime("%Y %M %d ")

        if fecha_fin < fecha_inicio:
            context["msg"] = "La fecha final tiene que ser mayor a la inicial"
            return render(request, "tiempo/resumen.html", context=context)

        synops = Synop.objects.filter(
            fecha__gte=fecha_inicio, fecha__lte=fecha_fin
        ).select_related("estacion")
        year, month, day = (int(x) for x in fecha_inicio.split("-"))
        year_fin, month_fin, day_fin = (int(x) for x in fecha_fin.split("-"))

        for element in self.datos_estaciones:
            self.datos_estaciones[element]["data"] = [
                0 for _ in range(day, day_fin + 1)
            ]
            self.datos_estaciones[element]["temp_date"] = [
                [] for _ in range(day, day_fin + 1)
            ]

        xvalues = {"values": [i for i in range(day, day_fin + 1)]}

        for synop in synops:
            synop_date = int(str(synop.fecha).split("-")[2]) - day
            if variable == "temp" and synop.vat_TTT != -999.0:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.vat_TTT)
            elif variable == "temp_min" and synop.var_TTT_minima != -999:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.var_TTT_minima)
            elif variable == "temp_max" and synop.var_TTT_maxima != -999:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.var_TTT_maxima)
            elif variable == "temp_rocio" and synop.var_TTT_rocio != -999:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.var_TTT_rocio)
            elif variable == "humedad" and synop.var_UUU != -999:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.var_UUU)
            elif variable == "presion" and synop.var_PPPP != -999:
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.var_PPPP)
            elif variable == "viento" and synop.var_ff != "No proporcionado":
                if "m/s" in synop.indicador_viento_Iw:
                    self.datos_estaciones[synop.estacion.name]["temp_date"][
                        synop_date
                    ].append(round((float(synop.var_ff) * 1.943), 2))
                else:
                    self.datos_estaciones[synop.estacion.name]["temp_date"][
                        synop_date
                    ].append(float(synop.var_ff))
            elif (
                variable == "precip" and synop.var_RRR != -999 and synop.var_RRR != 990
            ):
                self.datos_estaciones[synop.estacion.name]["temp_date"][
                    synop_date
                ].append(synop.var_RRR)

        context["xvalues"] = xvalues

        elements = []

        for value in self.datos_estaciones:
            for i in range(len(self.datos_estaciones[value]["data"])):
                list = self.datos_estaciones[value]["temp_date"][i]
                self.datos_estaciones[value]["data"][i] = (
                    round(statistics.mean(list), 2) if len(list) > 0 else 0
                )
            elements.append(
                {
                    "label": value,
                    "data": self.datos_estaciones[value]["data"],
                    "color": self.datos_estaciones[value]["color"],
                }
            )

        context["elements"] = elements
        context["title"] = titulos[variable]

        return render(request, "tiempo/resumen.html", context=context)


# Muestra lo que sale en la pagina de utiles
class Utiles(LoginRequiredMixin, View):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = calendar.monthrange(year, month)
    datos_estaciones = []

    def init(self):
        self.datos_estaciones = []
        estaciones = get_stations()

        i = 0
        for element in estaciones:

            self.datos_estaciones.append(
                {
                    "label": estaciones[element],
                    "code": element,
                    "data": [],
                    "color": generar_color(),
                }
            )

            i = i + 1

    def get(self, request):
        context = {}
        context["segment"] = "resumen-utiles"
        fecha = f"{self.year}-{self.month}-{1}"
        self.init()
        synops = (
            Synop.objects.filter(fecha=fecha)
            .order_by("hora")
            .select_related("estacion")
        )
        xvalues = []
        for synop in synops:
            if synop.hora not in xvalues:
                xvalues.append(synop.hora)

        for element in self.datos_estaciones:
            for i in range(0, len(xvalues)):
                element["data"].append(0)
                for synop in synops:
                    if (
                        xvalues[i] == synop.hora
                        and element["code"] == synop.estacion.code
                        and synop.vat_TTT != -999
                    ):
                        element["data"][i] = synop.vat_TTT

        context["elements"] = self.datos_estaciones
        stations = []

        context["stations"] = Estacion.objects.all()

        context["title"] = "Temperatura"
        context["xvalues"] = xvalues
        context["fecha"] = fecha

        return render(request, "tiempo/utiles.html", context=context)

    def post(self, request):
        context = {}
        context["segment"] = "resumen-utiles"
        self.init()
        fecha = request.POST.get("fecha_inicio")
        variable = request.POST.get("variable")
        titulos = {
            "temp": "Temperatura",
            "temp_min": "Temperatura mínima",
            "temp_max": "Temperatura máxima",
            "temp_rocio": "Temperatura punto de rocío",
            "humedad": "Humedad",
            "presion": "Presión",
            "viento": "Velocidad Viento en kn",
            "precip": "Precipitaciones",
        }

        synops = (
            Synop.objects.filter(fecha=fecha)
            .order_by("hora")
            .select_related("estacion")
        )

        xvalues = []
        for synop in synops:
            if synop.hora not in xvalues:
                xvalues.append(synop.hora)

        for element in self.datos_estaciones:
            for i in range(0, len(xvalues)):
                element["data"].append(0)
                for synop in synops:
                    if (
                        xvalues[i] == synop.hora
                        and element["code"] == synop.estacion.code
                    ):

                        if variable == "temp" and synop.vat_TTT != -999:
                            element["data"][i] = synop.vat_TTT
                        elif variable == "temp_min" and synop.var_TTT_minima != -999:
                            element["data"][i] = synop.var_TTT_minima
                        elif variable == "temp_max" and synop.var_TTT_maxima != -999:
                            element["data"][i] = synop.var_TTT_maxima
                        elif variable == "temp_rocio" and synop.var_TTT_rocio != -999:
                            element["data"][i] = synop.var_TTT_rocio
                        elif variable == "humedad" and synop.var_UUU != -999:
                            element["data"][i] = synop.var_UUU
                        elif variable == "presion" and synop.var_PPPP != -999:
                            element["data"][i] = synop.var_PPPP
                        elif (
                            variable == "viento" and synop.var_ff != "No proporcionado"
                        ):
                            if "m/s" in synop.indicador_viento_Iw:
                                element["data"][i] = round(
                                    (float(synop.var_ff) * 1.943), 2
                                )
                            else:
                                element["data"][i] = float(synop.var_ff)
                        elif (
                            variable == "precip"
                            and synop.var_RRR != -999
                            and synop.var_RRR != 990
                        ):
                            element["data"][i] = synop.var_RRR

        context["elements"] = self.datos_estaciones
        context["title"] = titulos[variable]
        context["xvalues"] = xvalues
        context["fecha"] = fecha

        return render(request, "tiempo/utiles.html", context=context)


# muestra el ultimo pronostico creado
class LastPronostico(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        query = Pronostico.objects.filter().order_by("-fecha")
        if query:
            context["object"] = query[0]
        else:
            context["msg"] = "No se han encontrado pronosticos desea crear uno."
        context["segment"] = "dashboard"
        return render(request, "tiempo/last_pronostico.html", context=context)


class ProvinciaBase(LoginRequiredMixin, View):
    model = Provincia
    fields = "__all__"
    success_url = reverse_lazy("provincia_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "general-settings-provincia"
        return context


class ProvinciaListView(ProvinciaBase, ListView):
    template_name = "tiempo/provincia_list.html"


class ProvinciaDeleteView(ProvinciaBase, DeleteView):
    template_name = "tiempo/provincia_delete.html"


class ProvinciaUpdateView(ProvinciaBase, UpdateView):
    template_name = "tiempo/provincia_update.html"


class ProvinciaCreateView(ProvinciaBase, CreateView):
    template_name = "tiempo/provincia_create.html"


class EstacionBase(LoginRequiredMixin, View):
    model = Estacion
    fields = "__all__"
    success_url = reverse_lazy("estacion_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "general-settings-estacion"
        return context


class EstacionListView(EstacionBase, ListView):
    template_name = "tiempo/estacion_list.html"


class EstacionDeleteView(EstacionBase, DeleteView):
    template_name = "tiempo/estacion_delete.html"


class EstacionUpdateView(EstacionBase, UpdateView):
    template_name = "tiempo/estacion_update.html"


class EstacionCreateView(EstacionBase, CreateView):
    template_name = "tiempo/estacion_create.html"
