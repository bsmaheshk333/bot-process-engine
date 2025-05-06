from rest_framework.decorators import APIView  # CBV
from rest_framework.response import Response
from rest_framework import status
from .models import WorkItemModel
from .serializers import WorkItemSerializer
from datetime import datetime
from typing import Union, List


class WorkItemFilterByDateRangeView(APIView):
    def formatted_time(self, date_string, format_specifier):
        return datetime.strptime(date_string, format_specifier)

    def validate_request_data(self, input_data: str) -> str:
        # fixme value cannot be List[str] -- so commented.
        # if isinstance(input_data, list):
        #     for item in input_data:
        #         if not isinstance(item, str):
        #             raise ValueError("Value must be string")
        if not isinstance(input_data, str):
            raise ValueError("Value must be string")
        return input_data

    def put(self, request):
        try:
            start_date = self.validate_request_data(request.data.get('start_date'))
            end_date = self.validate_request_data(request.data.get('end_date'))
            state = self.validate_request_data(request.data.get('state'))
            status_ = self.validate_request_data(request.data.get('status'))

            if not start_date or not end_date:  # or not state or not status_:
                return Response(data={"error": "start_date, end_date, state, status_ must be provided"},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                start_date = self.formatted_time(date_string=start_date, format_specifier="%d-%m-%Y %H:%M")
                end_date = self.formatted_time(date_string=end_date, format_specifier="%d-%m-%Y %H:%M")
            except ValueError:
                return Response({"error": "invalid datetime format."}, status=status.HTTP_400_BAD_REQUEST)

            if not start_date or not end_date:
                return Response({"error": "invalid date format."}, status=status.HTTP_400_BAD_REQUEST)
            work_items = WorkItemModel.objects.all().filter(start_time__gte=start_date, end_time__lte=end_date)
            serializer = WorkItemSerializer(work_items, many=True)
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BulkInsert(APIView):
    def post(self, request):
        serializer = WorkItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
