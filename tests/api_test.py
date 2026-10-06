# Teste de rotas da API usando unittest
import unittest
from datetime import date, time
from unittest.mock import patch

from backend.main import ConsultaCreate, agendar_consulta, app


class TestApiRoutes(unittest.TestCase):
    def test_api_routes_are_registered(self):
        routes = {
            (route.path, method)
            for route in app.routes
            for method in getattr(route, "methods", set())
        }

        expected_routes = {
            ("/paciente", "GET"),
            ("/paciente", "POST"),
            ("/medico", "GET"),
            ("/medico", "POST"),
            ("/consulta", "POST"),
        }

        self.assertTrue(expected_routes.issubset(routes))

    def test_agendar_consulta_converts_time_to_iso_string(self):
        consulta = ConsultaCreate(
            paciente_id=1,
            medico_id=1,
            data_consulta=date(2026, 10, 7),
            hora_consulta=time(14, 30),
            observacao="Consulta de teste",
            situacao="Agendada",
        )

        with patch("backend.main.classes.Consulta") as consulta_service_class:
            response = agendar_consulta(consulta)

        consulta_service_class.return_value.agendar_consulta.assert_called_once_with(
            paciente_id=1,
            medico_id=1,
            data_consulta=date(2026, 10, 7),
            hora_consulta="14:30:00",
            observacao="Consulta de teste",
            situacao="Agendada",
        )
        consulta_service_class.return_value.close_connection.assert_called_once()
        self.assertEqual(response, {"message": "Consulta agendada com sucesso"})


if __name__ == "__main__":
    unittest.main()