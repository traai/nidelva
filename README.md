# nidelva
Simulator for RL experiments

Work in progress.

Rough outline,

- Config -> Simulator.load_config -> Simulator.build_env -> environment
- Configs come from either json/xml/whatever files stored on disk
- Can also be created dynamically directly in python
- Simulator can resolve symbols from configs to actual environments/functions/whatever
