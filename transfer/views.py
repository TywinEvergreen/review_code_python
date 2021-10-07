from decimal import Decimal

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from transfer.models import AdditionalUserInformation
from transfer.serializers import TransferSerializer


# Не вижу смысла делать ViewSet для одной единственной non-CRUD операции.
# На мой взгляд куда удобнее сделать обычный APIView и руками с самого начала прописать логику.
class TransferAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransferSerializer

    # Эта функция настолько кривая, что мне проще просто переписать её на свой лад
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context=self)
        serializer.is_valid(raise_exception=True)

        amount = Decimal(serializer.data["amount"])
        users_to = serializer.data["users_to"]

        info = request.user.additional_information
        info.account -= amount
        info.save()

        sum_to_pay = Decimal(amount / len(users_to))
        for user_pk in users_to:
            receiver_info = AdditionalUserInformation.objects.get(user__pk=user_pk)
            receiver_info.account += sum_to_pay
            receiver_info.save()

        return Response(serializer.data)
