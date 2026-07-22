# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2,<3",
#     "mcp>=1.2.0,<2",
# ]
# ///

import sys
import requests
import argparse
import logging
from urllib.parse import urljoin

from mcp.server.fastmcp import FastMCP

DEFAULT_GHIDRA_SERVER = "http://127.0.0.1:8080/"

logger = logging.getLogger(__name__)

mcp = FastMCP("ghidra-mcp")

# Initialize ghidra_server_url with default value
ghidra_server_url = DEFAULT_GHIDRA_SERVER

def safe_get(endpoint: str, params: dict = None) -> list:
    """
    Perform a GET request with optional query parameters.
    """
    if params is None:
        params = {}

    url = urljoin(ghidra_server_url, endpoint)

    try:
        response = requests.get(url, params=params, timeout=5)
        response.encoding = 'utf-8'
        if response.ok:
            return response.text.splitlines()
        else:
            return [f"Error {response.status_code}: {response.text.strip()}"]
    except Exception as e:
        return [f"Request failed: {str(e)}"]

def safe_post(endpoint: str, data: dict | str, timeout: float = 5) -> str:
    try:
        url = urljoin(ghidra_server_url, endpoint)
        headers = {"X-GhidraMCP-Request": "bridge"}
        if isinstance(data, dict):
            response = requests.post(url, data=data, headers=headers, timeout=timeout)
        else:
            response = requests.post(
                url, data=data.encode("utf-8"), headers=headers, timeout=timeout
            )
        response.encoding = 'utf-8'
        if response.ok:
            return response.text.strip()
        else:
            return f"Error {response.status_code}: {response.text.strip()}"
    except Exception as e:
        return f"Request failed: {str(e)}"

@mcp.tool()
def list_methods(offset: int = 0, limit: int = 100) -> list:
    """
    List all function names in the program with pagination.
    """
    return safe_get("methods", {"offset": offset, "limit": limit})

@mcp.tool()
def list_classes(offset: int = 0, limit: int = 100) -> list:
    """
    List all namespace/class names in the program with pagination.
    """
    return safe_get("classes", {"offset": offset, "limit": limit})

@mcp.tool()
def decompile_function(name: str) -> str:
    """
    Decompile a specific function by name and return the decompiled C code.
    """
    return safe_post("decompile", name)

@mcp.tool()
def rename_function(old_name: str, new_name: str) -> str:
    """
    Rename a function by its current name to a new user-defined name.
    """
    return safe_post("renameFunction", {"oldName": old_name, "newName": new_name})

@mcp.tool()
def rename_data(address: str, new_name: str) -> str:
    """
    Rename a data label at the specified address.
    """
    return safe_post("renameData", {"address": address, "newName": new_name})

@mcp.tool()
def list_segments(offset: int = 0, limit: int = 100) -> list:
    """
    List all memory segments in the program with pagination.
    """
    return safe_get("segments", {"offset": offset, "limit": limit})

@mcp.tool()
def list_imports(offset: int = 0, limit: int = 100) -> list:
    """
    List imported symbols in the program with pagination.
    """
    return safe_get("imports", {"offset": offset, "limit": limit})

@mcp.tool()
def list_exports(offset: int = 0, limit: int = 100) -> list:
    """
    List exported functions/symbols with pagination.
    """
    return safe_get("exports", {"offset": offset, "limit": limit})

@mcp.tool()
def list_namespaces(offset: int = 0, limit: int = 100) -> list:
    """
    List all non-global namespaces in the program with pagination.
    """
    return safe_get("namespaces", {"offset": offset, "limit": limit})

@mcp.tool()
def list_data_items(offset: int = 0, limit: int = 100) -> list:
    """
    List defined data labels and their values with pagination.
    """
    return safe_get("data", {"offset": offset, "limit": limit})

@mcp.tool()
def search_functions_by_name(query: str, offset: int = 0, limit: int = 100) -> list:
    """
    Search for functions whose name contains the given substring.
    """
    if not query:
        return ["Error: query string is required"]
    return safe_get("searchFunctions", {"query": query, "offset": offset, "limit": limit})

@mcp.tool()
def rename_variable(function_name: str, old_name: str, new_name: str) -> str:
    """
    Rename a local variable within a function.
    """
    return safe_post("renameVariable", {
        "functionName": function_name,
        "oldName": old_name,
        "newName": new_name
    })

@mcp.tool()
def get_function_by_address(address: str) -> str:
    """
    Get a function by its address.
    """
    return "\n".join(safe_get("get_function_by_address", {"address": address}))

