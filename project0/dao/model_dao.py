from abc import ABC, abstractmethod


class ModelDAO(ABC):
    @abstractmethod
    def new_object(self, obj, other):
        pass

    @abstractmethod
    def get_object(self, obj_id, other_id):
        pass

    @abstractmethod
    def get_all_objects(self):
        pass

    @abstractmethod
    def update_object(self, obj_id):
        pass

    @abstractmethod
    def delete_object(self, obj_id, other_id):
        pass
