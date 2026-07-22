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

## Bookmarks and Global Data

### `register_global_data`

Registers typed global data at an address and creates or promotes its label as the
primary symbol. Before changing the program, the tool checks whether the same
address already has an equivalent data type, total size, and primary label. If it
does, the tool reports that the global is already registered and makes no changes.
The same protection applies when the requested address falls anywhere inside an
existing defined data item. For example, an address at byte offset `8` inside an
array of 100 integers is reported as already covered; no overlapping global or
label is created.

- Parameters: `location`, `label`, `data_type`, `size`, and optional
  `replace_existing` (default `false`).
- Example:
  `{"location": "00BC1EF8", "label": "g_pCollectionData", "data_type": "DWORD", "size": 4}`
- Array example:
  `{"location": "00BC2000", "label": "g_itemIds", "data_type": "DWORD", "size": 64}`

The data type must already exist in Ghidra, except for common built-in aliases and
pointer types. When `size` is a compatible multiple of a fixed-size type, the tool
creates an array. A new larger declaration automatically consumes fully contained
smaller data declarations and removes their labels. For example, creating ten
integers may absorb a previously defined integer in the middle of that range. A
data item that crosses the requested end remains protected, and the error reports
the exact conflict address and both ranges. Instructions are also protected unless
`replace_existing` is `true`.

### `delete_global_data`

Deletes the top-level defined global data that contains an address, including its
non-dynamic labels. The supplied address may be the global's start or any location
inside an array or structure. Bookmarks are preserved because they are separate
Ghidra objects.

- Parameter: `location`.
- Example: `{"location": "00BC1EF8"}`

The result reports the requested location, complete deleted range, data type,
size, and deleted labels. If no defined data contains the address, no changes are
made.

### `add_bookmark`

Creates or updates a categorized bookmark at a program address. Ghidra stores the
bookmark's Category, Location, Type, and comment. The Bookmark table's Label and
Code Unit columns are derived automatically from the primary symbol and code/data
already present at the address.

- Parameters: `category`, `location`, optional `comment`, and optional
  `bookmark_type` (default `Info`).
- Example:
  `{"category": "ExportGlobals", "location": "00BC1EF8", "comment": "Export this global"}`

To register an exportable global with a specific label, type, and size, call
`register_global_data` first and then call `add_bookmark` at the same address with
the desired category. Repeating an identical bookmark request makes no changes.

## Structures in the Data Type Manager

All structure tools identify the target with both `category_path` and
`struct_name`. This avoids ambiguity when different Data Type Manager folders
contain structures with the same name. Use `/` for the root folder or a complete
folder path such as `/TM/Network`.

Field data types may also use a complete path. Pointer and array suffixes are
supported, including `/TM/Types/Item *`, `/TM/Types/Item[10]`, and `DWORD[10]`.
When an unqualified data type name exists in more than one folder, the tool
returns an ambiguity error and requires the full path.

### `create_struct`

Creates a new structure at an exact Data Type Manager folder path. The operation
refuses to overwrite any existing data type with the same name. It may optionally
create the target folder, and the folder and structure are created in the same
transaction.

- Required parameters: `category_path` and `struct_name`.
- Optional parameters: `initial_size` (default `0`), `packing` (default
  `disabled`), `packing_value`, `description`, and `create_category` (default
  `false`).
- Non-packed example:
  `{"category_path": "/TM/Network", "struct_name": "PacketState", "initial_size": 32, "description": "Per-connection packet state", "create_category": true}`
- Explicitly packed example:
  `{"category_path": "/TMBasedef.h", "struct_name": "STRUCT_NEW_DATA", "packing": "explicit", "packing_value": 1, "description": "New server data structure"}`

`packing` accepts `disabled`, `default`, or `explicit`. Explicit packing requires a
positive `packing_value`. Packed structures must use `initial_size: 0` because
their size is derived from their fields. An empty, non-packed Ghidra structure
created with requested size `0` may report a one-byte not-yet-defined size until a
field is added; the result includes both requested and current size.

### `list_struct_fields`

Lists every defined field in a structure, including its offset, end offset,
ordinal, name, full data type path, byte length, comment, and bit-field status. It
also reports the total structure size and whether packing is enabled.

