from asciimatics.exceptions import NextScene, ResizeScreenError
from asciimatics.screen import Screen
from shadowlands.tui.scenes.loading import LoadingScene
from shadowlands.sl_dapp import ExitDapp, RunDapp
from shadowlands.tui.errors import ExitTuiError, PriceError
from shadowlands.tui.scenes.main import MainScene
from shadowlands.tui.debug import debug
from shadowlands.credstick import Credstick
import sys

#debug(self._screen._screen); import pdb; pdb.set_trace()
#debug(screen._screen); import pdb; pdb.set_trace()

class Interface():
    
    def __init__(self, _eth_node, config, preloaded_dapp=None):
        self._node = _eth_node
        self._config = config
        self._screen = None
        self._credstick = None
        self._loading_scene = True
        self._load_dapp = preloaded_dapp
        self._block_callback_watcher = None

    @property
    def credstick(self):
        return self._credstick

    @credstick.setter
    def credstick(self, credstick):
        self._credstick = credstick

    @property
    def node(self):
        return self._node

    @property
    def config(self):
        return self._config
        
    def tui(self, screen):
        self._screen = screen

        scenes = []
        if self._loading_scene:
            scenes.append(LoadingScene(self._screen, "LoadingScene", self))

        scenes.append(MainScene(self._screen, "Main", self))

        screen.play(scenes, stop_on_resize=True)


    def load(self):
        current_dapp = None

        while True:
            try:
                #raise RunDapp
                screen = Screen.wrapper(self.tui)
                break
            except ResizeScreenError as e:
                #debug(); import pdb; pdb.set_trace()
                # TODO make ResizeScreenError just raise NextScene
                pass
            except RunDapp:
                print("switching to dapp...")
                # load dapp from wherever it is
                from dapp import Dapp
                current_dapp = Dapp(screen, self.node)         
            except ExitDapp:
                del(sys.modules['dapp'])
            except ExitTuiError:
                print("Shutting it all down...")
                break

