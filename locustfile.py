"""locust- файл со сценариями обращения по post- и get- запросам."""
from locust import HttpUser, task, between

from functions import generate_random_string, generate_random_status


class QuickstartUser(HttpUser):
    """Определение класса для пользователей, которых необходимо моделировать."""

    wait_time = between(1, 5)

    @task  # type: ignore
    def get_deliveries(self) -> None:
        """Сценарий обращения по get-запросу."""
        self.client.get("/deliveries/")

    @task  # type: ignore
    def add_delivery(self) -> None:
        """Сценарий обращения по post-запросу."""
        id = generate_random_string(5)
        status = generate_random_status()
        self.client.post("/deliveries/", json={"id": id, "status": status})
