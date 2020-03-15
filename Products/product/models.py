from django.db import models

class Production(models.Model):
	"""Товар"""
	name = models.CharField("Название товара", max_length = 100)
	price = models.PositiveIntegerField("Цена", default = 0, help_text = "Указывать сумму в рублях")

	type_choices = [
		('TOP', 'Верх'),
		('BOTTOM', 'Низ'),
		('UNDEFINED', 'Не выбран'),
		]
	type_product = models.CharField("Тип", max_length = 50, choices = type_choices)

	def __str__(self):
		return self.name

	class Meta:
		"""Единственное и множественное число товара"""
		verbose_name = "Товар"
		verbose_name_plural = "Товары"

class Set(models.Model):
	"""Набор"""
	name = models.CharField("Название набора", max_length = 100)
	top = models.ManyToManyField(Production, verbose_name = "Товар с типом 'Верх'", limit_choices_to={'type_product': 'TOP'}, related_name = 'top', blank=True)
	bottom = models.ManyToManyField(Production, verbose_name = "Товар с типом 'Низ'", limit_choices_to={'type_product': 'BOTTOM'}, related_name = 'bottom', blank=True)

	def __str__(self):
		return self.name

	class Meta:
		"""Единственное и множественное число набора"""
		verbose_name = "Набор"
		verbose_name_plural = "Наборы"