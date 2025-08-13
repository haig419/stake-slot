"""Main file for generating results for sample lines-pay game."""
from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    num_threads = 4
    rust_threads = 8
    batching_size = 1000
    compression = False
    profiling = False

    # SMALL counts for a smoke test
    num_sim_args = {"base": 2000, "bonus": 2000}

    run_conditions = {
        "run_sims": True,
        "run_optimization": False,
        "run_analysis": False,
        "run_format_checks": True,
    }
    target_modes = list(num_sim_args.keys())

    print("[tokabu] init config/state …")
    config = GameConfig()
    gamestate = GameState(config)
    print("[tokabu] publish dir:", config.paths.publish_files)

    if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
        optimization_setup_class = OptimizationSetup(config)

    if run_conditions["run_sims"]:
        print("[tokabu] create_books starting …")
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )
        print("[tokabu] create_books finished")

    print("[tokabu] writing configs …")
    generate_configs(gamestate)

    if run_conditions["run_optimization"]:
        print("[tokabu] optimization …")
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)

    if run_conditions["run_analysis"]:
        print("[tokabu] analysis …")
        custom_keys = [{"symbol": "scatter"}]
        create_stat_sheet(gamestate, custom_keys=custom_keys)

    if run_conditions["run_format_checks"]:
        print("[tokabu] format checks …")
        execute_all_tests(config)

    print("[tokabu] done.")

