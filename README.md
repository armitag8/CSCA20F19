# CSCA20F19
Resources for students of CSCA20, hosted [here](https://armitag8.github.io/CSCA20F19)

## Build and Run
This command should work on any machine with Python, as long
as the command is being run from a command line (BASH, CMD, etc.)
whose current working directory is a local copy of the root of this
repository:

```
pip install SimpleHTTP404Server
cd docs
python -m SimpleHTTP404Server
```

**Note** It may be necessary to replace "python3" with just "python" on **Windows**.

Now, you can visit your local build of this website at:
```
http://localhost:8000
``` 

## Contributing

Any cool projects from students, educators or alumni of CSCA20 at UTSC are welcome. Just submit a PR, or contact me directly.

- Any Scratch project is added simply by:
    - putting the Scratch Project ID into `docs/scratchProjects.js` **OR**
    - putting your Scratch User ID into the `docs/scratchProjects.js` (for all your public projects to be shown)
- Any Python project is added by:
    - putting Python files and a `README.md` into a new folder in `examples/` **AND**
    - adding to `docs/scratchProjects.js`

Please make sure you test that your additions work by building, running and checking the website still works as above before you submit a PR.