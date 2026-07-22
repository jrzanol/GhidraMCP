# GhidraMCP — Available Tools

This document describes the tools exposed by `bridge_mcp_ghidra.py` and the
GhidraMCP plugin for Ghidra 12.1.2.

## Before You Start

- Open a program in Ghidra and keep `GhidraMCPPlugin` enabled.
- By default, the HTTP plugin listens at `http://127.0.0.1:8080/`.
- Configure your MCP client to start the bridge with the project's virtual
  environment Python executable.
- Addresses may use the same format displayed by Ghidra, such as `00523000` or
  `0x00523000`.
- The examples below show only the MCP call argument object. The exact method for
  selecting and invoking a tool depends on the MCP client.
- Write operations modify the open program and may create transactions in
  Ghidra's undo history.

## Listing and Search

### `list_methods`

Lists function names with pagination.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 100}`

### `list_classes`

Lists non-global namespaces and classes found in the program.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 50}`

### `list_segments`

Lists memory blocks/segments and their properties.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 100}`

### `list_imports`

Lists imported symbols.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 100}`

### `list_exports`

Lists exported functions and symbols.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 100}`

### `list_namespaces`

Lists non-global namespaces.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 100}`

### `list_data_items`

Lists defined data, including addresses and values.

- Parameters: `offset` (default `0`) and `limit` (default `100`).
- Example: `{"offset": 0, "limit": 100}`

### `search_functions_by_name`

Searches for functions whose names contain a substring.

- Parameters: `query`, `offset` (default `0`), and `limit` (default `100`).
- Example: `{"query": "Packet", "offset": 0, "limit": 50}`

### `list_functions`

Lists every function and entry-point address without pagination.

- Parameters: none.
- Example: `{}`

### `list_strings`

Lists defined strings and their addresses, with an optional content filter.

- Parameters: `offset` (default `0`), `limit` (default `2000`), and optional
  `filter`.
- Example: `{"offset": 0, "limit": 500, "filter": "login"}`

## Navigation, Decompilation, and Disassembly

### `get_function_by_address`

Returns the name, signature, entry point, and boundaries of the function that
starts at the given address.

- Parameter: `address`.
- Example: `{"address": "00523000"}`

### `get_current_address`

Returns the address currently selected in the Ghidra user interface.

- Parameters: none.
- Example: `{}`

### `get_current_function`

Returns the function containing the currently selected location.

- Parameters: none.
- Example: `{}`

### `decompile_function`

Finds a function by name and returns its decompiled C code.

- Parameter: `name`.
- Example: `{"name": "ProcessPacket"}`

### `decompile_function_by_address`

Decompiles the function at or containing the supplied address.

- Parameter: `address`.
- Example: `{"address": "00523000"}`

### `disassemble_function`

Returns a function's assembly instructions and end-of-line comments.

- Parameter: `address`.
- Example: `{"address": "00523000"}`

## Renaming and Type Changes

### `rename_function`

Finds a function by its current name and renames it.

- Parameters: `old_name` and `new_name`.
- Example: `{"old_name": "FUN_00523000", "new_name": "SetAction"}`

### `rename_function_by_address`

Finds a function by address and renames it.

- Parameters: `function_address` and `new_name`.
- Example: `{"function_address": "00523000", "new_name": "SetAction"}`

### `rename_data`

Renames the data symbol at the supplied address.

- Parameters: `address` and `new_name`.
- Example: `{"address": "00BC1EF8", "new_name": "g_pCollectionData"}`

### `rename_variable`

Renames a local variable inside a function identified by name.

- Parameters: `function_name`, `old_name`, and `new_name`.
- Example:
  `{"function_name": "ProcessPacket", "old_name": "local_10", "new_name": "packet"}`

### `set_function_prototype`

Parses and applies a new prototype to a function identified by address.

- Parameters: `function_address` and `prototype`.
- Example:
  `{"function_address": "00523000", "prototype": "void __cdecl SetAction(char *dst, char *src)"}`

### `set_local_variable_type`

Changes the type of a local variable in a function.

- Parameters: `function_address`, `variable_name`, and `new_type`.
- Example:
  `{"function_address": "00523000", "variable_name": "packet", "new_type": "PacketHeader *"}`

## Comments

### `set_decompiler_comment`

Sets a `PRE` comment, which is normally displayed in the decompiler.

- Parameters: `address` and `comment`.
- Example: `{"address": "00523000", "comment": "Validates the received packet"}`

### `set_disassembly_comment`

Sets an `EOL` comment displayed beside the instruction in the Listing.

- Parameters: `address` and `comment`.
- Example: `{"address": "00523010", "comment": "Player limit"}`

## Cross-References

### `get_xrefs_to`

Lists references that point to an address.

- Parameters: `address`, `offset` (default `0`), and `limit` (default `100`).
- Example: `{"address": "00523000", "offset": 0, "limit": 100}`

### `get_xrefs_from`

Lists references originating from an address.

- Parameters: `address`, `offset` (default `0`), and `limit` (default `100`).
- Example: `{"address": "00523000", "offset": 0, "limit": 100}`

### `get_function_xrefs`

Finds a function by name and lists references to it.

- Parameters: `name`, `offset` (default `0`), and `limit` (default `100`).
- Example: `{"name": "ProcessPacket", "offset": 0, "limit": 100}`

## Function Tags

### `list_function_tags`

Without an address, lists every tag defined in the program, its description, and
the number of functions using it. With an address, lists only the tags assigned to
the function at or containing that address.

- Optional parameter: `function_address`.
- List every tag: `{}`
- List tags assigned to one function: `{"function_address": "00523000"}`

### `add_function_tag`

Adds a tag to the function at or containing the supplied address. The tool rejects
thunk functions before starting a transaction. If the tag does not exist, it is
created; the description is used only during this initial creation.

- Parameters: `function_address`, `tag_name`, and optional `tag_description`.
- Example:
  `{"function_address": "00523000", "tag_name": "TMNativeAPI::Network", "tag_description": "Network functions"}`

## Script Execution

### `execute_ghidra_script`

Executes a trusted script found in an enabled `ghidra_scripts` directory. It
accepts a file name only, never a path. Output produced by `print`/`println` is
returned to the MCP client. Interactive scripts may wait for input in the Ghidra
window.

- Parameters: `script_name`, optional `arguments`, and `timeout_seconds` from `1`
  to `600` (default `120`).
- Example without arguments:
  `{"script_name": "ExportTMBasedef.java"}`
- Example with arguments:
  `{"script_name": "MyScript.java", "arguments": ["input", "output"], "timeout_seconds": 300}`

The execution endpoint accepts only local requests issued by the bridge. The
script still runs with the same permissions as the Ghidra process, so only execute
trusted files.
