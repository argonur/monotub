from unittest.mock import Mock
from core import AppCore

def test_run_writes_message_and_returns_zero():
    mock_output = Mock()

    core = AppCore(output=mock_output)
    result = core.run()

    # Verifica código de salida
    assert result == 0

    # Verifica que se escribió el mensaje correcto
    mock_output.write.assert_called_once_with("Hello from AppCore\n")


def test_build_message():
    core = AppCore()
    assert core._build_message() == "Hello from AppCore"
