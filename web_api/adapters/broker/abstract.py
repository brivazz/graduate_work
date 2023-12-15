import abc


class AbstractQueue(abc.ABC):
    @abc.abstractmethod
    async def send_data(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def read_data(self, *args, **kwargs):
        raise NotImplementedError
