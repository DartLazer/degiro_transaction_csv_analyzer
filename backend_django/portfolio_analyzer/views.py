from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from .analyze_portfolio import calculate_multi_year_gain  # Import your function


class CalculateMultiYearGainView(APIView):  # Use FileUploadParser for handling file uploads

    def post(self, request, *args, **kwargs):
        csv_file = request.data['csv_file']  # Access the uploaded file from the request data
        try:
            results = calculate_multi_year_gain(csv_file)  # Call your function with the csv_file
            return Response(results, status=status.HTTP_200_OK)  # Return the results as JSON response
        except ValueError as e:
            return Response({"error": 'Inccorect CSV File'}, status=status.HTTP_400_BAD_REQUEST)

