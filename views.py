import datetime

from django.db.models import Count
from datetime import datetime
from .serializers import DailySubSerializer,OfferSerialize, RequisitionSerializer, GroupMasterSerializer, DeclineSerializer
from .models import DailySub,Offer,Requisition , GroupMaster
from rest_framework.response import Response
from rest_framework import viewsets,status , views
from django.shortcuts import get_object_or_404,render
from django_filters.rest_framework import DjangoFilterBackend


class DailySubsAPIView(viewsets.ModelViewSet):
    """
        Class for the DailySub CRUD operations
        list method gets all the records from the DailySub database
        create method creates a new record and adds to the DailySub database
        update method updates the specific record in the DailySub database
        retrieve method gets the specific record in the DailySub database
    """
    queryset = DailySub.objects.all()
    serializer_class = DailySubSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('__all__')

    def list (self,request):
        filters = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(filters)
        serializer = DailySubSerializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data,status=status.HTTP_201_CREATED)
        return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class DailySubsView(viewsets.ModelViewSet):

    serializer_class=DailySubSerializer
    queryset=DailySub.objects.all()

    def update(self, request, pk=None):
        queryset = get_object_or_404(DailySub, id=pk)
        DailySubSerializer = self.serializer_class(queryset, data=request.data)
        if DailySubSerializer.is_valid():
            DailySubSerializer.save()
            return Response(DailySubSerializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(DailySubSerializer.errors, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        if pk is not None:     
            queryset = get_object_or_404(DailySub, id=pk)
            SingleRecord = self.serializer_class(queryset)
            return Response(SingleRecord.data, status=status.HTTP_200_OK)
            return Response(SingleRecord.errors,status=status.HTTP_404_NOT_FOUND)

class OffersAPIView(viewsets.ModelViewSet):
    
    queryset = Offer.objects.all()
    serializer_class = OfferSerialize
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ('__all__')

    def list(self, request):
        """
        This method is used to fetch all records form Offer Model.

        Params: None
        Return: Returns all existing offers
        """
        filters = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(filters)
        serializer = self.serializer_class(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def create(self, request):
        """
        This function is used to add new offer

        Params: request
        Return: Returns newly added record
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferView(viewsets.ModelViewSet):

    serializer_class = OfferSerialize
    queryset = Offer.objects.all()

    def retrieve(self, request, pk=None):
        """
        This method is used to retrieve specific record form Offer.
        :param request:
        :param pk: primary key of specific record.
        :return: Either returns specific record if available or returns error status code.
        """
        if pk is not None:
            queryset = get_object_or_404(Offer, id=pk)

            offerSerialize = self.serializer_class(queryset)
            return Response(offerSerialize.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        This method is used to update a specific record.
        :param request:
        :param pk: primary key of specific record.
        :return: Either returns specific record after successful update if available or returns error status code.
        """
        queryset = get_object_or_404(Offer, id=pk)

        offerSerialize = self.serializer_class(queryset, data=request.data)

        if offerSerialize.is_valid():
            offerSerialize.save()
            return Response(offerSerialize.data, status=status.HTTP_202_ACCEPTED)

        return Response(offerSerialize.errors, status=status.HTTP_404_NOT_FOUND)



class AddRequisitionsView(viewsets.ModelViewSet):
    """  
    View to add new requisition with validations.

    """
    queryset = Requisition.objects.all()

    serializer_class = RequisitionSerializer

    def list(self, request):
        """This function is used to fetch all requisitions

        Returns:
            Returns all requisitions
        """

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


    def create(self, request,format=None):
        """This function is used to add new requisition

        Params: request
        Return: Returns newly added record
        """
        serializer = RequisitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """This function is used to fetch specific requisition

        Args:
            pk (_type_, optional): _description_. Defaults to None.

        Returns:
            Returns specific requisition
        """
        if pk is not None:
            queryset = get_object_or_404(Requisition,id=pk)
            RequisitionSerializer = self.serializer_class(queryset)
            return Response(RequisitionSerializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self,request,pk=None):
        queryset = get_object_or_404(Requisition,id=pk)
        RequisitionSerializer = self.serializer_class(queryset, data=request.data)

        if RequisitionSerializer.is_valid():
            print("Valid")
            RequisitionSerializer.save()
            return Response(RequisitionSerializer.data, status=status.HTTP_200_OK)
        return Response(RequisitionSerializer.errors, status=status.HTTP_404_NOT_FOUND)


class DropdownListAPIView(views.APIView):
    """Dropdown List API View"""

    queryset = GroupMaster.objects.all()
    serializer_class = GroupMasterSerializer

    def get(self, request, *args, **kwargs):

        groups = self.queryset.filter(**self.kwargs).values("group").distinct()
        data = {}
        for group in groups:
            counter = 0
            grouped_data = []
            for record in self.queryset.filter(**group):
                counter += 1
                grouped_data.append({
                    "id": counter,
                    "name": record.name,
                    "isActive": record.isActive,
                })
            data[group["group"]] = grouped_data
        return Response(data, status.HTTP_200_OK)


class InterviewSelectReport(viewsets.ModelViewSet):
    serializer_class = DailySubSerializer
    queryset = DailySub.objects.all()
    l1totalCount = 0

    def calculation(self, practice, data, selectedpractices):

        if practice in selectedpractices:
            for item in data:
                if practice == item["practice"]:
                    return item["interviewCount"]

        return 0

    def retrieve(self, request):
        # global l1totalCount
        data = GroupMaster.objects.values('value').filter(
            group='Practice').order_by("value")

        practicesList = [name['value'] for name in data]
        resultData = {"interview": [{
            "practice": 'practice',
            "l1": 'L1 Interview Select',
            "l2": 'L2 Interview Select',
        }]}
        date1 = request.query_params.get("date")

        if (date1):
            date1 = datetime.strptime(date1, '%Y-%m-%d').date()
            l1Data = DailySub.objects.values('practice').filter(
                status="L1InterviewSelect", sourceDate=date1).annotate(interviewCount=Count('practice'))
            l2Data = DailySub.objects.values('practice').filter(
                status="L2InterviewSelect", sourceDate=date1).annotate(interviewCount=Count('practice'))
        else:
            todayYear = datetime.now().year
            l1Data = DailySub.objects.values('practice').filter(
                status="L1InterviewSelect", sourceDate__year=todayYear).annotate(interviewCount=Count('practice'))
            l2Data = DailySub.objects.values('practice').filter(
                status="L2InterviewSelect", sourceDate__year=todayYear).annotate(interviewCount=Count('practice'))

        selectedpracticesL1 = [data['practice'] for data in l1Data]
        selectedpracticesL2 = [data['practice'] for data in l2Data]
        l1TotalCount = 0
        l2TotalCount = 0
        for practice in practicesList:
            l1count = self.calculation(practice, l1Data, selectedpracticesL1)
            l2count = self.calculation(practice, l2Data, selectedpracticesL2)
            row = {
                "practice": practice,
                "l1": l1count,
                "l2": l2count,
            }
            l1TotalCount += l1count
            l2TotalCount += l2count

            resultData["interview"].append(row)
        # Table Footer Grand Total
        row = {
            "total": "Grand Total",
            "l1InterviewSelect": l1TotalCount,
            "l2InterviewSelect": l2TotalCount,
        }
        resultData["interview"].append(row)

        return Response(resultData)


class DeclineCount(viewsets.ModelViewSet):
    queryset = DailySub.objects.all()
    serializer_class = DailySubSerializer

    def get(self, request, *args, **kwargs):
        groups = self.queryset.values("declineReasons").distinct()
        data = {}
        for group in groups:
            counter = 0
            grouped_data = []
            for record in self.queryset.filter(status='Declined'):
                # counter += 1
                grouped_data.append({
                    "id": counter,
                    "declineReasons": record.declineReasons,
                })
            data[status["Declined"]] = grouped_data
        return Response(data, status.HTTP_200_OK)