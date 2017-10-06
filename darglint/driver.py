"""Defines the command line interface for darglint."""
import ast
import sys

from .darglint import (
    read_program,
    FunctionDescription,
    get_function_descriptions,
)
from .lex import lex
from .parse import parse_arguments, parse_return
from .errors import (
    ExcessParameterError,
    ExcessReturnError,
    MissingParameterError,
    MissingReturnError,
)


class IntegrityChecker(object):
    """Checks the integrity of the docstring compared to the definition."""

    def __init__(self):
        """Create a new checker for the given function and docstring."""
        self.function = None  # type: FunctionDescription
        self.errors = list()  # type: List[DarglintError]
        self._sorted = True

    def run_checks(self, function: FunctionDescription):
        """Run checks on the given function.

        Args:
            function: A function whose docstring we are verifying.

        """
        self.function = function
        self._check_parameters()
        self._check_return()
        self._sorted = False

    def _check_return(self):
        docstring = self.function.docstring
        doc_return = len(parse_return(lex(docstring))) > 0
        fun_return = self.function.has_return
        if fun_return and not doc_return:
            self.errors.append(
                MissingReturnError(self.function.function)
            )
        elif doc_return and not fun_return:
            self.errors.append(
                ExcessReturnError(self.function.function)
            )

    def _check_parameters(self):
        docstring = self.function.docstring
        docstring_arguments = set(parse_arguments(lex(docstring)))
        actual_arguments = set(self.function.argument_names)
        missing_in_doc = actual_arguments - docstring_arguments
        for missing in missing_in_doc:
            self.errors.append(
                MissingParameterError(self.function.function, missing)
            )
        missing_in_function = docstring_arguments - actual_arguments
        for missing in missing_in_function:
            self.errors.append(
                ExcessParameterError(self.function.function, missing)
            )

    def _sort(self):
        if not self._sorted:
            self.errors.sort(key=lambda x: x.function.lineno)
            self._sorted = True

    def get_error_report(self) -> str:
        """Return a string representation of the errors.

        Returns:
            A string representation of the errors.

        """
        if len(self.errors) == 0:
            return ''
        self._sort()
        current_function = self.errors[0].function
        ret = ['{} {}'.format(current_function.lineno, current_function.name)]
        for error in self.errors:
            if error.function != current_function:
                current_function = error.function
                ret.append(
                    '{} {}'.format(
                        current_function.lineno,
                        current_function.name,
                    )
                )
            ret.append('  ' + error.message)
        return '\n'.join(ret)


def main():
    """Check the parameters of all functions and methods."""
    program = read_program(sys.argv[1])
    tree = ast.parse(program)
    functions = get_function_descriptions(tree)
    checker = IntegrityChecker()
    for function in functions:
        checker.run_checks(function)
    print(checker.get_error_report())


if __name__ == '__main__':
    main()
