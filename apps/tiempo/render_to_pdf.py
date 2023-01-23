
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.urls import reverse_lazy
from django.shortcuts import render

import statistics

from apps.tiempo.models import *
from apps.tiempo.code_descriptions import *


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


data = {
    "company": "Dennnis Ivanov Company",
    "address": "123 Street name",
    "city": "Vancouver",
    "state": "WA",
    "zipcode": "98663",


    "phone": "555-555-2345",
    "email": "youremail@dennisivy.com",
    "website": "dennisivy.com",
}

# Opens up page as PDF

"""
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        object = Synop.objects.get(id=kwargs['pk'])
        data['object'] = object
        if 'm/s' in object.indicador_viento_Iw:
            data['viento_km'] = round((float(object.var_ff) * 3.6), 2)
            data['viento_m'] = round((float(object.var_ff)), 2)
            data['viento_kn'] = round((float(object.var_ff) * 1.943), 2)
            data['precip_in'] = round((float(object.var_RRR) * 0.039), 2)
        else:
            data['viento_km'] = round((float(object.var_ff) * 1.85), 2)
            data['viento_m'] = round((float(object.var_ff) * 0.514), 2)
            data['viento_kn'] = round((float(object.var_ff)), 2)
            data['precip_in'] = round((float(object.var_RRR) * 0.039), 2)
        pdf = render_to_pdf('tiempo/pdf/pdf_template.html', data)

        return HttpResponse(pdf, content_type='application/pdf')

"""
# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        object = Synop.objects.get(id=kwargs['pk'])
      
        data['object'] = object
        if 'm/s' in object.indicador_viento_Iw:
            data['viento_km'] = round((float(object.var_ff) * 3.6), 2)
            data['viento_m'] = round((float(object.var_ff)), 2)
            data['viento_kn'] = round((float(object.var_ff) * 1.943), 2)
            data['precip_in'] = round((float(object.var_RRR) * 0.039), 2)
        else:
            data['viento_km'] = round((float(object.var_ff) * 1.85), 2)
            data['viento_m'] = round((float(object.var_ff) * 0.514), 2)
            data['viento_kn'] = round((float(object.var_ff)), 2)
            data['precip_in'] = round((float(object.var_RRR) * 0.039), 2)
        pdf = render_to_pdf('tiempo/pdf/pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'Synop de {object.estacion.name} fecha_{object.fecha} hora_{object.hora} UTC.pdf'
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


class GeneralViewPDF(View):

    def get(self, request, *args, **kwargs):
        estacion = request.GET.get('estcion_pdf')
        fecha = request.GET.get('fecha')
        object = {}
        object['var_IIiii_code'] = estacion
        object['fecha'] = fecha

        flag = False

        synops_day = Synop.objects.filter(
            var_IIiii_code=estacion, fecha=fecha).values()
        temp, temp_min, temp_max, temp_rocio, min_12, humedad, viento, v_direccion, precipitacion, acumulada, ante_24, presion, mar, variasion = [
        ], [], [], [], [], [], [], [], [], [], [], [], [], []

        for synop in synops_day:
            if flag == False:
                object['var_IIiii'] = synop['var_IIiii']
                flag = True

            if synop['vat_TTT'] != -999.0:
                temp.append(synop['vat_TTT'])
            if synop['var_TTT_minima'] != -999:
                temp_min.append(synop['var_TTT_minima'])
            if synop['var_TTT_maxima'] != -999:
                temp_max.append(synop['var_TTT_maxima'])
            if synop['var_TTT_rocio'] != -999:
                temp_rocio.append(synop['var_TTT_rocio'])
            if synop['var_TT_suelo'] != -999:
                min_12.append(synop['var_TT_suelo'])
            if synop['var_UUU'] != -999:
                humedad.append(synop['var_UUU'])
            if synop['var_ff'] != "No proporcionado":
                if 'm/s' in synop['indicador_viento_Iw']:
                    viento.append(round((float(synop['var_ff']) * 1.943), 2))
                else:
                    viento.append(float(synop['var_ff']))
            if synop['var_dd'] != "No proporcionado":
                if synop['var_dd'] != 'Viento en calma' and synop['var_dd'] != 'Viento variable':
                    v_direccion.append(float(synop['var_dd']))
            if synop['var_RRR'] != -999:
                precipitacion.append(synop['var_RRR'])
            if synop['var_RRR_presipitacion'] != -999:
                acumulada.append(synop['var_RRR_presipitacion'])
            if synop['var_RRRR'] != -999:
                ante_24.append(synop['var_RRRR'])
            if synop['var_PPPP'] != -999:
                presion.append(synop['var_PPPP'])
            if synop['var_PPPP_mar'] != -999:
                mar.append(synop['var_PPPP_mar'])
            if synop['var_PPP_presion'] != -999:
                variasion.append(synop['var_PPP_presion'])

        object['vat_TTT'] = statistics.mean(temp) if len(temp) > 0 else '--'
        object['var_TTT_maxima'] = mayor(temp_max) if len(temp) > 0 else '--'
        object['var_TTT_minima'] = menor(temp_min) if len(temp) > 0 else '--'
        object['var_TTT_rocio'] = statistics.mean(temp_rocio) if len(temp_rocio) > 0 else '--'
        object['var_TT_suelo'] = statistics.mean(min_12) if len(min_12) > 0 else '--'
        object['var_UUU'] = statistics.mean(humedad) if len(humedad) > 0 else '--'

        object['var_ff'] = round(statistics.mean(viento), 2) if len(viento) > 0 else '--'
        object['var_dd'] = round(statistics.mean(v_direccion), 2) if len(v_direccion) > 0 else '--'
        object['var_direccion'] = calc_dir_vient(statistics.mean(v_direccion)) if len(v_direccion) > 0 else '--'
        object['var_ff_ms'] = round(statistics.mean(viento) * 0.514, 2) if len(viento) > 0 else '--'
        object['var_ff_km'] = round(statistics.mean(viento) * 1.85, 2) if len(viento) > 0 else '--'
        object['var_RRR'] = statistics.mean(precipitacion) if len(precipitacion) > 0 else '--'
        object['var_RRR_presipitacion'] = statistics.mean(acumulada) if len(acumulada) > 0 else '--'
        object['var_RRR_in'] = round((statistics.mean(precipitacion)*0.039), 2) if len(precipitacion) > 0 else '--'
        object['var_RRRR'] = statistics.mean(ante_24) if len(ante_24) > 0 else '--'
        object['var_PPPP'] = statistics.mean(presion) if len(presion) > 0 else '--'
        object['var_PPPP_mar'] = statistics.mean(mar) if len(mar) > 0 else '--'
        object['var_PPP_presion'] = statistics.mean(variasion) if len(variasion) > 0 else '--'

        data['object'] = object
        pdf = render_to_pdf('tiempo/pdf_template.html', data)

        return HttpResponse(pdf, content_type='application/pdf')


class ReporteDiario(View):
    def get(self, request):
        return render(request, 'tiempo/utiles.html', context={})

    def post(self, request):
        estacion = request.POST.get('estaciones_pdf')
        fecha = request.POST.get('fecha_reporte')
        object = {}
        object['var_IIiii_code'] = estacion
        
        object['fecha'] = fecha

        flag = False
        station = Estacion.objects.filter(code = estacion).first()
        synops_day = Synop.objects.filter(estacion = station, fecha=fecha).select_related('estacion')
        temp, temp_min, temp_max, temp_rocio, min_12, humedad, viento, v_direccion, precipitacion, acumulada, ante_24, presion, mar, variasion = [
        ], [], [], [], [], [], [], [], [], [], [], [], [], []

        for synop in synops_day:
            if flag == False:
                object['var_IIiii'] = synop.estacion.name
                flag = True

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
                if 'm/s' in synop.indicador_viento_Iw:
                    viento.append(
                        round((float(synop.var_ff) * 1.943), 2))
                else:
                    viento.append(float(synop.var_ff))
            if synop.var_dd != "No proporcionado":
                if synop.var_dd != 'Viento en calma' and synop.var_dd != 'Viento variable':
                    v_direccion.append(synop.var_dd)
            if synop.var_RRR != -999:
                precipitacion.append(synop.var_RRR)
            if synop.var_RRR_presipitacion != -999:
                acumulada.append(synop.var_RRR_presipitacion)
            if synop.var_RRRR != -999:
                ante_24.append(synop.var_RRRR)
            if synop.var_PPPP != -999:
                presion.append(synop.var_PPPP)
            if synop.var_PPPP_mar != -999:
                mar.append(synop.var_PPPP_mar)
            if synop.var_PPP_presion != -999:
                variasion.append(synop.var_PPP_presion)

        object['vat_TTT'] = round(statistics.mean(temp),2) if len(temp) > 0 else '--'
        
        object['var_TTT_maxima'] = mayor(temp_max) if len(temp_max) > 0 else '--'
        object['var_TTT_minima'] = menor(temp_min) if len(temp_min) > 0 else '--'
        object['var_TTT_rocio'] = round(statistics.mean(temp_rocio),2) if len(temp_rocio) > 0 else '--'
        object['var_TT_suelo'] = menor(min_12) if len(min_12) > 0 else '--'
        object['var_UUU'] = round(statistics.mean(humedad),2) if len(humedad) > 0 else '--'
        object['var_ff'] = round(statistics.mean(viento), 1) if len(viento) > 0 else '--'
        object['viento_km'] = round((statistics.mean(viento)*1.85), 1) if len(viento) > 0 else '--'
        object['viento_m'] = round((statistics.mean(viento) * 0.514), 1) if len(viento) > 0 else '--'
        #object['var_dd'] = round(statistics.mean(v_direccion), 2) if len(v_direccion) > 0 else '--'
        #object['var_direccion'] = calc_dir_vient(statistics.mean(v_direccion)) if len(v_direccion) > 0 else '--'
        object['var_RRR'] = round(statistics.mean(precipitacion),2) if len(precipitacion) > 0 else '--'
        object['var_RRR_presipitacion'] = round(statistics.mean(acumulada),2) if len(acumulada) > 0 else '--'
        object['var_RRR_in'] = round((statistics.mean(precipitacion)*0.039), 2) if len(precipitacion) > 0 else '--'
        object['var_RRRR'] = round(statistics.mean(ante_24),2) if len(ante_24) > 0 else '--'
        object['var_PPPP'] = round(statistics.mean(presion),2) if len(presion) > 0 else '--'
        object['var_PPPP_mar'] = round(statistics.mean(mar),2) if len(mar) > 0 else '--'
        object['var_PPP_presion'] = round(statistics.mean(variasion),2) if len(variasion) > 0 else '--'

        data['object'] = object
        pdf = render_to_pdf('tiempo/pdf/pdf_diario_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'Resumen diario-{estacion}-{fecha}.pdf'
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response

        


class GeneralDownloadPDF(View):
    def get(self, request, *args, **kwargs):
        object = Synop.objects.get(id=kwargs['pk'])
        data['object'] = object

        pdf = render_to_pdf('tiempo/pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f'{object.var_IIiii}-{object.fecha}-{object.hora}.pdf'
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
