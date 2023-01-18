from django.urls import path
from tracker_api.views import DailySubsAPIView, DailySubsView, OfferView, OffersAPIView, AddRequisitionsView ,DropdownListAPIView ,InterviewSelectReport


offer_List_View = OffersAPIView.as_view({'get': 'list', 'post': 'create'})
offer_specific_View = OfferView.as_view({'get': 'retrieve', 'put': 'update'})

dailySubs_List_View = DailySubsAPIView.as_view({'get': 'list', 'post': 'create'})
dailySubs_specific_View = DailySubsView.as_view({'get': 'retrieve', 'put': 'update'})

requisitions = AddRequisitionsView.as_view({'get': 'list', 'post': 'create'})
requisitions_specific = AddRequisitionsView.as_view({'get': 'retrieve', 'put': 'update'})

urlpatterns = [
    path('DailySub/', dailySubs_List_View, name="DailySub"),
    path('DailySub/<int:pk>', dailySubs_specific_View, name="DailySub-specific"),
    path('offers/', offer_List_View, name="offers"),
    path('offer/<int:pk>', offer_specific_View, name="offer"),
    path('requisitions/', requisitions, name='requisitions'),
    path('requisitions/<int:pk>', requisitions_specific, name="specific-requisition"),
    path("dropdown/<str:group>/", DropdownListAPIView.as_view(), name="dropdown-group"),
    path("dropdown/", DropdownListAPIView.as_view(), name="dropdown"),
    path("interview/",InterviewSelectReport.as_view({'get': 'retrieve'}), name="interview"),
]
