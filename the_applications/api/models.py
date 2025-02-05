from django.db import models

class CabEpicor01(models.Model):

	shipping_order = models.CharField("Orden de Embarque", max_length=40)
	status = models.CharField("Estatus", max_length=40)
	date = models.DateTimeField("Fecha de Creacion de Ruta", auto_now_add=True)
	type_vehicle = models.CharField("Transporte", max_length=40)
	destiny = models.CharField("Destino", max_length=40)
	type_transport = models.CharField("Tipo de Unidad", max_length=40)
	route_number = models.CharField("Numero de Ruta", max_length=40)
	delivery_schedule = models.CharField("Horario Asigando", max_length=40)
	liters = models.FloatField("Litros de la Ruta")
	warehouse = models.CharField("Almacen", max_length=40)
	delivery_date = models.DateTimeField("Fecha de Ruta", auto_now_add=True)
	transfer_guide = models.CharField("Guía de paquetera", max_length=40)

	def __str__(self):
		return self.shipping_order

class LinesEpicor01(models.Model):

	order = models.IntegerField("Orden")
	line = models.IntegerField("Linea")
	rel = models.IntegerField("Relación")
	header_id = models.ForeignKey(CabEpicor01, on_delete=models.CASCADE, default=False)

	def __str__(self):
		return self.shipping_order