import pytest
from pytest_examples import CodeExample, EvalExample, find_examples

IGNORE_PRINTS_START_LINES = {370}


@pytest.mark.parametrize("example", find_examples("README.md"), ids=str)
def test_readme(example: CodeExample, eval_example: EvalExample) -> None:
    eval_example.set_config(
        quotes="double",
        target_version="py38",
        upgrade=True,
        isort=True,
        ruff_select=["ALL"],
        ruff_ignore=["D10", "T20"],
    )
    if eval_example.update_examples:
        eval_example.format(example)
        if example.start_line not in IGNORE_PRINTS_START_LINES:
            eval_example.run_print_update(example)
        else:
            eval_example.run(example)
    else:
        eval_example.lint(example)
        if example.start_line not in IGNORE_PRINTS_START_LINES:
            eval_example.run_print_check(example)
        else:
            eval_example.run(example)
