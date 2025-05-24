import os

USE_SCRIPT_FOR_ADDRESS = os.getenv("USE_SCRIPT_FOR_ADDRESS", "false").lower() == "true"
PREV_OUT_RESOLVED = os.getenv("PREV_OUT_RESOLVED", "false").lower() == "true"

TX_COUNT_LIMIT = int(os.getenv("TX_COUNT_LIMIT", "100_000"))
TX_SEARCH_ID_LIMIT = int(os.getenv("TX_SEARCH_ID_LIMIT", "1_000"))
TX_SEARCH_BS_LIMIT = int(os.getenv("TX_SEARCH_BS_LIMIT", "100"))
HEALTH_TOLERANCE_DOWN = int(os.getenv("HEALTH_TOLERANCE_DOWN", "300"))

NETWORK_TYPE = os.getenv("NETWORK_TYPE", "mainnet").lower()
BPS = int(os.getenv("BPS", "8"))

match NETWORK_TYPE:
    case "mainnet":
        address_prefix = "spectre"
        address_example = (
            "spectre:qrxf48dgrdkjxllxczek3uweuldtan9nanzjsavk0ak9ynwn0zsayjjh7upez"
        )
    case "testnet":
        address_prefix = "spectretest"
        address_example = (
            "spectretest:qzsmk98292592ntx360xx69pzu6w8w8w3lt3e8nycdfnx2ftjr70su4v3k8vp"
        )
    case "simnet":
        address_prefix = "spectresim"
        address_example = (
            "spectresim:qrptljf8rfhtt8x2cxjy9gyasmyf9lznx2gr3n7hk0pq5y5f8prpucy5sac7r"
        )
    case "devnet":
        address_prefix = "spectredev"
        address_example = (
            "spectredev:qze59zjua5gaswuz2wv4945nzjneg4cy7fh53t0c78swhvzpdz7s594lpfdfx"
        )
    case _:
        raise ValueError(f"Network type {NETWORK_TYPE} not supported.")

ADDRESS_PREFIX = address_prefix
ADDRESS_EXAMPLE = address_example

REGEX_SPECTRE_ADDRESS = "^" + ADDRESS_PREFIX + ":[a-z0-9]{61,63}$"
