#!/usr/bin/env python3

import argparse

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
            "action": "store_true",
            "help": "Log additional information",
        },
    },
    SUBCOMMANDS: {
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


p = make_parser("my_app", app)

if __name__ == '__main__':
    args = p.parse_args()
    args.func(args)
