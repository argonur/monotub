from abc import ABC, abstractmethod

from monotub.measurement import Measurement


class DataSink(ABC):

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    def write(self, measurement: Measurement) -> None:
        ...

    @abstractmethod
    def cleanup(self) -> None:
        ...