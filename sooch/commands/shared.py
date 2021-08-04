from typing import Optional


class Services:
    def __init__(self):
        self.player_svc: Optional['Players'] = None
        self.reg_buildings_svc: Optional['RegBuildings'] = None


services = Services()
