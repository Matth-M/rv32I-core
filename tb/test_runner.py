import argparse
import os
from pathlib import Path
from typing import OrderedDict

from cocotb.runner import get_runner


def generic_tb_runner(design_name: str, project_path: Path):
    sim = os.getenv("SIM", "verilator")
    sources = list(project_path.glob("src/*.sv"))
    # Package needs to be the first source so other files can use it
    sources.insert(0, project_path.joinpath("src/pkg.sv"))
    sources = list(OrderedDict.fromkeys(sources))
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=f"{design_name}",
        build_dir=project_path.joinpath(f"tb/{design_name}/sim_build"),
        build_args=["-Wno-WIDTHTRUNC"],  # use this to add args for verilator
    )
    runner.test(
        hdl_toplevel=f"{design_name}",
        test_module=f"tb_{design_name}",
        test_dir=project_path.joinpath(f"tb/{design_name}"),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run testbenches.")
    parser.add_argument("--only", type=str, help="Run only the specified test.")
    args = parser.parse_args()

    # Find project root, containing the .git directory
    # Allows the test runner to be ran from root or tb/
    project_path = Path(__file__).resolve().parent
    directory_content = os.listdir(project_path)
    if ".git" not in directory_content:
        project_path = project_path.parent

    # Launch testbenches
    tests = ["sign_extender", "regfile", "program_counter", "memory", "cpu", "alu", "control"]
    if args.only:
        if args.only in tests:
            generic_tb_runner(args.only, project_path)
        else:
            print(
                f"Error: Test '{args.only}' not found in the list of available tests."
            )
    else:
        for t in tests:
            generic_tb_runner(t, project_path)
