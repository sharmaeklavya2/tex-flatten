# TeX-Flatten

Usually I split my TeX projects into multiple files.
But some conferences/journals ask for a single TeX file.
The script `tex-flatten.py` converts a multi-file project into a single TeX file.

## Features

* Removes comments (text after `%` in each line).

* Allows removing content in certain environments.
This is useful for removing conditional excludes,
like those offered by the [`comment`](https://ctan.org/pkg/comment) package.
By default, only the `comment` environment is ignored.
You can add additional ones using the `--ignore` command-line option.

* Code between the lines `% tex-flatten:ignore-begin`
and `% tex-flatten:ignore-end` is ignored.

* Replaces all `\input` commands by their file contents
(except the ones inside comments and ignored environments).

* Optionally, using the `--bbl-to-read` command-line option,
one can replace BibTeX commands by the entire bibliography from the `.bbl` file.

Run `python tex-flatten.py --help` to see the full command-line syntax.

## Example

    cd example
    python ../tex-flatten.py main.tex
