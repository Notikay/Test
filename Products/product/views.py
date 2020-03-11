from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ResultListSerializer
from .models import Production, Set
from collections import namedtuple

class LinkHeaderPagination(pagination.PageNumberPagination):

	def get_paginated_response(self, data):
		next_url = self.get_next_link()
		previous_url = self.get_previous_link()

		if next_url is not None and previous_url is not None:
			link = '<{next_url}>; rel = "next", <{previous_url}>; rel="prev"'
		elif next_url is not None:
			link = '<{next_url}>; rel = "next"'
		elif previous_url is not None:
			link = '<{previous_url}>; rel = "prev"'
		else:
			link = ''

		link = link.format(next_url = next_url, previous_url = previous_url)
		headers = {'Link': link, 'Count': self.page.paginator.count} if link else {}

		return Response(data, headers=headers)

class ResultListView(viewsets.ViewSet):

	def list(self, request, *args, **kwargs):
		Result = namedtuple('Result', ('productions', 'sets'))
		result = Result(
			productions = Production.objects.all(),
			sets = Set.objects.all()
			)
		serializer = ResultListSerializer(result)

		for el in serializer.data['sets']:
			serializer.data['productions'].append(el)
		serializer.data['sets'].clear()

		data = sorted(serializer.data['productions'], key=lambda x: x['name'])

		paginator = LinkHeaderPagination()
		page = paginator.paginate_queryset(data, request)

		if page is not None:
			return paginator.get_paginated_response(page)
		return Response(data)