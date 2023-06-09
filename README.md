# python-cli-template
A template for creating cli tools using python.

```python
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

```

```
$ ./main.py
usage: my_app [-h] [--flag-one STRING] [--flag-two COUNT] [--verbose] {sub1,sub2} ...

Welcome to my command line interface

options:
  -h, --help         show this help message and exit
  --flag-one STRING  Use flag one to do something
  --flag-two COUNT   Use flag two to do something else
  --verbose, -v      Log additional information

Available Commands:
  {sub1,sub2}
    sub1             Help for sub1
    sub2             Help for sub2

Text following the argument descriptions
```
