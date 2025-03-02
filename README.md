# scripts
Developer helper scripts
## Instalation
```bash
./install.sh
```
## Usage
### Contextify (ctx)
```bash
ctx
```
Create a context within a project for LLMs. 
Fuzzy find and select directories with `<TAB>` and create context with `<ENTER>`.
Context is saved to clipboard and can be pasted in your favorite LLM chat.

### Nest.js module generation (modgen)
```bash
modgen sample-module 'property1:string,property2:number' -a
```
Create a Nest.js module with prepopulated properties.
If -a is provided module will contain controller, service, repository and its interfaces.
If -s is provides module will contain service, repository and its interfaces.
Else the module will contain only repository and its inteface.

### Workspace (work)
```bash
work
```
Opens a tmux session with split window with NeoVIM and terminal.
Another window is opened with just terminal in second tab.
