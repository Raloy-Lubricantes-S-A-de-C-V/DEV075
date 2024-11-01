# django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import the_applications.func as f
from django.contrib.auth.models import User
from django.db.models import Q
import datetime as dt
from django.db.models import Count

from the_applications.datasheet.forms import CreateDataList, CopyDataList, FusionDataList
from the_applications.datasheet.models import Header as Cab, DataSheet as List, TempNextCode as Next, RelParent as Parent
from the_applications.notify.models import TypeNotify, Notify
from django.http import HttpResponse, JsonResponse



class Principal(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        context2 = {
            'erros': []
        }
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        data = request.POST
        form = CreateDataList(data)
        if form.is_valid():
            btn = data['activebtn'][0]
            name = data['name']
            context2['active_btn'] = int(btn)
            context2['folio'] = str(name)
            form.save(user=request.user.id)
            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user = request.user,
                type = type_notify,
                name = "Nuevo Data List - {}".format(str(name)),
                description = """
                El usuario '{} {}'  ha generado un nuevo Data List con folio '{}'.
                Recuerde que ya puede ser utilizado para el proceso de Ruteo.
                """.format(request.user.first_name,request.user.last_name, str(name)),
                priority = 2,
                picture = 'notify/pictures/list.png'
            )
            new_notify.save()
        else:
            form = CreateDataList()
        print(data)
        context2['form'] = form
        context2['user'] = request.user
        return render(
            request,
            'datasheet/main.html',
            context2,
        )

    def get_context_data(self, **kwargs):
        context2 = super().get_context_data(**kwargs)
        ## ------
        users = User.objects.all().values()
        type_notify = TypeNotify.objects.all().filter(active=True).values()
        users_array = []
        type_array = []
        for user in users:
            item = {
                'id': user['id'],
                'username': user['username']
            }
            users_array.append(item)
        for type in type_notify:
            item = {
                'id': type['id'],
                'name': type['name']
            }
            type_array.append(item)
            type_array.append(item)
        ## ------
        today = dt.datetime.today()
        print(today)
        try:
            hid = Cab.objects.latest('id').id
            codeTxt = str(hid).zfill(6)
            codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
            print(codeHead)
        except Exception as e:
            code = 1
            codeTxt = str(code).zfill(6)
            codeHead = "DL-{}{}{}".format(str(today.year)[2:4],str(today.month),codeTxt)
            print(codeHead)
        form_create = CreateDataList({'name':codeHead, 'state':'LI'})
        form_copy = CopyDataList()
        form_fusion = FusionDataList()
        context2['context'] = {
            "users": users_array,
            "type_notify": type_array,
            "type_data":"ODOO",
            "form_create":form_create,
            "form_copy":form_copy,
            "form_fusion": form_fusion
        }

        return context2

