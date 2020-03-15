from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ResultListSerializer
from .models import Production, Set
from collections import namedtuple

productions = Production.objects.order_by('name').all()
sets = Set.objects.order_by('name').all()

Result = namedtuple('Result', ('productions', 'sets'))
result = Result(
	productions = productions,
	sets = sets
	)
serializer = ResultListSerializer(result)

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
		paginator = LinkHeaderPagination()
		page = paginator.paginate_queryset(serializer.data['productions']+serializer.data['sets'], request)

		if page is not None:
			return paginator.get_paginated_response(page)
		return Response(serializer.data['productions']+serializer.data['sets'])