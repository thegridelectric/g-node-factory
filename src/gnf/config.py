"""Settings for the GNodeFactory, readable from environment and/or from env files."""

from gridworks.gw_config import AlgoApiSecrets
from gridworks.gw_config import Public
from gridworks.gw_config import VanillaSettings
from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import SecretStr


DEFAULT_ENV_FILE = ".env"


class GnfSettings(BaseSettings):
    """Settings for the gNodeFactory."""

    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: Public = Public()
    g_node_alias: str = "dwgps.gnf"
    g_node_id: str = "ba1bd498-8bed-4a80-aa61-aa91e5f7d532"
    g_node_instance_id: str = "9fc843f3-ba36-46cc-990e-f45d3c02c210"
    log_level: str = "WARNING"
    admin_acct_sk: SecretStr = SecretStr(
        "qUGjVDcxVa0TfV8IeL8ZG9FFROh/GzLaWS6Ie05jrHiLWHNvVZoPMX7bXlxHzGaJF9RAyueOoe1BXk+IUEBS2Q=="
    )
    graveyard_acct_sk: SecretStr = SecretStr(
        "6UKcDTGYg7sU41D3si+VKBQSd5w46Z4mjVkahRfLIQETgelijgk3svUjwQwu3APm4RNupjtbC68WLKUCHHDp0w=="
    )
    # rabbit_url: SecretStr = SecretStr("amqp://smqPublic:smqPublic@localhost:5672/d1__1")
    rabbit_url: SecretStr = SecretStr(
        "amqp://smqPublic:smqPublic@d1-1.electricity.works:5672/d1__1"
    )
    rabbit_mqtt_port: int = 1885
    django_secret_key: SecretStr = SecretStr(
        "ai#6hnzekef0l^8f4x$uq*4j4im+hdcax0v^lxca4^#ozgnc+j"
    )

    class Config:
        env_prefix = "GNF_"
        env_nested_delimiter = "__"


class GnrSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: Public = Public()
    sk: SecretStr = SecretStr(
        "RvfbAEdn2ADe0pF7984ioBuLTnd+t46cITzcEbE5v2i+gSoCj1dQJhh3hmCgvlexErCDilQ1O9tKs7SYTXjadQ=="
    )

    class Config:
        env_prefix = "GNR_"
        env_nested_delimiter = "__"
