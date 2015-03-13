# ![Logo](https://raw.github.com/jhermann/kunstkopf/master/doc/_static/kunstkopf-logo-24.png) kunstkopf

[kunstkopf](http://en.wikipedia.org/wiki/Dummy_head_recording)
[[ˈkʊnstkɔp͜f](https://translate.google.com/#de/de/Kunstkopf)]
is a home for tools that handle audio (meta-)data and control my hi-fi toys.


## Contributing

*kunstkopf* is written in [Python](http://www.python.org/),
and the documentation is generated using [Sphinx](https://pypi.python.org/pypi/Sphinx).
[Paver](https://pypi.python.org/pypi/Paver) is used to build and manage the project.

To set up a working directory, follow these steps:

    git clone https://github.com/jhermann/kunstkopf.git
    cd kunstkopf
    virtualenv --no-site-packages .
    . bin/activate
    pip install -r requirements.txt
    paver init

*kunstkopf* can also be found on [PyPI](https://pypi.python.org/pypi/kunstkopf)
and [Ohloh](https://www.ohloh.net/p/kunstkopf).


## License

*kunstkopf* is released under the
[GNU General Public License 3.0](http://www.gnu.org/licenses/gpl-3.0.txt),
see LICENSE for details.
