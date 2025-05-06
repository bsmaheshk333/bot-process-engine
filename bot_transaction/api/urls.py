from django.urls import path
from . import views

urlpatterns =[
    path("filter/workitem/date_range/", views.WorkItemFilterByDateRangeView.as_view(), name='filter_items'),
    path("bulkinsert/", views.BulkInsert.as_view(), name='bulkinsert'),

]