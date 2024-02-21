from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


# Create your views here.
class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    """
    A viewset for viewing and editing server instances.

    Attributes:
        queryset (QuerySet): The default queryset that retrieves all server objects.
    """

    @server_list_docs
    def list(self, request):
        """
        List servers based on various filters such as category, quantity, by_user,
        by_serverid, and with_num_members. This method applies filters based on the
        query parameters provided in the request.

        Args:
            request (HttpRequest): The request object containing query parameters
                for filtering the servers list. Expected query parameters are:
                - category (str): Filter servers by category.
                - qty (int): Limit the number of servers returned.
                - by_user (bool): Filter servers by the authenticated user.
                - by_serverid (str): Filter servers by server id.
                - with_num_members (bool): Include the number of members in the response.

        Returns:
            Response: A REST framework response object containing the serialized server data.

        Raises:
            AuthenticationFailed: If the user is not authenticated and tries to filter by_user or by_serverid.
            ValidationError: If an invalid server id is provided or if no server matches the provided server id.
        """

        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # if by_user or by_serverid and not request.user.is_authenticated:
        #     raise AuthenticationFailed(
        #         detail="You must be authenticated to use this feature."
        #     )

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user or by_serverid and not request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed(
                    detail="You must be authenticated to use this feature."
                )

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found."
                    )
                    # return Response({"detail": "Server not found"}, status=404)
            except ValueError:
                raise ValidationError(detail="Invalid server id.")

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(
            self.queryset, many=True, context={"number_members": with_num_members}
        )
        return Response(serializer.data)