@mcp.tool()
def get_current_address() -> str:
    """
    Get the address currently selected by the user.
    """
    return "\n".join(safe_get("get_current_address"))

@mcp.tool()
def get_current_function() -> str:
    """
    Get the function currently selected by the user.
    """
    return "\n".join(safe_get("get_current_function"))

@mcp.tool()
def list_functions() -> list:
    """
    List all functions in the database.
    """
    return safe_get("list_functions")

@mcp.tool()
def decompile_function_by_address(address: str) -> str:
    """
    Decompile a function at the given address.
    """
    return "\n".join(safe_get("decompile_function", {"address": address}))

@mcp.tool()
def disassemble_function(address: str) -> list:
    """
    Get assembly code (address: instruction; comment) for a function.
    """
    return safe_get("disassemble_function", {"address": address})

@mcp.tool()
def set_decompiler_comment(address: str, comment: str) -> str:
    """
    Set a comment for a given address in the function pseudocode.
    """
    return safe_post("set_decompiler_comment", {"address": address, "comment": comment})

@mcp.tool()
def set_disassembly_comment(address: str, comment: str) -> str:
    """
    Set a comment for a given address in the function disassembly.
    """
    return safe_post("set_disassembly_comment", {"address": address, "comment": comment})

@mcp.tool()
def rename_function_by_address(function_address: str, new_name: str) -> str:
    """
    Rename a function by its address.
    """
    return safe_post("rename_function_by_address", {"function_address": function_address, "new_name": new_name})

@mcp.tool()
def set_function_prototype(function_address: str, prototype: str) -> str:
    """
    Set a function's prototype.
    """
    return safe_post("set_function_prototype", {"function_address": function_address, "prototype": prototype})

@mcp.tool()
def set_local_variable_type(function_address: str, variable_name: str, new_type: str) -> str:
    """
    Set a local variable's type.
    """
    return safe_post("set_local_variable_type", {"function_address": function_address, "variable_name": variable_name, "new_type": new_type})

@mcp.tool()
def get_xrefs_to(address: str, offset: int = 0, limit: int = 100) -> list:
    """
    Get all references to the specified address (xref to).
    
    Args:
        address: Target address in hex format (e.g. "0x1400010a0")
        offset: Pagination offset (default: 0)
        limit: Maximum number of references to return (default: 100)
        
    Returns:
        List of references to the specified address
    """
    return safe_get("xrefs_to", {"address": address, "offset": offset, "limit": limit})

@mcp.tool()
def get_xrefs_from(address: str, offset: int = 0, limit: int = 100) -> list:
    """
    Get all references from the specified address (xref from).
    
    Args:
        address: Source address in hex format (e.g. "0x1400010a0")
        offset: Pagination offset (default: 0)
        limit: Maximum number of references to return (default: 100)
        
    Returns:
        List of references from the specified address
    """
    return safe_get("xrefs_from", {"address": address, "offset": offset, "limit": limit})

@mcp.tool()
def get_function_xrefs(name: str, offset: int = 0, limit: int = 100) -> list:
    """
    Get all references to the specified function by name.
    
    Args:
        name: Function name to search for
        offset: Pagination offset (default: 0)
        limit: Maximum number of references to return (default: 100)
        
    Returns:
        List of references to the specified function
    """
    return safe_get("function_xrefs", {"name": name, "offset": offset, "limit": limit})

@mcp.tool()
def list_function_tags(function_address: str | None = None) -> list:
    """
    List function tags.

    Without an address, returns every tag defined in the current program with its
    description and use count. With an address, returns only the tags assigned to
    the function at or containing that address.

    Args:
        function_address: Optional function address, such as ``00523000``.
    """
    params = {}
    if function_address:
        params["function_address"] = function_address
    return safe_get("function_tags", params)

@mcp.tool()
def add_function_tag(
    function_address: str,
    tag_name: str,
    tag_description: str = "",
) -> str:
    """
    Add a function tag to a non-thunk function.

    The plugin resolves the function at or containing the supplied address, rejects
    thunk functions, creates the tag when necessary, and commits the assignment in
    a Ghidra program transaction.

    Args:
        function_address: Address of the target function, such as ``00523000``.
        tag_name: Tag to assign, such as ``TMNativeAPI::Network``.
        tag_description: Optional description used only when creating a new tag.
    """
    if not function_address:
        return "Error: function_address is required"
    if not tag_name or not tag_name.strip():
        return "Error: tag_name is required"
    if "\n" in tag_name or "\r" in tag_name:
        return "Error: tag_name must be a single line"

    return safe_post("add_function_tag", {
        "function_address": function_address,
        "tag_name": tag_name.strip(),
        "tag_description": tag_description,
    })

