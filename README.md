# PyNetuse

PyNetuse is a python wrapper for Microsoft Windows `net use` command. The usage is simmilar to `net use` command, however there are few differences. See examples for more details.

**Note:** Version 1.0.x does not handle user privileges and credentials for mounting. This will be implemented in further versions.


## Examples

### List active connections

An alternative to `net use` command.

```python
from pynetuse.netuse import net_use

net_use() # Returns a list of NetUseConnectionObjects: [{driveLetter: "X:", networkPath: r"\\server\foo"}] or [] if no connections

```

### Connect new shared drive

An alternative to `net use X: \\server\foo` command.

```python
from pynetuse.netuse import net_use

connection = net_use(drive_letter="X:", network_path=r"\\server\foo")

print(connection) # {driveLetter: "X:", networkPath:r"\\server\foo"} - the new connection

```

### Delete shared drive

An alternative to `net use X: /delete`. Specify `force=True` if the disconnection shall be forced.

```python
from pynetuse.netuse import net_use

connection = net_use()[0]
connection.delete()

```