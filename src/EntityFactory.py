class EntityFactory:
    @staticmethod
    def get_entity(entity_type, x, y):
        if entity_type == "Enemy":
            return Enemy(x, y)
        elif entity_type == "Seed":
            return Seed(x, y)
        return None