@mcp.tool()
def add_bookmark(
    category: str,
    location: str,
    comment: str = "",
    bookmark_type: str = "Info",
) -> str:
    """
    Create or update a categorized Ghidra bookmark at an address.

    Ghidra stores the Category, Location, bookmark type, and comment. The Bookmark
    table's Label and Code Unit columns are derived from the program symbol and data
    at ``location``. Use ``register_global_data`` first when those columns need a
    specific global name, data type, and size.

    Args:
        category: Bookmark category, such as ``ExportGlobals``.
        location: Program address, such as ``00BC1EF8``.
        comment: Optional bookmark comment.
        bookmark_type: Existing Ghidra bookmark type (default ``Info``).
    """
    if not category or not category.strip():
        return "Error: category is required"
    if not location:
        return "Error: location is required"
    if "\n" in category or "\r" in category:
        return "Error: category must be a single line"

    return safe_post("add_bookmark", {
        "category": category.strip(),
        "location": location,
        "comment": comment,
        "bookmark_type": bookmark_type,
    })

@mcp.tool()
def register_global_data(
    location: str,
    label: str,
    data_type: str,
    size: int,
    replace_existing: bool = False,
) -> str:
    """
    Register typed global data and its primary symbol in the current program.

    If the same address already has equivalent data, size, and primary label, the
    tool reports that it is already registered and makes no changes. By default it
    also reports "already registered" when the address falls inside an existing
    defined data item, preventing overlapping globals. A larger declaration
    automatically consumes fully contained smaller data declarations and their
    labels. Instructions remain protected unless ``replace_existing`` is true, and
    partially overlapping data remains protected. A larger compatible size creates
    an array of the requested data type.

    Args:
        location: Address of the global data, such as ``00BC1EF8``.
        label: Primary symbol name, such as ``g_pCollectionData``.
        data_type: Existing Ghidra data type name, such as ``DWORD`` or
            ``STRUCT_ITEM``.
        size: Total data size in bytes.
        replace_existing: Whether conflicting defined code/data may be cleared.
    """
    if not location:
        return "Error: location is required"
    if not label or not label.strip():
        return "Error: label is required"
    if "\n" in label or "\r" in label:
        return "Error: label must be a single line"
    if not data_type or not data_type.strip():
        return "Error: data_type is required"
    if not 1 <= size <= 64 * 1024 * 1024:
        return "Error: size must be between 1 and 67108864 bytes"

    return safe_post("register_global_data", {
        "location": location,
        "label": label.strip(),
        "data_type": data_type.strip(),
        "size": str(size),
        "replace_existing": str(replace_existing).lower(),
    })

@mcp.tool()
def delete_global_data(location: str) -> str:
    """
    Delete the defined global data containing an address and its labels.

    The address may be the start of the global or any address inside it. The whole
    top-level data item is cleared. Bookmarks are kept because they are managed
    separately by Ghidra.

    Args:
        location: Start address or an address inside the global data item.
    """
    if not location:
        return "Error: location is required"

    return safe_post("delete_global_data", {"location": location})

def _validate_struct_reference(category_path: str, struct_name: str) -> str | None:
    if not category_path or not category_path.strip():
        return "Error: category_path is required; use / for the root folder"
    if not struct_name or not struct_name.strip():
        return "Error: struct_name is required"
    if any(c in category_path or c in struct_name for c in ("\n", "\r")):
        return "Error: category_path and struct_name must be single-line values"
    return None

@mcp.tool()
def list_struct_fields(category_path: str, struct_name: str) -> list:
    """
    List the defined fields of a structure in a specific Data Type Manager folder.

    Args:
        category_path: Folder path, such as ``/TM/Network`` or ``/`` for root.
        struct_name: Exact structure name in that folder.
    """
    error = _validate_struct_reference(category_path, struct_name)
    if error:
        return [error]
    return safe_get("struct_fields", {
        "category_path": category_path.strip(),
        "struct_name": struct_name.strip(),
    })

