class AppCore:
    def __init__(self, output=None):
        # Permite inyección de dependencias (clave para testing)
        self._output = output

    def run(self) -> int:
        message = self._build_message()
        self._write(message)
        return 0

    def _build_message(self) -> str:
        return "Hello from AppCore"

    def _write(self, message: str) -> None:
        if self._output:
            self._output.write(message + "\n")
        else:
            print(message)
