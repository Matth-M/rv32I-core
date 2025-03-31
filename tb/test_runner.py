import os
from pathlib import Path
from cocotb.runner import get_runner

def generic_tb_runner(design_name):
    sim = os.getenv("SIM", "verilator")
    proj_path = Path(__name__).resolve().parent.parent
    sources = list(proj_path.glob("src/*.sv"))
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=f"{design_name}",
        build_dir=f"./{design_name}/sim_build",
        build_args=[] # use this to add args for verilator
    )
    runner.test(hdl_toplevel=f"{design_name}", test_module=f"tb_{design_name}", test_dir=f"./{design_name}")


if __name__ == "__main__":
    generic_tb_runner("sign_extender")
