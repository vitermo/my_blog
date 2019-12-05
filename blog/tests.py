from django.core.paginator import Paginator

objects = ['john', 'paul', 'george', 'ringo']
p = Paginator(objects, 1)
print(p.page_range)
