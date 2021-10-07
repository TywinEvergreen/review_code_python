from django.contrib.auth.models import User
from rest_framework import serializers


# PEP8 требует ставить два пробела перед объявлением класса, если это не подкласс
class TransferSerializer(serializers.Serializer):
    # Опять же, множество пробелов после оператора - нарушение PEP8
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)
    users_to = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    )

    messages = {
        "not_enough_money": "На счёте недостаточно средств",
        "error": "Перевод не выполнен",
    }

    def validate(self, attrs):
        user = self.context.request.user

        if not hasattr(user, "additional_information"):
            raise serializers.ValidationError(self.messages["error"])
        elif attrs["amount"] > user.additional_information.account:
            raise serializers.ValidationError(self.messages["not_enough_money"])

        return super().validate(attrs)

