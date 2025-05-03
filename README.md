# spectre-rest-server
REST API server for Spectre written in Python.  

The rest server is designed to operate on the database populated by the [spectre-indexer](https://github.com/spectre-project/spectre-indexer).  
The latest version of the rest server will always be live here: https://api.spectre-network.org

## Build and run
Any third party integrator which depends on the api should make sure to run their own instance.


### Environment variables

* SPECTRED_HOST1 - host:port (grpc) to a spectre node, multiple nodes is supported. (default: none)
* SQL_URI - uri to a postgres db (default: postgresql+asyncpg://127.0.0.1:5432)
* SQL_URI_BLOCKS - uri to a postgres db to query for blocks, block_parent and blocks_transactions (default: SQL_URI)
* NETWORK_TYPE - mainnet/testnet/simnet/devnet (default: mainnet)
* BPS - Blocks per second, affects block difficulty calculation (default: 1)
* DISABLE_PRICE - If true /info/price and /info/market-data is disabled (default: false)
* USE_SCRIPT_FOR_ADDRESS - If true scripts_transactions will be used for address to tx, see indexer doc (default: false)
* DISABLE_LIMITS - currently only removes the limit of max 10,000 rows for transactions/count (default: false)
* TX_SEARCH_ID_LIMIT - adjust the maximum number of transactionIds for transactions/search (default: 1000)
* TX_SEARCH_BS_LIMIT - adjust the maximum blue score range for transactions/search (default: 100)
* PREV_OUT_RESOLVED - If true, transaction input previous outpoints are resolved with details (default: false)
* HEALTH_TOLERANCE_DOWN - Tolerance in seconds for health checks to consider a node down (default: 300)
* VSPC_REQUEST - If true enables /info/get-vscp-from-block (default: false)
* DEBUG - Enables additional logging (default: false)
