from dataclasses import dataclass


@dataclass(frozen=True)
class LandParameter:
    land_fast_speed = 3.0
    land_low_speed = 0.4
    land_safe_hgt = 3.0

    def get_first_land_second_delta(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return drone_hgt_meter / self.land_low_speed
        return (drone_hgt_meter - self.land_safe_hgt) / self.land_fast_speed

    def get_first_land_altitude(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return 0
        return self.land_safe_hgt

    def get_second_land_second_delta(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return 0
        return self.land_safe_hgt / self.land_low_speed

    def get_second_land_altitude_start(self, drone_hgt_meter: float) -> float:
        if drone_hgt_meter < self.land_safe_hgt:
            return 0
        return self.land_safe_hgt

    def get_land_second_delta(self, drone_hgt_meter: float) -> float:
        return self.get_first_land_second_delta(
            drone_hgt_meter
        ) + self.get_second_land_second_delta(drone_hgt_meter)


LAND_PARAMETER = LandParameter()