@mcp.tool()
def add_struct_field(
    category_path: str,
    struct_name: str,
    offset: int,
    field_name: str,
    data_type: str,
    length: int = -1,
    comment: str = "",
) -> str:
    """
    Add a field at an exact offset in a folder-qualified, non-packed structure.

    Existing fields are never shifted or overwritten. The structure grows when
    needed. Data types may use a full path, pointer suffix, or array syntax such as
    ``/TM/Types/Item *`` or ``DWORD[10]``.

    Args:
        category_path: Data Type Manager folder containing the structure.
        struct_name: Exact structure name.
        offset: Field byte offset, zero or greater.
        field_name: New field name.
        data_type: Field data type name or full path.
        length: Explicit byte length for dynamic types; ``-1`` uses natural size.
        comment: Optional field comment.
    """
    error = _validate_struct_reference(category_path, struct_name)
    if error:
        return error
    if offset < 0:
        return "Error: offset must be zero or greater"
    if not field_name or not field_name.strip():
        return "Error: field_name is required"
    if not data_type or not data_type.strip():
        return "Error: data_type is required"
    if length == 0 or length < -1:
        return "Error: length must be -1 or greater than zero"
    return safe_post("add_struct_field", {
        "category_path": category_path.strip(),
        "struct_name": struct_name.strip(),
        "offset": str(offset),
        "field_name": field_name.strip(),
        "data_type": data_type.strip(),
        "length": str(length),
        "comment": comment,
    })

@mcp.tool()
def remove_struct_field(
    category_path: str,
    struct_name: str,
    offset: int,
) -> str:
    """
    Remove the defined structure field containing an offset.

    For a non-packed structure the field becomes undefined space and the overall
    structure size is preserved.

    Args:
        category_path: Data Type Manager folder containing the structure.
        struct_name: Exact structure name.
        offset: Start of the field or any byte inside it.
    """
    error = _validate_struct_reference(category_path, struct_name)
    if error:
        return error
    if offset < 0:
        return "Error: offset must be zero or greater"
    return safe_post("remove_struct_field", {
        "category_path": category_path.strip(),
        "struct_name": struct_name.strip(),
        "offset": str(offset),
    })

@mcp.tool()
def modify_struct_field(
    category_path: str,
    struct_name: str,
    offset: int,
    new_offset: int | None = None,
    new_name: str | None = None,
    new_data_type: str | None = None,
    new_length: int | None = None,
    new_comment: str | None = None,
) -> str:
    """
    Modify a structure field's offset, name, data type, length, and/or comment.

    Omitted values remain unchanged. An empty ``new_name`` clears the field name,
    and an empty ``new_comment`` clears the comment. Layout changes do not overwrite
    another field and require a non-packed structure.

    Args:
        category_path: Data Type Manager folder containing the structure.
        struct_name: Exact structure name.
        offset: Start or interior byte of the existing field.
        new_offset: Optional new byte offset.
        new_name: Optional new name; empty clears it.
        new_data_type: Optional type name or full path.
        new_length: Optional new byte length.
        new_comment: Optional comment; empty clears it.
    """
    error = _validate_struct_reference(category_path, struct_name)
    if error:
        return error
    if offset < 0:
        return "Error: offset must be zero or greater"
    changes = (new_offset, new_name, new_data_type, new_length, new_comment)
    if all(value is None for value in changes):
        return "Error: provide at least one field change"
    if new_offset is not None and new_offset < 0:
        return "Error: new_offset must be zero or greater"
    if new_length is not None and new_length <= 0:
        return "Error: new_length must be greater than zero"
    if new_data_type is not None and not new_data_type.strip():
        return "Error: new_data_type cannot be blank"

    data = {
        "category_path": category_path.strip(),
        "struct_name": struct_name.strip(),
        "offset": str(offset),
    }
    if new_offset is not None:
        data.update({"has_new_offset": "true", "new_offset": str(new_offset)})
    if new_name is not None:
        data.update({"has_new_name": "true", "new_name": new_name})
    if new_data_type is not None:
        data.update({
            "has_new_data_type": "true",
            "new_data_type": new_data_type.strip(),
        })
    if new_length is not None:
        data.update({"has_new_length": "true", "new_length": str(new_length)})
    if new_comment is not None:
        data.update({"has_new_comment": "true", "new_comment": new_comment})
    return safe_post("modify_struct_field", data)

