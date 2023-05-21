#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path

# The following file describes how a cli can be represented using python data structures.
# In effect, this is a json representation of a cli, however we must represent the handler functions.
# A simple function (make_parser) can be used to generate a parser from this.

ABOUT = "about"
FLAGS = "flags"
SUBCOMMANDS = "subcommands"
DEFAULTS = "defaults"
ARGS = "args"
HANDLER = "handler"


def make_parser(name, data, parser=None):
    constructor_args = data.get(ABOUT, {})
    # override any "prog" name.
    constructor_args["prog"] = name
    if parser is None:
        parser = argparse.ArgumentParser(**constructor_args)
    else:
        subparser = parser
        parser = subparser.add_parser(name, **constructor_args)

    handler = data.get(HANDLER, lambda _: parser.print_help())
    defaults = data.get(DEFAULTS, {})
    defaults["func"] = defaults.get("func", handler)
    parser.set_defaults(**defaults)

    flags = data.get(FLAGS, {})
    for flag, kwargs in flags.items():
        parser.add_argument(*flag.split(","), **kwargs)

    args = data.get(ARGS, [])
    for (arg, kwargs) in args:
        parser.add_argument(arg, **kwargs)

    subcommands = data.get(SUBCOMMANDS, {})
    if subcommands:
        subparser = parser.add_subparsers(title="Available Commands")
        for k, v in subcommands.items():
            make_parser(k, v, parser=subparser)

    return parser


app_name = "my_app"

config_dir = Path.joinpath(Path.home(), ".config", app_name)
config_file = Path.joinpath(config_dir, "config.json")


def create_config(config_file, prompt=True):    
    p = Path(config_file)
    if not p.exists():
        if prompt:
            result = input("Create '{}' [y/N]\n".format(p))
            if result != "y":
                exit()
        config_dir = Path(config_file).parent
        logging.debug("Creating config directory: {}".format(config_dir))
        config_dir.mkdir(parents=True, exist_ok=True)
        logging.debug("Creating config file: {}".format(config_file))
        p.touch(exist_ok=True)

def initialize(args):
    create_config(args.get("config"), prompt=args.get("prompt"))

app = {
    ABOUT: {
        "description": "Welcome to my command line interface",
        "epilog": "Text following the argument descriptions"
    },
    FLAGS: {
        "--flag-one": {
            "metavar": "STRING",
            "type": str,
            "default": "some default value",
            "help": "Use flag one to do something",
        },
        "--flag-two": {
            "metavar": "COUNT",
            "type": int,
            "default": 5,
            "help": "Use flag two to do something else",
        },
        "--verbose,-v": {
            "action": "count",
            "help": "Set the verbosity level for logging",
            "default": 0
        },
        "--config": {
            "metavar": "PATH",
            "type": str,
            "help": "Path to a custom config file",
            "default": str(config_file),
        },
    },
    SUBCOMMANDS: {
        "init": {
            ABOUT: {
                "description": "Initialize the application. Required if you do not wish to explicitly specify a config file.",
            },
            FLAGS: {
                "--no-prompt": {
                    "action": "store_false",
                    "dest": "prompt",
                    "help": "Do not prompt for confirmation",
                }
            },
            HANDLER: initialize
        },
        "sub1": {
            ABOUT: {
                "description": "A description of sub1",
                "epilog": "this is the epilog for sub1",
                "help": "Help for sub1",
            },
            SUBCOMMANDS: {
                "sub1.1": {
                    ABOUT: {
                        "description": "A description of sub1.1",
                        "help": "Help for sub1.1",
                    },
                    HANDLER: lambda x: print("handler for sub1.1"),
                },
                "sub1.2": {
                    ABOUT: {
                        "description": "A description of sub1.2",
                        "help": "Help for sub1.2",
                    },
                    FLAGS: {
                        "--query,-q": {
                            "type": str,
                            "metavar": "<key>=<value>",
                            "action": "append",
                            "help": "Query parameter.Can use multiple.",
                        }
                    },
                    ARGS: [
                        (
                            "arg1",
                            {
                                "type": str,
                                "help": "Help for 'arg1' of sub1.2",
                            },
                        )
                    ],
                    HANDLER: lambda x: print("handler for sub1.2"),
                }
            },
        },
        "sub2": {
            ABOUT: {
                "description": "A description of sub2",
                "epilog": "this is the epilog for sub2",
                "help": "Help for sub2",
            },
            SUBCOMMANDS: {
                "sub2.1": {
                    ABOUT: {
                        "description": "A description of sub2.1",
                        "help": "Help for sub2.1",
                    },
                    HANDLER: lambda x: print("handler for sub2.1"),
                },
            }
        },
    },
}


p = make_parser(app_name, app)

if __name__ == '__main__':
    namespace = p.parse_args()
    loggingLevel = {
        0: logging.CRITICAL,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(min(namespace.verbose, 3))
    logging.basicConfig(encoding="utf-8", level=loggingLevel)
    namespace_dict = vars(namespace)
    logging.debug(namespace_dict)
    namespace.func(namespace_dict)