class PostGetSelectFusion(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        body = Cab.objects.all().filter(active=True).values('id', 'name')
        response['data'] = [{'id':q['id'], 'name':q['name']} for q in body]
        print("*********************")
        return JsonResponse(response)

class PostGetSelectCopy(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        body = Cab.objects.all().filter(Q(state_copy='OR') | Q(state_copy='CP'), active=True).values('id', 'name')
        response['data'] = [{'id':q['id'], 'name':q['name']} for q in body]
        print("*********************")
        return JsonResponse(response)

class PostActiveDeactiveDataList(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        actionx = int(request.POST['action'])
        if actionx == 0:
            action = False
        else:
            action = True
        header_id = Cab.objects.get(pk=id)
        today = dt.datetime.today()
        header_id.write_uid = request.user.id
        header_id.write_date = today
        header_name = Cab.objects.get(pk=id).name
        header_state = Cab.objects.get(pk=id).state
        header_active = Cab.objects.get(pk=id).active
        response['data'] = header_name
        if (header_state == 'CL' or header_state == 'AP') and action == False:
            response["error"] = True
            response["msj"] = 'No se puede desactivar el DataList "<b>{}</b>". Ya se han procesado los datos.'.format(header_name)
        elif  action == header_active:
            response["error"] = True
            response["msj"] = 'El estado del DataList "<b>{}</b>" no ha cambiado'.format(header_name)
        elif (header_state != 'CL' and header_state != 'AP') and action != header_active:
            if action == False:
                header_id.active = False
                header_id.save()
                response["msj"] = 'Se ha archivado el DataList "<b>{}</b>". No podrá ser procesado por ningún escenario'.format(header_name)
            else:
                header_id.active = True
                header_id.save()
                response["msj"] = 'Se ha desarchivado el  DataList "<b>{}</b>". Ya puede ser procesado por algún escenario'.format(header_name)
        else:
            response["error"] = True
            response["msj"] = 'Error no conocido'
        print("*********************")
        return JsonResponse(response)

class PostDeleteDataList(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        print("*********************")
        id = int(request.POST['id'])
        print(id)
        # ---- Revisión de Parent
        rel = Parent.objects.filter(id_parent=id).values('id_son')
        if rel:
            header_state = Cab.objects.get(pk=id).state
            name = Cab.objects.get(pk=id).name
            print("continius rel")
            active_delete = True
            sons = []
            for r in rel:
                print(r['id_son'])
                son_state = Cab.objects.get(pk=r['id_son']).state
                son = Cab.objects.get(pk=r['id_son'])
                sons.append(son)
                print(son_state)
                if son_state != "LI":
                    active_delete = False
            for r in rel:
                print(r['id_son'])
                son_state = Cab.objects.get(pk=r['id_son']).state_fusion
                son = Cab.objects.get(pk=r['id_son'])
                sons.append(son)
                print(son_state)
                if son_state == "BF" and son_state == "FS":
                    active_delete = False
            if active_delete:
                if header_state == "LI":
                    names_son = ""
                    for ss in sons:
                        lines = List.objects.filter(header_id=ss.id).all()
                        names_son = "{}{}..".format(names_son,ss.name)
                        try:
                            for l in lines:
                                l.delete()
                            ss.delete()
                        except Exception as e:
                            response["error"] = True
                            response[
                                "msj"] = 'No se ha podido eliminar el DataList "<b>{}</b>". Ha ocurrido un error interno [{}].'.format(
                                name, e)
                            response['data'] = name
                    father = Cab.objects.get(pk=id)
                    father_id = Cab.objects.get(pk=id).id
                    lines = List.objects.filter(header_id=father_id).all()
                    try:
                        for l in lines:
                            l.delete()
                        father.delete()
                        print("%%%%%%%%%%%%%%%%%%%")
                        rel_parent = Parent.objects.filter(id_parent=father_id).all()
                        print(rel_parent)
                        for r in rel_parent:
                            r.delete()
                        print("%%%%%%%%%%%%%%%%%%%")
                        response["error"] = False
                        response["msj"] = 'Se ha eliminado el DataList "<b>{}</b> y sus hijos [{}]"'.format(name,names_son.strip(".."))
                        response['data'] = name
                    except Exception as e:
                        response["error"] = True
                        response[
                            "msj"] = 'No se ha podido eliminar el DataList "<b>{}</b>". Ha ocurrido un error interno [{}].'.format(
                            name, e)
                        response['data'] = name
                else:
                    response["error"] = True
                    response["msj"] = 'No se ha podido eliminar el DataList "<b>{}</b>", su estado es diferente a <i>"Libre"</i>.'.format(name)
                    response['data'] = name
            else:
                response["error"] = True
                response["msj"] = 'No se ha podido eliminar el DataList "<b>{}</b>", contiene copias en estado diferente a <i>"Libre"</i> o pertenece a un Fusión.'.format(name)
                response['data'] = name
        else:
            header_id = Cab.objects.get(pk=id)
            header_state = header_id.state
            name = Cab.objects.get(pk=id).name
            state_fusion = Cab.objects.get(pk=id).state_fusion
            print(state_fusion)
            if header_state == "LI":
                try:
                    if state_fusion == 'FS':
                        rel_parent = Parent.objects.filter(id_son=id).values()
                        today = dt.datetime.today()
                        for rp in rel_parent:
                            parent_fs = Cab.objects.get(pk=rp["id_parent"])
                            parent_fs.write_uid = request.user.id
                            parent_fs.write_date = today
                            parent_fs.state_fusion = "OR"
                            parent_fs.save()
                            rel_parentx = Parent.objects.filter(id_son=id,id_parent=rp["id_parent"],type='FU').all()
                            rel_parentx.delete()
                    elif state_fusion == 'BF':
                        response["error"] = True
                        response["msj"] = 'No se ha podido eliminar el DataList "<b>{}</b>". Existe una fusión.'.format(name)
                        response['data'] = name
                    else:
                        son_parent = Parent.objects.get(id_son=id).id_parent  # 2
                        parenti = Cab.objects.get(pk=son_parent)
                        rel_parent = Parent.objects.filter(id_parent=son_parent).values('id_son')
                        i = 0
                        for rp in rel_parent:
                            i = i + 1
                        if i == 1:
                            today = dt.datetime.today()
                            parenti.state_copy = 'OR'
                            parenti.write_uid = request.user.id
                            parenti.write_date = today
                            parenti.save()
                        son_id = Parent.objects.get(id_son=id)
                        son_id.delete()
                except:
                    pass
                header = Cab.objects.get(pk=id)
                lines = List.objects.filter(header_id=id).all()
                try:
                    for l in lines:
                        l.delete()
                    header.delete()
                    response["error"] = False
                    response["msj"] = 'Se ha eliminado el DataList "<b>{}</b>"'.format(name)
                    response['data'] = name
                except Exception as e:
                    response["error"] = True
                    response["msj"] = 'No se ha podido eliminar el DataList "<b>{}</b>". Ha ocurrido un error interno [{}].'.format(name,e)
                    response['data'] = name
            else:
                response["error"] = True
                response["msj"] = 'Es imposible eliminar un DataList en estado diferente a "<b>Libre</b>"'
                response['data'] = name
        print("*********************")
        return JsonResponse(response)


class PostGetLastCodeDataList(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        today = dt.datetime.today()
        print(today)
        try:
            hid = Cab.objects.latest('id').id
            codeTxt = str(hid).zfill(6)
            codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
            print(codeHead)
        except Exception as e:
            code = 1
            codeTxt = str(code).zfill(6)
            codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
            print(codeHead)
        response['data'] = {'name': codeHead}
        return JsonResponse(response)



class PostTotalLitroId(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        datos = List.objects.filter(header_id=id).values('spo_qty','product_vol')
        liters = 0.0
        for d in datos:
            liters = liters + (float(d['spo_qty']) * float(d['product_vol']))
        response['data'] = f.format_qty(d=round(liters,2),t="float")
        return JsonResponse(response)

class PostTotalLitroIdRef(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        ref = request.POST['ref']
        datos = List.objects.filter(header_id=id, ref=ref).values('spo_qty','product_vol')
        liters = 0.0
        for d in datos:
            liters = liters + (float(d['spo_qty']) * float(d['product_vol']))
        #315063.61
        #360,51,3,.,61
        response['data'] = f.format_qty(d=round(liters,2),t="float")
        return JsonResponse(response)


class PostTotaClienteId(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        datos = List.objects.filter(header_id=id).values('id_partner').distinct()
        c = 0
        for d in datos:
            c = c + 1
        response['data'] = f.format_qty(d=c, t="number")
        return JsonResponse(response)

class PostTotaClienteIdRef(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        ref = request.POST['ref']
        datos = List.objects.filter(header_id=id, ref=ref).values('id_partner').distinct()
        c = 0
        for d in datos:
            c = c + 1
        response['data'] = f.format_qty(d=c, t="number")
        return JsonResponse(response)

class PostTotaDeterminantesIdRef(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        ref = request.POST['ref']
        datos = List.objects.filter(header_id=id, ref=ref).values('delivery_id').distinct()
        c = 0
        for d in datos:
            c = c + 1
        response['data'] = f.format_qty(d=c, t="number")
        return JsonResponse(response)
class PostTotaProductosIdRef(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        ref = request.POST['ref']
        datos = List.objects.filter(header_id=id, ref=ref).values('id_prod').distinct()
        c = 0
        for d in datos:
            c = c + 1
        response['data'] = f.format_qty(d=c, t="number")
        return JsonResponse(response)

class PostTotaDeterminantesId(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['id'])
        datos = List.objects.filter(header_id=id).values('delivery_id').distinct()
        c = 0
        for d in datos:
            c = c + 1
        response['data'] = f.format_qty(d=c, t="number")
        return JsonResponse(response)

class PostFusionDataList(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        context2 = {
            'erros': []
        }
        response = {
            'data': [],
            'error': False, #---------------------------------- AQUI
            'msj': ''
        }
        id1 = int(request.POST['header_fusion_1'])
        id2 = int(request.POST['header_fusion_2'])
        if id1 == id2:
            context2['active_btn3'] = 1
            context2['folio'] = Cab.objects.get(pk=id1).name
            print(context2)
        else:
            print("$$$$$$$$$$$$$$$$$$")
            print(" --> POST ID1")
            print(" --> ", id1)
            print(" --> POST ID2")
            print(" --> ", id2)
            today = dt.datetime.today()
            print(" --> Get fecha")
            header_1 = Cab.objects.get(pk=id1)
            print(" --> Get cabs ID1")
            header_1.write_uid = request.user.id
            print(" --> Update cabs ID1 - write_uid")
            header_1.write_date = today
            print(" --> Update cabs ID1 - write_date")
            header_1.state_fusion = 'BF'
            print(" --> Update cabs ID1 - state_fusion")
            header_1_name = header_1.name
            print(" --> Get name cabs ID1")
            header_2 = Cab.objects.get(pk=id2)
            print(" --> Get cabs ID2")
            header_2.write_uid = request.user.id
            print(" --> Update cabs ID2 - write_uid")
            header_2.write_date = today
            print(" --> Update cabs ID2 - write_date")
            header_2.state_fusion = 'BF'
            print(" --> Update cabs ID2 - state_fusion")
            header_2_name = header_2.name
            print(" --> Get name cabs ID2")
            header_copy = Cab.objects.filter(pk=id1).values()
            print(" --> Premodificación de Header")
            # -----
            next_number = Next.objects.filter(key="next_header").values("value")
            all_next = []
            for nn in next_number:
                if len(nn['value']) > 1:
                    all_next.append(int(nn['value']))
            if len(all_next) > 0:
                last_id = 0
                for an in all_next:
                    if an > last_id:
                        last_id = an
                hid = last_id + 1
                codeTxt = str(hid).zfill(6)
                codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
            else:
                hid = Cab.objects.latest('id').id
                codeTxt = str(hid).zfill(6)
                codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
            next_number_crete = Next(key="next_header", value=int(hid))
            next_number_crete.save()
            print(" --> Get code")
            print(" --> ", codeHead)
            # -----
            for d in header_copy:
                copyh = Cab(
                    name=codeHead,
                    state="LI",
                    state_copy="OR",
                    state_fusion="FS",
                    create_uid=d["create_uid"],
                    write_uid=d["write_uid"]
                )
                copyh.save()
            print(" --> Creación de nuevo Header")
            print(" --> ", copyh.id)
            lines1 = List.objects.filter(header_id=id1).values()
            for l in lines1:
                line = List(
                    number=l["number"],
                    ide=l["ide"],
                    ref=l["ref"],
                    oc=l["oc"],
                    invoice=l["invoice"],
                    id_partner=l["id_partner"],
                    partner=l["partner"],
                    state=l["state"],
                    createdata_date=l["createdata_date"],
                    create_time=l["create_time"],
                    delivery_date=l["delivery_date"],
                    appointment_time=l["appointment_time"],
                    comment=l["comment"],
                    pieces_received=l["pieces_received"],
                    boxes_received=l["boxes_received"],
                    pallets_received=l["pallets_received"],
                    id_prod=l["id_prod"],
                    sku=l["sku"],
                    package_type=l["package_type"],
                    product_sat=l["product_sat"],
                    product_uom=l["product_uom"],
                    product_uomt=l["product_uomt"],
                    description=l["description"],
                    weight=l["weight"],
                    site=l["site"],
                    origin_site=l["origin_site"],
                    delivery_id=l["delivery_id"],
                    delivery_name=l["delivery_name"],
                    delivery_city=l["delivery_city"],
                    delivery_town=l["delivery_town"],
                    delivery_location=l["delivery_location"],
                    delivery_cp=l["delivery_cp"],
                    delivery_address=l["delivery_address"],
                    delivery_latitude=l["delivery_latitude"],
                    delivery_length=l["delivery_length"],
                    delivery_rfc=l["delivery_rfc"],
                    type_service=l["type_service"],
                    type_order=l["type_order"],
                    type_delivery=l["type_delivery"],
                    last_quation_delivery=l["last_quation_delivery"],
                    last_delivery=l["last_delivery"],
                    pieces=l["pieces"],
                    boxes=l["boxes"],
                    pallets=l["pallets"],
                    responsible_rejection=l["responsible_rejection"],
                    routing_status=l["routing_status"],
                    type_action="FU",
                    create_uid=l["create_uid"],
                    write_uid=l["write_uid"],
                    header_id=copyh,
                    spo_qty=l["spo_qty"],
                    product_vol=l["product_vol"],
                    udv_total=l["udv_total"],
                    incoterm=l["incoterm"],
                    planta=l["planta"],
                )
                line.save()
            print(" --> Creación de lines del primer Header")
            lines2 = List.objects.filter(header_id=id2).values()
            for l in lines2:
                line = List(
                    number=l["number"],
                    ide=l["ide"],
                    ref=l["ref"],
                    oc=l["oc"],
                    invoice=l["invoice"],
                    id_partner=l["id_partner"],
                    partner=l["partner"],
                    state=l["state"],
                    createdata_date=l["createdata_date"],
                    create_time=l["create_time"],
                    delivery_date=l["delivery_date"],
                    appointment_time=l["appointment_time"],
                    comment=l["comment"],
                    pieces_received=l["pieces_received"],
                    boxes_received=l["boxes_received"],
                    pallets_received=l["pallets_received"],
                    id_prod=l["id_prod"],
                    sku=l["sku"],
                    package_type=l["package_type"],
                    product_sat=l["product_sat"],
                    product_uom=l["product_uom"],
                    product_uomt=l["product_uomt"],
                    description=l["description"],
                    weight=l["weight"],
                    site=l["site"],
                    origin_site=l["origin_site"],
                    delivery_id=l["delivery_id"],
                    delivery_name=l["delivery_name"],
                    delivery_city=l["delivery_city"],
                    delivery_town=l["delivery_town"],
                    delivery_location=l["delivery_location"],
                    delivery_cp=l["delivery_cp"],
                    delivery_address=l["delivery_address"],
                    delivery_latitude=l["delivery_latitude"],
                    delivery_length=l["delivery_length"],
                    delivery_rfc=l["delivery_rfc"],
                    type_service=l["type_service"],
                    type_order=l["type_order"],
                    type_delivery=l["type_delivery"],
                    last_quation_delivery=l["last_quation_delivery"],
                    last_delivery=l["last_delivery"],
                    pieces=l["pieces"],
                    boxes=l["boxes"],
                    pallets=l["pallets"],
                    responsible_rejection=l["responsible_rejection"],
                    routing_status=l["routing_status"],
                    type_action="FU",
                    create_uid=l["create_uid"],
                    write_uid=l["write_uid"],
                    header_id=copyh,
                    spo_qty=l["spo_qty"],
                    product_vol=l["product_vol"],
                    udv_total=l["udv_total"],
                    incoterm=l["incoterm"],
                    planta=l["planta"],
                )
                line.save()
            # ----
            print(" --> Creación de lines del segundo Header")
            header_1.save()
            header_2.save()
            print(" --> Se guardan los cambios de los header originales")
            rel1 = Parent(
                id_parent=id1,
                name_parent=header_1_name,
                id_son=copyh.id,
                name_son=codeHead,
                type="FU",
                create_uid=request.user.id,
                write_uid=request.user.id,
            )
            rel1.save()
            print(" --> Se crea primera relación de fusion")
            print(" --> ", rel1.id)
            rel2 = Parent(
                id_parent=id2,
                name_parent=header_2_name,
                id_son=copyh.id,
                name_son=codeHead,
                type="FU",
                create_uid=request.user.id,
                write_uid=request.user.id,
            )
            rel2.save()
            type_notify = TypeNotify.objects.get(pk=1)
            new_notify = Notify(
                user=request.user,
                type=type_notify,
                name="Fusión de DataList {} y {}".format(str(header_1_name), str(header_2_name)),
                description="""
                           El usuario '{} {}'  ha generado una fusión del DataList '{}' y del DataList 
                           '{}' cual se generó el nuevo folio '{}'.
                           Recuerde que ya puede ser utilizado para el proceso de Ruteo.
                           """.format(request.user.first_name, request.user.last_name, str(header_1_name), str(header_2_name),
                                      str(codeHead)),
                priority=2,
                picture='notify/pictures/fusionf.png'
            )
            new_notify.save()
            print(" --> Se crea segunda relación de fusion")
            print(" --> ", rel2.id)
            # ----
            context2['active_btn4'] = 1
            context2['folio'] = codeHead
            context2['folio1'] = header_1_name
            context2['folio2'] = header_2_name
            print(" --> Se crean los contextos")
            next_number_crete.delete()
            print(" --> Se elimina referencia")
        return render(
            request,
            'datasheet/main.html',
            context2,
        )

class PostCopyDataList(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'

    def post(self, request, *args, **kwargs):
        context2 = {
            'erros': []
        }
        response = {
            'data': [],
            'error': False,
            'msj': ''
        }
        id = int(request.POST['header_copy_1'])
        datos = Cab.objects.filter(pk=id).values()
        next_number = Next.objects.filter(key="next_header").values("value")
        today = dt.datetime.today()
        all_next = []
        for nn in next_number:
            if len(nn['value']) > 1 :
                all_next.append(int(nn['value']))
        if len(all_next) > 0 :
            last_id = 0
            for an in all_next:
                if an > last_id:
                    last_id = an
            hid = last_id + 1
            codeTxt = str(hid).zfill(6)
            codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
        else:
            hid = Cab.objects.latest('id').id
            codeTxt = str(hid).zfill(6)
            codeHead = "DL-{}{}{}".format(str(today.year)[2:4], str(today.month), codeTxt)
        next_number_crete = Next(key="next_header",value=int(hid))
        next_number_crete.save()
        for d in datos:
            copyh = Cab(
                name=codeHead,
                state=d["state"],
                state_copy="CA",
                state_fusion=d["state_fusion"],
                create_uid=request.user.id,
                write_uid=request.user.id
            )
            copyh.save()
        anterior = Cab.objects.get(pk=id)
        today = dt.datetime.today()
        anterior.write_uid = request.user.id
        anterior.write_date = today
        anterior.state_copy='CP'
        anterior.save()
        lines = List.objects.filter(header_id=id).values()
        for l in lines:
            line = List(
                number = l["number"],
                ide = l["ide"],
                ref = l["ref"],
                oc = l["oc"],
                invoice = l["invoice"],
                id_partner = l["id_partner"],
                partner = l["partner"],
                state = l["state"],
                createdata_date = l["createdata_date"],
                create_time = l["create_time"],
                delivery_date = l["delivery_date"],
                appointment_time = l["appointment_time"],
                comment = l["comment"],
                pieces_received = l["pieces_received"],
                boxes_received = l["boxes_received"],
                pallets_received = l["pallets_received"],
                id_prod = l["id_prod"],
                sku = l["sku"],
                package_type = l["package_type"],
                product_sat = l["product_sat"],
                product_uom = l["product_uom"],
                product_uomt = l["product_uomt"],
                description = l["description"],
                weight = l["weight"],
                site = l["site"],
                origin_site = l["origin_site"],
                delivery_id = l["delivery_id"],
                delivery_name = l["delivery_name"],
                delivery_city = l["delivery_city"],
                delivery_town = l["delivery_town"],
                delivery_location = l["delivery_location"],
                delivery_cp = l["delivery_cp"],
                delivery_address = l["delivery_address"],
                delivery_latitude = l["delivery_latitude"],
                delivery_length = l["delivery_length"],
                delivery_rfc = l["delivery_rfc"],
                type_service = l["type_service"],
                type_order = l["type_order"],
                type_delivery = l["type_delivery"],
                last_quation_delivery = l["last_quation_delivery"],
                last_delivery = l["last_delivery"],
                pieces = l["pieces"],
                boxes = l["boxes"],
                pallets = l["pallets"],
                responsible_rejection = l["responsible_rejection"],
                routing_status = l["routing_status"],
                type_action = "CP",
                create_uid = l["create_uid"],
                write_uid = l["write_uid"],
                header_id = copyh,
                spo_qty = l["spo_qty"],
                product_vol = l["product_vol"],
                udv_total = l["udv_total"],
                incoterm = l["incoterm"],
                planta = l["planta"],
            )
            line.save()
        next_number_crete.delete()
        context2['active_btn2'] = 1
        context2['user'] = request.user
        context2['after'] = anterior.name
        context2['before'] = codeHead
        rel = Parent(
            id_parent= id,
            name_parent = anterior.name,
            id_son = copyh.id,
            name_son = codeHead,
            type = "CO",
            create_uid = request.user.id,
            write_uid = request.user.id,
        )
        rel.save()
        type_notify = TypeNotify.objects.get(pk=1)
        new_notify = Notify(
            user=request.user,
            type=type_notify,
            name="Copia de Data List - {}".format(str(anterior.name)),
            description="""
                       El usuario '{} {}'  ha generado un copia Data List '{}' del cual se generó el nuevo folio '{}'.
                       Recuerde que ya puede ser utilizado para el proceso de Ruteo.
                       """.format(request.user.first_name, request.user.last_name, str(anterior.name), str(codeHead)),
            priority=2,
            picture='notify/pictures/copyf.png'
        )
        new_notify.save()
        return render(
            request,
            'datasheet/main.html',
            context2,
        )


class DataTablesHeader(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'


    def post(self, request, *args, **kwargs):
        query = Cab.objects.all().values()
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        for q in query:
            item = {
                'id': q['id'],
                'name': q['name'],
                'state': next((x[1] for x in Cab.STATE_HEADER if x[0] == q['state']), ""),
                'state_copy': next((x[1] for x in Cab.STATE_HEADER_COPY if x[0] == q['state_copy']), ""),
                'state_fusion': next((x[1] for x in Cab.STATE_FUSION if x[0] == q['state_fusion']), ""),
                'create_uid': User.objects.get(pk=q['create_uid']).username,
                'create_date':q['create_date'].strftime("%m/%d/%Y %H:%M:%S"),
                'active':q['active']
            }
            data.append(item)
        response['data']=data
        print(data)
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DataTablesDatasheets(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'


    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        print('---> ',id,' <---')
        query = List.objects.filter(header_id=id).values(
            'number',
            'ref',
            'partner',
            'state',
            'delivery_date',
            'site',
            'delivery_name',
            'delivery_city',
            'delivery_town',
            'type_service',
            'type_order',
            'type_delivery',
            'routing_status',
            'type_action',
            'planta',
            'ide'
        ).order_by('ref')
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        aux = ''
        for q in query:
            if aux !=  q['ref']:
                item = {
                    'number' : q['number'],
                    'ref' : q['ref'],
                    'partner' : q['partner'],
                    'state' : q['state'],
                    'delivery_date' : q['delivery_date'],
                    'site' : q['site'],
                    'delivery_name' : q['delivery_name'],
                    'delivery_city' : q['delivery_city'],
                    'delivery_town' : q['delivery_town'],
                    'type_service' : q['type_service'],
                    'type_order' : q['type_order'],
                    'type_delivery' :q['type_delivery'],
                    'routing_status' : next((x[1] for x in List.STATE_ROUTING if x[0] == q['routing_status']), ""),
                    'type_action' : next((x[1] for x in List.TYPE_ACTION if x[0] == q['type_action']), ""),
                    'planta' : q['planta'],
                    'ide': List.objects.filter(header_id=id,ref=q['ref']).count()
                }
                data.append(item)
                aux = q['ref']
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

class DataTablesDatasheetsLine(LoginRequiredMixin, TemplateView):
    template_name = 'datasheet/main.html'


    def post(self, request, *args, **kwargs):
        id = int(request.POST['id'])
        ref = request.POST['ref']
        print('---> ',id,' <---')
        query = List.objects.filter(header_id=id, ref=ref).values(
            'number',
            'ref',
            'partner',
            'delivery_name',
            'sku',
            'description',
            'package_type',
            'product_uom',
            'product_uomt',
            'product_sat',
            'site',
            'weight',
            'pieces',
            'boxes',
            'pallets',
            'product_vol',
            'spo_qty'
        ).order_by('ref')
        response = {
            'data':[],
            'error': False,
            'msj':''
        }
        data = []
        aux = ''
        for q in query:
            item = {
                'number': q['number'],
                'ref': q['ref'],
                'partner': q['partner'],
                'delivery_name': q['delivery_name'],
                'sku': q['sku'],
                'description': q['description'],
                'package_type': q['package_type'],
                'product_uom': q['product_uom'],
                'product_uomt': q['product_uomt'],
                'product_sat': q['product_sat'],
                'site': q['site'],
                'weight': f.format_qty(q['weight'],"float"),
                'pieces': q['pieces'],
                'boxes': q['boxes'],
                'pallets': f.format_qty(q['pallets'],"float"),
                'udv': f.format_qty(q['product_vol'],"float"),
                'qty': f.format_qty(q['spo_qty'],"float")
            }
            data.append(item)
        response['data']=data
        return JsonResponse(response)

    def get_context_data(self, context, **kwargs):
        context2 = super().get_context_data(**kwargs)
        return context2

@login_required
def ShowId(request):
    id = request.GET['id']
    csrfmiddlewaretoken = request.GET['csrfmiddlewaretoken']
    name = Cab.objects.get(pk=id).name
    state = next((x[1] for x in Cab.STATE_HEADER if x[0] == Cab.objects.get(pk=id).state), "")
    state_copy = next((x[1] for x in Cab.STATE_HEADER_COPY if x[0] == Cab.objects.get(pk=id).state_copy), "")
    state_fusion = next((x[1] for x in Cab.STATE_FUSION if x[0] == Cab.objects.get(pk=id).state_fusion), "")
    is_father =  Parent.objects.filter(id_parent=id).values('id_parent', 'name_parent', 'id_son', 'name_son')
    is_son =  Parent.objects.filter(id_son=id).values('id_parent', 'name_parent', 'id_son', 'name_son')
    print("******************************************************* >>>")
    is_father_list = []
    is_son_list = []
    for f in is_father:
        is_father_list.append({'id_parent': f['id_parent'], 'name_parent': f['name_parent'], 'id_son': f['id_son'], 'name_son': f['name_son']})
    print("**********")
    for s in is_son:
        is_son_list.append({'id_parent': s['id_parent'], 'name_parent': s['name_parent'], 'id_son': s['id_son'],'name_son': s['name_son']})
    print("******************************************************* <<<")
    print(">>> ", state, " <<<")
    # datalist = List.objects.filter(header_id=id).values()
    context = {
        "id_header": id,
        "name_header": name,
        "state": str(state).replace("(","").replace(")","").replace("'","").replace(",",""),
        "state_copy": str(state_copy).replace("(","").replace(")","").replace("'","").replace(",",""),
        "state_fusion": str(state_fusion).replace("(","").replace(")","").replace("'","").replace(",",""),
        "is_father_list": is_father_list,
        "is_son_list": is_son_list,
        "csrfmiddlewaretoken":csrfmiddlewaretoken
    }
    print(context)
    return render(
        request=request,
        template_name='datasheet/show.html',
        context=context
    )
@login_required
def ShowRef(request):
    ref = request.GET['ref']
    id = request.GET['id']
    name = Cab.objects.get(pk=id).name
    state = next((x[1] for x in Cab.STATE_HEADER if x[0] == Cab.objects.get(pk=id).state), ""),
    state_copy = next((x[1] for x in Cab.STATE_HEADER_COPY if x[0] == Cab.objects.get(pk=id).state_copy), ""),
    state_fusion = next((x[1] for x in Cab.STATE_FUSION if x[0] == Cab.objects.get(pk=id).state_fusion), "")

    context = {
        "id_header": id,
        "name_header": name,
        "state": str(state).replace("(","").replace(")","").replace("'","").replace(",",""),
        "state_copy": str(state_copy).replace("(","").replace(")","").replace("'","").replace(",",""),
        "state_fusion": str(state_fusion).replace("(","").replace(")","").replace("'","").replace(",",""),
        "ref":ref
    }
    print(context)
    return render(
        request=request,
        template_name='datasheet/showref.html',
        context=context
    )
