import os
from pathlib import Path

from cocotb.runner import get_runner


def generic_tb_runner(design_name: str, project_path: Path):
    sim = os.getenv("SIM", "verilator")
    sources = list(project_path.glob("src/*.sv"))
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=f"{design_name}",
        build_dir=project_path.joinpath(f"tb/{design_name}/sim_build"),
        build_args=[],  # use this to add args for verilator
    )
    runner.test(
        hdl_toplevel=f"{design_name}",
        test_module=f"tb_{design_name}",
        test_dir=project_path.joinpath(f"tb/{design_name}"),
    )


if __name__ == "__main__":
    # Find project root, containing the .git directory
    # Allows the test runner to be ran from root or tb/
    project_path = Path(__name__).resolve().parent
    directory_content = os.listdir(project_path)
    if ".git" not in directory_content:
        project_path = project_path.parent

    # Launch testbenches
    generic_tb_runner("sign_extender", project_path)
    generic_tb_runner("regfile", project_path)
    generic_tb_runner("program_counter", project_path)
    generic_tb_runner("instruction_memory", project_path)
