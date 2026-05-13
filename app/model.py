from dataclasses import dataclass, asdict
import pandas as pd

@dataclass
class CollisionInput:

    collision_index: str

    road_type: str
    speed_limit: int
    light_conditions: str
    special_conditions_at_site: str
    urban_or_rural_area: str
    latitude: float
    longitude: float
    time: str
    number_of_vehicles: int
    number_of_casualties: int

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(self)])

@dataclass
class VehicleInput:

    collision_index: str
    vehicle_reference: int

    vehicle_type: str
    vehicle_manoeuvre: str
    skidding_and_overturning: str
    hit_object_in_carriageway: str
    vehicle_leaving_carriageway: str
    hit_object_off_carriageway: str
    first_point_of_impact: str
    vehicle_left_hand_drive: str
    age_band_of_driver: str

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(self)])

@dataclass
class CasualtyInput:

    collision_index: str
    vehicle_reference: int

    age_band_of_casualty: str
    pedestrian_location: str
    pedestrian_movement: str
    casualty_type: str

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(self)])

@dataclass
class AccidentEvent:

    collision: CollisionInput
    vehicles: list[VehicleInput]
    casualties: list[CasualtyInput]

    def to_dataframes(self):

        collision_df = self.collision.to_dataframe()

        vehicle_df = pd.concat(
            [v.to_dataframe() for v in self.vehicles],
            ignore_index=True
        )

        casualty_df = pd.concat(
            [c.to_dataframe() for c in self.casualties],
            ignore_index=True
        )

        return {
            "collision": collision_df,
            "vehicle": vehicle_df,
            "casualty": casualty_df
        }