# DuckDB documentation index (URL catalog)

Scraped **2026-07-15** from [duckdb.org/docs](https://duckdb.org/docs/) → [current](https://duckdb.org/docs/current/) (sitemap).

## How to use this file

1. Skim or search this file for the topic (Python client, CSV/Parquet, COPY, window functions, …).
2. **Fetch the live URL** for full SQL/examples — do not invent DuckDB syntax from the summary alone.
3. Prefer **`/docs/current/`** pages. Entry: <https://duckdb.org/docs/current/>.
4. Camp default: local/in-process DuckDB (Python `duckdb` or CLI) — no remote server unless asked.

**Pages indexed:** 409

## High-signal pages (quick list)

- [Python API](https://duckdb.org/docs/current/clients/python/overview) — DuckDB Python client: in-process SQL, relations, Pandas/Arrow.
- [Command Line Client](https://duckdb.org/docs/current/clients/cli/overview) — DuckDB CLI: interactive shell, dot commands, local files.
- [SQL Introduction](https://duckdb.org/docs/current/sql/introduction) — SQL introduction for DuckDB — basic SELECT and operations.
- [SELECT Statement](https://duckdb.org/docs/current/sql/statements/select) — SELECT statement — query tables and files.
- [CREATE TABLE Statement](https://duckdb.org/docs/current/sql/statements/create_table) — CREATE TABLE — define tables and schemas.
- [INSERT Statement](https://duckdb.org/docs/current/sql/statements/insert) — INSERT — add rows from values or queries.
- [COPY Statement](https://duckdb.org/docs/current/sql/statements/copy) — COPY — load/export CSV, Parquet, and other formats.
- [Importing Data](https://duckdb.org/docs/current/data/overview) — Importing data overview — connect DuckDB to common sources.
- [CSV Import](https://duckdb.org/docs/current/data/csv/overview) — CSV import — read_csv / file query and options.
- [Reading and Writing Parquet Files](https://duckdb.org/docs/current/data/parquet/overview) — Parquet read/write and schema inspection.
- [JSON Overview](https://duckdb.org/docs/current/data/json/overview) — JSON functions and the json extension.
- [Executing SQL in Python](https://duckdb.org/docs/current/guides/python/execute_sql) — Execute SQL from Python via duckdb.sql / relations.
- [Import from Pandas](https://duckdb.org/docs/current/guides/python/import_pandas) — Create/insert tables from Pandas DataFrames.
- [SQL on Pandas](https://duckdb.org/docs/current/guides/python/sql_on_pandas) — Query Pandas DataFrames as tables in DuckDB.
- [Export to Pandas](https://duckdb.org/docs/current/guides/python/export_pandas) — Export query results to Pandas (.df()).
- [Jupyter Notebooks](https://duckdb.org/docs/current/guides/python/jupyter) — Use DuckDB in Jupyter notebooks.
- [Extensions](https://duckdb.org/docs/current/extensions/overview) — Extension mechanism — load features dynamically.
- [Configuration](https://duckdb.org/docs/current/configuration/overview) — Configuration options (SET / SET GLOBAL).

## Overview & start here (1)

### Documentation

- **URL:** https://duckdb.org/docs/current/
- **Summary:** Connecting to DuckDB DuckDB connection overview Quack remote protocol Client APIs C C++ CLI (command line interface) Go Java (JDBC) Node.js ODBC Python R Rust WebAssembly All client APIs SQL Introduction Statements Other Guides Installation Building DuckDB Browsing offline
- **Sections:** Connecting to DuckDB; Client APIs; SQL; Other

## Clients (Python, CLI, …) (58)

### ADBC Client

- **URL:** https://duckdb.org/docs/current/clients/adbc
- **Summary:** Installation To use the DuckDB ADBC client, download the libduckdb archive for your platform and follow the instructions below. The latest stable version of the DuckDB ADBC client is . Arrow Database Connectivity (ADBC), similarly to ODBC and JDBC, is a C-style API that enables code portability between different database systems. This allows developers to…
- **Sections:** Implemented Functionality; Database; Connection; Statement; Setting Up the DuckDB ADBC Driver; Downloading libduckdb

### Complete API

- **URL:** https://duckdb.org/docs/current/clients/c/api
- **Summary:** This page contains the reference for DuckDB's C API. The reference contains several deprecation notices. These concern methods whose long-term availability is not guaranteed as they may be removed in the future. That said, DuckDB's developers plan to carry out deprecations slowly as several of the deprecated methods do not yet have a fully functional alternative. Therefore, they will not be…
- **Sections:** API Reference Overview; Open Connect; Configuration; Error Data; Query Execution; Result Functions

### Appender

- **URL:** https://duckdb.org/docs/current/clients/c/appender
- **Summary:** Appenders are the most efficient way of loading data into DuckDB from within the C interface, and are recommended for fast data loading. The appender is much faster than using prepared statements or individual INSERT INTO statements. Appends are made in row-wise format. For every column, a duckdb_append_[type] call should be made, after which the row should be finished by calling…
- **Sections:** Example; API Reference Overview

### Configuration

- **URL:** https://duckdb.org/docs/current/clients/c/config
- **Summary:** Configuration options can be provided to change different settings of the database system. Note that many of these settings can be changed later on using PRAGMA statements as well. The configuration object should be created, filled with values and passed to duckdb_open_ext. Example duckdb_database db; duckdb_config config; // create the configuration object if (duckdb_create_config(&config) ==…
- **Sections:** Example; API Reference Overview

### Startup & Shutdown

- **URL:** https://duckdb.org/docs/current/clients/c/connect
- **Summary:** To use DuckDB, you must first initialize a duckdb_database handle using duckdb_open(). duckdb_open() takes as parameter the database file to read and write from. The special value NULL (nullptr) can be used to create an in-memory database. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the process). With the duckdb_database handle, you…
- **Sections:** Example; API Reference Overview

### Data Chunks

- **URL:** https://duckdb.org/docs/current/clients/c/data_chunk
- **Summary:** Data chunks represent a horizontal slice of a table. They hold a number of vectors, that can each hold up to the VECTOR_SIZE rows. The vector size can be obtained through the duckdb_vector_size function and is configurable, but is usually set to 2048. Data chunks and vectors are what DuckDB uses natively to store and represent data. For this reason, the data chunk interface is the most…
- **Sections:** API Reference Overview

### Overview

- **URL:** https://duckdb.org/docs/current/clients/c/overview
- **Summary:** Installation To use the DuckDB C API, download the libduckdb archive for your platform. The latest stable version of the DuckDB C API is . DuckDB implements a custom C API modeled somewhat following the SQLite C API. The API is contained in the duckdb.h header. Continue to Startup & Shutdown to get started, or check out the Full API overview. We also provide a…
- **Sections:** Installation; Pages in This Section

### Prepared Statements

- **URL:** https://duckdb.org/docs/current/clients/c/prepared
- **Summary:** A prepared statement is a parameterized query. The query is prepared with question marks (?) or dollar symbols ($1) indicating the parameters of the query. Values can then be bound to these parameters, after which the prepared statement can be executed using those parameters. A single query can be prepared once and executed many times. Prepared statements are useful to: Easily supply…
- **Sections:** Example; API Reference Overview

### Query

- **URL:** https://duckdb.org/docs/current/clients/c/query
- **Summary:** The duckdb_query method allows SQL queries to be run in DuckDB from C. This method takes two parameters, a (null-terminated) SQL query string and a duckdb_result result pointer. The result pointer may be NULL if the application is not interested in the result set or if the query produces no result. After the result is consumed, the duckdb_destroy_result method should be used to clean up the…
- **Sections:** Example; Value Extraction; duckdb_fetch_chunk; duckdb_value; API Reference Overview

### Replacement Scans

- **URL:** https://duckdb.org/docs/current/clients/c/replacement_scans
- **Summary:** The replacement scan API can be used to register a callback that is called when a table is read that does not exist in the catalog. For example, when a query such as SELECT * FROM my_table is executed and my_table does not exist, the replacement scan callback will be called with my_table as parameter. The replacement scan can then insert a table function with a specific parameter to replace…
- **Sections:** API Reference Overview

### Table Functions

- **URL:** https://duckdb.org/docs/current/clients/c/table_functions
- **Summary:** The table function API can be used to define a table function that can then be called from within DuckDB in the FROM clause of a query. API Reference Overview duckdb_table_function duckdb_create_table_function(); void duckdb_destroy_table_function(duckdb_table_function *table_function); void duckdb_table_function_set_name(duckdb_table_function table_function, const char *name); void…
- **Sections:** API Reference Overview; Table Function Bind; Table Function Init; Table Function

### Types

- **URL:** https://duckdb.org/docs/current/clients/c/types
- **Summary:** DuckDB is a strongly typed database system. As such, every column has a single type specified. This type is constant over the entire column. That is to say, a column that is labeled as an INTEGER column will only contain INTEGER values. DuckDB also supports columns of composite types. For example, it is possible to define an array of integers (INTEGER[]). It is also possible to define types as…
- **Sections:** Functions; duckdb_value; duckdb_fetch_chunk; API Reference Overview; Date Time Timestamp Helpers; Hugeint Helpers

### Values

- **URL:** https://duckdb.org/docs/current/clients/c/value
- **Summary:** The value class represents a single value of any type. API Reference Overview void duckdb_destroy_value(duckdb_value *value); duckdb_value duckdb_create_varchar(const char *text); duckdb_value duckdb_create_varchar_length(const char *text, idx_t length); duckdb_value duckdb_create_bool(bool input); duckdb_value duckdb_create_int8(int8_t input); duckdb_value duckdb_create_uint8(uint8_t input);…
- **Sections:** API Reference Overview

### Vectors

- **URL:** https://duckdb.org/docs/current/clients/c/vector
- **Summary:** Vectors represent a horizontal slice of a column. They hold a number of values of a specific type, similar to an array. Vectors are the core data representation used in DuckDB. Vectors are typically stored within data chunks. The vector and data chunk interfaces are the most efficient way of interacting with DuckDB, allowing for the highest performance. However, the interfaces are also…
- **Sections:** Vector Format; Primitive Types; NULL Values; Strings; Decimals; Enums

### Command Line Arguments

- **URL:** https://duckdb.org/docs/current/clients/cli/arguments
- **Summary:** The table below summarizes DuckDB's command line options. To list all command line options, use the command: duckdb -help For a list of dot commands available in the CLI shell, see the Dot Commands page. Argument Description -append Append the database to the end of the file -ascii Set output mode to ascii -bail Stop after hitting an error -batch Force batch I/O -box Set output mode…
- **Sections:** Passing a Sequence of Arguments

### Autocomplete

- **URL:** https://duckdb.org/docs/current/clients/cli/autocomplete
- **Summary:** The shell offers context-aware autocomplete of SQL queries through the autocomplete extension. autocomplete is triggered by pressing Tab. Multiple autocomplete suggestions can be present. You can cycle forwards through the suggestions by repeatedly pressing Tab, or Shift+Tab to cycle backwards. autocompletion can be reverted by pressing ESC twice. The shell autocompletes four different groups:…

### Dot Commands

- **URL:** https://duckdb.org/docs/current/clients/cli/dot_commands
- **Summary:** Dot commands are available in the DuckDB CLI client. To use one of these commands, begin the line with a period (.) immediately followed by the name of the command you wish to execute. Additional arguments to the command are entered, space separated, after the command. If an argument must contain a space, either single or double quotes may be used to wrap that parameter. Dot commands must be…
- **Sections:** List of Dot Commands; Using the .help Command; .output : Writing Results to a File; Querying the Database Schema; Dumping Database Content as SQL; Progress Bar

### Editing

- **URL:** https://duckdb.org/docs/current/clients/cli/editing
- **Summary:** The linenoise-based CLI editor is available for macOS, Linux and Windows. DuckDB's CLI uses a line-editing library based on linenoise, which has shortcuts that are based on Emacs mode of readline. Below is a list of available commands. You can also view these shortcuts from within the CLI using .help shortcuts. Moving Key Action Left Move back a character Right Move forward a character Up Move…
- **Sections:** Moving; History; Changing Text; Completing; Miscellaneous; External Editor Mode

### Friendly CLI

- **URL:** https://duckdb.org/docs/current/clients/cli/friendly_cli
- **Summary:** Along with our Friendly SQL, we provide friendly CLI features. Dark/Light Mode The CLI automatically detects whether the terminal is using a dark or light background and adjusts syntax highlighting colors accordingly. The mode can also be set manually using the .highlight_mode command: .highlight_mode dark .highlight_mode light To use a mix of colors suitable for both dark and light…
- **Sections:** Dark/Light Mode; 8-Bit Colors; Dynamic Prompt; Return the Result of the Last Query Using _

### Known Issues

- **URL:** https://duckdb.org/docs/current/clients/cli/known_issues
- **Summary:** Incorrect Memory Values on Old Linux Distributions and WSL 2 On Windows Subsystem for Linux 2 (WSL2), when querying the max_memory or memory_limit from the duckdb_settings, the values may be inaccurate on certain Ubuntu versions (e.g., 20.04 and 24.04). The issue also occurs on older distributions such as Red Hat Enterprise Linux 8 (RHEL 8): Example: FROM duckdb_settings() WHERE name LIKE…
- **Sections:** Incorrect Memory Values on Old Linux Distributions and WSL 2

### Output Formats

- **URL:** https://duckdb.org/docs/current/clients/cli/output_formats
- **Summary:** The .mode dot command may be used to change the appearance of the tables returned in the terminal output. In addition to customizing the appearance, these modes have additional benefits. This can be useful for presenting DuckDB output elsewhere by redirecting the terminal output to a file. Using the insert mode will build a series of SQL statements that can be used to insert the data at a…
- **Sections:** List of Output Formats; Changing the Output Format; Paging; duckbox Mode

### Command Line Client

- **URL:** https://duckdb.org/docs/current/clients/cli/overview
- **Summary:** Installation To use the DuckDB CLI client, visit the CLI installation page. The latest stable version of the DuckDB command line client is . Installation The DuckDB CLI (Command Line Interface) is a single, dependency-free executable. It is precompiled for Windows, Mac and Linux for both the stable version and for nightly builds produced by GitHub Actions.…
- **Sections:** Installation; Getting Started; Usage; Options; In-Memory vs. Persistent Database; Running SQL Statements in the CLI

### Safe Mode

- **URL:** https://duckdb.org/docs/current/clients/cli/safe_mode
- **Summary:** The DuckDB CLI client supports “safe mode”. In safe mode, the CLI is prevented from accessing external files other than the database file that it was initially connected to and prevented from interacting with the host file system. This has the following effects: The following dot commands are disabled: .cd .excel .import .log .once .open .output .read .sh .system Auto-complete no longer scans…

### Syntax Highlighting

- **URL:** https://duckdb.org/docs/current/clients/cli/syntax_highlighting
- **Summary:** Syntax highlighting in the CLI is currently only available for macOS and Linux. SQL queries that are written in the shell are automatically highlighted using syntax highlighting. There are several components of a query that are highlighted in different colors. The colors can be configured using dot commands. Syntax highlighting can also be disabled entirely using the .highlight off command.…
- **Sections:** Error Highlighting

### C++ API

- **URL:** https://duckdb.org/docs/current/clients/cpp
- **Summary:** Installation To use the DuckDB C++ API, download the libduckdb archive for your platform. The latest stable version of the DuckDB C++ API is . Warning DuckDB's C++ API is internal. It is not guaranteed to be stable and can change without notice. If you would like to build an application on DuckDB, we recommend using the C API. Installation The DuckDB C++ API…
- **Sections:** Installation; Basic API Usage; Startup & Shutdown; Querying; UDF API

### Go Client

- **URL:** https://duckdb.org/docs/current/clients/go
- **Summary:** Installation To use the DuckDB Go client, visit the Go installation page. The latest stable version of the DuckDB Go client is {% if site.current_duckdb_go_version != "" %}{% else %}{% endif %}. The DuckDB Go client, duckdb-go, allows using DuckDB via the database/sql interface. For examples on how to use this interface, see…
- **Sections:** Installation; Importing; Appender; Examples; Simple Example; More Examples

### Java (JDBC) Client

- **URL:** https://duckdb.org/docs/current/clients/java
- **Summary:** Installation To use the DuckDB Java (JDBC) client, visit the Java installation page. The latest stable version of the DuckDB Java (JDBC) client is {% if site.current_duckdb_java_short_version != "" %}{% else %}{% endif %}. Installation The DuckDB Java JDBC API can be installed from Maven Central. Please see the…
- **Sections:** Installation; Basic API Usage; Startup & Shutdown; Configuring Connections; Querying; Arrow Methods

### Node.js Client (Neo)

- **URL:** https://duckdb.org/docs/current/clients/node_neo/overview
- **Summary:** Installation To use the DuckDB Node.js client, visit the Node.js installation page. The latest stable version of the DuckDB Node.js (Neo) client is {% if site.current_duckdb_node_neo_version != "" %}{% else %}{% endif %}. An API for using DuckDB in Node.js. The primary package, @duckdb/node-api, is a high-level API…
- **Sections:** Roadmap; Platforms; Examples; Get Basic Information; Connect; Create Instance

### ODBC Configuration

- **URL:** https://duckdb.org/docs/current/clients/odbc/configuration
- **Summary:** This page documents the files using the ODBC configuration, odbc.ini and odbcinst.ini. These are either placed in the home directory as dotfiles (.odbc.ini and .odbcinst.ini, respectively) or in a system directory. For platform-specific details, see the pages for Linux, macOS, and Windows. odbc.ini and .odbc.ini The odbc.ini file contains the DSNs for the drivers, which can have specific…
- **Sections:** odbc.ini and .odbc.ini; odbcinst.ini and .odbcinst.ini

### ODBC API on Linux

- **URL:** https://duckdb.org/docs/current/clients/odbc/linux
- **Summary:** Driver Manager A driver manager is required to manage communication between applications and the ODBC driver. We tested and support unixODBC that is a complete ODBC driver manager for Linux. Users can install it from the command line: On Debian-based distributions (Ubuntu, Mint, etc.), run: sudo apt-get install unixodbc odbcinst On Fedora-based distributions (Amazon Linux, RHEL, CentOS, etc.),…
- **Sections:** Driver Manager; Setting Up the Driver

### ODBC API on macOS

- **URL:** https://duckdb.org/docs/current/clients/odbc/macos
- **Summary:** A driver manager is required to manage communication between applications and the ODBC driver. DuckDB supports unixODBC, which is a complete ODBC driver manager for macOS and Linux. Users can install it from the command line via Homebrew: brew install unixodbc DuckDB releases a universal [ODBC driver for macOS](https://github.com/duckdb/duckdb-odbc/releases/download/v{% if…

### ODBC API Overview

- **URL:** https://duckdb.org/docs/current/clients/odbc/overview
- **Summary:** Installation To use the DuckDB ODBC client, visit the ODBC installation page. The latest stable version of the DuckDB ODBC client is {% if site.current_duckdb_odbc_short_version != "" %}{% else %}{% endif %}. The ODBC (Open Database Connectivity) is a C-style API that provides access to different flavors of…
- **Sections:** DuckDB ODBC Driver; Pages in This Section

### ODBC API on Windows

- **URL:** https://duckdb.org/docs/current/clients/odbc/windows
- **Summary:** Setup Using the DuckDB ODBC API on Windows requires the following steps: Microsoft Windows requires an ODBC Driver Manager to manage communication between applications and the ODBC drivers. The Driver Manager on Windows is provided in a DLL file odbccp32.dll, and other files and tools. For detailed information check out the Common ODBC Component Files. DuckDB releases the ODBC driver as an…
- **Sections:** Setup; DSN Windows Setup; Default DuckDB DSN; Changing DuckDB DSN; More Detailed Windows Setup; Registry Keys

### Client Overview

- **URL:** https://duckdb.org/docs/current/clients/overview
- **Summary:** DuckDB is an in-process database system and offers client APIs (“drivers”) for several languages. Client API Maintainer Support tier Latest version C Core team {% include tooltip.html label="Primary" id="support_tier_primary" %} {% if site.current_duckdb_version != "" %}{% else %}{% endif %} Command Line Interface (CLI) Core team {%…
- **Sections:** Support Tiers; Compatibility; Pages in This Section

### Conversion between DuckDB and Python

- **URL:** https://duckdb.org/docs/current/clients/python/conversion
- **Summary:** This page documents the rules for converting Python objects to DuckDB and DuckDB results to Python. Object Conversion: Python Object to DuckDB This is a mapping of Python object types to DuckDB Logical Types: None → NULL bool → BOOLEAN datetime.timedelta → INTERVAL str → VARCHAR bytearray → BLOB memoryview → BLOB decimal.Decimal → DECIMAL / DOUBLE uuid.UUID → UUID The rest of the conversion…
- **Sections:** Object Conversion: Python Object to DuckDB; int; float; datetime.datetime; datetime.time; datetime.date

### Data Ingestion

- **URL:** https://duckdb.org/docs/current/clients/python/data_ingestion
- **Summary:** This page contains examples for data ingestion to Python using DuckDB. First, import the DuckDB package: import duckdb Then, proceed with any of the following sections. CSV Files CSV files can be read using the read_csv function, called either from within Python or directly from within SQL. By default, the read_csv function attempts to auto-detect the CSV settings by sampling from the provided…
- **Sections:** CSV Files; Parquet Files; JSON Files; Directly Accessing DataFrames and Arrow Objects; Pandas DataFrames – object Columns

### Python DB API

- **URL:** https://duckdb.org/docs/current/clients/python/dbapi
- **Summary:** The standard DuckDB Python API provides a SQL interface compliant with the DB-API 2.0 specification described by PEP 249 similar to the SQLite Python API. Connection To use the module, you must first create a DuckDBPyConnection object that represents a connection to a database. This is done through the duckdb.connect method. The 'config' keyword argument can be used to provide a dict that…
- **Sections:** Connection; In-Memory Connection; Default Connection; File-Based Connection; Querying; Prepared Statements

### Expression API

- **URL:** https://duckdb.org/docs/current/clients/python/expression
- **Summary:** The Expression class represents an instance of an expression. Why Would I Use the Expression API? Using this API makes it possible to dynamically build up expressions, which are typically created by the parser from the query string. This allows you to skip that and have more fine-grained control over the used expressions. Below is a list of currently supported expressions that can be created…
- **Sections:** Why Would I Use the Expression API?; Column Expression; Star Expression; Constant Expression; Case Expression; Function Expression

### Python Function API

- **URL:** https://duckdb.org/docs/current/clients/python/function
- **Summary:** You can create a DuckDB user-defined function (UDF) from a Python function so it can be used in SQL queries. Similarly to regular functions, they need to have a name, a return type and parameter types. Here is an example using a Python function that calls a third-party library. import duckdb from duckdb.sqltypes import VARCHAR from faker import Faker def generate_random_name(): fake = Faker()…
- **Sections:** Creating Functions; Using Partial Functions; Type Annotation; NULL Handling; Exception Handling; Side Effects

### Troubleshooting

- **URL:** https://duckdb.org/docs/current/clients/python/known_issues
- **Summary:** Troubleshooting Running EXPLAIN Renders Newlines In Python, the output of the EXPLAIN statement contains hard line breaks (\n): In [1]: import duckdb ...: duckdb.sql("EXPLAIN SELECT 42 AS x") Out[1]: ┌───────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ explain_key │ explain_value │ │ varchar │ varchar │…
- **Sections:** Troubleshooting; Running EXPLAIN Renders Newlines; Crashes and Errors on Windows; Parameterized Queries in Relational API; Known Issues; Numpy Import Multithreading

### Python API

- **URL:** https://duckdb.org/docs/current/clients/python/overview
- **Summary:** Installation To use the DuckDB Python client, visit the Python installation page. The latest stable version of the DuckDB Python client is . Installation The DuckDB Python API can be installed using pip: pip install duckdb. Please see the installation page for details. It is also possible to install DuckDB using conda: conda install python-duckdb -c…
- **Sections:** Installation; Basic API Usage; Data Input; DataFrames; Result Conversion; Writing Data to Disk

### Python Client API

- **URL:** https://duckdb.org/docs/current/clients/python/reference/
- **Summary:** class duckdb.BinaryValue(object: Any)¶ Bases: Value class duckdb.BinderException¶ Bases: ProgrammingError class duckdb.BitValue(object: Any)¶ Bases: Value class duckdb.BlobValue(object: Any)¶ Bases: Value class duckdb.BooleanValue(object: Any)¶ Bases: Value class duckdb.CSVLineTerminator¶ Bases: pybind11_object Members: LINE_FEED CARRIAGE_RETURN_LINE_FEED CSVLineTerminator.name -> str…

### Relational API

- **URL:** https://duckdb.org/docs/current/clients/python/relational_api
- **Summary:** The Relational API is an alternative API that can be used to incrementally construct queries. The API is centered around DuckDBPyRelation nodes. The relations can be seen as symbolic representations of SQL queries. Lazy Evaluation The relations do not hold any data – and nothing is executed – until a method that triggers execution is called. For example, we create a relation, which loads 1…
- **Sections:** Lazy Evaluation; Relation Creation; Relation Definition Details; Transformation; Functions; Output

### Spark API

- **URL:** https://duckdb.org/docs/current/clients/python/spark_api
- **Summary:** The DuckDB Spark API implements the PySpark API, allowing you to use the familiar Spark API to interact with DuckDB. All statements are translated to DuckDB's internal plans using our relational API and executed using DuckDB's query engine. Warning The DuckDB Spark API is currently experimental and features are still missing. We are very interested in feedback. Please report any functionality…
- **Sections:** Example; Contribution Guidelines

### Types API

- **URL:** https://duckdb.org/docs/current/clients/python/types
- **Summary:** The DuckDBPyType class represents a type instance of our data types. Converting from Other Types To make the API as easy to use as possible, we have added implicit conversions from existing type objects to a DuckDBPyType instance. This means that wherever a DuckDBPyType object is expected, it is also possible to provide any of the options listed below. Python Built-Ins The table below shows…
- **Sections:** Converting from Other Types; Python Built-Ins; Numpy DTypes; Nested Types; Creation Functions

### R Client

- **URL:** https://duckdb.org/docs/current/clients/r
- **Summary:** Installation To use the DuckDB R client, visit the R installation page. The latest stable version of the DuckDB R client is {% if site.current_duckdb_r_version != "" %}{% else %}{% endif %} Installation duckdb: R Client The DuckDB R client can be installed using the following command: install.packages("duckdb") Please see the…
- **Sections:** Installation; duckdb : R Client; duckplyr : dplyr Client; Reference Manual; Basic Client Usage; Startup & Shutdown

### Rust Client

- **URL:** https://duckdb.org/docs/current/clients/rust
- **Summary:** Installation To use the DuckDB Rust client, visit the Rust installation page. The latest stable version of the DuckDB Rust client is {% if site.current_duckdb_rust_version != "" %}{% else %}{% endif %}. Installation The DuckDB Rust client can be installed from crates.io. Please see the docs.rs for details. Basic API Usage…
- **Sections:** Installation; Basic API Usage; Startup & Shutdown; Querying; Appender

### Dart Client

- **URL:** https://duckdb.org/docs/current/clients/tertiary_clients/dart
- **Summary:** The latest stable version of the DuckDB Dart client is {% if site.current_duckdb_dart_version != "" %}{% else %}{% endif %}. DuckDB.Dart is the native Dart API for DuckDB. Installation DuckDB.Dart can be installed from pub.dev. Please see the API Reference for details. Use This Package as a Library Depend on It Add the…
- **Sections:** Installation; Use This Package as a Library; Usage Examples; Querying an In-Memory Database; Using Multiple Connections; Web Support

### Julia Client

- **URL:** https://duckdb.org/docs/current/clients/tertiary_clients/julia
- **Summary:** The DuckDB Julia package provides a high-performance front-end for DuckDB. Much like SQLite, DuckDB runs in-process within the Julia client, and provides a DBInterface front-end. The package also supports multi-threaded execution. It uses Julia threads/tasks for this purpose. If you wish to run queries in parallel, you must launch Julia with multi-threading support (by e.g., setting the…
- **Sections:** Installation; Basics; Scanning DataFrames; Appender API; Concurrency; Original Julia Connector

### Tertiary Clients

- **URL:** https://duckdb.org/docs/current/clients/tertiary_clients/overview
- **Summary:** The following table lists the tertiary clients of DuckDB. Tertiary clients come without any support guarantees. Client API Maintainer Common Lisp ak-coram Crystal amauryt Dart TigerEye Elixir (Duckdbex) AlexR2D2 Elixir (QuackDB) Danila Poyarkov Erlang MM Zeeman Haskell Tritlo Julia The DuckDB team Perl Giuseppe Di Terlizzi PHP satur-io Pyodide The DuckDB team Raku bduggan Ruby suketa Scala…
- **Sections:** Pages in This Section

### PHP Client

- **URL:** https://duckdb.org/docs/current/clients/tertiary_clients/php
- **Summary:** The DuckDB PHP client is a tertiary client and is maintained by a third-party. Client API for PHP, focused on performance. The DuckDB PHP client uses the official C API internally through FFI, achieving good benchmark results. This library is more than just a wrapper for the C API; it introduces custom, PHP-friendly methods to simplify working with DuckDB. It is compatible with Linux, Windows…
- **Sections:** Automatic Install (Recommended for Newcomers); Quick Start; Connection; Prepared Statements; Appenders; DuckDB-Powerful

### Swift Client

- **URL:** https://duckdb.org/docs/current/clients/tertiary_clients/swift
- **Summary:** DuckDB has a Swift client. See the announcement post for details. Instantiating DuckDB DuckDB supports both in-memory and persistent databases. To work with an in-memory database, run: let database = try Database(store: .inMemory) To work with a persistent database, run: let database = try Database(store: .file(at: "test.db")) Queries can be issued through a database connection. let connection…
- **Sections:** Instantiating DuckDB; Application Example; Creating an Application-Specific Type; Loading a CSV File; Querying the Database; Complete Project

### Data Ingestion

- **URL:** https://duckdb.org/docs/current/clients/wasm/data_ingestion
- **Summary:** DuckDB-Wasm has multiple ways to import data, depending on the format of the data. There are two steps to import data into DuckDB. First, the data file is imported into a local file system using register functions (registerEmptyFileBuffer, registerFileBuffer, registerFileHandle, registerFileText, registerFileURL). Then, the data file is imported into DuckDB using insert functions…
- **Sections:** Data Import; Open & Close Connection; Apache Arrow; CSV; JSON; Parquet

### Deploying DuckDB-Wasm

- **URL:** https://duckdb.org/docs/current/clients/wasm/deploying_duckdb_wasm
- **Summary:** A DuckDB-Wasm deployment needs to access the following components: the DuckDB-Wasm main library component, distributed as TypeScript and compiled to JavaScript code the DuckDB-Wasm Worker component, compiled to JavaScript code, possibly instantiated multiple times for threaded environments the DuckDB-Wasm module, compiled as a WebAssembly file and instantiated by the browser any relevant…
- **Sections:** Main Library Component; JS Worker Component; Wasm Worker Component; DuckDB Extensions; Security Considerations

### Extensions

- **URL:** https://duckdb.org/docs/current/clients/wasm/extensions
- **Summary:** DuckDB-Wasm's (dynamic) extension loading is modeled after the regular DuckDB's extension loading, with a few relevant differences due to the difference in platform. Format Extensions in DuckDB are binaries to be dynamically loaded via dlopen. A cryptographical signature is appended to the binary. An extension in DuckDB-Wasm is a regular Wasm file to be dynamically loaded via Emscripten's…
- **Sections:** Format; INSTALL and LOAD; Autoloading; List of Officially Available Extensions; HTTPFS; Extension Signing

### Instantiation

- **URL:** https://duckdb.org/docs/current/clients/wasm/instantiation
- **Summary:** DuckDB-Wasm has multiple ways to be instantiated depending on the use case. cdn(jsdelivr) import * as duckdb from '@duckdb/duckdb-wasm'; const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles(); // Select a bundle based on browser checks const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES); const worker_url = URL.createObjectURL( new Blob([`importScripts("${bundle.mainWorker}");`], {type:…
- **Sections:** cdn(jsdelivr); webpack; vite; Statically Served

### DuckDB Wasm

- **URL:** https://duckdb.org/docs/current/clients/wasm/overview
- **Summary:** Installation To use the DuckDB Wasm client, visit the duckdb-wasm GitHub repository. The latest stable version of the DuckDB WebAssembly client is {% if site.current_duckdb_wasm_version != "" %}{% else %}{% endif %}. DuckDB has been compiled to WebAssembly, so it can run inside any browser on any device. {% include…
- **Sections:** Getting Started with DuckDB-Wasm; Limitations; Pages in This Section

### Query

- **URL:** https://duckdb.org/docs/current/clients/wasm/query
- **Summary:** DuckDB-Wasm provides functions for querying data. Queries are run sequentially. First, a connection needs to be created by calling connect. Then, queries can be run by calling query or send. Query Execution // Create a new connection const conn = await db.connect(); // Either materialize the query result await conn.query<{ v: arrow.Int }>(` SELECT * FROM generate_series(1, 100) t(v) `); //…
- **Sections:** Query Execution; Prepared Statements; Arrow Table to JSON; Export Parquet

## SQL reference (126)

### Constraints

- **URL:** https://duckdb.org/docs/current/sql/constraints
- **Summary:** In SQL, constraints can be specified for tables. Constraints enforce certain properties over data that is inserted into a table. Constraints can be specified along with the schema of the table as part of the CREATE TABLE statement. In certain cases, constraints can also be added to a table using the ALTER TABLE statement, but this is not currently supported for all constraints. Warning…
- **Sections:** Syntax; Check Constraint; Not Null Constraint; Primary Key and Unique Constraint; Foreign Keys

### Array Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/array
- **Summary:** An ARRAY column stores fixed-sized arrays. All fields in the column must have the same length and the same underlying type. Arrays are typically used to store arrays of numbers, but can contain any uniform data type, including ARRAY, LIST and STRUCT types. Arrays can be used to store vectors such as word embeddings or image embeddings. To store variable-length lists, use the LIST type. See the…
- **Sections:** Creating Arrays; Defining an Array Field; Retrieving Values from Arrays; Functions; Examples; Ordering

### Bitstring Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/bitstring
- **Summary:** Name Aliases Description BITSTRING BIT Variable-length strings of 1s and 0s Bitstrings are strings of 1s and 0s. The bit type data is of variable length. A bitstring value requires 1 byte for each group of 8 bits, plus a fixed amount to store some metadata. By default bitstrings will not be padded with zeroes. Bitstrings can be very large, having the same size restrictions as BLOBs. Creating a…
- **Sections:** Creating a Bitstring; Functions

### Blob Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/blob
- **Summary:** Name Aliases Description BLOB BYTEA, BINARY, VARBINARY Variable-length binary data The blob (Binary Large OBject) type represents an arbitrary binary object stored in the database system. The blob type can contain any type of binary data with no restrictions. What the actual bytes represent is opaque to the database system. Create a BLOB value with a single byte (170): SELECT '\xAA'::BLOB;…
- **Sections:** Functions

### Boolean Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/boolean
- **Summary:** Name Aliases Description BOOLEAN BOOL Logical Boolean (true / false) The BOOLEAN type represents a statement of truth (“true” or “false”). In SQL, the BOOLEAN field can also have a third state “unknown” which is represented by the SQL NULL value. Select the three possible values of a BOOLEAN column: SELECT true, false, NULL::BOOLEAN; Boolean values can be explicitly created using the literals…
- **Sections:** Conjunctions; Expressions

### Date Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/date
- **Summary:** Name Aliases Description DATE Calendar date (year, month, day) A date specifies a combination of year, month and day. DuckDB follows the SQL standard's lead by counting dates exclusively in the Gregorian calendar, even for years before that calendar was in use. Dates can be created using the DATE keyword, where the data must be formatted according to the ISO 8601 format (YYYY-MM-DD). SELECT…
- **Sections:** Special Values; Functions

### Enum Data Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/enum
- **Summary:** Name Description ENUM Dictionary representing all possible string values of a column The enum type represents a dictionary data structure with all possible unique values of a column. For example, a column storing the days of the week can be an enum holding all possible days. Enums are particularly interesting for string columns with low cardinality (i.e., fewer distinct values). This is…
- **Sections:** Creating Enums; Using Enums; Enums vs. Strings; Ordering of Enums; Functions; Enum Removal

### Geometry Data Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/geometry
- **Summary:** Name Description GEOMETRY Geospatial entity The GEOMETRY data type is used to store and manipulate geometric objects, such as points, lines, and polygons. The GEOMETRY type was part of the spatial extension but became a built-in data type in DuckDB v1.5. Most of the benefits of having GEOMETRY as a built-in type (e.g., storage optimizations, statistics, etc.) are therefore only available in…
- **Sections:** Types of Geometries; Multi-Dimensional Geometries; Empty Geometries; Geometry Storage; Shredding and Compression; Geometry Statistics

### Interval Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/interval
- **Summary:** INTERVALs represent periods of time that can be added to or subtracted from DATE, TIMESTAMP, TIMESTAMPTZ, or TIME values. Name Description INTERVAL Period of time An INTERVAL can be constructed by providing amounts together with units. Units that aren't months, days, or microseconds are converted to equivalent amounts in the next smaller of these three basis units. SELECT INTERVAL 1 YEAR, --…
- **Sections:** Arithmetic with Timestamps, Dates and Intervals; Equality and Comparison; Functions

### List Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/list
- **Summary:** A LIST column encodes lists of values. Fields in the column can have values with different lengths, but they must all have the same underlying type. LISTs are typically used to store arrays of numbers, but can contain any uniform data type, including other LISTs and STRUCTs. LISTs are similar to PostgreSQL's ARRAY type. DuckDB uses the LIST terminology, but some array_ functions are provided…
- **Sections:** Creating Lists; Retrieving from Lists; Comparison and Ordering; Functions

### Literal Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/literal_types
- **Summary:** DuckDB has special literal types for representing NULL, integer and string literals in queries. These have their own binding and conversion rules. Prior to DuckDB version 0.10.0, integer and string literals behaved identically to the INTEGER and VARCHAR types. Null Literals The NULL literal is denoted with the keyword NULL. The NULL literal can be implicitly converted to any other type.…
- **Sections:** Null Literals; Integer Literals; Other Numeric Literals; Underscores in Numeric Literals; String Literals; Implicit String Literal Concatenation

### Map Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/map
- **Summary:** MAPs are similar to STRUCTs in that they are an ordered list of key-value pairs. However, MAPs do not need to have the same keys present for each row, and thus are suitable for use cases where the schema is unknown beforehand or varies per row. MAPs must have a single type for all keys, and a single type for all values. Keys and values can be any type, and the type of the keys does not need to…
- **Sections:** Creating Maps; Retrieving from Maps; Comparison Operators; Functions

### NULL Values

- **URL:** https://duckdb.org/docs/current/sql/data_types/nulls
- **Summary:** NULL values are special values that are used to represent missing data in SQL. Columns of any type can contain NULL values. Logically, a NULL value can be seen as “the value of this field is unknown”. A NULL value can be inserted to any field that does not have the NOT NULL qualifier: CREATE TABLE integers (i INTEGER); INSERT INTO integers VALUES (NULL); NULL values have special semantics in…
- **Sections:** NULL and Functions; NULL and AND / OR; NULL and IN / NOT IN; NULL and Aggregate Functions

### Numeric Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/numeric
- **Summary:** Fixed-Width Integer Types The types TINYINT, SMALLINT, INTEGER, BIGINT and HUGEINT store whole numbers, that is, numbers without fractional components, of various ranges. Attempts to store values outside of the allowed range will result in an error. The types UTINYINT, USMALLINT, UINTEGER, UBIGINT and UHUGEINT store whole unsigned numbers. Attempts to store negative numbers or values outside…
- **Sections:** Fixed-Width Integer Types; Variable-Length Integers; Fixed-Point Decimals; Floating-Point Types; Universally Unique Identifiers ( UUID s); UUIDv4

### Data Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/overview
- **Summary:** General-Purpose Data Types The table below shows all the built-in general-purpose data types. The alternatives listed in the aliases column can be used to refer to these types as well, however, note that the aliases are not part of the SQL standard and hence might not be accepted by other database engines. Name Aliases Description BIGINT INT8, LONG Signed eight-byte integer BIT BITSTRING…
- **Sections:** General-Purpose Data Types; Nested / Composite Types; Rules for Case Sensitivity; Updating Values of Nested Types; Nesting; Performance Implications

### Struct Data Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/struct
- **Summary:** Conceptually, a STRUCT column contains an ordered list of columns called “entries”. The entries are referenced by name using strings. This document refers to those entry names as keys. Each row in the STRUCT column must have the same keys. The names of the struct entries are part of the schema. Each row in a STRUCT column must have the same layout. The names of the struct entries are…
- **Sections:** Creating Structs; Adding or Updating Fields of Structs; Retrieving from Structs; unnest / STRUCT.*; Dot Notation Order of Operations; No Dots

### Text Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/text
- **Summary:** In DuckDB, strings can be stored in the VARCHAR field. The field allows storage of Unicode characters. Internally, the data is encoded as UTF-8. Name Aliases Description VARCHAR CHAR, BPCHAR, STRING, TEXT Variable-length character string VARCHAR(n) CHAR(n), BPCHAR(n), STRING(n), TEXT(n) Variable-length character string. The maximum length n has no effect and is only provided for compatibility…
- **Sections:** Specifying a Length Limit; Specifying a Compression Type; Text Type Values; Strings with Special Characters; Functions

### Time Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/time
- **Summary:** The TIME and TIMETZ types specify the hour, minute, second, microsecond of a day. Name Aliases Description TIME TIME WITHOUT TIME ZONE Time of day TIMETZ TIME WITH TIME ZONE Time of day, with time zone offset TIME_NS Time of day, nanosecond precision Instances can be created using the type names as a keyword, where the data must be formatted according to the ISO 8601 format…

### Timestamp Types

- **URL:** https://duckdb.org/docs/current/sql/data_types/timestamp
- **Summary:** Timestamps represent points in time. As such, they combine DATE and TIME information. They can be created using the type name followed by a string formatted according to the ISO 8601 format, YYYY-MM-DD hh:mm:ss[.zzzzzzzzz][+-TT[:tt]], which is also the format we use in this documentation. Decimal places beyond the supported precision are ignored. Timestamp Types Name Aliases Description…
- **Sections:** Timestamp Types; Conversion between Strings and Naïve / Time Zone-Aware Timestamps; Special Values; Functions; Time Zones; Instants

### Time Zone Reference List

- **URL:** https://duckdb.org/docs/current/sql/data_types/timezones
- **Summary:** An up-to-date version of this list can be pulled from the pg_timezone_names() table function: SELECT name, abbrev FROM pg_timezone_names() ORDER BY name; name abbrev ACT ACT AET AET AGT AGT ART ART AST AST Africa/Abidjan Iceland Africa/Accra Iceland Africa/Addis_Ababa EAT Africa/Algiers Africa/Algiers Africa/Asmara EAT Africa/Asmera EAT Africa/Bamako Iceland Africa/Bangui Africa/Bangui…

### Typecasting

- **URL:** https://duckdb.org/docs/current/sql/data_types/typecasting
- **Summary:** Typecasting is an operation that converts a value in one particular data type to the closest corresponding value in another data type. Like other SQL engines, DuckDB supports both implicit and explicit typecasting. Explicit Casting Explicit typecasting is performed by using a CAST expression. For example, CAST(col AS VARCHAR) or col::VARCHAR explicitly cast the column col to VARCHAR. See the…
- **Sections:** Explicit Casting; Implicit Casting; Combination Casting; Casting Operations Matrix; Lossy Casts; Overflows

### Union Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/union
- **Summary:** A UNION type (not to be confused with the SQL UNION operator) is a nested type capable of holding one of multiple “alternative” values, much like the union in C. The main difference is that these UNION types are tagged unions and thus always carry a discriminator “tag” which signals which alternative it is currently holding, even if the inner value itself is null. UNION types are thus more…
- **Sections:** Example; Union Casts; Casting to Unions; Casting between Unions; Comparison and Sorting; Functions

### Variant Type

- **URL:** https://duckdb.org/docs/current/sql/data_types/variant
- **Summary:** The VARIANT type stores typed, binary data where each row is self-contained with its own type information. This differs from the JSON type, which is physically stored as text. Because type metadata is embedded per-value, VARIANT provides better compression and query performance than JSON for semi-structured data. The VARIANT type is inspired by Snowflake's semi-structured VARIANT data type. It…
- **Sections:** Examples; Storing Different Types in the Same Column; Checking the Type of a Value; Extracting Fields from Nested Variants; Parquet Support; Writing VARIANT to Parquet

### Friendly SQL

- **URL:** https://duckdb.org/docs/current/sql/dialect/friendly_sql
- **Summary:** DuckDB offers several advanced SQL features and syntactic sugar to make SQL queries more concise. We refer to these colloquially as “friendly SQL”. Several of these features were first introduced by DuckDB, while some are inspired by other systems. Many of the features originally introduced by DuckDB (e.g., GROUP BY ALL) have been since adapted by other systems. Tip We have a Friendly SQL 2026…
- **Sections:** Clauses; Query Features; Literals and Identifiers; Data Types; Data Import; Functions and Expressions

### Indexing

- **URL:** https://duckdb.org/docs/current/sql/dialect/indexing
- **Summary:** DuckDB uses 1-based indexing except for JSON objects, which use 0-based indexing. Examples The index origin is 1 for strings, lists, etc. SELECT list[1] AS element FROM (SELECT ['first', 'second', 'third'] AS list); ┌─────────┐ │ element │ │ varchar │ ├─────────┤ │ first │ └─────────┘ The index origin is 0 for JSON objects. SELECT json[1] AS element FROM (SELECT '["first", "second",…
- **Sections:** Examples

### Keywords and Identifiers

- **URL:** https://duckdb.org/docs/current/sql/dialect/keywords_and_identifiers
- **Summary:** Identifiers Similarly to other SQL dialects and programming languages, identifiers in DuckDB's SQL are subject to several rules. Unquoted identifiers need to conform to a number of rules: They must not be a reserved keyword (see duckdb_keywords()), e.g., SELECT 123 AS SELECT will fail. They must not start with a number or special character, e.g., SELECT 123 AS 1col is invalid. They cannot…
- **Sections:** Identifiers; Deduplicating Identifiers; Database Names; Rules for Case-Sensitivity; Keywords and Function Names; Case-Sensitivity of Identifiers

### Order Preservation

- **URL:** https://duckdb.org/docs/current/sql/dialect/order_preservation
- **Summary:** For many operations, DuckDB preserves the order of rows, similarly to data frame libraries such as Pandas. Example Take the following table for example: CREATE TABLE tbl AS SELECT * FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) t(x, y); SELECT * FROM tbl; x y 1 a 2 b 3 c Let's take the following query that returns the rows where x is an odd number: SELECT * FROM tbl WHERE x % 2 == 1; x y 1 a 3 c…
- **Sections:** Example; Clauses; Insertion Order

### Overview

- **URL:** https://duckdb.org/docs/current/sql/dialect/overview
- **Summary:** DuckDB's SQL dialect is based on PostgreSQL. DuckDB tries to closely match PostgreSQL's semantics, however, some use cases require slightly different behavior. For example, interchangeability with data frame libraries necessitates order preservation of inserts to be supported by default. These differences are documented in the pages below.
- **Sections:** Pages in This Section

### PostgreSQL Compatibility

- **URL:** https://duckdb.org/docs/current/sql/dialect/postgresql_compatibility
- **Summary:** DuckDB's SQL dialect closely follows the conventions of the PostgreSQL dialect. The few exceptions to this are listed
- **Sections:** Floating-Point Arithmetic; Division on Integers; UNION of Boolean and Integer Values; Implicit Casting on Equality Checks; Case Sensitivity for Quoted Identifiers; Using Double Equality Sign for Comparison

### SQL Quirks

- **URL:** https://duckdb.org/docs/current/sql/dialect/sql_quirks
- **Summary:** Like all programming languages and libraries, DuckDB has its share of idiosyncrasies and inconsistencies. Some are vestiges of our feathered friend's evolution; others are inevitable because we strive to adhere to the SQL Standard and specifically to PostgreSQL's dialect (see the “PostgreSQL Compatibility” page for exceptions). The rest may simply come down to different preferences, or we may…
- **Sections:** Aggregating Empty Groups; 0 vs. 1-Based Indexing; Types; UINT8 vs. INT8; Expressions; Results That May Surprise You

### CASE Expression

- **URL:** https://duckdb.org/docs/current/sql/expressions/case
- **Summary:** The CASE expression performs a switch based on a condition. The basic form is identical to the ternary condition used in many programming languages (CASE WHEN cond THEN a ELSE b END is equivalent to cond ? a : b). With a single condition this can be expressed with IF(cond, a, b). CREATE OR REPLACE TABLE integers AS SELECT unnest([1, 2, 3]) AS i; SELECT i, CASE WHEN i > 2 THEN 1 ELSE 0 END AS…
- **Sections:** SWITCH Expression

### Casting

- **URL:** https://duckdb.org/docs/current/sql/expressions/cast
- **Summary:** Casting refers to the operation of converting a value in a particular data type to the corresponding value in another data type. Casting can occur either implicitly or explicitly. The syntax described here performs an explicit cast. More information on casting can be found on the typecasting page. Explicit Casting The standard SQL syntax for explicit casting is CAST(expr AS TYPENAME), where…
- **Sections:** Explicit Casting; Casting Rules; TRY_CAST; cast_to_type Function

### Collations

- **URL:** https://duckdb.org/docs/current/sql/expressions/collations
- **Summary:** Collations provide rules for how text should be sorted or compared in the execution engine. Collations are useful for localization, as the rules for how text should be ordered are different for different languages or for different countries. These orderings are often incompatible with one another. For example, in English the letter y comes between x and z. However, in Lithuanian the letter y…
- **Sections:** Using Collations; Default Collations; ICU Collations

### Comparisons

- **URL:** https://duckdb.org/docs/current/sql/expressions/comparison_operators
- **Summary:** Comparison Operators The table below shows the standard comparison operators. Whenever either of the input arguments is NULL, the output of the comparison is NULL. Operator Description Example Result < less than 2 < 3 true > greater than 2 > 3 false <= less than or equal to 2 <= 3 true >= greater than or equal to 4 >= NULL NULL = or == equal NULL = NULL NULL <> or != not equal 2 <> 2 false The…
- **Sections:** Comparison Operators; Combination Casting; BETWEEN and IS [NOT] NULL

### IN Operator

- **URL:** https://duckdb.org/docs/current/sql/expressions/in
- **Summary:** The IN operator checks containment of the left expression inside the collection on the right hand side (RHS). Supported collections on the RHS are tuples, lists, and maps, as well as subqueries that return a single column. The single-column restriction applies only to subqueries; tuples, lists, and maps may themselves contain composite values. IN (val1, val2, ...) (Tuple) The IN operator on a…
- **Sections:** IN (val1, val2, ...) (Tuple); IN [val1, val2, ...] (List); IN Map; IN Subquery; IN String; NOT IN

### Logical Operators

- **URL:** https://duckdb.org/docs/current/sql/expressions/logical_operators
- **Summary:** The following logical operators are available: AND, OR and NOT. SQL uses a three-valued logic system with true, false and NULL. Note that logical operators involving NULL do not always evaluate to NULL. For example, NULL AND false will evaluate to false, and NULL OR true will evaluate to true. Below are the complete truth tables. Binary Operators: AND and OR a b a AND b a OR b true true true…
- **Sections:** Binary Operators: AND and OR; Unary Operator: NOT

### Expressions

- **URL:** https://duckdb.org/docs/current/sql/expressions/overview
- **Summary:** An expression is a combination of values, operators and functions. Expressions are highly composable, and range from very simple to arbitrarily complex. They can be found in many different parts of SQL statements. This section describes the different types of operators and functions that can be used within expressions.
- **Sections:** Pages in This Section

### Star Expression

- **URL:** https://duckdb.org/docs/current/sql/expressions/star
- **Summary:** Syntax The * expression can be used in a SELECT statement to select all columns that are projected in the FROM clause. SELECT * FROM tbl; TABLE.* and STRUCT.* The * expression can be prepended by a table name to select only columns from that table. SELECT tbl.* FROM tbl JOIN other_tbl USING (id); Similarly, the * expression can also be used to retrieve all keys from a struct as separate…
- **Sections:** Syntax; TABLE.* and STRUCT.*; EXCLUDE Clause; REPLACE Clause; RENAME Clause; Column Filtering via Pattern Matching Operators

### Subqueries

- **URL:** https://duckdb.org/docs/current/sql/expressions/subqueries
- **Summary:** Subqueries are parenthesized query expressions that appear as part of a larger, outer query. Subqueries are usually based on SELECT ... FROM, but in DuckDB other query constructs such as PIVOT can also appear as a subquery. Scalar Subquery Scalar subqueries are subqueries that return a single value. They can be used anywhere where an expression can be used. If a scalar subquery returns more…
- **Sections:** Scalar Subquery; Grades; ARRAY Subqueries; Subquery Comparisons: ALL , ANY and SOME; ALL; ANY

### TRY Expression

- **URL:** https://duckdb.org/docs/current/sql/expressions/try
- **Summary:** The TRY expression ensures that errors caused by the input rows in the child (scalar) expression result in NULL for those rows, instead of causing the query to throw an error. The TRY expression was inspired by the TRY_CAST expression. Examples The following calls return errors when invoked without the TRY expression. When they are wrapped into a TRY expression, they return NULL: Casting…
- **Sections:** Examples; Casting; Logarithm on Zero; Casting Multiple Rows; Limitations

### Aggregate Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/aggregates
- **Summary:** Examples Produce a single row containing the sum of the amount column: SELECT sum(amount) FROM sales; Produce one row per unique region, containing the sum of amount for each group: SELECT region, sum(amount) FROM sales GROUP BY region; Return only the regions that have a sum of amount higher than 100: SELECT region FROM sales GROUP BY region HAVING sum(amount) > 100; Return the number of…
- **Sections:** Examples; Syntax; DISTINCT Clause in Aggregate Functions; ORDER BY Clause in Aggregate Functions; Handling NULL Values; General Aggregate Functions

### Array Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/array
- **Summary:** All LIST functions work with the ARRAY data type. Additionally, several ARRAY-native functions are also supported. Array-Native Functions Function Description array_cosine_distance(array1, array2) Computes the cosine distance between two arrays of the same size. The array elements cannot be NULL. The arrays can have any size as long as the size is the same for both arguments.…
- **Sections:** Array-Native Functions

### Bitstring Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/bitstring
- **Summary:** This section describes functions and operators for examining and manipulating BITSTRING values. Bitstrings must be of equal length when performing the bitwise operands AND, OR and XOR. When bit shifting, the original length of the string is preserved. Bitstring Operators The table below shows the available mathematical operators for BIT type. Operator Description Example Result & Bitwise AND…
- **Sections:** Bitstring Operators; Bitstring Functions; Bitstring Aggregate Functions

### Blob Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/blob
- **Summary:** This section describes functions and operators for examining and manipulating BLOB values. Function Description arg1 || arg2 Concatenates two strings, lists, or blobs. Any NULL input results in NULL. See also concat(arg1, arg2, ...) and list_concat(list1, list2, ...). base64(blob) Alias for to_base64. decode(blob[, on_error]) Converts blob to VARCHAR. The optional on_error parameter controls…

### Date Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/date
- **Summary:** This section describes functions and operators for examining and manipulating DATE values. Date Operators The table below shows the available mathematical operators for DATE types. Operator Description Example Result + addition of days (integers) DATE '1992-03-22' + 5 1992-03-27 + addition of AN INTERVAL DATE '1992-03-22' + INTERVAL 5 DAY 1992-03-27 00:00:00 + addition of a variable INTERVAL…
- **Sections:** Date Operators; Date Functions; Date Part Extraction Functions

### Date Format Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/dateformat
- **Summary:** The strftime and strptime functions can be used to convert between DATE / TIMESTAMP values and strings. This is often required when parsing CSV files, displaying output to the user or transferring information between programs. Because there are many possible date representations, these functions accept a format string that describes how the date or timestamp should be structured. strftime…
- **Sections:** strftime Examples; strptime Examples; CSV Parsing; Format Specifiers

### Date Part Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/datepart
- **Summary:** The date_part, date_trunc and date_diff functions can be used to extract or manipulate parts of temporal types such as TIMESTAMP, TIMESTAMPTZ, DATE and INTERVAL. The parts to be extracted or manipulated are specified by one of the strings in the tables below. The example column provides the corresponding parts of the timestamp 2021-08-03 11:59:44.123456. Only the entries of the first table can…
- **Sections:** Part Specifiers Usable as Date Part Specifiers and in Intervals; Part Specifiers Only Usable as Date Part Specifiers; Part Functions

### Enum Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/enum
- **Summary:** This section describes functions and operators for examining and manipulating ENUM values. The examples assume an enum type created as: CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy', 'anxious'); These functions can take NULL or a specific value of the type as argument(s). With the exception of enum_range_boundary, the result depends only on the type of the argument and not on its value. Name…

### Geometry Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/geometry
- **Summary:** This section describes the functions for for examining and manipulating GEOMETRY values. Note: The spatial extension provides additional functions for working with GEOMETRY values, which are documented in the Spatial Functions section. Geometry Operators The table below lists the operators that can be used with GEOMETRY values. Operator Description Example Result && Returns true if the…
- **Sections:** Geometry Operators; Built-in Geometry Functions

### Interval Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/interval
- **Summary:** This section describes functions and operators for examining and manipulating INTERVAL values. Interval Operators The table below shows the available mathematical operators for INTERVAL types. Operator Description Example Result + Addition of an INTERVAL INTERVAL 1 HOUR + INTERVAL 5 HOUR INTERVAL 6 HOUR + Addition to a DATE DATE '1992-03-22' + INTERVAL 5 DAY 1992-03-27 00:00:00 + Addition to a…
- **Sections:** Interval Operators; Interval Functions

### Lambda Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/lambda
- **Summary:** Deprecated DuckDB v1.3 deprecated the old lambda single arrow syntax (x -> x + 1) in favor of the Python-style syntax (lambda x : x + 1). DuckDB v1.3 also introduces a new setting to configure the lambda syntax. SET lambda_syntax = 'DEFAULT'; SET lambda_syntax = 'ENABLE_SINGLE_ARROW'; SET lambda_syntax = 'DISABLE_SINGLE_ARROW'; Currently, DEFAULT enables both syntax styles, i.e., the old…
- **Sections:** Scalar Functions That Accept Lambda Functions; Nesting Lambda Functions; Scoping; Indexes as Parameters; Examples; list_transform Examples

### List Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/list
- **Summary:** Function Description list[index] Extracts a single list element using a (1-based) index. list[begin[:end][:step]] Extracts a sublist using slice conventions. Negative values are accepted. list1 && list2 Alias for list_has_any. list1 <-> list2 Alias for list_distance. list1 <=> list2 Alias for list_cosine_distance. list1 <@ list2 Alias for list_has_all. list1 @> list2 Alias for list_has_all.…
- **Sections:** List Operators; List Comprehension; Range Functions; range; generate_series; Date Ranges

### Map Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/map
- **Summary:** Name Description cardinality(map) Return the size of the map (or the number of entries in the map). element_at(map, key) Return the value for a given key as a list, or an empty list if the key is not contained in the map. The type of the key provided in the second parameter must match the type of the map's keys; else, an error is thrown. map_concat(maps...) Returns a map created from merging…

### Nested Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/nested
- **Summary:** There are five nested data types: Name Type page Functions page ARRAY ARRAY type ARRAY functions LIST LIST type LIST functions MAP MAP type MAP functions STRUCT STRUCT type STRUCT functions UNION UNION type UNION functions

### Numeric Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/numeric
- **Summary:** Numeric Operators The table below shows the available mathematical operators for numeric types. Operator Description Example Result + Addition 2 + 3 5 - Subtraction 2 - 3 -1 * Multiplication 2 * 3 6 / Float division 5 / 2 2.5 // Division 5 // 2 2 % Modulo (remainder) 5 % 4 1 ** Exponent 3 ** 4 81 ^ Exponent (alias for **) 3 ^ 4 81 & Bitwise AND 91 & 15 11 | Bitwise OR 32 | 3 35 << Bitwise…
- **Sections:** Numeric Operators; Division and Modulo Operators; Supported Types; Numeric Functions

### Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/overview
- **Summary:** Function Syntax Function Chaining via the Dot Operator DuckDB supports the dot syntax for function chaining. This allows the function call fn(arg1, arg2, arg3, ...) to be rewritten as arg1.fn(arg2, arg3, ...). For example, take the following use of the replace function: SELECT replace(goose_name, 'goose', 'duck') AS duck_name FROM unnest(['African goose', 'Faroese goose', 'Hungarian goose',…
- **Sections:** Function Syntax; Function Chaining via the Dot Operator; Using with Literals and Arrays; Limitations; Query Functions; Pages in This Section

### Pattern Matching

- **URL:** https://duckdb.org/docs/current/sql/functions/pattern_matching
- **Summary:** There are four separate approaches to pattern matching provided by DuckDB: the traditional SQL LIKE operator, the more recent SIMILAR TO operator (added in SQL:1999), a GLOB operator, and POSIX-style regular expressions. LIKE The LIKE expression returns true if the string matches the supplied pattern. (As expected, the NOT LIKE expression returns false if LIKE returns true, and vice versa. An…
- **Sections:** LIKE; SIMILAR TO; Globbing; GLOB; Glob Function to Find Filenames; Globbing Semantics

### Regular Expressions

- **URL:** https://duckdb.org/docs/current/sql/functions/regular_expressions
- **Summary:** DuckDB offers pattern matching operators (LIKE, SIMILAR TO, GLOB), as well as support for regular expressions via functions. Regular Expression Syntax DuckDB uses the RE2 library as its regular expression engine. For the regular expression syntax, see the RE2 docs. Functions All functions accept an optional set of options. Name Description regexp_extract(string, pattern[, group = 0][,…
- **Sections:** Regular Expression Syntax; Functions; Options for Regular Expression Functions; Using regexp_matches; Using regexp_replace; Using regexp_extract

### Struct Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/struct
- **Summary:** Name Description struct.entry Dot notation that serves as an alias for struct_extract from named STRUCTs. struct[entry] Bracket notation that serves as an alias for struct_extract from named STRUCTs. struct[idx] Bracket notation that serves as an alias for struct_extract from unnamed STRUCTs (tuples), using an index (1-based). row(any, ...) Create an unnamed STRUCT (tuple) containing the…

### Text Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/text
- **Summary:** Text Functions and Operators This section describes functions and operators for examining and manipulating STRING values. Function Description string[index] Extracts a single character using a (1-based) index. string[begin:end] Extracts a string using slice conventions similar to Python. Missing begin or end arguments are interpreted as the beginning or end of the list respectively. Negative…
- **Sections:** Text Functions and Operators; Text Similarity Functions; Formatters; fmt Syntax; printf Syntax

### Time Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/time
- **Summary:** This section describes functions and operators for examining and manipulating TIME values. Time Operators The table below shows the available mathematical operators for TIME types. Operator Description Example Result + addition of an INTERVAL TIME '01:02:03' + INTERVAL 5 HOUR 06:02:03 - subtraction of an INTERVAL TIME '06:02:03' - INTERVAL 5 HOUR 01:02:03 Time Functions The table below shows…
- **Sections:** Time Operators; Time Functions

### Timestamp Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/timestamp
- **Summary:** This section describes functions and operators for examining and manipulating TIMESTAMP values. See also the related TIMESTAMPTZ functions. Timestamp Operators The table below shows the available mathematical operators for TIMESTAMP types. Operator Description Example Result + addition of an INTERVAL TIMESTAMP '1992-03-22 01:02:03' + INTERVAL 5 DAY 1992-03-27 01:02:03 - subtraction of…
- **Sections:** Timestamp Operators; Scalar Timestamp Functions; Timestamp Table Functions

### Timestamp with Time Zone Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/timestamptz
- **Summary:** This section describes functions and operators for examining and manipulating TIMESTAMP WITH TIME ZONE (or TIMESTAMPTZ) values. See also the related TIMESTAMP functions. Time zone support is provided by the built-in ICU extension. In the examples below, the current time zone is presumed to be America/Los_Angeles using the Gregorian calendar. Built-In Timestamp with Time Zone Functions The…
- **Sections:** Built-In Timestamp with Time Zone Functions; Timestamp with Time Zone Strings; ICU Timestamp with Time Zone Operators; ICU Timestamp with Time Zone Functions; ICU Timestamp Table Functions; ICU Timestamp Without Time Zone Functions

### Union Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/union
- **Summary:** Name Description union.tag Dot notation serves as an alias for union_extract. union_extract(union, 'tag') Extract the value with the named tags from the union. NULL if the tag is not currently selected. union_value(tag := any) Create a single member UNION containing the argument value. The tag of the value will be the bound variable name. union_tag(union) Retrieve the currently selected tag of…

### Utility Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/utility
- **Summary:** Scalar Utility Functions The functions below are difficult to categorize into specific function types and are broadly useful. Name Description alias(column) Return the name of the column. can_cast_implicitly(source_value, target_value) Whether or not we can implicitly cast from the types of the source value to the target value. checkpoint(database) Synchronize WAL with file for (optional)…
- **Sections:** Scalar Utility Functions; Utility Table Functions

### Window Functions

- **URL:** https://duckdb.org/docs/current/sql/functions/window_functions
- **Summary:** DuckDB supports window functions, which can use multiple rows to calculate a value for each row. Window functions are blocking operators, i.e., they require their entire input to be buffered, making them one of the most memory-intensive operators in SQL. Window functions are available in SQL since SQL:2003 and are supported by major SQL database systems. Examples Generate a row_number column…
- **Sections:** Examples; Syntax; General-Purpose Window Functions; Aggregate Window Functions; DISTINCT Arguments; ORDER BY Arguments

### Indexes

- **URL:** https://duckdb.org/docs/current/sql/indexes
- **Summary:** Index Types DuckDB has two built-in index types. Indexes can also be defined via extensions. Min-Max Index (Zonemap) A min-max index (also known as zonemap or block range index) is automatically created for columns of all general-purpose data types. Adaptive Radix Tree (ART) An Adaptive Radix Tree (ART) is mainly used to ensure primary key constraints and to speed up point and very highly…
- **Sections:** Index Types; Min-Max Index (Zonemap); Adaptive Radix Tree (ART); Indexes Defined by Extensions; Persistence; CREATE INDEX and DROP INDEX Statements

### SQL Introduction

- **URL:** https://duckdb.org/docs/current/sql/introduction
- **Summary:** This page provides an overview of how to perform simple operations in SQL. This tutorial is only intended to give you an introduction and is in no way a complete tutorial on SQL. This tutorial is adapted from the PostgreSQL tutorial. DuckDB's SQL dialect closely follows the conventions of the PostgreSQL dialect. The few exceptions to this are listed on the PostgreSQL compatibility page. In the…
- **Sections:** Concepts; Creating a New Table; Populating a Table with Rows; Querying a Table; Joins between Tables; Aggregate Functions

### DuckDB_% Metadata Functions

- **URL:** https://duckdb.org/docs/current/sql/meta/duckdb_table_functions
- **Summary:** DuckDB offers a collection of table functions that provide metadata about the current database. These functions reside in the main schema and their names are prefixed with duckdb_. The resultset returned by a duckdb_ table function may be used just like an ordinary table or view. For example, you can use a duckdb_ function call in the FROM clause of a SELECT statement, and you may refer to the…
- **Sections:** duckdb_columns; duckdb_constraints; duckdb_coordinate_systems; duckdb_databases; duckdb_dependencies; duckdb_extensions

### Information Schema

- **URL:** https://duckdb.org/docs/current/sql/meta/information_schema
- **Summary:** The views in the information_schema are SQL-standard views that describe the catalog entries of the database. These views can be filtered to obtain information about a specific column or table. DuckDB's implementation is based on PostgreSQL's information schema. Tables character_sets: Character Sets Column Description Type Example character_set_catalog Currently not implemented – always NULL.…
- **Sections:** Tables; character_sets : Character Sets; columns : Columns; constraint_column_usage : Constraint Column Usage; key_column_usage : Key Column Usage; referential_constraints : Referential Constraints

### PEG Parser

- **URL:** https://duckdb.org/docs/current/sql/peg_parser
- **Summary:** DuckDB v1.5 shipped an experimental parser based on PEG (Parser Expression Grammars). The new parser enables better suggestions, improved error messages, and allows extensions to extend the grammar. The PEG parser is currently disabled by default but you can opt-in using: CALL enable_peg_parser(); The PEG parser is already used for generating suggestions. You can cycle through the options…

### FILTER Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/filter
- **Summary:** The FILTER clause may optionally follow an aggregate function in a SELECT statement. This will filter the rows of data that are fed into the aggregate function in the same way that a WHERE clause filters rows, but localized to the specific aggregate function. There are multiple types of situations where this is useful, including when evaluating multiple aggregates with different filters, and…
- **Sections:** Examples; Aggregate Function Syntax (Including FILTER Clause)

### FROM and JOIN Clauses

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/from
- **Summary:** The FROM clause specifies the source of the data on which the remainder of the query should operate. Logically, the FROM clause is where the query starts execution. The FROM clause can contain a single table, a combination of multiple tables that are joined together using JOIN clauses, or another SELECT query inside a subquery node. DuckDB also has an optional FROM-first syntax which enables…
- **Sections:** Examples; Table Functions; Joins; Outer Joins; Cross Product Joins (Cartesian Product); Conditional Joins

### GROUP BY Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/groupby
- **Summary:** The GROUP BY clause specifies which grouping columns should be used to perform any aggregations in the SELECT clause. If the GROUP BY clause is specified, the query is always an aggregate query, even if no aggregations are present in the SELECT clause. When a GROUP BY clause is specified, all tuples that have matching data in the grouping columns (i.e., all tuples that belong to the same…
- **Sections:** GROUP BY ALL; Multiple Dimensions; Examples; GROUP BY ALL Examples; Syntax

### GROUPING SETS

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/grouping_sets
- **Summary:** GROUPING SETS, ROLLUP and CUBE can be used in the GROUP BY clause to perform a grouping over multiple dimensions within the same query. Note that this syntax is not compatible with GROUP BY ALL. Examples Compute the average income along the provided four different dimensions: -- the syntax () denotes the empty set (i.e., computing an ungrouped aggregate) SELECT city, street_name, avg(income)…
- **Sections:** Examples; Description; Identifying Grouping Sets with GROUPING_ID(); Syntax

### HAVING Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/having
- **Summary:** The HAVING clause can be used after the GROUP BY clause to provide filter criteria after the grouping has been completed. In terms of syntax the HAVING clause is identical to the WHERE clause, but while the WHERE clause occurs before the grouping, the HAVING clause occurs after the grouping. Examples Count the number of entries in the addresses table that belong to each different city,…
- **Sections:** Examples; Syntax

### LIMIT and OFFSET Clauses

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/limit
- **Summary:** LIMIT is an output modifier. Logically it is applied at the very end of the query. The LIMIT clause restricts the amount of rows fetched. The OFFSET clause indicates at which position to start reading the values, i.e., the first OFFSET values are ignored. Note that while LIMIT can be used without an ORDER BY clause, the results might not be deterministic without the ORDER BY clause. This can…
- **Sections:** Examples; Syntax

### ORDER BY Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/orderby
- **Summary:** ORDER BY is an output modifier. Logically it is applied near the very end of the query (just prior to LIMIT or OFFSET, if present). The ORDER BY clause sorts the rows on the sorting criteria in either ascending or descending order. In addition, every order clause can specify whether NULL values should be moved to the beginning or to the end. The ORDER BY clause may contain one or more…
- **Sections:** ORDER BY ALL; NULL Order Modifier; Collations; Examples; ORDER BY ALL Examples; Syntax

### Prepared Statements

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/prepared_statements
- **Summary:** DuckDB supports prepared statements where parameters are substituted when the query is executed. This can improve readability and is useful for preventing SQL injections. Syntax There are three syntaxes for denoting parameters in prepared statements: auto-incremented (?), positional ($1), and named ($param). Note that not all clients support all of these syntaxes, e.g., the JDBC client only…
- **Sections:** Syntax; Example Dataset; Auto-Incremented Parameters: ?; Positional Parameters: $1; Named Parameters: $parameter; Dropping Prepared Statements: DEALLOCATE

### QUALIFY Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/qualify
- **Summary:** The QUALIFY clause is used to filter the results of WINDOW functions. This filtering of results is similar to how a HAVING clause filters the results of aggregate functions applied based on the GROUP BY clause. The QUALIFY clause avoids the need for a subquery or WITH clause to perform this filtering (much like HAVING avoids a subquery). An example using a WITH clause instead of QUALIFY is…
- **Sections:** Examples; Syntax

### SAMPLE Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/sample
- **Summary:** The SAMPLE clause allows you to run the query on a sample from the base table. This can significantly speed up processing of queries, at the expense of accuracy in the result. Samples can also be used to quickly see a snapshot of the data when exploring a dataset. The sample clause is applied right after anything in the FROM clause (i.e., after any joins, but before the WHERE clause or any…
- **Sections:** Examples; Syntax

### SELECT Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/select
- **Summary:** The SELECT clause specifies the list of columns that will be returned by the query. While it appears first in the clause, logically the expressions here are executed only at the end. The SELECT clause can contain arbitrary expressions that transform the output, as well as aggregates and window functions. Examples Select all columns from the table called tbl: SELECT * FROM tbl; Perform…
- **Sections:** Examples; Syntax; SELECT List; Star Expressions; DISTINCT Clause; DISTINCT ON Clause

### Set Operations

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/setops
- **Summary:** Set operations allow queries to be combined according to set operation semantics. Set operations refer to the UNION [ALL], INTERSECT [ALL] and EXCEPT [ALL] clauses. The vanilla variants use set semantics, i.e., they eliminate duplicates, while the variants with ALL use bag semantics. Traditional set operations unify queries by column position, and require the to-be-combined queries to have the…
- **Sections:** UNION; Vanilla UNION (Set Semantics); UNION ALL (Bag Semantics); UNION [ALL] BY NAME; INTERSECT; Vanilla INTERSECT (Set Semantics)

### Unnesting

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/unnest
- **Summary:** Examples Unnest a list, generating 3 rows (1, 2, 3): SELECT unnest([1, 2, 3]); Unnesting a struct, generating two columns (a, b): SELECT unnest({'a': 42, 'b': 84}); Recursive unnest of a list of structs: SELECT unnest([{'a': 42, 'b': 84}, {'a': 100, 'b': NULL}], recursive := true); Limit depth of recursive unnest using max_depth: SELECT unnest([[[1, 2], [3, 4]], [[5, 6], [7, 8, 9], []], [[10,…
- **Sections:** Examples; Unnesting Lists; Unnesting Structs; Recursive Unnest; Setting the Maximum Depth of Unnesting; Keeping Track of List Entry Positions

### VALUES Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/values
- **Summary:** The VALUES clause is used to specify a fixed number of rows. The VALUES clause can be used as a stand-alone statement, as part of the FROM clause, or as input to an INSERT INTO statement. Examples Generate two rows and directly return them: VALUES ('Amsterdam', 1), ('London', 2); Generate two rows as part of a FROM clause, and rename the columns: SELECT * FROM (VALUES ('Amsterdam', 1),…
- **Sections:** Examples; Syntax

### WHERE Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/where
- **Summary:** The WHERE clause specifies any filters to apply to the data. This allows you to select only a subset of the data in which you are interested. Logically the WHERE clause is applied immediately after the FROM clause. Examples Select all rows where the id is equal to 3: SELECT * FROM tbl WHERE id = 3; Select all rows that match the given case-sensitive LIKE expression: SELECT * FROM tbl WHERE…
- **Sections:** Examples; Syntax

### WINDOW Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/window
- **Summary:** The WINDOW clause allows you to specify named windows that can be used within window functions. These are useful when you have multiple window functions, as they allow you to avoid repeating the same window clause. Syntax
- **Sections:** Syntax

### WITH Clause

- **URL:** https://duckdb.org/docs/current/sql/query_syntax/with
- **Summary:** The WITH clause allows you to specify common table expressions (CTEs). Regular (non-recursive) common-table-expressions are essentially views that are limited in scope to a particular query. CTEs can reference each other and can be nested. Recursive CTEs can reference themselves. Basic CTE Examples Create a CTE called cte and use it in the main query: WITH cte AS (SELECT 42 AS x) SELECT * FROM…
- **Sections:** Basic CTE Examples; CTE Materialization; Recursive CTEs; Example: Fibonacci Sequence; Example: Tree Traversal; Graph Traversal

### Samples

- **URL:** https://duckdb.org/docs/current/sql/samples
- **Summary:** Samples are used to randomly select a subset of a dataset. Examples Select a sample of exactly 5 rows from tbl using reservoir sampling: SELECT * FROM tbl USING SAMPLE 5; Select a sample of approximately 10% of the table using system sampling: SELECT * FROM tbl USING SAMPLE 10%; Warning By default, when you specify a percentage, each vector is included in the sample with that probability. If…
- **Sections:** Examples; Syntax; Sampling Methods; reservoir; bernoulli; system

### ALTER TABLE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/alter_table
- **Summary:** The ALTER TABLE statement changes the schema of an existing table in the catalog. Examples CREATE TABLE integers (i INTEGER, j INTEGER); Add a new column with name k to the table integers, it will be filled with the default value NULL: ALTER TABLE integers ADD COLUMN k INTEGER; Add a new column with name l to the table integers, it will be filled with the default value 10: ALTER TABLE integers…
- **Sections:** Examples; Syntax; RENAME TABLE; RENAME COLUMN; ADD COLUMN; DROP COLUMN

### ALTER VIEW Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/alter_view
- **Summary:** The ALTER VIEW statement changes the schema of an existing view in the catalog. Examples Rename a view: ALTER VIEW view1 RENAME TO view2; ALTER VIEW changes the schema of an existing view. All the changes made by ALTER VIEW fully respect the transactional semantics, i.e., they will not be visible to other transactions until committed, and can be fully reverted through a rollback. Note that…
- **Sections:** Examples

### ANALYZE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/analyze
- **Summary:** The ANALYZE statement recomputes the statistics on DuckDB's tables. Usage The statistics recomputed by the ANALYZE statement are only used for join order optimization. It is therefore recommended to recompute these statistics for improved join orders, especially after performing large updates (inserts and/or deletes). To recompute the statistics, run: ANALYZE;
- **Sections:** Usage

### ATTACH and DETACH Statements

- **URL:** https://duckdb.org/docs/current/sql/statements/attach
- **Summary:** DuckDB allows attaching to and detaching from database files. Examples Attach the database file.db with the alias inferred from the name (file): ATTACH 'file.db'; Attach the database file.db with an explicit alias (file_db): ATTACH 'file.db' AS file_db; Attach the database file.db in read only mode: ATTACH 'file.db' (READ_ONLY); Attach the database file.db with a block size of 16 kB: ATTACH…
- **Sections:** Examples; ATTACH; ATTACH Syntax; Explicit Storage Versions; Database Encryption; Options

### CALL Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/call
- **Summary:** The CALL statement invokes the given table function and returns the results. Thanks to the FROM-first syntax and the fact that procedures in DuckDB are implemented as table functions, you can use FROM instead of CALL. Examples Invoke the 'duckdb_functions' table function: CALL duckdb_functions(); Invoke the 'pragma_table_info' table function: CALL pragma_table_info('pg_am'); Select only the…
- **Sections:** Examples; Syntax

### CHECKPOINT Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/checkpoint
- **Summary:** The CHECKPOINT statement synchronizes data in the write-ahead log (WAL) to the database data file. Examples Synchronize data in the default database: CHECKPOINT; Synchronize data in the specified database: CHECKPOINT file_db; Synchronize data and prevent new transactions from starting: FORCE CHECKPOINT; In earlier DuckDB versions, FORCE CHECKPOINT aborted any in-progress transactions. From…
- **Sections:** Examples; Checkpointing In-Memory Tables; Syntax; Behavior; Reclaiming Space

### COMMENT ON Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/comment_on
- **Summary:** The COMMENT ON statement allows adding metadata to catalog entries (tables, columns, etc.). It follows the PostgreSQL syntax. Examples Create a comment on a TABLE: COMMENT ON TABLE test_table IS 'very nice table'; Create a comment on a COLUMN: COMMENT ON COLUMN test_table.test_table_column IS 'very nice column'; Create a comment on a VIEW: COMMENT ON VIEW test_view IS 'very nice view'; Create…
- **Sections:** Examples; Reading Comments; Limitations; Syntax

### COPY Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/copy
- **Summary:** Examples Read a CSV file into the lineitem table, using auto-detected CSV options: COPY lineitem FROM 'lineitem.csv'; Read a CSV file into the lineitem table, using manually specified CSV options: COPY lineitem FROM 'lineitem.csv' (DELIMITER '|'); Read a Parquet file into the lineitem table: COPY lineitem FROM 'lineitem.pq' (FORMAT parquet); Read a JSON file into the lineitem table, using…
- **Sections:** Examples; Overview; COPY ... FROM; Syntax; COPY ... TO; COPY ... TO Options

### CREATE INDEX Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_index
- **Summary:** CREATE INDEX The CREATE INDEX statement constructs an index on the specified column(s) of the specified table. Examples Create a unique index films_id_idx on the column id of table films: CREATE UNIQUE INDEX films_id_idx ON films (id); Create index s_idx that allows for duplicate values on column revenue of table films: CREATE INDEX s_idx ON films (revenue); Create index if it does not yet…
- **Sections:** CREATE INDEX; Examples; Parameters; Syntax; DROP INDEX; Limitations

### CREATE MACRO Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_macro
- **Summary:** The CREATE MACRO statement can create a scalar or table macro (function) in the catalog. For a scalar macro, CREATE MACRO is followed by the name of the macro, and optionally parameters within a set of parentheses. The keyword AS is next, followed by the text of the macro. By design, a scalar macro may only return a single value. For a table macro, the syntax is similar to a scalar macro…
- **Sections:** Examples; Scalar Macros; Table Macros; Overloading; Syntax; Limitations

### CREATE SCHEMA Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_schema
- **Summary:** The CREATE SCHEMA statement creates a schema in the catalog. The default schema is main. Examples Create a schema: CREATE SCHEMA s1; Create a schema if it does not exist yet: CREATE SCHEMA IF NOT EXISTS s2; Create a schema or replace a schema if it exists: CREATE OR REPLACE SCHEMA s2; Create table in the schemas: CREATE TABLE s1.t (id INTEGER PRIMARY KEY, other_id INTEGER); CREATE TABLE s2.t…
- **Sections:** Examples; Syntax

### CREATE SECRET Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_secret
- **Summary:** The CREATE SECRET statement creates a new secret in the Secrets Manager. Syntax for CREATE SECRET Warning When using the command line client, the CREATE SECRET statements are stored in your DuckDB history as plain text. Syntax for DROP SECRET Warning When using the command line client , the CREATE SECRET statements are stored in your DuckDB history as plain text.
- **Sections:** Syntax for CREATE SECRET; Syntax for DROP SECRET

### CREATE SEQUENCE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_sequence
- **Summary:** The CREATE SEQUENCE statement creates a new sequence number generator. Examples Generate an ascending sequence starting from 1: CREATE SEQUENCE serial; Generate sequence from a given start number: CREATE SEQUENCE serial START 101; Generate odd numbers using INCREMENT BY: CREATE SEQUENCE serial START WITH 1 INCREMENT BY 2; Generate a descending sequence starting from 99: CREATE SEQUENCE serial…
- **Sections:** Examples; Creating and Dropping Sequences; Using Sequences for Primary Keys; Selecting the Next Value; Selecting the Current Value; Syntax

### CREATE TABLE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_table
- **Summary:** The CREATE TABLE statement creates a table in the catalog. Examples Create a table with two integer columns (i and j): CREATE TABLE t1 (i INTEGER, j INTEGER); Create a table with a primary key: CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR); Create a table with a composite primary key: CREATE TABLE t1 (id INTEGER, j VARCHAR, PRIMARY KEY (id, j)); Create a table with various different…
- **Sections:** Examples; Temporary Tables; CREATE OR REPLACE; IF NOT EXISTS; CREATE TABLE ... AS SELECT (CTAS); Copying the Schema

### CREATE TYPE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_type
- **Summary:** The CREATE TYPE statement defines a new type in the catalog. Examples Create a simple ENUM type: CREATE TYPE mood AS ENUM ('happy', 'sad', 'curious'); Create a simple STRUCT type: CREATE TYPE many_things AS STRUCT(k INTEGER, l VARCHAR); Create a simple UNION type: CREATE TYPE one_thing AS UNION(number INTEGER, string VARCHAR); Create a type alias: CREATE TYPE x_index AS INTEGER; Syntax The…
- **Sections:** Examples; Syntax; Limitations

### CREATE VIEW Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/create_view
- **Summary:** The CREATE VIEW statement defines a new view in the catalog. Examples Create a simple view: CREATE VIEW view1 AS SELECT * FROM tbl; Create a view or replace it if a view with that name already exists: CREATE OR REPLACE VIEW view1 AS SELECT 42; Create a view and replace the column names: CREATE VIEW view1(a) AS SELECT 42; The SQL query behind an existing view can be read using the…
- **Sections:** Examples; Syntax

### DELETE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/delete
- **Summary:** The DELETE statement removes rows from the table identified by the table-name. If the WHERE clause is not present, all records in the table are deleted. If a WHERE clause is supplied, then only those rows for which the WHERE clause results in true are deleted. Rows for which the expression is false or NULL are retained. Examples Remove the rows matching the condition i = 2 from the database:…
- **Sections:** Examples; USING Clause; RETURNING Clause; Syntax; The TRUNCATE Statement; Limitations on Reclaiming Memory and Disk Space

### DESCRIBE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/describe
- **Summary:** The DESCRIBE statement shows the schema of a table, view or query. Usage DESCRIBE tbl; To describe a query, prepend DESCRIBE to a query. DESCRIBE SELECT * FROM tbl; Alias The SHOW statement is an alias for DESCRIBE. See Also For more examples, see the guide on DESCRIBE. DESCRIBE tbl ; To describe a query, prepend DESCRIBE to a query.
- **Sections:** Usage; Alias; See Also

### DROP Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/drop
- **Summary:** The DROP statement removes a catalog entry added previously with the CREATE command. Examples Delete the table with the name tbl: DROP TABLE tbl; Drop the view with the name view1; do not throw an error if the view does not exist: DROP VIEW IF EXISTS view1; Drop function fn: DROP FUNCTION fn; Drop index idx: DROP INDEX idx; Drop schema sch: DROP SCHEMA sch; Drop sequence seq: DROP SEQUENCE…
- **Sections:** Examples; Syntax; Dependencies of Dropped Objects; Limitations; Dependencies on Views; Limitations on Reclaiming Disk Space

### EXPORT and IMPORT DATABASE Statements

- **URL:** https://duckdb.org/docs/current/sql/statements/export
- **Summary:** The EXPORT DATABASE command allows you to export the contents of the database to a specific directory. The IMPORT DATABASE command allows you to then read the contents again. Examples Export the database to the target directory 'target_directory' as CSV files: EXPORT DATABASE 'target_directory'; Export to directory 'target_directory', using the given options for the CSV serialization: EXPORT…
- **Sections:** Examples; EXPORT DATABASE; Syntax; IMPORT DATABASE

### INSERT Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/insert
- **Summary:** The INSERT statement inserts new data into a table. Examples Insert the values 1, 2, 3 into tbl: INSERT INTO tbl VALUES (1), (2), (3); Insert the result of a query into a table: INSERT INTO tbl SELECT * FROM other_tbl; Insert values into the i column, inserting the default value into other columns: INSERT INTO tbl (i) VALUES (1), (2), (3); Explicitly insert the default value into a column:…
- **Sections:** Examples; Syntax; Insert Column Order; INSERT INTO ... [BY POSITION]; INSERT INTO ... BY NAME; ON CONFLICT Clause

### LOAD / INSTALL Statements

- **URL:** https://duckdb.org/docs/current/sql/statements/load_and_install
- **Summary:** INSTALL The INSTALL statement downloads an extension so it can be loaded into a DuckDB session. Examples Install the httpfs extension: INSTALL httpfs; Install the h3 community extension: INSTALL h3 FROM community; Syntax LOAD The LOAD statement loads an installed DuckDB extension into the current session. Examples Load the httpfs extension: LOAD httpfs; Load the spatial extension: LOAD…
- **Sections:** INSTALL; Examples; Syntax; LOAD

### MERGE INTO Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/merge_into
- **Summary:** The MERGE INTO statement is an alternative to INSERT INTO ... ON CONFLICT that doesn't need a primary key since it allows for a custom match condition. This is a very useful alternative for upserting use cases (INSERT + UPDATE) when the destination table does not have a primary key constraint. Examples First, let's create a simple table. CREATE TABLE people (id INTEGER, name VARCHAR, salary…
- **Sections:** Examples; Syntax

### Statements Overview

- **URL:** https://duckdb.org/docs/current/sql/statements/overview
- **Summary:** DuckDB is an in-process SQL database management system focused on analytical query processing. It is designed to be easy to install and easy to use. DuckDB has no external dependencies. DuckDB has bindings for C/C++, Python, R, Java, Node.js, Go and other languages.
- **Sections:** Pages in This Section

### PIVOT Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/pivot
- **Summary:** The PIVOT statement allows distinct values within a column to be separated into their own columns. The values within those new columns are calculated using an aggregate function on the subset of rows that match each distinct value. DuckDB implements both the SQL Standard PIVOT syntax and a simplified PIVOT syntax that automatically detects the columns to create while pivoting. PIVOT_WIDER may…
- **Sections:** Simplified PIVOT Syntax; Example Data; PIVOT ON and USING; PIVOT ON , USING , and GROUP BY; IN Filter for ON Clause; Multiple Expressions per Clause

### Profiling Queries

- **URL:** https://duckdb.org/docs/current/sql/statements/profiling
- **Summary:** DuckDB supports profiling queries via the EXPLAIN and EXPLAIN ANALYZE statements. EXPLAIN To see the query plan of a query without executing it, run: EXPLAIN query; The output of EXPLAIN contains the estimated cardinalities for each operator. EXPLAIN ANALYZE To profile a query, run: EXPLAIN ANALYZE query; The EXPLAIN ANALYZE statement runs the query, and shows the actual cardinalities for each…
- **Sections:** EXPLAIN; EXPLAIN ANALYZE

### SELECT Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/select
- **Summary:** The SELECT statement retrieves rows from the database. Examples Select all columns from the table tbl: SELECT * FROM tbl; Select the rows from tbl: SELECT j FROM tbl WHERE i = 3; Perform an aggregate grouped by the column i: SELECT i, sum(j) FROM tbl GROUP BY i; Select only the top 3 rows from the tbl: SELECT * FROM tbl ORDER BY i DESC LIMIT 3; Join two tables together using the USING clause:…
- **Sections:** Examples; Syntax; SELECT Clause; FROM Clause; SAMPLE Clause; WHERE Clause

### SET and RESET Statements

- **URL:** https://duckdb.org/docs/current/sql/statements/set
- **Summary:** The SET statement modifies the provided DuckDB configuration option at the specified scope. Examples Update the memory_limit configuration value: SET memory_limit = '10GB'; Configure the system to use 1 thread: SET threads = 1; Or use the TO keyword: SET threads TO 1; Change configuration option to default value: RESET threads; Retrieve configuration value: SELECT current_setting('threads');…
- **Sections:** Examples; Set a Global Variable; Syntax; RESET; Scopes; Configuration

### SET VARIABLE and RESET VARIABLE Statements

- **URL:** https://duckdb.org/docs/current/sql/statements/set_variable
- **Summary:** DuckDB supports the definition of SQL-level variables using the SET VARIABLE and RESET VARIABLE statements. Variable Scopes DuckDB supports two levels of variable scopes: Scope Description SESSION Variables with a SESSION scope are local to you and only affect the current session. GLOBAL Variables with a GLOBAL scope are specific configuration option variables that affect the entire DuckDB…
- **Sections:** Variable Scopes; SET VARIABLE; Syntax; RESET VARIABLE

### SHOW, SHOW DATABASES, and SHOW SCHEMAS Statements

- **URL:** https://duckdb.org/docs/current/sql/statements/show
- **Summary:** SHOW Statement The SHOW statement is an alias for DESCRIBE. It shows the schema of a table, view or query. SHOW DATABASES Statement The SHOW DATABASES statement shows a list of all attached databases: ATTACH 'my.duckdb' AS my_database; SHOW DATABASES; database_name memory my_database DETACH my_database; SHOW DATABASES; database_name memory SHOW SCHEMAS Statement This statement was introduced…
- **Sections:** SHOW Statement; SHOW DATABASES Statement; SHOW SCHEMAS Statement

### SUMMARIZE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/summarize
- **Summary:** The SUMMARIZE statement returns summary statistics for a table, view or a query. Usage SUMMARIZE tbl; To summarize a query, prepend SUMMARIZE to a query. SUMMARIZE SELECT * FROM tbl; See Also For more examples, see the guide on SUMMARIZE. SUMMARIZE tbl ; To summarize a query, prepend SUMMARIZE to a query.
- **Sections:** Usage; See Also

### Transaction Management

- **URL:** https://duckdb.org/docs/current/sql/statements/transactions
- **Summary:** DuckDB supports ACID database transactions. Transactions provide isolation, i.e., changes made by a transaction are not visible from concurrent transactions until it is committed. A transaction can also be aborted, which discards any changes it made so far. Statements DuckDB provides the following statements for transaction management. Starting a Transaction To start a transaction, run: BEGIN…
- **Sections:** Statements; Starting a Transaction; Committing a Transaction; Rolling Back a Transaction; Multi-Statement Transactions; Isolation Level

### UNPIVOT Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/unpivot
- **Summary:** The UNPIVOT statement allows multiple columns to be stacked into fewer columns. In the basic case, multiple columns are stacked into two columns: a NAME column (which contains the name of the source column) and a VALUE column (which contains the value from the source column). DuckDB implements both the SQL Standard UNPIVOT syntax and a simplified UNPIVOT syntax. Both can utilize a COLUMNS…
- **Sections:** Simplified UNPIVOT Syntax; Example Data; UNPIVOT Manually; UNPIVOT Dynamically Using COLUMNS Expression; UNPIVOT into Multiple Value Columns; Using UNPIVOT within a SELECT Statement

### UPDATE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/update
- **Summary:** The UPDATE statement modifies the values of rows in a table. Examples For every row where i is NULL, set the value to 0 instead: UPDATE tbl SET i = 0 WHERE i IS NULL; Set all values of i to 1 and all values of j to 2: UPDATE tbl SET i = 1, j = 2; Syntax UPDATE changes the values of the specified columns in all rows that satisfy the condition. Only the columns to be modified need be mentioned…
- **Sections:** Examples; Syntax; Update from Other Table; Update from Same Table; Update Using Joins; Upsert (Insert or Update)

### UPDATE EXTENSIONS

- **URL:** https://duckdb.org/docs/current/sql/statements/update_extensions
- **Summary:** The UPDATE EXTENSIONS statement allows synchronizing the locally installed extension state with the repository that published a given extension. This statement is the recommended way to keep up to date with new features or bug fixes being rolled out by extension developers. Note that DuckDB extensions cannot be reloaded during runtime, therefore UPDATE EXTENSIONS does not reload the updated…
- **Sections:** Updating All Extensions; Updating Selected Extensions; How It Works

### USE Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/use
- **Summary:** The USE statement selects a database and optional schema, or just a schema to use as the default. Examples --- Sets the 'memory' database as the default. Will use 'main' schema implicitly or error --- if it does not exist. USE memory; --- Sets the 'duck.main' database and schema as the default USE duck.main; -- Sets the `main` schema of the currently selected database as the default, in this…
- **Sections:** Examples; Syntax

### VACUUM Statement

- **URL:** https://duckdb.org/docs/current/sql/statements/vacuum
- **Summary:** The VACUUM statement only has basic support in DuckDB and is mostly provided for PostgreSQL-compatibility. Some variants of it, such as when calling for a given column, recompute the distinct statistics (the number of distinct entities) if they have become stale due to updates. Warning The behavior of VACUUM is not consistent with PostgreSQL semantics and it is likely going to change in the…
- **Sections:** Examples; Vacuum with Indexes; Reclaiming Space; Syntax

## Data import / export (26)

### Appender

- **URL:** https://duckdb.org/docs/current/data/appender
- **Summary:** The Appender can be used to load bulk data into a DuckDB database. It is currently available in the C, C++, Go, Java and Rust APIs. The Appender is tied to a connection, and will use the transaction context of that connection when appending. An Appender always appends to a single table in the database file. In the C++ API, the Appender works as follows: DuckDB db; Connection con(db); // create…
- **Sections:** Date, Time and Timestamps; Commit Frequency; Handling Constraint Violations; Appender Support in Other Clients

### CSV Auto Detection

- **URL:** https://duckdb.org/docs/current/data/csv/auto_detection
- **Summary:** When using read_csv, the system tries to automatically infer how to read the CSV file using the CSV sniffer. This step is necessary because CSV files are not self-describing and come in many different dialects. The auto-detection works roughly as follows: Detect the dialect of the CSV file (delimiter, quoting rule, escape). Detect the types of each of the columns. Detect whether or not the…
- **Sections:** Sample Size; sniff_csv Function; Prompt; Detection Steps; Dialect Detection; Type Detection

### CSV Import

- **URL:** https://duckdb.org/docs/current/data/csv/overview
- **Summary:** Examples The following examples use the flights.csv file. Read a CSV file from disk, auto-infer options: SELECT * FROM 'flights.csv'; Use the read_csv function with custom options: SELECT * FROM read_csv('flights.csv', delim = '|', header = true, columns = { 'FlightDate': 'DATE', 'UniqueCarrier': 'VARCHAR', 'OriginCityName': 'VARCHAR', 'DestCityName': 'VARCHAR' }); Read a CSV from stdin,…
- **Sections:** Examples; CSV Loading; Parameters; auto_type_candidates Details; CSV Functions; Writing Using the COPY Statement

### Reading Faulty CSV Files

- **URL:** https://duckdb.org/docs/current/data/csv/reading_faulty_csv_files
- **Summary:** CSV files can come in all shapes and forms, with some presenting many errors that make the process of cleanly reading them inherently difficult. To help users read these files, DuckDB supports detailed error messages, the ability to skip faulty lines and the possibility of storing faulty lines in a temporary table to assist users with a data cleaning step. Structural Errors DuckDB supports the…
- **Sections:** Structural Errors; Anatomy of a CSV Error; Using the ignore_errors Option; Retrieving Faulty CSV Lines; Reject Scans; Reject Errors

### CSV Import Tips

- **URL:** https://duckdb.org/docs/current/data/csv/tips
- **Summary:** Below is a collection of tips to help when attempting to import complex CSV files. In the examples, we use the flights.csv file. Override the Header Flag if the Header Is Not Correctly Detected If a file contains only string columns the header auto-detection might fail. Provide the header option to override this behavior. SELECT * FROM read_csv('flights.csv', header = true); Provide Names if…
- **Sections:** Override the Header Flag if the Header Is Not Correctly Detected; Provide Names if the File Does Not Contain a Header; Override the Types of Specific Columns; Use COPY When Loading Data into a Table; Use union_by_name When Loading Files with Different Schemas; Sample Size

### Data Sources

- **URL:** https://duckdb.org/docs/current/data/data_sources
- **Summary:** DuckDB supports several data sources, including file formats, network protocols, and database systems: AWS S3 buckets and storage with S3-compatible API Azure Blob Storage Blob files Cloudflare R2 CSV Delta Lake DuckLake Excel httpfs Iceberg JSON Lance tables MySQL Parquet PostgreSQL SQLite Text files Vortex files

### INSERT Statements

- **URL:** https://duckdb.org/docs/current/data/insert
- **Summary:** INSERT statements are the standard way of loading data into a relational database. When using INSERT statements, the values are supplied row-by-row. While simple, there is significant overhead involved in parsing and processing individual INSERT statements. This makes lots of individual row-by-row insertions very inefficient for bulk insertion. Bestpractice As a rule-of-thumb, avoid using lots…
- **Sections:** Syntax

### Caveats

- **URL:** https://duckdb.org/docs/current/data/json/caveats
- **Summary:** Equality Comparison Warning Currently, equality comparison of JSON files can differ based on the context. In some cases, it is based on raw text comparison, while in other cases, it uses logical content comparison. The following query returns true for all fields: SELECT a != b, -- Space is part of physical JSON content. Despite equal logical content, values are treated as not equal. c != d, --…
- **Sections:** Equality Comparison

### Creating JSON

- **URL:** https://duckdb.org/docs/current/data/json/creating_json
- **Summary:** JSON Creation Functions The following functions are used to create JSON. Function Description to_json(any) Create JSON from a value of any type. Our LIST is converted to a JSON array, and our STRUCT and MAP are converted to a JSON object. json_quote(any) Alias for to_json. array_to_json(list) Alias for to_json that only accepts LIST. row_to_json(list) Alias for to_json that only accepts…
- **Sections:** JSON Creation Functions

### JSON Format Settings

- **URL:** https://duckdb.org/docs/current/data/json/format_settings
- **Summary:** The JSON extension can attempt to determine the format of a JSON file when setting format to auto. Here are some example JSON files and the corresponding format settings that should be used. In each of the below cases, the format setting was not needed, as DuckDB was able to infer it correctly, but it is included for illustrative purposes. A query of this shape would work in each case: SELECT…
- **Sections:** Format: newline_delimited; Format: array; Format: unstructured; records Options

### Installing and Loading the JSON Extension

- **URL:** https://duckdb.org/docs/current/data/json/installing_and_loading
- **Summary:** The json extension is shipped by default in DuckDB builds, otherwise, it will be transparently autoloaded on first use. If you would like to install and load it manually, run: INSTALL json; LOAD json;

### JSON Processing Functions

- **URL:** https://duckdb.org/docs/current/data/json/json_functions
- **Summary:** JSON Extraction Functions There are two extraction functions, which have their respective operators. The operators can only be used if the string is stored as the JSON logical type. These functions support the same two location notations as JSON Scalar functions. Function Alias Operator Description json_exists(json, path) Returns true if the supplied path exists in the json, and false…
- **Sections:** JSON Extraction Functions; JSON Scalar Functions; JSON Aggregate Functions; Transforming JSON to Nested Types; JSON Table Functions

### JSON Type

- **URL:** https://duckdb.org/docs/current/data/json/json_type
- **Summary:** DuckDB supports json via the JSON logical type. For example: SELECT '[1, null, {"key": "value"}]'::JSON; [1, null, {"key": "value"}] Logically, the JSON type is similar to a VARCHAR, but with the restriction that it must be valid JSON. Physically, the data is stored as a VARCHAR. For example, you can't parse invalid JSON: SELECT 'unquoted'::JSON; Conversion Error: Malformed JSON at byte 0 of…

### Loading JSON

- **URL:** https://duckdb.org/docs/current/data/json/loading_json
- **Summary:** The DuckDB JSON reader can automatically infer which configuration flags to use by analyzing the JSON file. This will work correctly in most situations, and should be the first option attempted. In rare situations where the JSON reader cannot figure out the correct configuration, it is possible to manually configure the JSON reader to correctly parse the JSON file. The read_json Function The…
- **Sections:** The read_json Function; Functions for Reading JSON Objects; Parameters; Functions for Reading JSON as a Table; Loading with the COPY Statement Using FORMAT json

### JSON Overview

- **URL:** https://duckdb.org/docs/current/data/json/overview
- **Summary:** DuckDB supports SQL functions that are useful for reading values from existing JSON and creating new JSON data. JSON is supported with the json extension which is shipped with most DuckDB distributions and is auto-loaded on first use. If you would like to install or load it manually, please consult the “Installing and Loading” page. About JSON JSON is an open standard file format and data…
- **Sections:** About JSON; JSONPath and JSON Pointer Syntax; Indexing; Examples; Loading JSON; Writing JSON

### SQL to/from JSON

- **URL:** https://duckdb.org/docs/current/data/json/sql_to_and_from_json
- **Summary:** DuckDB provides functions to serialize and deserialize SELECT statements between SQL and JSON, as well as executing JSON serialized statements. Function Type Description json_deserialize_sql(json) Scalar Deserialize one or many json serialized statements back to an equivalent SQL string. json_execute_serialized_sql(varchar) Table Execute json serialized statements and return the resulting…
- **Sections:** Examples

### Writing JSON

- **URL:** https://duckdb.org/docs/current/data/json/writing_json
- **Summary:** The contents of tables or the result of queries can be written directly to a JSON file using the COPY statement. For example: CREATE TABLE cities AS FROM (VALUES ('Amsterdam', 1), ('London', 2)) cities(name, id); COPY cities TO 'cities.json'; This will result in cities.json with the following content: {"name":"Amsterdam","id":1} {"name":"London","id":2} See the COPY statement for more…

### Combining Schemas

- **URL:** https://duckdb.org/docs/current/data/multiple_files/combining_schemas
- **Summary:** Examples Read a set of CSV files combining columns by position: SELECT * FROM read_csv('flights*.csv'); Read a set of CSV files combining columns by name: SELECT * FROM read_csv('flights*.csv', union_by_name = true); Combining Schemas When reading from multiple files, we have to combine schemas from those files. That is because each file has its own schema that can differ from the other files.…
- **Sections:** Examples; Combining Schemas; Union by Position; Union by Name

### Reading Multiple Files

- **URL:** https://duckdb.org/docs/current/data/multiple_files/overview
- **Summary:** DuckDB can read multiple files of different types (CSV, Parquet, JSON files) at the same time using either the glob syntax, or by providing a list of files to read. See the combining schemas page for tips on reading files with different schemas. CSV Read all files with a name ending in .csv in the folder dir: SELECT * FROM 'dir/*.csv'; Read all files with a name ending in .csv, two directories…
- **Sections:** CSV; Parquet; Multi-File Reads and Globs; List Parameter; Glob Syntax; List of Globs

### Importing Data

- **URL:** https://duckdb.org/docs/current/data/overview
- **Summary:** The first step to using a database system is to insert data into that system. DuckDB can directly connect to many popular data sources and offers several data ingestion methods that allow you to easily and efficiently fill up the database.
- **Sections:** INSERT Statements; File Loading: Relative Paths; File Formats; CSV Loading; Parquet Loading; JSON Loading

### Parquet Encryption

- **URL:** https://duckdb.org/docs/current/data/parquet/encryption
- **Summary:** Starting with version 0.10.0, DuckDB supports reading and writing encrypted Parquet files. DuckDB broadly follows the Parquet Modular Encryption specification with some limitations. Reading and Writing Encrypted Files Using the PRAGMA add_parquet_key function, named encryption keys of 128, 192, or 256 bits can be added to a session. These keys are stored in-memory: PRAGMA…
- **Sections:** Reading and Writing Encrypted Files; Writing Encrypted Parquet Files; Reading Encrypted Parquet Files; Interoperability; Limitations; Performance Implications

### Querying Parquet Metadata

- **URL:** https://duckdb.org/docs/current/data/parquet/metadata
- **Summary:** Parquet Metadata The parquet_metadata function can be used to query the metadata contained within a Parquet file, which reveals various internal details of the Parquet file such as the statistics of the different columns. This can be useful for figuring out what kind of skipping is possible in Parquet files, or even to obtain a quick overview of what the different columns contain. The function…
- **Sections:** Parquet Metadata; Parquet Schema; Parquet File Metadata; Parquet Key-Value Metadata; Full Metadata; Bloom Filters

### Reading and Writing Parquet Files

- **URL:** https://duckdb.org/docs/current/data/parquet/overview
- **Summary:** Examples Read a single Parquet file: SELECT * FROM 'test.parquet'; Figure out which columns/types are in a Parquet file: DESCRIBE SELECT * FROM 'test.parquet'; Create a table from a Parquet file: CREATE TABLE test AS SELECT * FROM 'test.parquet'; If the file does not end in .parquet, use the read_parquet function: SELECT * FROM read_parquet('test.parq'); Use list parameter to read three…
- **Sections:** Examples; Parquet Files; read_parquet Function; Parameters; Using the schema Parameter; Partial Reading

### Parquet Tips

- **URL:** https://duckdb.org/docs/current/data/parquet/tips
- **Summary:** Below is a collection of tips to help when dealing with Parquet files. Tips for Reading Parquet Files Use union_by_name When Loading Files with Different Schemas The union_by_name option can be used to unify the schema of files that have different or missing columns. For files that do not have certain columns, NULL values are filled in: SELECT * FROM read_parquet('flights*.parquet',…
- **Sections:** Tips for Reading Parquet Files; Use union_by_name When Loading Files with Different Schemas; Tips for Writing Parquet Files; Enabling PER_THREAD_OUTPUT; Selecting a ROW_GROUP_SIZE; The ROW_GROUPS_PER_FILE Option

### Hive Partitioning

- **URL:** https://duckdb.org/docs/current/data/partitioning/hive_partitioning
- **Summary:** Examples Read data from a Hive partitioned dataset: SELECT * FROM read_parquet('orders/*/*/*.parquet', hive_partitioning = true); Write a table to a Hive partitioned dataset: COPY orders TO 'orders' (FORMAT parquet, PARTITION_BY (year, month)); Note that the PARTITION_BY options cannot use expressions. You can produce columns on the fly using the following syntax: COPY (SELECT *,…
- **Sections:** Examples; Hive Partitioning; Filter Pushdown; Auto-detection; Hive Types; Writing Partitioned Files

### Partitioned Writes

- **URL:** https://duckdb.org/docs/current/data/partitioning/partitioned_writes
- **Summary:** Examples Write a table to a Hive partitioned dataset of Parquet files: COPY orders TO 'orders' (FORMAT parquet, PARTITION_BY (year, month)); Write a table to a Hive partitioned dataset of CSV files, allowing overwrites: COPY orders TO 'orders' (FORMAT csv, PARTITION_BY (year, month), OVERWRITE_OR_IGNORE); Write a table to a Hive partitioned dataset of GZIP-compressed CSV files, setting…
- **Sections:** Examples; Partitioned Writes; Filename Pattern; Overwriting; Appending; Handling Slashes in Columns

## Guides & how-tos (85)

### Tableau – A Data Visualization Tool

- **URL:** https://duckdb.org/docs/current/guides/data_viewers/tableau
- **Summary:** Tableau is a popular commercial data visualization tool. In addition to a large number of built-in connectors, it also provides generic database connectivity via ODBC and JDBC connectors. Tableau has two main versions: Desktop and Online (Server). For Desktop, connecting to a DuckDB database is similar to working in an embedded environment like Python. For Online, since DuckDB is in-process,…
- **Sections:** Database Creation; Installing the JDBC Driver; Driver Links; Using the PostgreSQL Dialect; Installing the Tableau DuckDB Connector; Server (Online)

### CLI Charting with YouPlot

- **URL:** https://duckdb.org/docs/current/guides/data_viewers/youplot
- **Summary:** DuckDB can be used with CLI graphing tools to quickly pipe input to stdout to graph your data in one line. YouPlot is a Ruby-based CLI tool for drawing visually pleasing plots on the terminal. It can accept input from other programs by piping data from stdin. It takes tab-separated (or delimiter of your choice) data and can easily generate various types of plots including bar, line, histogram…
- **Sections:** Installing YouPlot; Piping DuckDB Queries to stdout; Connecting DuckDB to YouPlot; Additional Example: stdin + stdout

### MySQL Import

- **URL:** https://duckdb.org/docs/current/guides/database_integration/mysql
- **Summary:** To run a query directly on a running MySQL database, the mysql extension is required. Installation and Loading The extension can be installed using the INSTALL SQL command. This only needs to be run once. INSTALL mysql; To load the mysql extension for usage, use the LOAD SQL command: LOAD mysql; Usage After the mysql extension is installed, you can attach to a MySQL database using the…
- **Sections:** Installation and Loading; Usage

### Database Integration

- **URL:** https://duckdb.org/docs/current/guides/database_integration/overview
- **Summary:** DuckDB is an in-process SQL database management system focused on analytical query processing. It is designed to be easy to install and easy to use. DuckDB has no external dependencies. DuckDB has bindings for C/C++, Python, R, Java, Node.js, Go and other languages.
- **Sections:** Pages in This Section

### PostgreSQL Import

- **URL:** https://duckdb.org/docs/current/guides/database_integration/postgres
- **Summary:** To run a query directly on a running PostgreSQL database, the postgres extension is required. Installation and Loading The extension can be installed using the INSTALL SQL command. This only needs to be run once. INSTALL postgres; To load the postgres extension for usage, use the LOAD SQL command: LOAD postgres; Usage After the postgres extension is installed, tables can be queried from…
- **Sections:** Installation and Loading; Usage

### SQLite Import

- **URL:** https://duckdb.org/docs/current/guides/database_integration/sqlite
- **Summary:** To run a query directly on a SQLite file, the sqlite extension is required. Installation and Loading The extension can be installed using the INSTALL SQL command. This only needs to be run once. INSTALL sqlite; To load the sqlite extension for usage, use the LOAD SQL command: LOAD sqlite; Usage After the SQLite extension is installed, tables can be queried from SQLite using the sqlite_scan…
- **Sections:** Installation and Loading; Usage

### CSV Export

- **URL:** https://duckdb.org/docs/current/guides/file_formats/csv_export
- **Summary:** To export the data from a table to a CSV file, use the COPY statement: COPY tbl TO 'output.csv' (HEADER, DELIMITER ','); The result of queries can also be directly exported to a CSV file: COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ','); For additional options, see the COPY statement documentation. COPY tbl TO 'output.csv' ( HEADER , DELIMITER ',' ); The result of queries can…

### CSV Import

- **URL:** https://duckdb.org/docs/current/guides/file_formats/csv_import
- **Summary:** To read data from a CSV file, use the read_csv function in the FROM clause of a query: SELECT * FROM read_csv('input.csv'); Alternatively, you can omit the read_csv function and let DuckDB infer it from the extension: SELECT * FROM 'input.csv'; To create a new table using the result from a query, use CREATE TABLE ... AS SELECT statement: CREATE TABLE new_tbl AS SELECT * FROM…

### Excel Export

- **URL:** https://duckdb.org/docs/current/guides/file_formats/excel_export
- **Summary:** DuckDB supports exporting data to Excel .xlsx files via the excel extension. Please note that .xls files are not supported. To install and load the extension, run: INSTALL excel; LOAD excel; Exporting Excel Sheets To export a table to an Excel file, use the COPY statement with the FORMAT xlsx option: COPY tbl TO 'output.xlsx' WITH (FORMAT xlsx); The result of a query can also be directly…
- **Sections:** Exporting Excel Sheets; Type Conversions; See Also

### Excel Import

- **URL:** https://duckdb.org/docs/current/guides/file_formats/excel_import
- **Summary:** DuckDB supports reading Excel .xlsx files. However, .xls files are not supported. Importing Excel Sheets Use the read_xlsx function in the FROM clause of a query: SELECT * FROM read_xlsx('test_excel.xlsx'); Alternatively, you can omit the read_xlsx function and let DuckDB infer it from the extension: SELECT * FROM 'test_excel.xlsx'; However, if you want to be able to pass options to control…
- **Sections:** Importing Excel Sheets; Importing a Specific Range; Creating a New Table; Loading to an Existing Table; Importing a Sheet with/without a Header; Detecting Types

### File Access with the file: Protocol

- **URL:** https://duckdb.org/docs/current/guides/file_formats/file_access
- **Summary:** DuckDB supports using the file: protocol. It currently supports the following formats: file:/some/path (host omitted completely) file:///some/path (empty host) file://localhost/some/path (localhost as host) Note that the following formats are not supported because they are non-standard: file:some/relative/path (relative path) file://some/path (double-slash path) Additionally, the file:…

### JSON Export

- **URL:** https://duckdb.org/docs/current/guides/file_formats/json_export
- **Summary:** To export the data from a table to a JSON file, use the COPY statement: COPY tbl TO 'output.json'; The result of queries can also be directly exported to a JSON file: COPY (SELECT * FROM range(3) tbl(n)) TO 'output.json'; {"n":0} {"n":1} {"n":2} The JSON export writes JSON lines by default, standardized as Newline-delimited JSON. The ARRAY option can be used to write a single JSON array object…

### JSON Import

- **URL:** https://duckdb.org/docs/current/guides/file_formats/json_import
- **Summary:** To read data from a JSON file, use the read_json function in the FROM clause of a query: SELECT * FROM read_json('input.json'); To create a new table using the result from a query, use CREATE TABLE AS from a SELECT statement: CREATE TABLE new_tbl AS SELECT * FROM read_json('input.json'); To load data into an existing table from a query, use INSERT INTO from a SELECT statement: INSERT INTO tbl…

### File Formats

- **URL:** https://duckdb.org/docs/current/guides/file_formats/overview
- **Summary:** DuckDB is an in-process SQL database management system focused on analytical query processing. It is designed to be easy to install and easy to use. DuckDB has no external dependencies. DuckDB has bindings for C/C++, Python, R, Java, Node.js, Go and other languages.
- **Sections:** Pages in This Section

### Parquet Export

- **URL:** https://duckdb.org/docs/current/guides/file_formats/parquet_export
- **Summary:** To export the data from a table to a Parquet file, use the COPY statement: COPY tbl TO 'output.parquet' (FORMAT parquet); The result of queries can also be directly exported to a Parquet file: COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT parquet); The flags for setting compression, row group size, etc. are listed in the Reading and Writing Parquet files page. COPY tbl TO…

### Parquet Import

- **URL:** https://duckdb.org/docs/current/guides/file_formats/parquet_import
- **Summary:** To read data from a Parquet file, use the read_parquet function in the FROM clause of a query: SELECT * FROM read_parquet('input.parquet'); Alternatively, you can omit the read_parquet function and let DuckDB infer it from the extension: SELECT * FROM 'input.parquet'; To create a new table using the result from a query, use the CREATE TABLE ... AS SELECT statement: CREATE TABLE new_tbl AS…
- **Sections:** Adjusting the Schema on the Fly

### Querying Parquet Files

- **URL:** https://duckdb.org/docs/current/guides/file_formats/query_parquet
- **Summary:** To run a query directly on a Parquet file, use the read_parquet function in the FROM clause of a query. SELECT * FROM read_parquet('input.parquet'); The Parquet file will be processed in parallel. Filters will be automatically pushed down into the Parquet scan, and only the relevant columns will be read automatically. For more information see the blog post “Querying Parquet with Precision…

### Directly Read DuckDB Databases

- **URL:** https://duckdb.org/docs/current/guides/file_formats/read_duckdb
- **Summary:** DuckDB allows directly reading DuckDB files through the read_duckdb function: read_duckdb('path_to_database', table_name = 'table_to_read'); Using this function is equivalent to performing the following steps: Attaching to the database using a read-only connection. Querying the table specified through the table_name argument. Closing the connection to the database database. Examples Reading a…
- **Sections:** Examples; Reading a Specific Table; Reading from Multiple Databases; Reading from Databases with a Single Table; Limitations

### Directly Reading Files

- **URL:** https://duckdb.org/docs/current/guides/file_formats/read_file
- **Summary:** DuckDB allows directly reading files via the read_text and read_blob functions. These functions accept a filename, a list of filenames, or a glob pattern. They output the content of each file as a VARCHAR or BLOB, respectively, along with metadata such as the file size and last modified time. read_text The read_text table function reads from the selected source(s) to a VARCHAR. Each file…
- **Sections:** read_text; read_blob; Schema; Hive Partitioning; Handling Missing Metadata; Support for Projection Pushdown

### Glossary of Terms

- **URL:** https://duckdb.org/docs/current/guides/glossary
- **Summary:** This page contains a glossary of a few common terms used in DuckDB. Terms In-Process Database Management System The DBMS runs in the client application's process instead of running as a separate process, which is common in the traditional client–server setup. An alternative term is embeddable database management system. In general, the term “embedded database management system” should be…
- **Sections:** Terms; In-Process Database Management System; Replacement Scan; Extension; Platform

### Describe

- **URL:** https://duckdb.org/docs/current/guides/meta/describe
- **Summary:** Describing a Table To view the schema of a table, use the DESCRIBE statement (or its aliases DESC and SHOW) followed by the table name. CREATE TABLE tbl (i INTEGER PRIMARY KEY, j VARCHAR); DESCRIBE tbl; SHOW tbl; -- equivalent to DESCRIBE tbl; column_name column_type null key default extra i INTEGER NO PRI NULL NULL j VARCHAR YES NULL NULL NULL Describing a Query To view the schema of the…
- **Sections:** Describing a Table; Describing a Query; Using DESCRIBE in a Subquery; Describing Remote Tables

### DuckDB Environment

- **URL:** https://duckdb.org/docs/current/guides/meta/duckdb_environment
- **Summary:** DuckDB provides a number of functions and PRAGMA options to retrieve information on the running DuckDB instance and its environment. Version The version() function returns the version number of DuckDB. SELECT version() AS version; version v Using a PRAGMA: PRAGMA version; library_version source_id v {{ site.current_duckdb_hash…
- **Sections:** Version; Platform; Extensions; Meta Table Functions

### EXPLAIN: Inspect Query Plans

- **URL:** https://duckdb.org/docs/current/guides/meta/explain
- **Summary:** EXPLAIN SELECT * FROM tbl; The EXPLAIN statement displays the physical plan, i.e., the query plan that will get executed, and is enabled by prepending the query with EXPLAIN. The physical plan is a tree of operators that are executed in a specific order to produce the result of the query. To generate an efficient physical plan, the query optimizer transforms the existing physical plan into a…
- **Sections:** Additional Explain Settings; See Also

### EXPLAIN ANALYZE: Profile Queries

- **URL:** https://duckdb.org/docs/current/guides/meta/explain_analyze
- **Summary:** Prepending a query with EXPLAIN ANALYZE both pretty-prints the query plan, and executes it, providing run-time performance numbers for every operator, as well as the estimated cardinality (EC) and the actual cardinality. EXPLAIN ANALYZE SELECT * FROM tbl; Note that the cumulative wall-clock time that is spent on every operator is shown. When multiple threads are processing the query in…
- **Sections:** See Also

### List Tables

- **URL:** https://duckdb.org/docs/current/guides/meta/list_tables
- **Summary:** The SHOW TABLES command can be used to obtain a list of all tables within the selected schema. CREATE TABLE tbl (i INTEGER); SHOW TABLES; name tbl SHOW or SHOW ALL TABLES can be used to obtain a list of all tables within all attached databases and schemas. CREATE TABLE tbl (i INTEGER); CREATE SCHEMA s1; CREATE TABLE s1.tbl (v VARCHAR); SHOW ALL TABLES; database schema table_name column_names…
- **Sections:** See Also

### Summarize

- **URL:** https://duckdb.org/docs/current/guides/meta/summarize
- **Summary:** The SUMMARIZE command can be used to easily compute a number of aggregates over a table or a query. The SUMMARIZE command launches a query that computes a number of aggregates over all columns (min, max, approx_unique, avg, std, q25, q50, q75, count), and return these along the column name, column type, and the percentage of NULL values in the column. Note that the quantiles and percentiles…
- **Sections:** Usage; Example; Using SUMMARIZE in a Subquery; Summarizing Remote Tables

### Cloudflare R2 Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/cloudflare_r2_import
- **Summary:** Prerequisites For Cloudflare R2, the S3 Compatibility API allows you to use DuckDB's S3 support to read and write from R2 buckets. This requires the httpfs extension, which can be installed using the INSTALL SQL command. This only needs to be run once. Credentials and Configuration You will need to generate an S3 auth token and create an R2 secret in DuckDB: CREATE SECRET ( TYPE r2, KEY_ID…
- **Sections:** Prerequisites; Credentials and Configuration; Querying

### Attach to a DuckDB Database over HTTPS or S3

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/duckdb_over_https_or_s3
- **Summary:** You can establish a read-only connection to a DuckDB instance via HTTPS or the S3 API. Prerequisites This guide requires the httpfs extension, which can be installed using the INSTALL httpfs SQL command. This only needs to be run once. Attaching to a Database over HTTPS To connect to a DuckDB database via HTTPS, use the ATTACH statement as follows: ATTACH…
- **Sections:** Prerequisites; Attaching to a Database over HTTPS; Attaching to a Database over the S3 API; Limitations

### Fastly Object Storage Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/fastly_object_storage_import
- **Summary:** Prerequisites For Fastly Object Storage, the S3 Compatibility API allows you to use DuckDB's S3 support to read and write from Fastly buckets. This requires the httpfs extension, which can be installed using the INSTALL SQL command. This only needs to be run once. Credentials and Configuration You will need to generate an S3 auth token and create an S3 secret in DuckDB: CREATE SECRET my_secret…
- **Sections:** Prerequisites; Credentials and Configuration; Querying

### Google Cloud Storage Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/gcs_import
- **Summary:** Prerequisites The Google Cloud Storage (GCS) can be used via the httpfs extension. This can be installed with the INSTALL httpfs SQL command. This only needs to be run once. Credentials and Configuration You need to create HMAC keys and declare them: CREATE SECRET ( TYPE gcs, KEY_ID 'AKIAIOSFODNN7EXAMPLE', SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY' ); Querying After setting up the GCS…
- **Sections:** Prerequisites; Credentials and Configuration; Querying; Attaching to a Database

### HTTP Parquet Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/http_import
- **Summary:** To load a Parquet file over HTTP(S), the httpfs extension is required. This can be installed using the INSTALL SQL command. This only needs to be run once. INSTALL httpfs; To load the httpfs extension for usage, use the LOAD SQL command: LOAD httpfs; After the httpfs extension is set up, Parquet files can be read over http(s): SELECT * FROM read_parquet('https://domain/path/to/file.parquet');…

### Network and Cloud Storage

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/overview
- **Summary:** DuckDB is an in-process SQL database management system focused on analytical query processing. It is designed to be easy to install and easy to use. DuckDB has no external dependencies. DuckDB has bindings for C/C++, Python, R, Java, Node.js, Go and other languages.
- **Sections:** Pages in This Section

### S3 Parquet Export

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/s3_export
- **Summary:** To write a Parquet file to S3, the httpfs extension is required. This can be installed using the INSTALL SQL command. This only needs to be run once. INSTALL httpfs; To load the httpfs extension for usage, use the LOAD SQL command: LOAD httpfs; After loading the httpfs extension, set up the credentials to write data. Note that the region parameter should match the region of the bucket you want…

### S3 Express One

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/s3_express_one
- **Summary:** In late 2023, AWS announced the S3 Express One Zone, a high-speed variant of traditional S3 buckets. DuckDB can read S3 Express One buckets using the httpfs extension. Credentials and Configuration The configuration of S3 Express One buckets is similar to regular S3 buckets with one exception: you must specify the endpoint according to the following pattern:…
- **Sections:** Credentials and Configuration; Instance Location; Querying; Performance

### S3 Iceberg Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/s3_iceberg_import
- **Summary:** Prerequisites Loading an Iceberg file from S3 requires both the httpfs and iceberg extensions. Install them using the INSTALL SQL command. You only need to install extensions once. INSTALL httpfs; INSTALL iceberg; To load the extensions, use the LOAD command: LOAD httpfs; LOAD iceberg; Credentials After loading the extensions, set up the credentials and S3 region to read data. You may either…
- **Sections:** Prerequisites; Credentials; Loading Iceberg Tables from S3

### S3 Parquet Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/s3_import
- **Summary:** Prerequisites To load a Parquet file from S3, the httpfs extension is required. This can be installed using the INSTALL SQL command. This only needs to be run once. INSTALL httpfs; To load the httpfs extension for usage, use the LOAD SQL command: LOAD httpfs; Credentials and Configuration After loading the httpfs extension, set up the credentials and S3 region to read data: CREATE SECRET (…
- **Sections:** Prerequisites; Credentials and Configuration; Querying; Google Cloud Storage (GCS) and Cloudflare R2

### Tigris Import

- **URL:** https://duckdb.org/docs/current/guides/network_cloud_storage/tigris_import
- **Summary:** Prerequisites For Tigris, the S3-compatible API allows you to use DuckDB's S3 support to read and write from Tigris buckets. This requires the httpfs extension, which can be installed using the INSTALL SQL command. This only needs to be run once. Credentials and Configuration You will need to generate an access key pair and create an S3 secret in DuckDB: CREATE SECRET my_secret ( TYPE s3,…
- **Sections:** Prerequisites; Credentials and Configuration; Querying

### ODBC 101: A Duck Themed Guide to ODBC

- **URL:** https://duckdb.org/docs/current/guides/odbc/general
- **Summary:** What is ODBC? ODBC which stands for Open Database Connectivity, is a standard that allows different programs to talk to different databases including, of course, DuckDB. This makes it easier to build programs that work with many different databases, which saves time as developers don't have to write custom code to connect to each database. Instead, they can use the standardized ODBC interface,…
- **Sections:** What is ODBC?; General Concepts; Handles; Connecting; Error Handling and Diagnostics; Buffers and Binding

### Browsing Offline

- **URL:** https://duckdb.org/docs/current/guides/offline-copy
- **Summary:** The offline documentation is currently not available. Please check back later. You can browse the DuckDB documentation offline in the following formats: Single Markdown file (approx. 5 MB) PDF file (approx. 35 MB)

### Guides

- **URL:** https://duckdb.org/docs/current/guides/overview
- **Summary:** The guides section contains compact how-to guides that are focused on achieving a single goal. For API references and examples, see the rest of the documentation. Note that there are many tools using DuckDB, which are not covered in the official guides. To find a list of these tools, check out the Awesome DuckDB repository. Tip For a short introductory tutorial, check out the “Analyzing…
- **Sections:** Data Import and Export; CSV Files; Parquet Files; HTTP(S), S3 and GCP; JSON Files; Excel Files with the Spatial Extension

### Benchmarks

- **URL:** https://duckdb.org/docs/current/guides/performance/benchmarks
- **Summary:** For several of the recommendations in our performance guide, we use microbenchmarks to back up our claims. For these benchmarks, we use datasets from the TPC-H benchmark and the LDBC Social Network Benchmark’s BI workload. Datasets We use the LDBC BI SF300 dataset's Comment table (20 GB .tar.zst archive, 21 GB when decompressed into .csv.gz files), while others use the same table's…
- **Sections:** Datasets; A Note on Benchmarks; Disclaimer on Benchmarks

### Environment

- **URL:** https://duckdb.org/docs/current/guides/performance/environment
- **Summary:** The environment where DuckDB is run has an obvious impact on performance. This page focuses on the effects of the hardware configuration and the operating system used. Hardware Configuration CPU DuckDB's officially supported architectures are AMD64 (x86_64) and ARM64 (AArch64) CPU architectures. DuckDB works efficiently on both of these architectures. DuckDB can be compiled to other…
- **Sections:** Hardware Configuration; CPU; Memory; Local Disk; Network-Attached Disks; Operating System

### File Formats

- **URL:** https://duckdb.org/docs/current/guides/performance/file_formats
- **Summary:** Handling Parquet Files DuckDB has advanced support for Parquet files, which includes directly querying Parquet files. When deciding on whether to query these files directly or to first load them to the database, you need to consider several factors. Reasons for Querying Parquet Files Availability of basic statistics: Parquet files use a columnar storage format and contain basic statistics such…
- **Sections:** Handling Parquet Files; Reasons for Querying Parquet Files; Reasons against Querying Parquet Files; The Effect of Row Group Sizes; Parquet File Sizes; Hive Partitioning for Filter Pushdown

### Tuning Workloads

- **URL:** https://duckdb.org/docs/current/guides/performance/how_to_tune_workloads
- **Summary:** The preserve_insertion_order Option When importing or exporting datasets (from/to the Parquet or CSV formats), which are much larger than the available memory, an out of memory error may occur: Out of Memory Error: failed to allocate data of size ... (.../... used) In these cases, consider setting the preserve_insertion_order configuration option to false: SET preserve_insertion_order = false;…
- **Sections:** The preserve_insertion_order Option; Parallelism (Multi-Core Processing); The Effect of Row Groups on Parallelism; Too Many Threads; Larger-than-Memory Workloads (Out-of-Core Processing); Spilling to Disk

### Data Import

- **URL:** https://duckdb.org/docs/current/guides/performance/import
- **Summary:** Recommended Import Methods When importing data from other systems to DuckDB, there are several considerations to take into account. We recommend importing using the following order: For systems which are supported by a DuckDB scanner extension, it's preferable to use the scanner. DuckDB currently offers scanners for MySQL, PostgreSQL and SQLite, as well as a generic ODBC scanner. If there is a…
- **Sections:** Recommended Import Methods; Methods to Avoid

### Indexing

- **URL:** https://duckdb.org/docs/current/guides/performance/indexing
- **Summary:** DuckDB has two types of indexes: zonemaps and ART indexes. Zonemaps DuckDB automatically creates zonemaps (also known as min-max indexes) for the columns of all general-purpose data types. Operations like predicate pushdown into scan operators and computing aggregations use zonemaps. If a filter criterion (like WHERE column1 = 123) is in use, DuckDB can skip any row group whose min-max range…
- **Sections:** Zonemaps; The Effect of Ordering on Zonemaps; Microbenchmark: The Effect of Ordering; Ordered Integers; ART Indexes; ART Index Scans

### Join Operations

- **URL:** https://duckdb.org/docs/current/guides/performance/join_operations
- **Summary:** How to Force a Join Order DuckDB has a cost-based query optimizer, which uses statistics in the base tables (stored in a DuckDB database or Parquet files) to estimate the cardinality of operations. Turn off the Join Order Optimizer To turn off the join order optimizer, set the following PRAGMAs: SET disabled_optimizers = 'join_order,build_side_probe_side'; This disables both the join order…
- **Sections:** How to Force a Join Order; Turn off the Join Order Optimizer; Create Temporary Tables

### My Workload Is Slow

- **URL:** https://duckdb.org/docs/current/guides/performance/my_workload_is_slow
- **Summary:** If you find that your workload in DuckDB is slow, we recommend performing the following checks. More detailed instructions are linked for each point. Do you have enough memory? DuckDB works best if you have 1-4 GB memory per thread. Is your system maybe overcommitting memory, forcing the operating system to swap? Try lowering the amount of memory available from the default 80% of the total RAM…

### Out-of-Memory Issues

- **URL:** https://duckdb.org/docs/current/guides/performance/oom
- **Summary:** Configuration Options If you are experiencing out-of-memory issues with DuckDB, try tweaking the following configuration options: Reduce the number of threads using the SET threads = ... command. Setting the memory limit lower than the default 80% can help prevent out of memory errors. While this configuration sounds counter-intuitive, it helps because some of DuckDB's operations circumvent…
- **Sections:** Configuration Options; Schema and Indexes

### Performance Guide

- **URL:** https://duckdb.org/docs/current/guides/performance/overview
- **Summary:** DuckDB aims to automatically achieve high performance by using well-chosen default configurations and having a forgiving architecture. Of course, there are still opportunities for tuning the system for specific workloads. The Performance Guide's pages contain guidelines and tips for achieving good performance when loading and processing data with DuckDB. The guides include several…
- **Sections:** Pages in This Section

### Schema

- **URL:** https://duckdb.org/docs/current/guides/performance/schema
- **Summary:** Types It is important to use the correct type for encoding columns (e.g., BIGINT, DATE, DATETIME). While it is always possible to use string types (VARCHAR, etc.) to encode more specific values, this is not recommended. Strings use more space and are slower to process in operations such as filtering, join, and aggregation. When loading CSV files, you may leverage the CSV reader's…
- **Sections:** Types; Microbenchmark: Using Timestamps; Microbenchmark: Joining on Strings; Constraints; Microbenchmark: The Effect of Primary Keys

### Working with Huge Databases

- **URL:** https://duckdb.org/docs/current/guides/performance/working_with_huge_databases
- **Summary:** This page contains information for working with huge DuckDB database files. While most DuckDB databases are well below 1 TB, in our 2024 user survey, 1% of respondents used DuckDB files of 2 TB or more (corresponding to roughly 10 TB of CSV files). DuckDB's native database format supports huge database files without any practical restrictions, however, there are a few things to keep in mind…

### Executing SQL in Python

- **URL:** https://duckdb.org/docs/current/guides/python/execute_sql
- **Summary:** SQL queries can be executed using the duckdb.sql function. import duckdb duckdb.sql("SELECT 42").show() By default this will create a relation object. The result can be converted to various formats using the result conversion functions. For example, the fetchall method can be used to convert the result to Python objects. results = duckdb.sql("SELECT 42").fetchall() print(results) [(42,)]…

### Export to Apache Arrow

- **URL:** https://duckdb.org/docs/current/guides/python/export_arrow
- **Summary:** All results of a query can be exported to an Apache Arrow Table using the to_arrow_table function. Alternatively, results can be returned as a RecordBatchReader using the to_arrow_reader function and results can be read one batch at a time. In addition, relations built using DuckDB's Relational API can also be exported. Deprecated The fetch_arrow_table, fetch_record_batch, and…
- **Sections:** Export to an Arrow Table; Export as a RecordBatchReader; Export from Relational API

### Export to Numpy

- **URL:** https://duckdb.org/docs/current/guides/python/export_numpy
- **Summary:** The result of a query can be converted to a Numpy array using the fetchnumpy() function. For example: import duckdb import numpy as np my_arr = duckdb.sql("SELECT unnest([1, 2, 3]) AS x, 5.0 AS y").fetchnumpy() my_arr {'x': array([1, 2, 3], dtype=int32), 'y': masked_array(data=[5.0, 5.0, 5.0], mask=[False, False, False], fill_value=1e+20)} Then, the array can be processed using Numpy…
- **Sections:** See Also

### Export to Pandas

- **URL:** https://duckdb.org/docs/current/guides/python/export_pandas
- **Summary:** The result of a query can be converted to a Pandas DataFrame using the df() function. import duckdb # read the result of an arbitrary SQL query to a Pandas DataFrame results = duckdb.sql("SELECT 42").df() results 42 0 42 See Also DuckDB also supports importing from Pandas.
- **Sections:** See Also

### Using fsspec Filesystems

- **URL:** https://duckdb.org/docs/current/guides/python/filesystems
- **Summary:** DuckDB support for fsspec filesystems allows querying data in filesystems that DuckDB's httpfs extension does not support. fsspec has a large number of inbuilt filesystems, and there are also many external implementations. This capability is only available in DuckDB's Python client because fsspec is a Python library, while the httpfs extension is available in many DuckDB clients. Example The…
- **Sections:** Example

### Integration with Ibis

- **URL:** https://duckdb.org/docs/current/guides/python/ibis
- **Summary:** Ibis is a Python dataframe library that supports 20+ backends, with DuckDB as the default. Ibis with DuckDB provides a Pythonic interface for SQL with great performance. Installation You can pip install Ibis with the DuckDB backend: pip install 'ibis-framework[duckdb,examples]' # examples is only required to access the sample data Ibis provides or use conda: conda install ibis-framework or use…
- **Sections:** Installation; Create a Database File; Interactive Mode; Common Operations; filter; select

### Import from Apache Arrow

- **URL:** https://duckdb.org/docs/current/guides/python/import_arrow
- **Summary:** CREATE TABLE AS and INSERT INTO can be used to create a table from any query. We can then create tables or insert into existing tables by referring to the Apache Arrow object in the query. This example imports from an Arrow Table, but DuckDB can query different Apache Arrow formats as seen in the SQL on Arrow guide. import duckdb import pyarrow as pa # connect to an in-memory database my_arrow…

### Import from Numpy

- **URL:** https://duckdb.org/docs/current/guides/python/import_numpy
- **Summary:** It is possible to query Numpy arrays from DuckDB. There is no need to register the arrays manually – DuckDB can find them in the Python process by name thanks to replacement scans. For example: import duckdb import numpy as np my_arr = np.array([(1, 9.0), (2, 8.0), (3, 7.0)]) duckdb.sql("SELECT * FROM my_arr") ┌─────────┬─────────┬─────────┐ │ column0 │ column1 │ column2 │ │ double │ double │…
- **Sections:** See Also

### Import from Pandas

- **URL:** https://duckdb.org/docs/current/guides/python/import_pandas
- **Summary:** CREATE TABLE ... AS and INSERT INTO can be used to create a table from any query. We can then create tables or insert into existing tables by referring to the Pandas DataFrame in the query. There is no need to register the DataFrames manually – DuckDB can find them in the Python process by name thanks to replacement scans. import duckdb import pandas # Create a Pandas dataframe my_df =…
- **Sections:** See Also

### Installing the Python Client

- **URL:** https://duckdb.org/docs/current/guides/python/install
- **Summary:** Installing via Pip The latest release of the Python client can be installed using pip. pip install duckdb The pre-release Python client (known as the “preview” or “nightly” build) can be installed using --pre. pip install duckdb --upgrade --pre Installing from Source The latest Python client can be installed from source from the tools/pythonpkg directory in the DuckDB GitHub repository.…
- **Sections:** Installing via Pip; Installing from Source

### Jupyter Notebooks

- **URL:** https://duckdb.org/docs/current/guides/python/jupyter
- **Summary:** DuckDB's Python client can be used directly in Jupyter notebooks with no additional configuration if desired. However, additional libraries can be used to simplify SQL query development. This guide will describe how to utilize those additional libraries. See other guides in the Python section for how to use DuckDB and Python together. In this example, we use the JupySQL package. This example…
- **Sections:** Library Installation; Library Import and Configuration; Connecting to DuckDB Natively; Connecting to DuckDB via SQLAlchemy; Querying DuckDB; Querying Pandas Dataframes

### marimo Notebooks

- **URL:** https://duckdb.org/docs/current/guides/python/marimo
- **Summary:** marimo is an open-source reactive notebook for Python and SQL that's tightly integrated with DuckDB's Python client, letting you mix and match Python and SQL in a single git-versionable notebook. Unlike traditional notebooks, when you run a cell or interact with a UI element, marimo automatically (or lazily) runs affected cells, keeping code and outputs consistent. Its integration with DuckDB…
- **Sections:** Installation; SQL in marimo; Connecting a Custom DuckDB Connection; Database, Schema, and Table Auto-Discovery; Reference a Local Dataframe; Reference the Output of a SQL Cell

### Multiple Python Threads

- **URL:** https://duckdb.org/docs/current/guides/python/multiple_threads
- **Summary:** This page demonstrates how to simultaneously insert into and read from a DuckDB database across multiple Python threads. This could be useful in scenarios where new data is flowing in and an analysis should be periodically re-run. Note that this is all within a single Python process (see the FAQ for details on DuckDB concurrency). Feel free to follow along in this Google Colab notebook. Setup…
- **Sections:** Setup; Reader and Writer Functions; Create Threads; Run Threads and Show Results

### Integration with Polars

- **URL:** https://duckdb.org/docs/current/guides/python/polars
- **Summary:** Polars is a DataFrames library built in Rust with bindings for Python and Node.js. It uses Apache Arrow's columnar format as its memory model. DuckDB can read Polars DataFrames and convert query results to Polars DataFrames. It does this internally using the efficient Apache Arrow integration. Note that the pyarrow library must be installed for the integration to work. Installation pip install…
- **Sections:** Installation; Polars to DuckDB; DuckDB to Polars

### Relational API on Pandas

- **URL:** https://duckdb.org/docs/current/guides/python/relational_api_pandas
- **Summary:** DuckDB offers a relational API that can be used to chain together query operations. These are lazily evaluated so that DuckDB can optimize their execution. These operators can act on Pandas DataFrames, DuckDB tables or views (which can point to any underlying storage format that DuckDB can read, such as CSV or Parquet files, etc.). Here we show a simple example of reading from a Pandas…

### SQL on Apache Arrow

- **URL:** https://duckdb.org/docs/current/guides/python/sql_on_arrow
- **Summary:** DuckDB can query multiple different types of Apache Arrow objects. Apache Arrow Tables Arrow Tables stored in local variables can be queried as if they are regular tables within DuckDB. import duckdb import pyarrow as pa # connect to an in-memory database con = duckdb.connect() my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4], 'j': ["one", "two", "three", "four"]}) # query the Apache…
- **Sections:** Apache Arrow Tables; Apache Arrow Datasets; Apache Arrow Scanners; Apache Arrow RecordBatchReaders

### SQL on Pandas

- **URL:** https://duckdb.org/docs/current/guides/python/sql_on_pandas
- **Summary:** Pandas DataFrames stored in local variables can be queried as if they are regular tables within DuckDB. import duckdb import pandas # Create a Pandas dataframe my_df = pandas.DataFrame.from_dict({'a': [42]}) # query the Pandas DataFrame "my_df" # Note: duckdb.sql connects to the default in-memory database connection results = duckdb.sql("SELECT * FROM my_df").df() The seamless integration of…

### Analyzing a Git Repository

- **URL:** https://duckdb.org/docs/current/guides/snippets/analyze_git_repository
- **Summary:** You can use DuckDB to analyze Git logs using the output of the git log command. Exporting the Git Log We start by picking a character that doesn't occur in any part of the commit log (author names, messages, etc). Since version v1.2.0, DuckDB's CSV reader supports 4-byte delimiters, making it possible to use emojis! 🎉 Despite being featured in the Emoji Movie (IMDb rating: 3.4), we can assume…
- **Sections:** Exporting the Git Log; Loading the Git Log into DuckDB; Analyzing the Log; Common Topics; Visualizing the Number of Commits

### Copying an In-Memory Database to a File

- **URL:** https://duckdb.org/docs/current/guides/snippets/copy_in-memory_database_to_file
- **Summary:** Imagine the following situation – you started DuckDB in in-memory mode but would like to persist the state of your database to disk. To achieve this, attach to a new disk-based database and use the COPY FROM DATABASE ... TO command: ATTACH 'my_database.db'; COPY FROM DATABASE memory TO my_database; DETACH my_database; Ensure that the disk-based database file does not exist before attaching to…

### Create Synthetic Data

- **URL:** https://duckdb.org/docs/current/guides/snippets/create_synthetic_data
- **Summary:** DuckDB allows you to quickly generate synthetic datasets. To do so, you may use: range functions hash functions, e.g., hash, md5, sha256 the Faker Python package via the Python function API using cross products (Cartesian products) For example: import duckdb from duckdb.sqltypes import * from faker import Faker fake = Faker() def random_date(): return fake.date_between() def…

### Dutch Railway Datasets

- **URL:** https://duckdb.org/docs/current/guides/snippets/dutch_railway_datasets
- **Summary:** Examples in this documentation often use datasets based on the Dutch Railway datasets. These high-quality datasets are maintained by the team behind the Rijden de Treinen (Are the trains running?) application. This page contains download links to our mirrors to the datasets. In 2024, we have published a blog post on the analysis of these datasets. Loading the Datasets You can load the datasets…
- **Sections:** Loading the Datasets; Datasets; 80-Month Datasets; Yearly Datasets; Monthly Datasets

### Importing Duckbox Tables

- **URL:** https://duckdb.org/docs/current/guides/snippets/importing_duckbox_tables
- **Summary:** The scripts provided in this page work on Linux, macOS, and WSL. By default, the DuckDB CLI client renders query results in the duckbox format, which uses rich, ASCII-art inspired tables to show data. These tables are often shared verbatim in other documents. For example, take the table used to demonstrate new CSV features in the DuckDB v1.2.0 release blog post: ┌─────────┬───────┐ │ a │ b │ │…
- **Sections:** Loading Duckbox Tables to DuckDB; Using shellfs; Limitations

### Sharing Macros

- **URL:** https://duckdb.org/docs/current/guides/snippets/sharing_macros
- **Summary:** DuckDB has a powerful macro mechanism that allows creating shorthands for common tasks. Sharing a Scalar Macro First, we define a macro that pretty-prints a non-negative integer as a short string with thousands, millions, and billions (without rounding) as follows: duckdb pretty_print_integer_macro.duckdb CREATE MACRO pretty_print_integer(n) AS CASE WHEN n >= 1_000_000_000 THEN printf('%dB', n…
- **Sections:** Sharing a Scalar Macro; Sharing a Table Macro

### DBeaver SQL IDE

- **URL:** https://duckdb.org/docs/current/guides/sql_editors/dbeaver
- **Summary:** DBeaver is a powerful and popular desktop SQL editor and integrated development environment (IDE). It has both an open source and enterprise version. DBeaver is useful for visually inspecting the available tables in DuckDB and for quickly building complex queries. DuckDB's JDBC connector allows DBeaver to query DuckDB files, and by extension, any other files that DuckDB can access (like…
- **Sections:** Installing DBeaver; Alternative Driver Installation

### AsOf Join

- **URL:** https://duckdb.org/docs/current/guides/sql_features/asof_join
- **Summary:** What is an AsOf Join? Time series data is not always perfectly aligned. Clocks may be slightly off, or there may be a delay between cause and effect. This can make connecting two sets of ordered data challenging. AsOf joins are a tool for solving this and other similar problems. One of the problems that AsOf joins are used to solve is finding the value of a varying property at a specific point…
- **Sections:** What is an AsOf Join?; Portfolio Example Dataset; Inner AsOf Joins; Outer AsOf Joins; AsOf Joins with the USING Keyword; Clarification on Column Selection with USING in ASOF Joins

### Full-Text Search

- **URL:** https://duckdb.org/docs/current/guides/sql_features/full_text_search
- **Summary:** DuckDB supports full-text search via the fts extension. A full-text index allows for a query to quickly search for all occurrences of individual words within longer text strings. Example: Shakespeare Corpus Here's an example of building a full-text index of Shakespeare's plays. CREATE TABLE corpus AS SELECT * FROM 'https://blobs.duckdb.org/data/shakespeare.parquet'; DESCRIBE corpus;…
- **Sections:** Example: Shakespeare Corpus; Creating a Full-Text Search Index; Note on Generating the Corpus Table

### Graph Queries

- **URL:** https://duckdb.org/docs/current/guides/sql_features/graph_queries
- **Summary:** DuckDB supports graph queries via the DuckPGQ community extension, which implements the SQL/PGQ syntax from the SQL:2023 standard. Warning DuckPGQ is a community extension and is still under active development. It is not available in the latest DuckDB release (1.5.x). If you want to work with DuckPGQ, make sure to use DuckDB v1.4.4. Moreover, some features may be incomplete. See the DuckPGQ…
- **Sections:** Installing DuckPGQ; Creating a Property Graph; Pattern Matching; Path Finding; Graph Algorithms; Use Case: Financial Fraud Detection

### Merge Statement for SCD Type 2

- **URL:** https://duckdb.org/docs/current/guides/sql_features/merge
- **Summary:** This is a practical, step-by-step guide to using DuckDB’s MERGE statement (introduced in v1.4.0) to perform upserts and build Slowly Changing Dimension Type 2 (SCD Type 2) tables. Type 2 SCDs let you keep full historical versions of records while clearly identifying the current version, perfect for audit trails, data warehousing, and analytical workloads. Type 2 SCDs are practical when you…
- **Sections:** Why Use MERGE in DuckDB?; Prerequisites; Key Terminology; Build an SCD Type 2 Dimension Table; Step 1: Create the Incoming (source) Table; Step 2: Create the Master (target) Table

### query and query_table Functions

- **URL:** https://duckdb.org/docs/current/guides/sql_features/query_and_query_table_functions
- **Summary:** The query_table and query functions enable powerful and more dynamic SQL. The query_table function returns the table whose name is specified by its string argument; the query function returns the table obtained by executing the query specified by its string argument. Both functions only accept constant strings. For example, they allow passing in a table name as a prepared statement parameter:…

### Timestamp Issues

- **URL:** https://duckdb.org/docs/current/guides/sql_features/timestamps
- **Summary:** Timestamp with Time Zone Promotion Casts Working with time zones in SQL can be quite confusing at times. For example, when filtering to a date range, one might try the following query: SET timezone = 'America/Los_Angeles'; CREATE TABLE times AS FROM range('2025-08-30'::TIMESTAMPTZ, '2025-08-31'::TIMESTAMPTZ, INTERVAL 1 HOUR) tbl(t); FROM times WHERE t <= '2025-08-30';…
- **Sections:** Timestamp with Time Zone Promotion Casts; Time Zone Performance; Half-Open Intervals

### Command Line

- **URL:** https://duckdb.org/docs/current/guides/troubleshooting/command_line
- **Summary:** Attaching to HTTPS Databases in v1.5.2 DuckDB v1.5.2 has a known issue where opening an HTTPS database directly from the command line fails with an error during httpfs extension autoloading: duckdb https://blobs.duckdb.org/data/tpch-sf1.db Extension Autoloading Error: An error occurred while trying to automatically install the required extension 'httpfs': Initialization function…
- **Sections:** Attaching to HTTPS Databases in v1.5.2; Piped Scripts Not Running in v1.5.0

### Crashes

- **URL:** https://duckdb.org/docs/current/guides/troubleshooting/crashes
- **Summary:** DuckDB is thoroughly tested via an extensive test suite. However, bugs can still occur and these can sometimes lead to crashes. This page contains practical information on how to troubleshoot DuckDB crashes. Types of Crashes There are a few major types of crashes: Termination signals: The process stops with a SIGSEGV (segmentation fault), SIGABRT, etc.: these should never occur. Please submit…
- **Sections:** Types of Crashes; Recovering Data; Troubleshooting the Crash; Using the Latest Stable and Preview Builds; Search for Existing Issues; Disabling the Query Optimizer

### Out of Memory Errors

- **URL:** https://duckdb.org/docs/current/guides/troubleshooting/oom_errors
- **Summary:** DuckDB has a state of the art out-of-core query engine that can spill to disk for larger-than-memory processing. We continuously strive to improve DuckDB's scalability and prevent out of memory errors whenever possible. That said, you may still experience out-of-memory errors if you run queries with multiple blocking operators, certain aggregation functions, PIVOT operations, etc., or if you…
- **Sections:** Types of “Out of Memory” Errors; OutOfMemoryException; OOM Reaper (Linux); Troubleshooting Out-of-Memory Errors; See Also

## Core extensions (47)

### AutoComplete Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/autocomplete
- **Summary:** The autocomplete extension adds support for autocomplete in the CLI client. The extension is shipped by default with the CLI client. Behavior For the behavior of the autocomplete extension, see the documentation of the CLI client. Functions Function Description sql_auto_complete(query_string) Attempts autocompletion on the given query_string. Example SELECT * FROM sql_auto_complete('SEL');…
- **Sections:** Behavior; Functions; Example

### Avro Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/avro
- **Summary:** The avro extension enables DuckDB to read Apache Avro files. The avro extension was released as a community extension in late 2024 and became a core extension in early 2025. The read_avro Function The extension adds a single DuckDB function, read_avro. This function can be used like so: FROM read_avro('some_file.avro'); This function will expose the contents of the Avro file as a DuckDB table.…
- **Sections:** The read_avro Function; File IO; Schema Conversion; Implementation; Limitations and Future Plans

### AWS Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/aws
- **Summary:** The aws extension adds functionality, e.g., authentication, on top of the httpfs extension's S3 capabilities, using the AWS SDK. Installing and Loading The aws extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually, run: INSTALL aws; LOAD aws; In most cases, the aws extension works in conjunction with…
- **Sections:** Installing and Loading; Configuration and Authentication; config Provider; credential_chain Provider; Validation; Auto-Refresh

### Azure Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/azure
- **Summary:** The azure extension is a loadable extension that adds a filesystem abstraction for Azure Blob Storage to DuckDB, enabling both reading and writing data. Installing and Loading The azure extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually, run: INSTALL azure; LOAD azure; Usage Once the authentication…
- **Sections:** Installing and Loading; Usage; Azure Blob Storage; Azure Data Lake Storage (ADLS); Writing to Azure Blob Storage; Configuration

### Delta Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/delta
- **Summary:** The delta extension adds support for the Delta Lake open-source storage format. It is built using the Delta Kernel. The extension offers read and write support for Delta tables, both local and remote. For implementation details, see the announcement blog post. Warning We are aware of a regression in Azure Onelake which appears to be a consequence of a change in delta-kernel-rs. You can track…
- **Sections:** Installing and Loading; Usage; Reading from an S3 Bucket; Reading from Azure Blob Storage; Reading from Google Cloud Storage; Appending Data

### DuckLake

- **URL:** https://duckdb.org/docs/current/core_extensions/ducklake
- **Summary:** DuckLake 1.0 was released in April 2026. Read the announcement blog post. The ducklake extension adds support for attaching to databases stored in the DuckLake format. The complete documentation of this extension is available at the DuckLake website. Installing and Loading To install ducklake, run: INSTALL ducklake; The ducklake extension will be transparently autoloaded on first use in an…
- **Sections:** Installing and Loading; Usage; Tables; Functions; ducklake_snapshots; ducklake_table_info

### Encodings Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/encodings
- **Summary:** The encodings extension adds support for reading CSVs using more than 1,000 character encodings. For a complete list of supported encodings, see All Supported Encodings. For detailed information on character encoding, see the ICU data repository. Installing and Loading INSTALL encodings; LOAD encodings; Usage Refer to the encoding while reading from files. To read a .csv file with shift_jis…
- **Sections:** Installing and Loading; Usage; All Supported Encodings

### Excel Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/excel
- **Summary:** The excel extension provides functions to format numbers per Excel's formatting rules by wrapping the i18npool library and to read/write Excel (.xlsx) files. However, please note that .xls files are not supported. Installing and Loading The excel extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually,…
- **Sections:** Installing and Loading; Excel Scalar Functions; Examples; Reading XLSX Files; Type and Range Inference; Writing XLSX Files

### Full-Text Search Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/full_text_search
- **Summary:** Full-Text Search is an extension to DuckDB that allows for search through strings, similar to SQLite's FTS5 extension. Installing and Loading The fts extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually, run: INSTALL fts; LOAD fts; Usage The extension adds two PRAGMA statements to DuckDB: one to…
- **Sections:** Installing and Loading; Usage; PRAGMA create_fts_index; PRAGMA drop_fts_index; match_bm25 Function; stem Function

### HTTP(S) Support

- **URL:** https://duckdb.org/docs/current/core_extensions/httpfs/https
- **Summary:** With the httpfs extension, it is possible to directly query files over the HTTP(S) protocol. This works for all files supported by DuckDB or its various extensions, and provides read-only access. SELECT * FROM 'https://domain.tld/file.extension'; Partial Reading For CSV files, files will be downloaded entirely in most cases, due to the row-based nature of the format. For Parquet files, DuckDB…
- **Sections:** Partial Reading; Scanning Multiple Files; Authenticating; HTTP Proxy; Using a Custom Certificate File

### Hugging Face Support

- **URL:** https://duckdb.org/docs/current/core_extensions/httpfs/hugging_face
- **Summary:** The httpfs extension introduces support for the hf:// protocol to access datasets hosted in Hugging Face repositories. See the announcement blog post for details. Usage Hugging Face repositories can be queried using the following URL pattern: hf://datasets/⟨my_username⟩/⟨my_dataset⟩/⟨path_to_file⟩ For example, to read a CSV file, you can use the following query: SELECT * FROM…
- **Sections:** Usage; Creating a Local Table; Multiple Files; Versioning and Revisions; Authentication; CONFIG

### httpfs Extension for HTTP and S3 Support

- **URL:** https://duckdb.org/docs/current/core_extensions/httpfs/overview
- **Summary:** The httpfs extension is an autoloadable extension implementing a file system that allows reading remote/writing remote files. For plain HTTP(S), only file reading is supported. For object storage using the S3 API, the httpfs extension supports reading/writing/globbing files. Installation and Loading The httpfs extension will be, by default, autoloaded on first use of any functionality exposed…
- **Sections:** Installation and Loading; HTTP(S); S3 API; Pages in This Section

### S3 API Support

- **URL:** https://duckdb.org/docs/current/core_extensions/httpfs/s3api
- **Summary:** The httpfs extension supports reading/writing/globbing files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers. Platforms The httpfs filesystem is tested with AWS S3, Minio, Google…
- **Sections:** Platforms; Configuration and Authentication; config Provider; credential_chain Provider; Overview of S3 Secret Parameters; Platform-Specific Secret Types

### Legacy Authentication Scheme for S3 API

- **URL:** https://duckdb.org/docs/current/core_extensions/httpfs/s3api_legacy_authentication
- **Summary:** Prior to version 0.10.0, DuckDB did not have a Secrets manager. Hence, the configuration of and authentication to S3 endpoints was handled via variables. This page documents the legacy authentication scheme for the S3 API. Warning This page describes a legacy method to store secrets as DuckDB settings. This increases the risk of accidentally leaking secrets (e.g., by printing their values).…
- **Sections:** Legacy Authentication Scheme; Per-Request Configuration; Configuration

### Amazon S3 Tables

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/amazon_s3_tables
- **Summary:** Support for S3 Tables is currently experimental. The iceberg extension supports reading Iceberg tables stored in Amazon S3 Tables. Requirements Install the following extensions: INSTALL aws; INSTALL httpfs; INSTALL iceberg; Connecting to Amazon S3 Tables You can let DuckDB detect your AWS credentials and configuration based on the default profile in your ~/.aws directory by creating the…
- **Sections:** Requirements; Connecting to Amazon S3 Tables

### Amazon SageMaker Lakehouse (AWS Glue)

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/amazon_sagemaker_lakehouse
- **Summary:** Support for Amazon SageMaker Lakehouse (AWS Glue) is currently experimental. The iceberg extension supports reading Iceberg tables through the Amazon SageMaker Lakehouse (a.k.a. AWS Glue) catalog. Requirements To use it, install the following extensions: INSTALL aws; INSTALL httpfs; INSTALL iceberg; If you want to switch back to using extensions from the core repository, follow the extension…
- **Sections:** Requirements; Connecting to Amazon SageMaker Lakehouse (AWS Glue)

### Iceberg REST Catalogs

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/iceberg_rest_catalogs
- **Summary:** This page covers connecting to Iceberg REST Catalogs: authentication, the full set of ATTACH options, and setup instructions for specific catalogs. For the basics of attaching a catalog and querying it, see Catalog Managed Tables; for write operations, see Writing to Iceberg. If you are attaching to an Iceberg REST Catalog managed by Amazon, please see the instructions for attaching to Amazon…
- **Sections:** ATTACH Options; Working with an Attached Catalog; Specific Catalog Examples; Cloudflare R2 Catalog; Polaris; Lakekeeper

### Iceberg Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/overview
- **Summary:** The iceberg extension implements support for the Apache Iceberg open table format. There are two ways to work with Iceberg in DuckDB: Individual tables are read directly from storage, by pointing at a table's metadata. This requires no catalog and is read-only. Catalog-managed tables are accessed by attaching an Iceberg REST catalog. This unlocks the full feature set, including writing. This…
- **Sections:** Installing and Loading; Updating the Extension; Individual Tables; Common Parameters; Querying Individual Tables; Accessing Iceberg Metadata

### Functions and Settings Reference

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/reference
- **Summary:** This page is a reference for all functions and settings provided by the iceberg extension. For task-oriented documentation, see the Overview (reading), Writing to Iceberg, and Iceberg REST Catalogs pages. Functions that take a table accept either a path to a table's metadata (e.g., 'data/iceberg/lineitem_iceberg') or, when a catalog is attached, a fully qualified table name (e.g.,…
- **Sections:** Common Parameters; Read and Metadata Functions; Table and Schema Property Functions; DuckLake Interoperability; Partition Transform Functions; Settings

### Troubleshooting

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/troubleshooting
- **Summary:** Curl Request Fails Problem When trying to attach to an Iceberg REST Catalog endpoint, DuckDB returns the following error: IO Error: Curl Request to '/v1/oauth/tokens' failed with error: 'URL using bad/illegal format or missing URL' Solution Make sure that you have the latest Iceberg extension installed: duckdb FORCE INSTALL iceberg FROM core_nightly; Exit DuckDB and start a new session: duckdb…
- **Sections:** Curl Request Fails; Problem; Solution; HTTP Error 403

### Writing to Iceberg

- **URL:** https://duckdb.org/docs/current/core_extensions/iceberg/writing
- **Summary:** The iceberg extension supports writing to Iceberg tables that are managed by an Iceberg REST Catalog. All write operations go through the attached catalog and are committed as new Iceberg snapshots. Writing requires an attached catalog. The path-based iceberg_scan interface described in the overview is read-only. To write, first attach an Iceberg REST catalog. The examples below assume a…
- **Sections:** Creating Schemas and Tables; Partitioning; Table Properties; Inserting Data; Updating and Deleting; Merging Data

### ICU Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/icu
- **Summary:** The icu extension contains an easy-to-use version of the collation/timezone part of the ICU library. Installing and Loading The icu extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually, run: INSTALL icu; LOAD icu; Features The icu extension introduces the following features: Region-dependent collations…
- **Sections:** Installing and Loading; Features

### inet Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/inet
- **Summary:** The inet extension defines the INET data type for storing IPv4 and IPv6 Internet addresses. It supports the CIDR notation for subnet masks (e.g., 198.51.100.0/22, 2001:db8:3c4d::/48). Installing and Loading The inet extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually, run: INSTALL inet; LOAD inet;…
- **Sections:** Installing and Loading; Examples; Operations on INET Values; host Function; netmask Function; network Function

### Redirecting…

- **URL:** https://duckdb.org/docs/current/core_extensions/jemalloc
- **Summary:** DuckDB documentation: Redirecting…

### Lance Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/lance
- **Summary:** The lance extension adds support for reading and writing Lance tables. Lance is a modern lakehouse format optimized for ML/AI workloads, with native cloud storage support. Installing and Loading You can install the lance extension from DuckDB's core extensions repository and load it using the following commands: INSTALL lance; LOAD lance; Usage Full SQL reference Cloud storage reference Query…
- **Sections:** Installing and Loading; Usage; Query a Lance Dataset; Write a Lance Dataset; Create a Lance Dataset via CREATE TABLE (Directory Namespace); Vector Search

### MotherDuck Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/motherduck
- **Summary:** The motherduck extension allows connecting to MotherDuck, a cloud data warehouse built on DuckDB. Installing and Loading The motherduck extension will be transparently autoinstalled and autoloaded on first use from the official extension repository. If you would like to install and load it manually, you can use the motherduck extension name or the md shorthand: INSTALL md; LOAD md; Usage You…
- **Sections:** Installing and Loading; Usage; Platforms; MotherDuck Documentation

### MySQL Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/mysql
- **Summary:** The mysql extension allows DuckDB to directly read and write data from/to a running MySQL instance. The data can be queried directly from the underlying MySQL database. Data can be loaded from MySQL tables into DuckDB tables, or vice versa. Installing and Loading To install the mysql extension, run: INSTALL mysql; The extension is loaded automatically upon first use. If you prefer to load it…
- **Sections:** Installing and Loading; Reading Data from MySQL; Configuration; Configuring via Secrets; SSL Connections; Reading MySQL Tables

### ODBC Extension Functions

- **URL:** https://duckdb.org/docs/current/core_extensions/odbc/functions
- **Summary:** odbc_begin_transaction odbc_bind_params odbc_close odbc_commit odbc_connect odbc_copy odbc_create_params odbc_list_data_sources odbc_list_drivers odbc_query odbc_rollback odbc_begin_transaction odbc_begin_transaction(conn_handle BIGINT) -> VARCHAR Sets the SQL_ATTR_AUTOCOMMIT attribute to SQL_AUTOCOMMIT_OFF on the specified connection thus effectively starting an implicit transaction.…
- **Sections:** odbc_begin_transaction; odbc_bind_params; odbc_close; odbc_commit; odbc_connect; odbc_copy

### ODBC Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/odbc/overview
- **Summary:** The odbc_scanner extension allows connecting to other databases (using their ODBC drivers) and run queries with the odbc_query or copy data from DuckDB with the odbc_copy functions. The extension is also available under the alias odbc. Installing and Loading On Linux and macOS the extension requires unixODBC driver manager to be installed. See below for installation instructions. The extension…
- **Sections:** Installing and Loading; Usage Example; Installing the Nightly Version; Support Status of DBMS-Specific Types; Installing unixODBC Driver Manager on Linux or macOS; Connection String Examples

### Core Extensions

- **URL:** https://duckdb.org/docs/current/core_extensions/overview
- **Summary:** List of Core Extensions Name Description Maintainer Support tier Aliases autocomplete Adds support for autocomplete in the shell DuckDB team {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} avro Add support for reading Avro files DuckDB team {% include tooltip.html label="Secondary" id="support_tier_secondary_extension" %} aws Provides features that depend…
- **Sections:** List of Core Extensions; Pages in This Section

### PostgreSQL Extension Connection Pool

- **URL:** https://duckdb.org/docs/current/core_extensions/postgres/connection_pool
- **Summary:** PostgreSQL server spawns a backend process for every incoming client connection. This model leads to the two following points with the postgres extension that can cause performance problems: opening a new connection is relatively expensive the number of the connections opened at the same time should not be too high To deal with these points the extensions uses an in-memory connection pool.…
- **Sections:** Parallel Scans; Connection Proxies; Reaper Thread; Thread-local Cache; Configuration Options

### PostgreSQL Extension Functions

- **URL:** https://duckdb.org/docs/current/core_extensions/postgres/functions
- **Summary:** pg_clear_cache postgres_attach postgres_configure_pool postgres_execute postgres_hstore_get postgres_hstore_to_json postgres_query postgres_scan postgres_scan_pushdown read_postgres_binary pg_clear_cache pg_clear_cache() -> TABLE Clears cached schema entries (like table names with column lists) for all attached PostgreSQL catalogs. Attached schema is going to be re-read on the next access.…
- **Sections:** pg_clear_cache; postgres_attach; postgres_configure_pool; postgres_execute; postgres_hstore_get; postgres_hstore_to_json

### PostgreSQL Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/postgres/overview
- **Summary:** The postgres extension allows DuckDB to directly read and write data from a running PostgreSQL database instance. The data can be queried directly from the underlying PostgreSQL database. Data can be loaded from PostgreSQL tables into DuckDB tables, or vice versa. See the official announcement for implementation details and background. Installing and Loading The postgres extension will be…
- **Sections:** Installing and Loading; Connecting; Configuration; Configuring via Secrets; Configuring via Environment Variables; Usage

### PostgreSQL Extension and the Secret Manager

- **URL:** https://duckdb.org/docs/current/core_extensions/postgres/secrets
- **Summary:** User credentials and other PostgreSQL database connection details can be stored using the DuckDB Secrets Manager. The following syntax can be used to create a secret: CREATE SECRET ( TYPE postgres, HOST '127.0.0.1', PORT 5432, DATABASE postgres, USER 'postgres', PASSWORD '' ); The information from the secret will be used when ATTACH is called. We can leave the PostgreSQL connection string…
- **Sections:** Managing Multiple Secrets; Secret Configuration Options; AWS RDS IAM Authentication; Connecting with IAM Authentication from Command Line; Configuring Secrets for IAM Authentication; Storing Secrets inside a PostgreSQL Database

### Quack Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/quack
- **Summary:** The quack extension adds support for the Quack remote protocol. Usage Quack is currently in a beta state. Quack will be transparently autoinstalled and autoloaded on first use. If you would like to install Quack explicitly, run: INSTALL quack; If you would like to load Quack explicitly, run: LOAD quack; Limitations Warning As of DuckDB v1.5.3, quack is in an experimental state. The protocol,…
- **Sections:** Usage; Limitations

### Spatial Functions

- **URL:** https://duckdb.org/docs/current/core_extensions/spatial/functions
- **Summary:** Function Index Scalar Functions Function Summary DuckDB_PROJ_Compiled_Version Returns a text description of the PROJ library version that this instance of DuckDB was compiled against. DuckDB_Proj_Version Returns a text description of the PROJ library version that is being used by this instance of DuckDB. ST_Affine Applies an affine transformation to a geometry. ST_Area Compute the area of a…
- **Sections:** Function Index; Scalar Functions; DuckDB_PROJ_Compiled_Version; DuckDB_Proj_Version; ST_Affine; ST_Area

### GDAL Integration

- **URL:** https://duckdb.org/docs/current/core_extensions/spatial/gdal
- **Summary:** The spatial extension integrates the GDAL translator library to read and write spatial data from a variety of geospatial vector file formats. See the documentation for the st_read table function for how to make use of this in practice. In order to spare users from having to setup and install additional dependencies on their system, the spatial extension bundles its own copy of the GDAL…
- **Sections:** GDAL Based COPY Function; Limitations

### Spatial Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/spatial/overview
- **Summary:** The spatial extension provides support for geospatial data processing in DuckDB. For an overview of the extension, see our blog post. Installing and Loading To install the spatial extension, run: INSTALL spatial; Note that the spatial extension is not autoloadable. Therefore, you need to load it before using it: LOAD spatial; INSTALL spatial ; Note that the spatial extension is not…
- **Sections:** Installing and Loading; Pages in This Section

### R-Tree Indexes

- **URL:** https://duckdb.org/docs/current/core_extensions/spatial/r-tree_indexes
- **Summary:** The spatial extension provides support for spatial indexing through the R-tree extension index type. Why Should I Use an R-Tree Index? When working with geospatial datasets, it is very common that you want to filter rows based on their spatial relationship with a specific region of interest. Unfortunately, even though DuckDB's vectorized execution engine is pretty fast, this sort of operation…
- **Sections:** Why Should I Use an R-Tree Index?; How Do R-Tree Indexes Work?; What Are the Limitations of R-Tree Indexes in DuckDB?; How to Use R-Tree Indexes in DuckDB; Example; Performance Considerations

### SQLite Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/sqlite
- **Summary:** The SQLite extension allows DuckDB to directly read and write data from a SQLite database file. The data can be queried directly from the underlying SQLite tables. Data can be loaded from SQLite tables into DuckDB tables, or vice versa. Installing and Loading The sqlite extension will be transparently autoloaded on first use from the official extension repository. If you would like to install…
- **Sections:** Installing and Loading; Usage; Data Types; Opening SQLite Databases Directly; Writing Data to SQLite; Concurrency

### SQLSmith Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/sqlsmith
- **Summary:** The sqlsmith extension is used for testing. Installing and Loading INSTALL sqlsmith; LOAD sqlsmith; Functions The sqlsmith extension registers the following functions: sqlsmith fuzzyduck reduce_sql_statement fuzz_all_functions INSTALL sqlsmith ; LOAD sqlsmith ; Functions The sqlsmith extension registers the following functions:
- **Sections:** Installing and Loading; Functions

### TPC-DS Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/tpcds
- **Summary:** The tpcds extension implements the data generator and queries for the TPC-DS benchmark. Installing and Loading The tpcds extension will be transparently autoloaded on first use from the official extension repository. If you would like to install and load it manually, run: INSTALL tpcds; LOAD tpcds; Usage To generate data for scale factor 1, use: CALL dsdgen(sf = 1); To run a query, e.g., query…
- **Sections:** Installing and Loading; Usage; Listing Queries; Listing Expected Answers; Generating the Schema; Data Generator Parameters

### TPC-H Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/tpch
- **Summary:** The tpch extension implements the data generator and queries for the TPC-H benchmark. Installing and Loading The tpch extension is shipped by default in some DuckDB builds, otherwise it will be transparently autoloaded on first use. If you would like to install and load it manually, run: INSTALL tpch; LOAD tpch; Benchmarking with the TPC-H Workload To run the full TPC-H workload with DuckDB,…
- **Sections:** Installing and Loading; Benchmarking with the TPC-H Workload; Usage; Generating Data; Running a Query; Listing Queries

### UI Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/ui
- **Summary:** The ui extension adds a user interface for your local DuckDB instance. The UI is built and maintained by MotherDuck. An overview of its features can be found in the MotherDuck documentation. Usage To start the UI from the command line: duckdb -ui To start the UI from SQL: CALL start_ui(); Running either of these will open the UI in your default browser. The UI connects to the DuckDB instance…
- **Sections:** Usage; Local Query Execution; Configuration; Local Port; Remote URL; Polling Interval

### Unity Catalog Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/unity_catalog
- **Summary:** The unity_catalog extension adds support for the Unity Catalog atop the Delta Lake format and DuckDB Delta extension. The delta extension adds support for the Delta Lake open-source storage format. It is built using the Delta Kernel. The extension offers read support for Delta tables, both local and remote. For implementation details, see the announcement blog post. Note Both extensions are…
- **Sections:** Installing and Loading; Usage; Reading; Writing; Catalog-Managed Commits; Features

### Vortex Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/vortex
- **Summary:** The vortex extension allows you to read and write files using the Vortex file format. It is currently available for the Linux (linux_amd64, linux_arm64) and macOS (osx_amd64, osx_arm64) distributions. Installing and Loading To install and load the extension, run: INSTALL vortex; LOAD vortex; Reading Vortex Files Using the read_vortex function to read Vortex files: SELECT * FROM…
- **Sections:** Installing and Loading; Reading Vortex Files; Writing Vortex Files

### Vector Similarity Search Extension

- **URL:** https://duckdb.org/docs/current/core_extensions/vss
- **Summary:** The vss extension is an experimental extension for DuckDB that adds indexing support to accelerate vector similarity search queries using DuckDB's new fixed-size ARRAY type. See the announcement blog post and the “What's New in the Vector Similarity Search Extension?” post. Usage To create a new HNSW (Hierarchical Navigable Small Worlds) index on a table with an ARRAY column, use the CREATE…
- **Sections:** Usage; Index Options; Persistence; Inserts, Updates, Deletes and Re-Compaction; Bonus: Vector Similarity Search Joins; Limitations

## Extensions overview (7)

### Advanced Installation Methods

- **URL:** https://duckdb.org/docs/current/extensions/advanced_installation_methods
- **Summary:** Downloading Extensions Directly from S3 Downloading an extension directly can be helpful when building a Lambda service or container that uses DuckDB. DuckDB extensions are stored in public S3 buckets, but the directory structure of those buckets is not searchable. As a result, a direct URL to the file must be used. To download an extension file directly, use the following format:…
- **Sections:** Downloading Extensions Directly from S3; Installing an Extension from an Explicit Path; Loading an Extension from an Explicit Path; Building and Installing Extensions from Source; Statically Linking Extensions

### Community Extensions

- **URL:** https://duckdb.org/docs/current/extensions/community_extensions
- **Summary:** Community-contributed extensions can be installed from the Community Extensions repository since summer 2024. Please visit the “Community Extensions” section of the documentation for more details.

### Extension Distribution

- **URL:** https://duckdb.org/docs/current/extensions/extension_distribution
- **Summary:** Platforms Extension binaries are distributed for several platforms (see below). For platforms where packages for certain extensions are not available, users can build them from source and install the resulting binaries manually. All official extensions are distributed for the following platforms. Platform name Operating system Architecture CPU types linux_amd64 Linux x86_64 (AMD64) …
- **Sections:** Platforms; Extensions Signing; Signed Extensions; Unsigned Extensions; Binary Compatibility; Creating a Custom Repository

### Installing Extensions

- **URL:** https://duckdb.org/docs/current/extensions/installing_extensions
- **Summary:** To install core DuckDB extensions, use the INSTALL command. For example: INSTALL httpfs; This installs the extension from the default repository (core). Extension Repositories By default, DuckDB extensions are installed from a single repository containing extensions built and signed by the core DuckDB team. This ensures the stability and security of the core set of extensions. These extensions…
- **Sections:** Extension Repositories; Installing Extensions from Different Repositories; Working with Multiple Repositories; Force Installing to Upgrade Extensions; Switching between Repositories; Installing Extensions through Client APIs

### Extensions

- **URL:** https://duckdb.org/docs/current/extensions/overview
- **Summary:** DuckDB has a flexible extension mechanism that allows for dynamically loading extensions. Extensions can enhance DuckDB's functionality by providing support for additional file formats, introducing new types, and domain-specific functionality. Extensions are loadable on all clients (e.g., Python and R). Extensions distributed via the Core and Community repositories are built and tested on…
- **Sections:** Listing Extensions; Built-In Extensions; Installing More Extensions; Explicit INSTALL and LOAD; Autoloading Extensions; Community Extensions

### Troubleshooting of Extensions

- **URL:** https://duckdb.org/docs/current/extensions/troubleshooting
- **Summary:** You might be visiting this page directed via a DuckDB error message, similar to: INSTALL non_existing; HTTP Error: Failed to download extension "non_existing" at URL "http://extensions.duckdb.org/v1.4.0/osx_arm64/non_existing.duckdb_extension.gz" (HTTP 404) Candidate extensions: "inet", "encodings", "core_functions", "sqlite_scanner", "postgres_scanner" For more info, visit…
- **Sections:** Manual Process to Download Extensions via the Browser

### Versioning of Extensions

- **URL:** https://duckdb.org/docs/current/extensions/versioning_of_extensions
- **Summary:** Extension Versioning Most software has some sort of version number. Version numbers serve a few important goals: Tie a binary to a specific state of the source code Allow determining the expected feature set Allow determining the state of the APIs Allow efficient processing of bug reports (e.g., bug #1337 was introduced in version v3.4.5 ) Allow determining chronological order of releases…
- **Sections:** Extension Versioning; Unstable Extensions; Pre-Release Extensions; Stable Extensions; Release Cycle of Pre-Release and Stable Core Extensions; Nightly Builds

## Configuration (3)

### Configuration

- **URL:** https://duckdb.org/docs/current/configuration/overview
- **Summary:** DuckDB has a number of configuration options that can be used to change the behavior of the system. The configuration options can be set using either the SET statement or the PRAGMA statement. They can be reset to their original values using the RESET statement. The values of configuration options can be queried via the current_setting() scalar function or using the duckdb_settings() table…
- **Sections:** Examples; Secrets Manager; Configuration Reference; Global Configuration Options; Local Configuration Options; Pages in This Section

### Pragmas

- **URL:** https://duckdb.org/docs/current/configuration/pragmas
- **Summary:** The PRAGMA statement is a SQL extension adopted by DuckDB from SQLite. PRAGMA statements can be issued in a similar manner to regular SQL statements. PRAGMA commands may alter the internal state of the database engine, and can influence the subsequent execution or behavior of the engine. PRAGMA statements that assign a value to an option can also be issued using the SET statement and the value…
- **Sections:** Metadata; Resource Management; Collations; Default Ordering for NULLs; Ordering by Non-Integer Literals; Implicit Casting to VARCHAR

### Secrets Manager

- **URL:** https://duckdb.org/docs/current/configuration/secrets_manager
- **Summary:** The Secrets manager provides a unified user interface for secrets across all backends that use them. Secrets can be scoped, so different storage prefixes can have different secrets, allowing for example to join data across organizations in a single query. Secrets can also be persisted, so that they do not need to be specified every time DuckDB is launched. Warning Persistent secrets are stored…
- **Sections:** Types of Secrets; Creating a Secret; Secret Providers; Temporary Secrets; Persistent Secrets; Deleting Secrets

## Connecting (2)

### Concurrency

- **URL:** https://duckdb.org/docs/current/connect/concurrency
- **Summary:** Handling Concurrency Single Process In in-process mode, DuckDB has two configurable options for concurrency: Read-write mode: one process can both read and write to the database. Read-only mode: multiple processes can read from the database, but no processes can write (access_mode = 'READ_ONLY'). When using read-write mode, DuckDB supports multiple writer threads using a combination of MVCC…
- **Sections:** Handling Concurrency; Single Process; Multiple Processes; Optimistic Concurrency Control; Troubleshooting

### Connect

- **URL:** https://duckdb.org/docs/current/connect/overview
- **Summary:** Connect or Create a Database To use DuckDB, you must first create a connection to a database. The exact syntax varies between the client APIs but it typically involves passing an argument to configure persistence. Persistence DuckDB can operate in both persistent mode, where the data is saved to disk, and in in-memory mode, where the entire dataset is stored in the main memory. Tip Both…
- **Sections:** Connect or Create a Database; Persistence; Persistent Database; In-Memory Database; Pages in This Section

## Operations manual (13)

### DuckDB Docker Container

- **URL:** https://duckdb.org/docs/current/operations_manual/duckdb_docker
- **Summary:** DuckDB has an official Docker image, which supports both the ARM64 (AArch64) and x86_64 (AMD64) architectures. Usage To use the DuckDB Docker image, run: docker run --rm -it -v "$(pwd):/workspace" -w /workspace duckdb/duckdb Using the DuckDB UI with Docker To use the DuckDB UI with Docker, enable host networking. This setting forwards all ports from the container, so exercise caution and avoid…
- **Sections:** Usage; Using the DuckDB UI with Docker

### Files Created by DuckDB

- **URL:** https://duckdb.org/docs/current/operations_manual/footprint_of_duckdb/files_created_by_duckdb
- **Summary:** DuckDB creates several files and directories on disk. This page lists both the global and the local ones. Global Files and Directories DuckDB creates the following global files and directories in the user's home directory (denoted with ~): Location Description Shared between versions Shared between clients ~/.duckdbrc The content of this file is executed when starting the DuckDB CLI client.…
- **Sections:** Global Files and Directories; Local Files and Directories

### Gitignore for DuckDB

- **URL:** https://duckdb.org/docs/current/operations_manual/footprint_of_duckdb/gitignore_for_duckdb
- **Summary:** If you work in a Git repository, you may want to configure your Gitignore to disable tracking files created by DuckDB. These potentially include the DuckDB database, write-ahead log, and temporary files. Sample Gitignore Files In the following, we present sample Gitignore configuration snippets for DuckDB. Ignore Temporary Files but Keep Database This configuration is useful if you would like…
- **Sections:** Sample Gitignore Files; Ignore Temporary Files but Keep Database; Ignore Database and Temporary Files

### Reclaiming Space

- **URL:** https://duckdb.org/docs/current/operations_manual/footprint_of_duckdb/reclaiming_space
- **Summary:** DuckDB uses a single-file format, which has some inherent limitations w.r.t. reclaiming disk space. CHECKPOINT To reclaim space after deleting rows, use the CHECKPOINT statement. VACUUM The VACUUM statement does not trigger vacuuming deletes and hence does not reclaim space. Compacting a Database by Copying To compact the database, you can create a fresh copy of the database using the COPY…
- **Sections:** CHECKPOINT; VACUUM; Compacting a Database by Copying

### Install Script

- **URL:** https://duckdb.org/docs/current/operations_manual/installing_duckdb/install_script
- **Summary:** You can install the DuckDB CLI client using an install script. Linux and macOS To use the DuckDB install script on Linux and macOS, run: curl https://install.duckdb.org | sh Click to see the output of the install script. % Total % Received % Xferd Average Speed Time Time Time Current Dload Upload Total Spent Left Speed 100 3507 100 3507 0 0 34367 0 --:--:-- --:--:-- --:--:-- 34382…
- **Sections:** Linux and macOS; Windows

### Limits

- **URL:** https://duckdb.org/docs/current/operations_manual/limits
- **Summary:** This page contains DuckDB's built-in limit values. To check the value of a setting on your system, use the current_setting function. Limit Values Limit Default value Configuration option Comment Array size 100000 - BLOB size 4 GB - Expression depth 1000 max_expression_depth Memory allocation for a vector 128 GB - Memory use 80% of RAM memory_limit Note: This limit only applies to the…
- **Sections:** Limit Values; Size of Database Files

### Logging

- **URL:** https://duckdb.org/docs/current/operations_manual/logging/overview
- **Summary:** DuckDB implements a logging mechanism that provides users with detailed information about events such as query execution, performance metrics and system events. Basics The DuckDB logging mechanism can be enabled or disabled using a special function, enable_logging. Logs are stored in a special view named duckdb_logs, which can be queried like any standard table. Example: CALL enable_logging();…
- **Sections:** Basics; Log Level; Log Types; Logging-Specific Types; Structured Logging; List of Available Log Types

### Non-Deterministic Behavior

- **URL:** https://duckdb.org/docs/current/operations_manual/non-deterministic_behavior
- **Summary:** Several operators in DuckDB exhibit non-deterministic behavior. Most notably, SQL uses set semantics, which allows results to be returned in a different order. DuckDB exploits this to improve performance, particularly when performing multi-threaded query execution. Other factors, such as using different compilers, operating systems and hardware architectures, can also cause changes in…
- **Sections:** Set Semantics; Different Results on Different Platforms: array_distinct; Floating-Point Aggregate Operations with Multi-Threading; Working Around Non-Determinism

### Overview

- **URL:** https://duckdb.org/docs/current/operations_manual/overview
- **Summary:** We designed DuckDB to be easy to deploy and operate. We believe that most users do not need to consult the pages of the operations manual. However, there are certain setups – e.g., when DuckDB is running in mission-critical infrastructure – where we would like to offer advice on how to configure DuckDB. The operations manual contains advice for these cases and also offers convenient…
- **Sections:** Pages in This Section

### Embedding DuckDB

- **URL:** https://duckdb.org/docs/current/operations_manual/securing_duckdb/embedding_duckdb
- **Summary:** CLI Client The Command Line Interface (CLI) client is intended for interactive use cases and not for embedding. As a result, it has more features that could be abused by a malicious actor. For example, the CLI client has the .sh feature that allows executing arbitrary shell commands. This feature is only present in the CLI client and not in any other DuckDB clients. .sh ls Tip Calling DuckDB's…
- **Sections:** CLI Client

### Securing DuckDB

- **URL:** https://duckdb.org/docs/current/operations_manual/securing_duckdb/overview
- **Summary:** DuckDB is a powerful analytical database engine. It can read and write files, access the network, load extensions, and use system resources. Like any powerful tool, these capabilities require appropriate configuration when working with sensitive data or in shared environments. This page documents DuckDB's security model and security-related settings. The right configuration depends on your use…
- **Sections:** Untrusted Input; Untrusted SQL Input; Untrusted Non-SQL Input; Extensions; Autoloading; Core vs. Community Extensions

### Securing Extensions

- **URL:** https://duckdb.org/docs/current/operations_manual/securing_duckdb/securing_extensions
- **Summary:** DuckDB has a powerful extension mechanism, which has the same privileges as the user running DuckDB's (parent) process. This introduces security considerations. Therefore, we recommend reviewing the configuration options listed
- **Sections:** DuckDB Signature Checks; Overview of Security Levels for Extensions; Community Extensions; Disabling Autoinstalling and Autoloading Known Extensions; Always Require Signed Extensions

### HTTP User-Agent

- **URL:** https://duckdb.org/docs/current/operations_manual/user_agents
- **Summary:** HTTP User-Agent Core DuckDB sets the default user-agent as follows: duckdb/v1.4.4(osx_arm64) cli 6ddac802ff which indicates version, architecture, client, buildref in the agent string. The user-agent string can also be modified via the custom_user_agent setting, see Configuration. The currently generated user-agent string can be seen via PRAGMA user_agent;, see Configuration/Pragmas. In…
- **Sections:** HTTP User-Agent; Extensions; Azure; Delta (and Unity Catalog); HTTPFS - HTTPS/S3

## Internals (5)

### jemalloc

- **URL:** https://duckdb.org/docs/current/internals/jemalloc
- **Summary:** The jemalloc extension replaces the system's memory allocator with jemalloc. jemalloc extension is statically linked and cannot be installed or loaded during runtime. For thechnical reasons, we used to distribute jemalloc as an extension. Since DuckDB v1.5.3, it is distributred as a third-party library. Operating System Support The availability of the jemalloc extension depends on the…
- **Sections:** Operating System Support; Linux; macOS; Windows; Configuration; Environment Variables

### Overview of DuckDB Internals

- **URL:** https://duckdb.org/docs/current/internals/overview
- **Summary:** Tip For a detailed explanation of DuckDB internals, see the Design and Implementation of DuckDB Internals ("DiDi") library entry.
- **Sections:** Parser; ParsedExpression; TableRef; QueryNode; SQL Statement; Binder

### Pivot Internals

- **URL:** https://duckdb.org/docs/current/internals/pivot
- **Summary:** PIVOT Pivoting is implemented as a combination of SQL query re-writing and a dedicated PhysicalPivot operator for higher performance. Each PIVOT is implemented as set of aggregations into lists and then the dedicated PhysicalPivot operator converts those lists into column names and values. Additional pre-processing steps are required if the columns to be created when pivoting are detected…
- **Sections:** PIVOT; UNPIVOT; Internals

### Storage Versions and Format

- **URL:** https://duckdb.org/docs/current/internals/storage
- **Summary:** Compatibility Backward Compatibility Backward compatibility refers to the ability of a newer DuckDB version to read storage files created by an older DuckDB version. Version 0.10 is the first release of DuckDB that supports backward compatibility in the storage format. DuckDB v0.10 can read and operate on files created by the previous DuckDB version – DuckDB v0.9. For future DuckDB versions,…
- **Sections:** Compatibility; Backward Compatibility; Forward Compatibility; How to Move between Storage Formats; Default Storage Version; Explicit Storage Versions

### Execution Format

- **URL:** https://duckdb.org/docs/current/internals/vector
- **Summary:** Vector is the container format used to store in-memory data during execution. DataChunk is a collection of Vectors, used for instance to represent a column list in a PhysicalProjection operator. Data Flow DuckDB uses a vectorized query execution model. All operators in DuckDB are optimized to work on Vectors of a fixed size. This fixed size is commonly referred to in the code as…
- **Sections:** Data Flow; Vector Format; Flat Vectors; Constant Vectors; Dictionary Vectors; Sequence Vectors

## Development (27)

### Benchmark Suite

- **URL:** https://duckdb.org/docs/current/dev/benchmark
- **Summary:** DuckDB has an extensive benchmark suite. When making changes that have potential performance implications, it is important to run these benchmarks to detect potential performance regressions. Getting Started To build the benchmark suite, run the following command in the DuckDB repository: BUILD_BENCHMARK=1 BUILD_EXTENSIONS='tpch' make Listing Benchmarks To list all available benchmarks, run:…
- **Sections:** Getting Started; Listing Benchmarks; Running Benchmarks; Running a Single Benchmark; Running Multiple Benchmarks Using a Regular Expression; Creating Benchmarks

### Android

- **URL:** https://duckdb.org/docs/current/dev/building/android
- **Summary:** DuckDB has experimental support for Android. Please use the latest main branch of DuckDB instead of the stable versions. Building the DuckDB Library Using the Android NDK We provide build instructions for setups using macOS and Android Studio. For other setups, please adjust the steps accordingly. Open Android Studio. Select the Tools menu and pick SDK Manager. Select the SDK Tools tab and…
- **Sections:** Building the DuckDB Library Using the Android NDK; Building the CLI in Termux; Troubleshooting; Log Library Is Missing

### Building Configuration

- **URL:** https://duckdb.org/docs/current/dev/building/build_configuration
- **Summary:** Build Types DuckDB can be built in many different settings, most of these correspond directly to CMake but not all of them. release This build has been stripped of all the assertions and debug symbols and code, optimized for performance. debug This build runs with all the debug information, including symbols, assertions and #ifdef DEBUG blocks. Due to these, binaries of this build are expected…
- **Sections:** Build Types; release; debug; relassert; reldebug; benchmark

### Building Extensions

- **URL:** https://duckdb.org/docs/current/dev/building/building_extensions
- **Summary:** Extensions can be built from source and installed from the resulting local binary. Building Extensions To build using extension flags, set the BUILD_EXTENSIONS flag to the list of extensions that you want to be built. For example: BUILD_EXTENSIONS='autocomplete;httpfs;icu;json;tpch' GEN=ninja make This option also accepts out-of-tree extensions such as delta:…
- **Sections:** Building Extensions; Special Extension Flags; BUILD_JEMALLOC; BUILD_TPCE; Debug Flags; CRASH_ON_ASSERT

### Linux

- **URL:** https://duckdb.org/docs/current/dev/building/linux
- **Summary:** Prerequisites On Linux, install the required packages with the package manager of your distribution. Ubuntu and Debian CLI Client On Ubuntu and Debian (and also MX Linux, Linux Mint, etc.), the requirements for building the DuckDB CLI client are the following: sudo apt-get update sudo apt-get install -y git g++ cmake ninja-build libssl-dev libcurl4-openssl-dev git clone…
- **Sections:** Prerequisites; Ubuntu and Debian; Fedora, CentOS and Red Hat; Arch Linux; Alpine Linux; Using the DuckDB CLI Client on Linux

### macOS

- **URL:** https://duckdb.org/docs/current/dev/building/macos
- **Summary:** Prerequisites Install Xcode and Homebrew. Then, install the required packages with: brew install git cmake ninja Building DuckDB Clone and build DuckDB as follows. git clone https://github.com/duckdb/duckdb cd duckdb GEN=ninja make Once the build finishes successfully, you can find the duckdb binary in the build directory: build/release/duckdb For different build configurations (debug,…
- **Sections:** Prerequisites; Building DuckDB; Troubleshooting; Build Failure: 'string' file not found; Debug Build Prints malloc Warning

### Building DuckDB from Source

- **URL:** https://duckdb.org/docs/current/dev/building/overview
- **Summary:** When Should You Build DuckDB? DuckDB binaries are available for stable and preview builds on the installation page. In most cases, it's recommended to use these binaries. When you are running on an experimental platform (e.g., Raspberry Pi) or you would like to build the project for an unmerged pull request, you can build DuckDB from source based on the duckdb/duckdb repository hosted on…
- **Sections:** When Should You Build DuckDB?; Build Instructions; Prerequisites; Building with the Makefile; Speeding up Subsequent Builds; Platforms

### Python

- **URL:** https://duckdb.org/docs/current/dev/building/python
- **Summary:** The DuckDB Python package has its own repository at duckdb/duckdb-python and uses pybind11 to create Python bindings with DuckDB. Prerequisites This guide assumes: You have a working copy of the DuckDB Python package source (including git submodules and tags) You have Astral UV version >= 0.8.0 installed You run commands from the root of the duckdb-python source We are opinionated about using…
- **Sections:** Prerequisites; 1. DuckDB Python Repository; 2. Install Astral uv; Development Environment Setup; 1. Platform-Specific Setup; 2. Install Dependencies and Build

### R

- **URL:** https://duckdb.org/docs/current/dev/building/r
- **Summary:** This page contains instructions for building the R client library. Parallelizing the Build Problem: By default, R compiles packages using a single thread, which causes the build to be slow. Solution: To parallelize the compilation, create or edit the ~/.R/Makevars file, and add a line like the following: MAKEFLAGS = -j8 The above will parallelize the compilation using 8 threads. On…
- **Sections:** Parallelizing the Build

### Raspberry Pi

- **URL:** https://duckdb.org/docs/current/dev/building/raspberry_pi
- **Summary:** DuckDB is not officially distributed for the Raspberry Pi OS (previously called Raspbian). You can build it following the instructions
- **Sections:** Raspberry Pi (64-bit); Raspberry Pi (32-bit)

### Troubleshooting

- **URL:** https://duckdb.org/docs/current/dev/building/troubleshooting
- **Summary:** This page contains solutions to common problems reported by users. If you have platform-specific issues, make sure you also consult the troubleshooting guide for your platform such as the one for Linux builds. The Build Runs Out of Memory Problem: Ninja parallelizes the build, which can cause out-of-memory issues on systems with limited resources. These issues have also been reported to occur…
- **Sections:** The Build Runs Out of Memory

### Unofficial and Unsupported Platforms

- **URL:** https://duckdb.org/docs/current/dev/building/unofficial_and_unsupported_platforms
- **Summary:** Warning The platforms listed
- **Sections:** 32-bit Architectures; Big-Endian Architectures; RISC-V Architectures; Native Build (Recommended); Build with RVV (RISC-V Vector Extension); Cross-Compilation

### Windows

- **URL:** https://duckdb.org/docs/current/dev/building/windows
- **Summary:** On Windows, DuckDB requires the Microsoft Visual C++ Redistributable package both as a build-time and runtime dependency. Note that unlike the build process on UNIX-like systems, the Windows builds directly call CMake. Visual Studio To build DuckDB on Windows, we recommend using the Visual Studio compiler. To use it, follow the instructions in the CI workflow: python scripts/windows_ci.py…
- **Sections:** Visual Studio; MSYS2 and MinGW64; Building the Go Client

### Internal Errors

- **URL:** https://duckdb.org/docs/current/dev/internal_errors
- **Summary:** Internal errors signal an assertion failure within DuckDB. They usually occur due to unexpected conditions or errors in the program's logic. For example, running issue 17002 on DuckDB v1.2.1 results in an internal error. INTERNAL Error: Attempted to access index 3 within vector of size 3 The issue is fixed in DuckDB v1.2.2 and newer versions. After encountering an internal error, DuckDB enters…

### Metrics

- **URL:** https://duckdb.org/docs/current/dev/metrics
- **Summary:** DuckDB provides a set of metrics that can be used to monitor the performance and health of the database. The query tree has two types of nodes: the QUERY_ROOT and OPERATOR nodes. The QUERY_ROOT refers exclusively to the top-level node, and the metrics it contains are measured over the entire query. The OPERATOR nodes refer to the individual operators in the query plan. Some metrics are only…
- **Sections:** All Metrics; Metric Groups; Core Metrics; Execution Metrics; File Metrics; Operator Metrics

### Profiling

- **URL:** https://duckdb.org/docs/current/dev/profiling
- **Summary:** Profiling is essential to help understand why certain queries exhibit specific performance characteristics. DuckDB contains several built-in features to enable query profiling, which this page covers. For a high-level example of using EXPLAIN, see the “Inspect Query Plans” page. Statements The EXPLAIN Statement The first step to profiling a query can include examining the query plan. The…
- **Sections:** Statements; The EXPLAIN Statement; The EXPLAIN ANALYZE Statement; The FORMAT Option; Pragmas; Table Functions

### Release Cycle

- **URL:** https://duckdb.org/docs/current/dev/release_cycle
- **Summary:** This document outlines the DuckDB and core extension release cycle framework. It is intended for developers working on DuckDB extensions to better understand the underlying processes. Overview DuckDB follows Semantic Versioning (v<MAJOR>.<MINOR>.<PATCH>) Minor versions are released approximately every 4 months Patch releases are issued as needed for: The latest stable version The current Long…
- **Sections:** Overview; Terminology; Main Branches and Tags; The Main DuckDB Release Cycle; Phase 1: Mid-Cycle; Phase 2: Pre-Release

### DuckDB Repositories

- **URL:** https://duckdb.org/docs/current/dev/repositories
- **Summary:** Several components of DuckDB are maintained in separate repositories. Main Repositories duckdb: core DuckDB project duckdb-web: documentation and blog Clients duckdb-go: Go client duckdb-java: Java (JDBC) client duckdb-node-neo: Node.js client duckdb-odbc: ODBC client duckdb-pyodide: Pyodide client duckdb-python: Python client duckdb-r: R client duckdb-rs: Rust client duckdb-swift: Swift…
- **Sections:** Main Repositories; Clients; Connectors; Extensions; Specifications

### Catch C/C++ Tests

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/catch
- **Summary:** While we prefer the sqllogic tests for testing most functionality, for certain tests only SQL is not sufficient. This typically happens when you want to test the C++ API. When using pure SQL is really not an option it might be necessary to make a C++ test using Catch. Catch tests reside in the test directory as well. Here is an example of a catch test that tests the storage of the system:…

### Debugging

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/debugging
- **Summary:** The purpose of the tests is to figure out when things break. Inevitably changes made to the system will cause one of the tests to fail, and when that happens the test needs to be debugged. First, it is always recommended to run in debug mode. This can be done by compiling the system using the command make debug. Second, it is recommended to only run the test that breaks. This can be done by…
- **Sections:** Triggering Which Tests to Run

### sqllogictest Introduction

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/intro
- **Summary:** For testing plain SQL, we use an extended version of the SQL logic test suite, adopted from SQLite. Every test is a single self-contained file located in the test/sql directory. To run tests located outside of the default test directory, specify --test-dir <root_directory> and make sure provided test file paths are relative to that root directory. The test describes a series of SQL statements,…
- **Sections:** Query Verification; Editors & Syntax Highlighting; Temporary Files; Require & Extensions

### Loops

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/loops
- **Summary:** Loops can be used in sqllogictests when it is required to execute the same query many times but with slight modifications in constant values. For example, suppose we want to fire off 100 queries that check for the presence of the values 0...100 in a table: # create the table 'integers' with values 0...100 statement ok CREATE TABLE integers AS SELECT * FROM range(0, 100, 1) t1(i); # verify…
- **Sections:** Data Generation without Loops

### Multiple Connections

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/multiple_connections
- **Summary:** For tests whose purpose is to verify that the transactional management or versioning of data works correctly, it is generally necessary to use multiple connections. For example, if we want to verify that the creation of tables is correctly transactional, we might want to start a transaction and create a table in con1, then fire a query in con2 that checks that the table is not accessible yet…
- **Sections:** Concurrent Connections

### Overview

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/overview
- **Summary:** How is DuckDB Tested? Testing is vital to make sure that DuckDB works properly and keeps working properly. For that reason, we put a large emphasis on thorough and frequent testing: We run a batch of small tests on every commit using GitHub Actions, and run a more exhaustive batch of tests on pull requests and commits in the main branch. We use a fuzzer, which automatically reports issues…
- **Sections:** How is DuckDB Tested?; Pages in This Section

### Persistent Testing

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/persistent_testing
- **Summary:** By default, all tests are run in in-memory mode (unless --force-storage is enabled). In certain cases, we want to force the usage of a persistent database. We can initiate a persistent database using the load command, and trigger a reload of the database using the restart command. # load the DB from disk load __TEST_DIR__/storage_scan.db statement ok CREATE TABLE test (a INTEGER); statement ok…

### Result Verification

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/result_verification
- **Summary:** The standard way of verifying results of queries is using the query statement, followed by the letter I times the number of columns that are expected in the result. After the query, four dashes (----) are expected followed by the result values separated by tabs. For example, query II SELECT 42, 84 UNION ALL SELECT 10, 20; ---- 42 84 10 20 For legacy reasons the letters R and T are also…
- **Sections:** NULL Values and Empty Strings; Error Verification; Regex; File; Row-Wise vs. Value-Wise Result Ordering; Hashes and Outputting Values

### Writing Tests

- **URL:** https://duckdb.org/docs/current/dev/sqllogictest/writing_tests
- **Summary:** Development and Testing It is crucial that any new features that get added have correct tests that not only test the “happy path”, but also test edge cases and incorrect usage of the feature. In this section, we describe how DuckDB tests are structured and how to make new tests for DuckDB. The tests can be run by running the unittest program located in the test folder. For the default…
- **Sections:** Development and Testing; Philosophy; Frameworks; Client Connector Tests; Functions for Generating Test Data; test_all_types Function

## Lakehouse formats (1)

### Lakehouse Formats

- **URL:** https://duckdb.org/docs/current/lakehouse_formats
- **Summary:** Lakehouse formats, often referred to as open table formats, are specifications for storing data in object storage while maintaining some guarantees such as ACID transactions or keeping snapshot history. Over time, multiple lakehouse formats have emerged, each one with its own unique approach to managing its metadata (a.k.a. catalog). In this page, we will go over the support that DuckDB offers…
- **Sections:** DuckDB Lakehouse Support Matrix

## Quack / other (8)

### Quack Remote Protocol

- **URL:** https://duckdb.org/docs/current/quack/overview
- **Summary:** We released Quack on May 12, 2026. Read the announcement blog post! The Quack extension turns a DuckDB instance into a server that other DuckDB instances (clients) can connect to over HTTP. This page covers the protocol at a glance and walks through basic usage on both sides of the wire. For the full list of functions, settings, and logging knobs, see the Reference. For configuring TLS and…
- **Sections:** Quack in a Nutshell; Server-Side Usage; Starting a Server; URI Format; Stopping a Server; Client-Side Usage

### Reference

- **URL:** https://duckdb.org/docs/current/quack/reference
- **Summary:** This page lists every function, setting, and log type exposed by the quack extension. For a tour of the protocol, start with the Overview. Function Reference Server Management Function Description quack_serve(uri, token := 'token_value', allow_other_hostname := false, disable_ssl := false) Start a server on uri. Localhost-only by default. Pass token to set the server's authentication token…
- **Sections:** Function Reference; Server Management; Client Queries; Utility; ATTACH Options; Settings

### Security

- **URL:** https://duckdb.org/docs/current/quack/security
- **Summary:** This page covers Quack's security posture end to end: what the server exposes, what stays local, the role of a TLS-terminating reverse proxy, and the authentication / authorization callbacks the server runs on every connection and every query. Exposure Model A Quack server exposes the full SQL surface of the underlying DuckDB instance, including read and write access to every table the…
- **Sections:** Exposure Model; Authentication and Authorization; Default Configuration; The Callback Contract; Authentication Hook; Authorization Hook

### Deploying Quack

- **URL:** https://duckdb.org/docs/current/quack/setup/deployment
- **Summary:** This page collects deployment recipes for running a public-facing Quack server. Today there is one recipe (AWS EC2), we will introduce more over time. On AWS EC2 The fastest way to get a public-facing Quack server is the one-click AWS CloudFormation template maintained alongside the extension. It provisions a small EC2 instance running DuckDB, the quack extension behind nginx and Let's Encrypt…
- **Sections:** On AWS EC2; One-Click Launch; Connecting from a Local DuckDB; Tearing Down; What the Stack Provisions; For Maintainers

### Quack Setup

- **URL:** https://duckdb.org/docs/current/quack/setup/overview
- **Summary:** This section contains setup guides for using the Quack Remote Protocol.
- **Sections:** Pages in This Section

### Quack on WebAssembly

- **URL:** https://duckdb.org/docs/current/quack/setup/quack_wasm
- **Summary:** CloudFormation Stack We provide an example template for initializing a CloudFormation stack, based on pre-baked public AMI, based on Ubuntu, which will: via DuckDB, install and load Quack, create a randomized token, and do quack_serve on the 0.0.0.0:1294 port. setup via nginx a proxy between 0.0.0.0:1294 and the incoming :443 port obtain a valid TLS certificate via Let's Encrypt All together,…
- **Sections:** CloudFormation Stack; Deploy via Web UI; Deploy via aws CLI; Destroy; Web UI

### Securing Quack with a Reverse Proxy

- **URL:** https://duckdb.org/docs/current/quack/setup/reverse_proxy
- **Summary:** The Quack server speaks plain HTTP only and binds to localhost by default. See Security for the rationale behind these configurations. For any deployment beyond local-only, the recommended pattern is the same as for any other HTTP-based database / application server: put a proven HTTP reverse proxy in front of it, and let the proxy terminate TLS. The Quack client cooperates with this: for…
- **Sections:** Local Test Setup with Caddy; 1. Run Caddy; 2. Start Quack and Connect Through the Proxy; Nginx + Let's Encrypt; Caddy + Let's Encrypt

### Troubleshooting Quack

- **URL:** https://duckdb.org/docs/current/quack/troubleshooting
- **Summary:** Quack is currently available as a beta release. It is not ready for production and is subject to breaking changes until the release of DuckDB v2.0. If you experience any issues with Quack, try upgrading all your DuckDB clients to the latest version of the quack extension: FORCE INSTALL quack;

