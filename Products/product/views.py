from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ResultListSerializer
from .models import Production, Set
from collections import namedtuple
from django.contrib.sites.shortcuts import get_current_site

import math

set_range = [0, 5] # Начальные значения для диапазона данных Set.
Result = namedtuple('Result', ('productions', 'sets')) # Создаем именованный кортеж для результатов полученных данных при запросах.
count = Production.objects.count()+Set.objects.count()

# Вычисление диапазона данных Production.
def objectRangeProduction(page_num):
	prod_start = (page_num - 1) * 5
	prod_end = prod_start + 5
	return [prod_start, prod_end]

# Вычисление диапазона данных Set.
def objectRangeSet(set_start, set_end):
	set_start += 5
	set_end = set_start + 5
	return [set_start, set_end]

# Получение url'ов для пагинации.
def get_next_previous_url(page_num, request):
	previous_url = None if (page_num - 1 == 0) else f'http://{get_current_site(request).domain}{request.path}?page={page_num - 1}'
	next_url = None if (page_num + 1 > math.ceil(count / 5)) else f'http://{get_current_site(request).domain}{request.path}?page={page_num + 1}'
	return [next_url, previous_url]

class ResultListView(viewsets.ViewSet):

	def list(self, request, *args, **kwargs):

		try:
			page_num = int(request.GET['page'])
		except KeyError:
			page_num = 1

		next_url, previous_url = get_next_previous_url(page_num, request)

		prod_start, prod_end = objectRangeProduction(page_num)

		'''
		Если данных из Production меньше 5 на одной сранице, 
		то добавляется недостающее кол-во из Set, 
		и диапазон  данных Set начинается с нового значения.
		'''
		if (prod_end - Production.objects.count() < 5) and (prod_end - Production.objects.count() > 0):
			productions = Production.objects.order_by('name').all()[prod_start:prod_end]
			sets = Set.objects.order_by('name').all()[0:prod_end-Production.objects.count()]
			set_range[0] = prod_end-Production.objects.count()
			set_range[1] = set_range[0] + 5

		# Вывод данных Set.
		elif (prod_end - Production.objects.count() >= 5):
			productions = Production.objects.order_by('name').all()[0:0]
			sets = Set.objects.order_by('name').all()[set_range[0]:set_range[1]]
			set_range[0], set_range[1] = objectRangeSet(set_range[0], set_range[1])

		# Вывод данных Production.
		else:
			productions = Production.objects.order_by('name').all()[prod_start:prod_end]
			sets = Set.objects.order_by('name').all()[0:0]

		# Запись результатов полученных данных.
		result = Result(
			productions = productions,
			sets = sets
			)
		serializer = ResultListSerializer(result)

		link = f'<{next_url}>; rel = "next", <{previous_url}>; rel="prev"'
		headers = {"link": link, 'Count': count}

		return Response(serializer.data['productions']+serializer.data['sets'], headers=headers)