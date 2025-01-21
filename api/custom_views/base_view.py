from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from ..utils.filterer import QuerysetFilter 

class BaseView(APIView):
    model = None  # To be set in the child class
    serializer_class = None  # To be set in the child class

    def get_queryset(self, request):
        """Override this method to customize queryset filtering."""
        return QuerysetFilter.filter_queryset(self.model, request.query_params)

    def get(self, request, pk=None):
        user = request.user

        # Check if the user belongs to the "student" group
        if user.groups.filter(name__iexact='student').exists():
            try:
                instances = None
                # Fetch records based on students user ID or username
                try:
                    if self.model.__name__.lower() == "student":
                        instances = self.model.objects.filter(id=user.username)
                    elif self.model.__name__.lower() == "user":
                        instances = self.model.objects.filter(username=user.username)
                    else:                    
                        instances = self.model.objects.filter(student=user.username)
                except:                    
                    raise NotFound(detail=f"No records found for user {user.username}.")

                # Check if no records are found
                if not instances.exists():
                    raise NotFound(detail=f"No records found for user {user.username}.")
                
                # Serialize the list of student data
                serializer = self.serializer_class(instances, many=True, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except ValueError as e:
                raise NotFound(detail=f"Invalid ID format: {e}")

        # For other user groups or non-student users
        if self.model.__name__.lower() == "user" and not user.groups.filter(name__iexact='admin').exists():
            try:
                instances = self.model.objects.filter(username=user.username)
                if not instances.exists():
                    raise NotFound(detail=f"No records found for user {user.username}.")
                
                serializer = self.serializer_class(instances, many=True, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except self.model.DoesNotExist:
                raise NotFound(detail=f"No records found for user {user.username}.")
            except ValueError as e:
                raise NotFound(detail=f"Invalid ID format: {e}")

        if pk:
            try:
                instance = self.model.objects.get(id=pk)
                serializer = self.serializer_class(instance, context={"request": request})
                return Response(serializer.data)
            except self.model.DoesNotExist:
                raise NotFound(detail=f"{self.model.__name__} with ID {pk} not found")
            except ValueError as e:
                raise NotFound(detail=f"Invalid ID format: {e}")

        # General queryset for non-student users (or without specific PK)
        queryset = self.get_queryset(request)
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        
        return Response(serializer.data if serializer.data else {"detail": f"No records in {self.model.__name__}."})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk:
            try:
                instance = self.model.objects.get(id=pk)
            except self.model.DoesNotExist:
                raise NotFound(detail=f"{self.model.__name__} with ID {pk} not found")

            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update instances based on filters
        queryset = self.get_queryset(request)
        if not queryset.exists():
            return Response({"detail": "No matching records found to update"}, status=status.HTTP_404_NOT_FOUND)

        updated_instances = []
        for instance in queryset:
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_instances.append(serializer.data)

        return Response({"success": True, "updated_instances": updated_instances}, status=status.HTTP_200_OK)

    # def delete(self, request, pk=None):
    #     if pk:
    #         try:
    #             instance = self.model.objects.get(id=pk)
    #             instance.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         except self.model.DoesNotExist:
    #             raise NotFound(detail=f"{self.model.__name__} with ID {pk} not found")

    #     # Delete instances based on filters
    #     queryset = self.get_queryset(request)
    #     if not queryset.exists():
    #         return Response({"detail": "No matching records found to delete"}, status=status.HTTP_404_NOT_FOUND)

    #     deleted_count = queryset.delete()[0]  # Returns a tuple (count, details)
    #     return Response({"detail": f"Deleted {deleted_count} instance(s)"}, status=status.HTTP_204_NO_CONTENT)