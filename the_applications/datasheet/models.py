from django.db import models
from django.db.models.constraints import UniqueConstraint

# Create your models here.

class ModelReg(models.Model):
    name = models.CharField(max_length=100, default='')
class Header(models.Model):
    STATE_HEADER = [
        ("LI", "Libre"),
        ("AS", "Asignado"),
        ("AN", "Analizado"),
        ("CL", "Clasificado"),
        ("AP", "Aprobado")
    ]
    STATE_HEADER_COPY = [
        ("OR", ""),
        ("CP", "Copiado"),
        ("CA", "Copia")
    ]
    STATE_FUSION = [
        ("OR", ""),
        ("FS", "Fusionado"),
        ("BF", "Base")
    ]
    name = models.CharField("Folio", max_length=40)
    state = models.CharField("Estado", max_length=20,choices=STATE_HEADER, default="LI")
    state_copy = models.CharField("Estado copia", max_length=20,choices=STATE_HEADER_COPY, default="OR")
    state_fusion = models.CharField("Estado Fusión", max_length=20,choices=STATE_FUSION, default="OR")
    active = models.BooleanField("Activo", default=True)
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name'], name='unique_blocking')
        ]

class RelParent(models.Model):
    TYPE_REL = [
        ("CO", "Copia"),
        ("FU", "Fusión"),
        ("DV", "Derivado"),
        ("GB", "Agrupación"),
        ("TF", "Transformación"),
    ]
    id_parent = models.IntegerField()
    name_parent = models.CharField("Folio", max_length=40, default=False)
    id_son = models.IntegerField()
    name_son = models.CharField("Folio", max_length=40, default=False)
    type = models.CharField("Tipo", max_length=20, choices=TYPE_REL, default="CO")
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()

class DataSheet(models.Model):
    STATE_DATASHEET = [
        ("SA","Sin asignar"),
        ("PO","Procesando"),
        ("AS","Asignado"),
        ("CO","Corregido")
    ]
    STATE_ROUTING = [
        ("PR", "Pendiente"),
        ("ES", "Escenario"),
        ("AP", "Aprobación"),
        ("RO", "Ruteado"),
        ("IR", "En ruta"),
    ]
    TYPE_ACTION = [
        ("SA", "Sin acciones"),
        ("FU", "Fusionado"),
        ("CP", "Copiado"),
    ]
    number = models.CharField("Folio", max_length=40)  #
    ide = models.IntegerField("Identificador") #
    ref = models.CharField("Referencia Interna", max_length=40) #
    oc = models.IntegerField("Pedido") #
    invoice = models.CharField("Factura", max_length=40) #
    id_partner = models.IntegerField("Cuenta", default=False)
    partner = models.CharField("Cuenta", max_length=160)
    state = models.CharField("Estatus", max_length=20,choices=STATE_DATASHEET, default="SA") #
    createdata_date = models.DateField("Fecha de creación", auto_now_add=True) #
    create_time = models.TimeField("Hora de creación",  auto_now_add=True) #
    delivery_date = models.DateField("Fecha de entrega") #
    appointment_time = models.TimeField("Hora de creación")  #
    comment = models.TextField("Comentarios adicionales") #
    pieces_received = models.FloatField("Piezas recibidas") #
    boxes_received = models.FloatField("Cajas recibidas") #
    pallets_received = models.FloatField("Cajas recibidas") #
    id_prod = models.IntegerField("Id producto", default=False) # #
    sku = models.CharField("Código", max_length=15) #
    package_type = models.CharField("Tipo de paquete", max_length=20, default="") #
    product_sat = models.CharField("UOM SAT", max_length=20, default="") #
    product_uom = models.CharField("UOM", max_length=20, default="") #
    product_uomt = models.CharField("UOM T", max_length=20, default="") #
    description = models.TextField("Descripción") #
    weight = models.FloatField("Peso") #
    site = models.CharField("Bodega", max_length=20) #
    origin_site = models.CharField("Nombre del origen", max_length=40) #
    delivery_id = models.FloatField("Id destino", default=False) #
    delivery_name = models.TextField("Nombre del destino") #
    delivery_city = models.CharField("Estado del destino", max_length=50) #
    delivery_town = models.CharField("Municipio del destino", max_length=80) #
    delivery_location = models.CharField("Colonia del destino", max_length=80) #
    delivery_cp = models.CharField("CP del destino", max_length=10) #
    delivery_address = models.TextField("Dirección del destino") #
    delivery_latitude = models.FloatField("Latitud del destino") #
    delivery_length = models.FloatField("Longitud del destino") #
    delivery_rfc = models.CharField("RFC", max_length=20, default="") #
    type_service = models.CharField("Tipo de servicio", max_length=20) #
    type_order = models.CharField("Tipo de orden", max_length=20) #
    type_delivery = models.CharField("Tipo de entrega", max_length=20) #
    last_quation_delivery = models.TextField("Última solicitud de embarque") #
    last_delivery = models.TextField("Último embarque") #
    pieces = models.FloatField("Piezas") #
    boxes = models.FloatField("Cajas") #
    pallets = models.FloatField("Pallets") #
    responsible_rejection = models.CharField("Responsable del rechazo", max_length=40) #
    routing_status = models.CharField("Estatus de Ruteo", max_length=40, choices=STATE_ROUTING, default="PR") #
    type_action = models.CharField("Tipo de Accion", max_length=40, choices=TYPE_ACTION, default="SA")  #
    write_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_uid = models.IntegerField()
    write_uid = models.IntegerField()
    header_id = models.ForeignKey(Header, on_delete=models.CASCADE, default=False)
    spo_qty = models.FloatField("Cantidad reportada",default=0.0) #
    product_vol = models.FloatField("UDV", default=0.0) #
    udv_total = models.FloatField("UDV Total", default=0.0) #
    incoterm = models.CharField("Incocoterm", max_length=40, default="")  #
    planta = models.IntegerField("Planta", default=0)


class TempNextCode(models.Model):

    key = models.CharField("Llave", max_length=50, default="")
    value = models.CharField("Llave", max_length=50, default="")