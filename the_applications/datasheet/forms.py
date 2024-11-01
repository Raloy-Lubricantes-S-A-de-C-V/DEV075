"""Apps forms."""
import os
# Django
from django import forms
from the_applications.notify.models import TypeNotify, Notify
from django.contrib.auth.models import User
from django.db.models import Q
from the_applications.datasheet.models import Header, DataSheet
from the_applications.conexion import selecciona_basedatos
import datetime as dt


class FusionDataList(forms.Form):

    CHOICE_STATE = [('0', '')]

    header_fusion_1 = forms.ChoiceField(
        label="DataList Uno",
        choices=CHOICE_STATE,
        widget=forms.Select(attrs={'class': 'form-control', 'required': True})
    )

    header_fusion_2 = forms.ChoiceField(
        label="DataList Dos",
        choices=CHOICE_STATE,
        widget=forms.Select(attrs={'class': 'form-control', 'required': True})
    )

    def __init__(self, *args, **kwargs):
        super(FusionDataList, self).__init__(*args, **kwargs)
        body = Header.objects.all().filter(active=True).values('id','name')
        CHOICE_STATE = [(q['id'], q['name']) for q in body]
        self.fields['header_fusion_1'].choices = CHOICE_STATE
        self.fields['header_fusion_2'].choices = CHOICE_STATE

    def save(self):
        pass

class CopyDataList(forms.Form):

    CHOICE_STATE = [('0', '')]

    header_copy_1 = forms.ChoiceField(
        label="Estado",
        choices=CHOICE_STATE,
        widget=forms.Select(attrs={'class': 'form-control', 'required': True})
    )

    def __init__(self, *args, **kwargs):
        super(CopyDataList, self).__init__(*args, **kwargs)
        body = Header.objects.all().filter(Q(state_copy='OR') | Q(state_copy='CP'), active=True).values('id','name')
        CHOICE_STATE = [(q['id'], q['name']) for q in body]
        self.fields['header_copy_1'].choices = CHOICE_STATE

    def save(self):
        pass


