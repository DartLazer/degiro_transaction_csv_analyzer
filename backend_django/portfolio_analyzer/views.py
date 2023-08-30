from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .analyze_portfolio import calculate_multi_year_gain
import os


class CalculateMultiYearGainView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            csv_file = request.data.get('csv_file', None)
            if csv_file is None:
                raise ValueError("CSV file missing")

            # Check if the uploaded file has the '.csv' extension
            file_name = csv_file.name  # This should get the uploaded file name
            file_extension = os.path.splitext(file_name)[1]  # Split the filename and take the extension

            if file_extension.lower() != '.csv':
                raise ValueError("Invalid file type: Only .csv files are allowed")

            # Your existing logic here
            results = calculate_multi_year_gain(csv_file)
            return Response(results, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
