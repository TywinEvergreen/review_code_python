from django.urls import reverse
from rest_framework.test import APITestCase

from transfer.factories import AdditionalUserInformationFactory, UserFactory
from transfer.serializers import TransferSerializer


class TransferAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.additional_info1 = AdditionalUserInformationFactory()
        self.additional_info2 = AdditionalUserInformationFactory()
        self.additional_info3 = AdditionalUserInformationFactory()

        self.client.force_login(self.additional_info1.user)
        self.url = reverse("transfer")

    def test_do_transfer(self):
        response = self.client.post(self.url, {
            "amount": 100,
            "users_to": [
                self.additional_info2.user.pk,
                self.additional_info3.user.pk,
            ],
        })

        self.additional_info1.refresh_from_db()
        self.additional_info2.refresh_from_db()
        self.additional_info3.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.additional_info1.account, 0.50)
        self.assertEqual(self.additional_info2.account, 150.50)
        self.assertEqual(self.additional_info3.account, 150.50)

    def test_do_failed_transfer(self):
        response1 = self.client.post(self.url, {
            "amount": 200,
            "users_to": [
                self.additional_info2.user.pk,
            ],
        })

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(
            response1.data["non_field_errors"][0],
            TransferSerializer.messages["not_enough_money"]
        )

        user = UserFactory()
        self.client.force_login(user)

        response2 = self.client.post(self.url, {
            "amount": 123,
            "users_to": [
                self.additional_info2.user.pk,
            ],
        })
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(
            response2.data["non_field_errors"][0],
            TransferSerializer.messages["error"]
        )


