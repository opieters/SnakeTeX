# The Command Line Interface (CLI)

The main interface for most users will be the command line interface (CLI). This provides the necessary tools for most users to compile and build their LaTeX projects. First we will go through basic commands with the example we created earlier in [the SnakeTeX template walkthrough](snaketex.md).

The programme is called be invoking the `stex`command in the regular shell. You can see all options by passing the `--help` option to the programme:

```shell
$ stex --help
```

## Compiling a Project

Once the `config.yml` file has been set-up, compiling a project is as easy as this:

```shell
$ stex compile
```

This will create the output `.tex` file in the `build` folder (unless otherwise) specified along with all the required assets (in the `assets` folder by default).

The above way is the easiest, but for large files and multi-user projects it might not always be necessary to compile the entire project and only the part you're currently working on. This is possible by specifying the parts _that need to be compiled_ after the `compile` command.

Only compiling `chapter1` and `chapter2` can be done with:

```shell
$ stex compile chapter1 chapter2
```

You can add as many as you like.

## Building a Project

After compiling a project, you probably want to build it. This is done with the `build` command. No optional arguments are possible:

```shell
$ stex build
```

This will create the output PDF file that can be distributed. It is important to mention that the produced PDF file is a clean file. By clean file we mean that it was compiled for a sufficient number of times to get all labels, float placements and tables correct. This is usually not the case after the first run.

## A Fresh Start

Sometimes assets might change or you just want to clean the build directory. This can be dome through the `clean` command:

```shell
$ stex clean
```

This will _clear all files_ from the build directory.

## Non-default Configuration

Users that want to use a different name for the SnakeTeX configuration file can do so by passing the `--config` option along with the filename to the `stex` command. This can be specified **before** any of the above commands.

For those who would like to see more text-based output while running the commands should provide the `--debug` flag. This is not necessary for regular users. 