class CreateDataList(forms.Form):

    name = forms.CharField(
        label="Codigo DataList",
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        help_text="Este codigo no debe repetirse"
    )
    CHOICE_STATE = (
        ("LI", "Libre"),
    )
    state = forms.ChoiceField(
        label="Estado",
        choices = CHOICE_STATE,
        widget=forms.Select(attrs={'class': 'form-control', 'required': True})
    )


    def clean_name(self):
        if not self.cleaned_data['name']:
            raise forms.ValidationError('Es obligatorio poner un "Codigo DataList"')
        name = Header.objects.filter(name__iexact=self.cleaned_data['name'])
        if name == self.cleaned_data['name']:
            raise forms.ValidationError('Se ha encontrado un regustro con la misma clave.')
        return self.cleaned_data['name']


    def save(self,user):
        data = self.cleaned_data
        header = Header(name=data['name'], create_uid=user, write_uid=user)
        header.save()
        try:
            bd_odoo = selecciona_basedatos.inicia_odoo()
            cursor = bd_odoo.cursor()
            query = """
select
    concat('RY-',x.sp_id) number,
    x.sp_id ide,
    x.sp_name "ref",
    x.so_id oc,
    coalesce(x.sp_invoice,0) invoice,
    x.id_partner id_partner,
    x.name_partner partner,
    CURRENT_DATE createdata_date,
    CURRENT_TIME create_time,
    to_char(x.sp_date, 'yyyy-mm-dd') delivery_date,
    coalesce(x.appointment_date,'1991-03-30 00:00:00')::timestamp appointment_time,
    coalesce(x.dest_comment,'') "comment",
    0.0 pieces_received,
    0.0 boxes_received,
    0.0 pallets_received,
    x.product_id id_prod,
    x.product_code sku,
    x.product_name description,
    x.package_type package_type,
    x.product_sat product_sat,
    x.product_uom product_uom,
    x.sat_t product_uomt,
    x.product_weight weight,
    x.spo_sl_name site,
    concat('Physical Location/APT/',x.spo_sl_name) origin_site,
    x.dest_id  delivery_id,
    x.dest_name delivery_name,
    coalesce(x.dest_settlement,'') delivery_city,
    coalesce(x.dest_municipaly,'') delivery_town,
    coalesce(x.dest_state,'') delivery_location,
    coalesce(x.dest_zip,'') delivery_cp,
    coalesce(x.dest_street,'') delivery_address,
    x.dest_latitud delivery_latitude,
    x.dest_longitud delivery_length,
    x.vat,
    coalesce(x.sp_servicetype,'') type_service,
    coalesce(x.type_picking,'') type_order,
    '' type_delivery,
    '' last_quation_delivery,
    '' last_delivery,
    1 pieces,
    1 boxes,
    0.1 pallets,
    '' responsible_rejection,
    coalesce(x.spo_qty,0) spo_qty,
    coalesce(x.product_vol,0) product_vol,
    coalesce(x.udv_total,0) udv_total,
    coalesce(x.incoterms_id,0) incoterm,
    coalesce(x.planta,False) planta
from
    (
        select
            so.id so_id,
            sp.id sp_id,
            sp."name" sp_name,
            sp.invoice_related_id sp_invoice,
            spt.name type_picking,
            so.partner_id id_partner,
            rp2.name name_partner,
            RP2.vat vat,
            sl3."name" spo_sl_name,
            rp.id dest_id,
            rp."name" dest_name,
            rp.street dest_street,
            rp.zip dest_zip,
            rp.street2 dest_municipaly,
            rp.city dest_settlement,
            rp.x_latitud dest_latitud,
            rp.x_longitud dest_longitud,
            rcs.tms dest_state,
            pp.id product_id,
            pt.package_type,
            pp.default_code product_code,
            pt."name" product_name,
            pu.name product_uom,
            CASE
                WHEN pt.package_type = 'TAMBOR' AND pt.udv >= 200  AND pt.udv <= 300  THEN 'LITRO'
                WHEN pt.package_type = 'TOTE' AND pt.udv = 1000 THEN 'LITRO'
                WHEN pt.package_type = 'TAMBOR' AND pt.udv = 1  THEN 'UNIDAD'
                WHEN pt.package_type = 'TOTE' AND pt.udv = 1 THEN 'UNIDAD'
                else pt.package_type
                END sat_t,
            sp2.code product_sat,
            spo.qty_done spo_qty,
            pp.weight product_weight,
            pt.udv product_vol,
            round(spo.udv_total) udv_total,
            sp."date" sp_date,
            ai.incoterms_id incoterms_id,
            sp.service_type sp_servicetype,
            sp.x_tms_entrega_en_planta planta,
            rp.comment  dest_comment,
            so.appointment_date
        from
            stock_picking sp
                inner join stock_picking_type spt on
                    sp.picking_type_id = spt.id
                inner join stock_location sl on
                    sp.location_id = sl.id
                inner join stock_location sl2 on
                    sp.location_dest_id = sl2.id
                left join sale_order so on
                    sp.origin = so."name"
                left join stock_pack_operation spo on
                    spo.picking_id = sp.id
                left join stock_location sl3 on
                    spo.location_id = sl3.id
                left join res_partner rp on
                    sp.partner_id = rp.id
                left join res_country_state rcs on
                    rp.state_id = rcs.id
                left join product_product pp on
                    spo.product_id = pp.id
                left join product_template pt on
                    pp.product_tmpl_id = pt.id
                left join product_uom pu on
                    pt.uom_id = pu.id
                left join sat_producto sp2 on
                    pt.sat_product_id = sp2.id
                left join account_invoice ai on
                    sp.invoice_related_id = ai.id
                left join res_partner rp2 on
                    so.partner_id = rp2.id
        where
                sp.tms_folio = 'Sin asignar'
    )x;"""
            cursor.execute(query)
            result_odoo = cursor.fetchall()
            for i in result_odoo:
                m=0
                for n in i:
                    m = m + 1
                if i[10] == '1991-03-30 00:00:00':
                    hora = '00:00:00'
                else:
                    hora = i[10].strftime("%H:%M:%S")
                datasheet = DataSheet(
                    number = i[0], # 0. - RY - 2402605
                    ide = i[1], # 1. - 2402605
                    ref = i[2], # 2. - APT / OUT / 424872
                    oc = i[3], # 3. - 529164
                    invoice = i[4], # 4. - 838214
                    id_partner = i[5], # 5. - 90122
                    partner = i[6], # 6. - GENERAL MOTORS DE MEXICO
                    createdata_date = i[7], # 7. - 2024 - 10 - 17
                    create_time = i[8], # 8. - 19: 44:32.494215 + 00: 00
                    delivery_date =  i[9], # 9. - 27 / 06 / 2024
                    appointment_time = hora, # 10. - None
                    comment = i[11], # 11. - HORARIO DE 8:30AM A 6.30PM
                    pieces_received = i[12], # 12. - 0.0
                    boxes_received = i[13], # 13. - 0.0
                    pallets_received = i[14], # 14. - 0.0
                    id_prod = i[15], # 15. - 97739
                    sku = i[16], # 16. - P11913
                    description = i[17], # 17. - 19434465 ACDELCO TRANSMISION SAE 75 W - 90 API GL - 5 946 ML / CIL(CJ / 12)
                    package_type = i[18], # 18. - BOTELLA
                    product_sat = i[19], # 19. - 15121508
                    product_uom = i[20], # 20. - BOTELLA
                    product_uomt = i[21], # 21. - BOTELLA
                    weight = i[22], # 22. - 0.0000
                    site = i[23], # 23. - Cedis I
                    origin_site = i[24], # 24. - Physical Location / APT / Cedis I
                    delivery_id = i[25], # 25. - 90147
                    delivery_name = i[26], # 26. - 19624 MOTORES GENERALES LA SILLA, S.A.DE C.V
                    delivery_city = i[27], # 27. - MONTERREY
                    delivery_town = i[28], # 28. - CENTRO
                    delivery_location = i[29], # 29. - NL
                    delivery_cp = i[30], # 30. - 64000
                    delivery_address = i[31], # 31. - AVENIDA PINO SUAREZ NORTE 351
                    delivery_latitude = i[32], # 32. - 0.0
                    delivery_length = i[33], # 33. - 0.0
                    delivery_rfc = i[34],
                    type_service = i[35],
                    type_order = i[36],  # 34. - CAS
                    type_delivery = i[37], # 35. - Delivery Orders
                    last_quation_delivery = i[38], # 36. -
                    last_delivery = i[39], # 37. -
                    pieces = i[40],   # 38. - 1
                    boxes = i[41], # 39. - 1
                    pallets = i[42], # 40. - 0.1
                    responsible_rejection = i[43],  # 41. -
                    spo_qty = i[44],  # 42. - 48.00000000
                    product_vol = i[45],  # 43. - 0.946
                    udv_total = i[46], # 44. - 45.0
                    incoterm = i[47], # 45. - None
                    planta = i[48],  # 46. - False
                    create_uid=user,
                    write_uid=user,
                    header_id=header
                )
                datasheet.save()
            cursor.close()
            bd_odoo.close()
        except  (Exception, psycopg2.Error) as errorx:
            msj = True
            error = True
            print("Error while connecting to PostgreSQL", errorx)