@mcp.tool()
def modify_struct(
    category_path: str,
    struct_name: str,
    new_name: str | None = None,
    new_size: int | None = None,
) -> str:
    """
    Rename and/or resize a structure in a specific Data Type Manager folder.

    Shrinking may remove fields that no longer fit. Explicit resizing is rejected
    for packed structures because their size is determined by packing.

    Args:
        category_path: Data Type Manager folder containing the structure.
        struct_name: Current exact structure name.
        new_name: Optional new structure name.
        new_size: Optional new total size in bytes, zero or greater.
    """
    error = _validate_struct_reference(category_path, struct_name)
    if error:
        return error
    if new_name is None and new_size is None:
        return "Error: provide new_name and/or new_size"
    if new_name is not None and not new_name.strip():
        return "Error: new_name cannot be blank"
    if new_size is not None and new_size < 0:
        return "Error: new_size must be zero or greater"

    data = {
        "category_path": category_path.strip(),
        "struct_name": struct_name.strip(),
    }
    if new_name is not None:
        data.update({"has_new_name": "true", "new_name": new_name.strip()})
    if new_size is not None:
        data.update({"has_new_size": "true", "new_size": str(new_size)})
    return safe_post("modify_struct", data)

@mcp.tool()
def list_strings(offset: int = 0, limit: int = 2000, filter: str = None) -> list:
    """
    List all defined strings in the program with their addresses.
    
    Args:
        offset: Pagination offset (default: 0)
        limit: Maximum number of strings to return (default: 2000)
        filter: Optional filter to match within string content
        
    Returns:
        List of strings with their addresses
    """
    params = {"offset": offset, "limit": limit}
    if filter:
        params["filter"] = filter
    return safe_get("strings", params)

@mcp.tool()
def execute_ghidra_script(
    script_name: str,
    arguments: list[str] | None = None,
    timeout_seconds: int = 120,
) -> str:
    """
    Execute a trusted script found in an enabled Ghidra ``ghidra_scripts`` directory.

    Only a file name is accepted; paths and directory traversal are rejected. Script
    output written with ``print``/``println`` is returned to the MCP client. Scripts
    that display interactive dialogs may block until the user answers them in Ghidra.

    Args:
        script_name: Script file name including its extension, such as ``MyScript.java``.
        arguments: Optional values exposed to the script through ``getScriptArgs()``.
        timeout_seconds: How long to wait for completion, from 1 to 600 seconds.
    """
    if not script_name or any(char in script_name for char in ("/", "\\", ":", "\0")):
        return "Error: script_name must be a file name, not a path"
    if script_name in (".", ".."):
        return "Error: script_name must be a file name, not a path"

    script_arguments = arguments or []
    if len(script_arguments) > 64:
        return "Error: at most 64 script arguments are allowed"
    if not 1 <= timeout_seconds <= 600:
        return "Error: timeout_seconds must be between 1 and 600"

    data = {
        "script_name": script_name,
        "argument_count": str(len(script_arguments)),
    }
    for index, argument in enumerate(script_arguments):
        data[f"argument_{index}"] = argument

    return safe_post("execute_script", data, timeout=timeout_seconds)

def main():
    parser = argparse.ArgumentParser(description="MCP server for Ghidra")
    parser.add_argument("--ghidra-server", type=str, default=DEFAULT_GHIDRA_SERVER,
                        help=f"Ghidra server URL, default: {DEFAULT_GHIDRA_SERVER}")
    parser.add_argument("--mcp-host", type=str, default="127.0.0.1",
                        help="Host to run MCP server on (only used for sse), default: 127.0.0.1")
    parser.add_argument("--mcp-port", type=int,
                        help="Port to run MCP server on (only used for sse), default: 8081")
    parser.add_argument("--transport", type=str, default="stdio", choices=["stdio", "sse"],
                        help="Transport protocol for MCP, default: stdio")
    args = parser.parse_args()
    
    # Use the global variable to ensure it's properly updated
    global ghidra_server_url
    if args.ghidra_server:
        ghidra_server_url = args.ghidra_server
    
    if args.transport == "sse":
        try:
            # Set up logging
            log_level = logging.INFO
            logging.basicConfig(level=log_level)
            logging.getLogger().setLevel(log_level)

            # Configure MCP settings
            mcp.settings.log_level = "INFO"
            if args.mcp_host:
                mcp.settings.host = args.mcp_host
            else:
                mcp.settings.host = "127.0.0.1"

            if args.mcp_port:
                mcp.settings.port = args.mcp_port
            else:
                mcp.settings.port = 8081

            logger.info(f"Connecting to Ghidra server at {ghidra_server_url}")
            logger.info(f"Starting MCP server on http://{mcp.settings.host}:{mcp.settings.port}/sse")
            logger.info(f"Using transport: {args.transport}")

            mcp.run(transport="sse")
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
    else:
        mcp.run()
        
if __name__ == "__main__":
    main()

