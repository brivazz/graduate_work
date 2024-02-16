import abc


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    async def set_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, *args, **kwargs):
        raise NotImplementedError
