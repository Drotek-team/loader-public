import pytest
from pytest_examples import (  # pyright: ignore # TODO(jonathan): Fix pytest-examples
    CodeExample,
    EvalExample,
    find_examples,
)


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
    if eval_example.update_examples:  # pragma: no cover
        eval_example.format(example)
        eval_example.run_print_update(example)
    else:
        eval_example.lint(example)
        eval_example.run_print_check(example)
