from helpers import search_data
import state

class ClassFactory:
    """Construct a new class with members matching the key-value pairs of the provided data"""
    def __init__(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

class Wargear(ClassFactory):
    def __init__(self, data):
        ClassFactory.__init__(self, data)

class Model(ClassFactory):
    def __init__(self, data):
        ClassFactory.__init__(self, data)
        self.init_damage_profiles()
        self.wargear: list[Wargear] = []

        # Add default wargear
        # Prompt for mapped wargear

    def add_wargear(self, wg:Wargear):
        """Add an already-instantiated Wargear object"""
        self.wargear.append(wg)

    def remove_wargear(self, index:int):
        """Remove a wargear by its index"""
        self.wargear.pop(index)

    def init_damage_profiles(self):
        self.damage_profiles = []
        profiles = search_data(state.damage_profiles_csv, datasheet_id=self.datasheet_id)
        if profiles:
            header_profile = profiles[0]
            profiles.pop(0)

            for profile in profiles:
                damage_profile = {}
                for col in ("Col1", "Col2", "Col3", "Col4", "Col5"):
                    if profile[col]:
                        damage_profile[header_profile[col]] = profile[col]
                self.damage_profiles.append(damage_profile)



