from farms.farm import Farm, FieldData
from helpers.helper import Helper


class PlantFarm(Farm):
    WHEAT = 1
    CORN = 2
    CLOVER = 3
    RAPESEED = 4
    SUGAR_BEETS = 5
    HERBS = 6
    SUNFLOWER = 7
    BACHELORS_BUTTONS = 8
    CARROT = 17
    CUCUMBER = 18
    RADISH = 19
    STRAWBERRY = 20
    TOMATO = 21
    ONION = 22
    SPINACH = 23
    CAULIFLOWER = 24
    POTATO = 26
    ASPARAGUS = 29
    ZUCCHINI = 31
    BERRIES = 32
    RASPBERRIES = 33
    THISTLES = 108
    DAISIES = 109
    TEA = 129


    plant_range = {
        WHEAT: 2,
        CORN: 4,
        CLOVER: 2,
        RAPESEED: 4,
        SUGAR_BEETS: 4,
        HERBS: 4,
        SUNFLOWER: 4,
        BACHELORS_BUTTONS: 4,
        CARROT: 1,
        CUCUMBER: 1,
        RADISH: 1,
        STRAWBERRY: 1,
        TOMATO: 1,
        ONION: 1,
        SPINACH: 1,
        CAULIFLOWER: 1,
        POTATO: 1,
        ASPARAGUS: 2,
        ZUCCHINI: 1,
        BERRIES: 1,
        RASPBERRIES: 1,
        THISTLES: 4,
        DAISIES: 4,
        TEA: 4,
    }

    def __init__(self, farm_id, position, buildingid, level, status, animals, product, name, client, items, seed):
        super().__init__(farm_id, position, buildingid, level,
                         status, animals, product, name, client, items, seed)
        self.fields = None
        self.update()
        


    def update(self):
        self.init_garden()


    def collect(self):
        self.update()
        self.harvest()
        self.plant(seed=self.seed)
        self.water()


    def init_garden(self) -> list:
        params = {
            "rid": self.client.rid,
            "mode": "gardeninit",
            "farm": self.farm_id,
            "position": self.position,
        }

        rsp_data = self.fetch_farm_data(params=params)
        if rsp_data is not None:
            fields_data = rsp_data['datablock'][1]
            fields = []
            for field_id, field_data in fields_data.items():
                if field_id == "water":
                    break
                field = FieldData(
                    field_id=field_data["teil_nr"],
                    plant=field_data["inhalt"],
                    planted=field_data["gepflanzt"],
                    collection_at=field_data["zeit"],
                    watered=field_data["wasser"],
                    guild=field_data["guild"],
                    buildingid=field_data["buildingid"],
                    x=field_data["x"],
                    y=field_data["y"],
                    iswater=field_data["iswater"],
                    phase=field_data["phase"]
                )
                fields.append(field)

            self.fields = fields

    
    def harvest(self):
        params = {
            "rid": self.client.rid,
            "mode": "cropgarden",
            "farm": self.farm_id,
            "position": self.position
        }
        response = self.fetch_farm_data(params=params)
        
        if response is not None:
            if type(response["datablock"]) == list:
                Helper.response(self.farm_id, self.position, "There are no ready-made plants here yet")
            else:
                self.update()
                Helper.response(self.farm_id, self.position, "All the crops have been harvested")


    def get_empty_fields(self):
        used_fields = [data.field_id for data in self.fields]
        all_field_ids = [i for i in range(1, 121)]

        missing_field_ids = [
            field_id for field_id in all_field_ids if str(field_id) not in used_fields]
        return missing_field_ids


    def get_unwatered_fields(self):
        unwatered_fields = [int(field.field_id)
                            for field in self.fields if field.iswater is False]
        return unwatered_fields

    def calculate_area(self, fields, field_range):
        blocked_fields = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
        area = []
        for field in fields:
            if field not in area:
                if field_range == 2 and field not in blocked_fields:
                    f = [field, field + 1]
                elif field_range == 4 and field not in blocked_fields:
                    f = [field, field + 1, field + 12, field + 13]
                else:
                    f = [field]
                area.extend(f)

        new_area = []
        for i in range(0, len(fields), field_range):
            new_area.append(','.join(map(str, area[i:i+field_range])))

        return new_area


    def plant(self, seed: int, cid=22):
        field_range = self.plant_range.get(seed)
        empty_fields = self.get_empty_fields()
        if not empty_fields:
            Helper.response(self.farm_id, self.position, "No ready-made plants")
            return 0

        fields_area = self.calculate_area(
            fields=empty_fields, field_range=field_range)

        params = ""
        for i in range(len(fields_area)):
            val = f"&pflanze[]={seed}&feld[]={fields_area[i].split(',')[0]}&felder[]={fields_area[i]}"
            params = params + val

        params = params + f"&cid={cid}"
        url = f"{self.client.url}?rid={self.client.rid}&mode=garden_plant&farm={self.farm_id}&position={self.position}" + params

        response = self.fetch_farm_data(url=url)
        if response is not None:
            self.update()
            Helper.response(self.farm_id, self.position, "All the crops have been planted")


    def water(self):
        unwatered_fields = self.get_unwatered_fields()
        if not unwatered_fields:
            Helper.response(self.farm_id, self.position, "No plants to water")
            return 0

        unwatered_fields_cpy = unwatered_fields.copy()
        fields_area = []

        while unwatered_fields_cpy:
            for field in self.fields:
                first_element = unwatered_fields_cpy[0]
                if int(field.field_id) == first_element:
                    field_range = field.x * field.y
                    area = self.calculate_area(
                        [first_element], field_range)
                    fields_area.extend(area)
                    int_area = [int(x) for x in area[0].split(',')]
                    unwatered_fields_cpy = [
                        x for x in unwatered_fields_cpy if x not in int_area]
                if not unwatered_fields_cpy:
                    break

        params = ""
        for i in range(len(fields_area)):
            val = f"&feld[]={fields_area[i].split(',')[0]}&felder[]={fields_area[i]}"
            params = params + val

        url = f"{self.client.url}?rid={self.client.rid}&mode=garden_water&farm={self.farm_id}&position={self.position}" + params

        response = self.fetch_farm_data(url=url)
        if response is not None:
            self.update()
            Helper.response(self.farm_id, self.position, "All the crops have been watered")