- Parameters: `category_path` and `struct_name`.
- Example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader"}`

### `add_struct_field`

Adds a field using one of two placement modes. For a non-packed structure, use an
exact byte `offset`; existing fields are not shifted or overwritten and the
structure grows when needed. For a packed structure, use an insertion `ordinal`;
Ghidra calculates the field offset and repacks subsequent fields.

- Required parameters: `category_path`, `struct_name`, `field_name`, and
  `data_type`.
- Placement: provide exactly one of `offset` or `ordinal`.
- Optional parameters: `length` (default `-1`, natural size), `comment`, and
  `allow_repack` (default `false`).
- Built-in type example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader", "offset": 8, "field_name": "itemCount", "data_type": "DWORD", "comment": "Number of items"}`
- Array example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader", "offset": 12, "field_name": "itemIds", "data_type": "DWORD[10]"}`
- Packed insertion preview:
  `{"category_path": "/TMBasedef.h", "struct_name": "STRUCT_ITEM", "ordinal": 3, "field_name": "NewValue", "data_type": "DWORD"}`

Packed insertion is transactional. Without `allow_repack`, the result previews the
new total size, actual inserted offset, and every existing field whose offset would
change, then rolls back. Repeat the same request with `"allow_repack": true` to
commit. For a dynamically sized type, supply a positive `length`. For a fixed
type, use array syntax instead of a length greater than the natural size.

### `remove_struct_field`

Removes the defined field containing an offset. The offset may point to the first
byte or any byte inside the field. In a non-packed structure, the removed field
becomes undefined space and the total structure size is preserved.

- Parameters: `category_path`, `struct_name`, and `offset`.
- Example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader", "offset": 12}`

### `modify_struct_field`

Changes one or more properties of an existing field: offset, name, data type,
length, or comment. Omitted properties remain unchanged. Passing an empty string
as `new_name` or `new_comment` clears that property. The original field is restored
automatically if any part of the transaction fails.

- Required parameters: `category_path`, `struct_name`, and `offset`.
- Optional changes: `new_offset`, `new_name`, `new_data_type`, `new_length`, and
  `new_comment`.
- Packed-layout confirmation: `allow_repack` (default `false`).
- Rename and comment example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader", "offset": 8, "new_name": "entryCount", "new_comment": "Validated entry count"}`
- Move and replace example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader", "offset": 12, "new_offset": 16, "new_data_type": "/TM/Types/Item[10]"}`
- Safe packed-structure retype:
  `{"category_path": "/TMBasedef.h", "struct_name": "STRUCT_ITEM", "offset": 12, "new_data_type": "/TMBasedef.h/STRUCT_ITEMLIST"}`

For a non-packed structure, moving or replacing a field refuses to overlap another
field and reports the exact conflicting offset and range. For a packed structure,
`new_offset` is rejected because packing determines offsets. Type and length
changes are applied by component ordinal inside a transaction, then the complete
layout is compared with the original layout. If no field offset or total structure
size changes, the retype is committed automatically.

If the packed replacement would move fields or change the total size, the
transaction is rolled back and the result reports the proposed size and every
changed offset. Review that preview and repeat the same call with
`"allow_repack": true` to commit deliberately:

`{"category_path": "/TMBasedef.h", "struct_name": "STRUCT_ITEM", "offset": 12, "new_data_type": "DWORD[10]", "allow_repack": true}`

This workflow allows the structures exported by `ExportTMBasedef.java` to be
retyped directly in Ghidra without a manual post-generation merge. Layout changes
for bit fields remain intentionally rejected; their name and comment can still be
changed.

### `modify_struct`

Renames and/or resizes a structure in a specific folder. Existing uses of the
managed structure continue to reference the updated data type.

- Required parameters: `category_path` and `struct_name`.
- Provide `new_name`, `new_size`, or both.
- Rename example:
  `{"category_path": "/TM/Network", "struct_name": "PacketHeader", "new_name": "TM_PacketHeader"}`
- Resize example:
  `{"category_path": "/TM/Network", "struct_name": "TM_PacketHeader", "new_size": 64}`

Shrinking a structure removes fields that no longer fit, so use `list_struct_fields`
first when reducing its size. Packed structures may be renamed but cannot be
resized explicitly because their size is controlled by packing.

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
