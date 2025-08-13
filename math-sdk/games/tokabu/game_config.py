import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode
import random
from src.executables.executables import Executables

class GameExecutables(Executables):
    # If your template already has pre_spin, just add the body below to it.
    def pre_spin(self, gamestate):
        cfg = gamestate.config

        # Pick a random height for each reel in [rows_min[i], rows_max[i]]
        heights = [random.randint(cfg.rows_min[i], cfg.rows_max[i]) for i in range(cfg.num_reels)]
        cfg.num_rows = heights  # <-- engine expects a list here when it builds the board

        # (Optional) expose current ways to UI/analytics
        try:
            ways = 1
            for h in heights:
                ways *= h
            # stash anywhere your stack expects context (if available)
            gamestate.context["tokabu_ways"] = ways
        except Exception:
            pass

        # If your base class has important logic, keep it
        try:
            super().pre_spin(gamestate)
        except AttributeError:
            # base may not define pre_spin; ignore
            pass

class GameConfig(Config):
    """Game specific configuration class (Tokabu – Megaways-style)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        # --- IDs / meta ---
        self.game_id = "tokabu"                 # lowercase id is handy for paths
        self.provider_number = 0
        self.working_name = "Tokabu Ways"
        self.wincap = 5000
        self.win_type = "ways"                  # keep ways
        self.rtp = 0.97
        self.construct_paths()

        # --- Megaways-style dimensions ---
        # 6 reels, variable rows each spin (engine should choose a height per reel in [min,max])
        self.num_reels = 6

        # If your engine supports variable heights via min/max, set these:
        self.rows_min = [2,2,2,2,2,2]
        self.rows_max = [7,7,7,7,7,7]

        # If the framework expects num_rows when heights are fixed, set it to None/empty so
        # the variable-height logic kicks in. (If your engine ignores this, it’s harmless.)
        self.num_rows = self.rows_max[:]

        # Optional: enable cascades/tumbles if supported by your executable
        # (set to False if your current game_executables doesn’t implement it yet)
        self.tumbles = True

        # --- Board & Symbol Properties (example pays, per 1.0 bet) ---
        # Your original had 3–5 of a kind. Megaways usually pays up to 6.
        # Keep your existing values for 3–5 and add 6OAK scaling.
        self.paytable = {
            # High symbols
            (6, "H1"): 25, (5, "H1"): 10, (4, "H1"): 5,  (3, "H1"): 3,
            (6, "H2"): 10, (5, "H2"): 8,  (4, "H2"): 4,  (3, "H2"): 2,
            (6, "H3"): 6,  (5, "H3"): 5,  (4, "H3"): 2,  (3, "H3"): 1,
            (6, "H4"): 4,  (5, "H4"): 3,  (4, "H4"): 1,  (3, "H4"): 0.5,
            (6, "H5"): 3,  (5, "H5"): 2,  (4, "H5"): 0.8,(3, "H5"): 0.4,
            # Low symbols
            (6, "L1"): 2.0,(5, "L1"): 2,  (4, "L1"): 0.8,(3, "L1"): 0.4,
            (6, "L2"): 1.6,(5, "L2"): 1.5,(4, "L2"): 0.5,(3, "L2"): 0.2,
            (6, "L3"): 1.6,(5, "L3"): 1.5,(4, "L3"): 0.5,(3, "L3"): 0.2,
            (6, "L4"): 1.2,(5, "L4"): 1,  (4, "L4"): 0.3,(3, "L4"): 0.1,
        }

        self.include_padding = True
        # Keep your symbol roles; add others later if you introduce e.g. multiplier wilds
        self.special_symbols = {"wild": ["W"], "scatter": ["S"], "multiplier": []}

        # --- Triggers (Megaways style usually 4+ to start; tweak as you like) ---
        # Base: 4+ scatters → FS; FreeGame retriggers on 3+ or 2+ depending on design
        self.freespin_triggers = {
            self.basegame_type: {4: 10, 5: 15, 6: 20},
            self.freegame_type: {3: 5, 4: 8, 5: 10},   # retrigger amounts
        }
        self.anticipation_triggers = {self.basegame_type: 3, self.freegame_type: 2}

        # --- Reels / reel weights selection ---
        # Keep your CSV mapping; BR0/FR0/FRWCAP can still be used as “symbol pools”
        # The engine should sample symbols to fill each reel’s variable height per spin
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "FRWCAP": "FRWCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        # --- Bet modes / distributions unchanged except for scatter counts we tweaked above ---
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "FRWCAP": 5},
                            },
                            "force_wincap": True,
                            "force_freegame": True,
                            # If you want 4+ scatters everywhere, change these too:
                            "scatter_triggers": {4: 100, 5: 20, 6: 5},
                            "mult_values": {1: 20, 2: 50, 3: 80, 4: 100, 5: 20},
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {4: 100, 5: 20, 6: 5},
                            "mult_values": {1: 200, 2: 100, 3: 80, 4: 50, 5: 20},
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "mult_values": {1: 1},
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                            "mult_values": {1: 1},
                        },
                    ),
                ],
            ),
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "FRWCAP": 5},
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {4: 100, 5: 20, 6: 5},
                            "mult_values": {1: 20, 2: 100, 3: 80, 4: 90, 5: 80},
                        },
                    ),
                ],
            ),
        ]
