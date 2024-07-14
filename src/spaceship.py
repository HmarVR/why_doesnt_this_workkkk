from typing import TYPE_CHECKING
from struct import pack


if TYPE_CHECKING:
    from main import Game
    import zengl


def state(func):
    def wrapper(self, *args, **kwargs):
        if self.app.share_data["state"] == "space":
            return func(self, *args, **kwargs)
        else:
            return None
    return wrapper


class SpaceShip:
    def __init__(
        self, app: "Game", vao_name="spaceship", pos=(0, 0, 0), roll=0, scale=(1, 1)
    ) -> None:
        self.app = app
        self.ctx: zengl.context = app.ctx
        self.vao_name = vao_name

        self.app.share_data["spaceship"] = self
        
        self.fuel = 100
        self.fuel_max = 100
        
        self.app.share_data["fuel"] = self.fuel
        self.app.share_data["fuel_max"] = self.fuel_max
        
    @state
    def update(self):
        self.app.share_data["fuel"] = self.fuel
        self.app.share_data["fuel_max"] = self.fuel_max
        self.render()

    def render(self):
        pass
        # self.init_uniforms()
        # self.vao.render()
        
    def destroy(self):
        pass