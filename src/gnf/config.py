"""Settings for the GNodeFactory, readable from environment and/or from env files."""

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import SecretStr


DEFAULT_ENV_FILE = ".env"


class FastAPISettings(BaseModel):
    port: int = 8000


class DjangoSettings(BaseModel):
    """Django settings"""

    secret_key: str = "ai#6hnzekef0l^8f4x$uq*4j4im+hdcax0v^lxca4^#ozgnc+j"


class RabbitBrokerClient(BaseModel):
    """Settings for connecting to an Rabbit Broker"""

    url: SecretStr = SecretStr("amqp://smqPublic:smqPublic@localhost:5672/dev_registry")


class Algo(BaseModel):
    """This class is the publicly available information about the GNodeFactory"""

    algod_address: str = "http://localhost:4001"
    algod_token: SecretStr = SecretStr(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    kmd_address: str = "http://localhost:4002"
    kmd_token: SecretStr = SecretStr(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    gen_kmd_wallet_name: str = "unencrypted-default-wallet"
    gen_kmd_wallet_password: SecretStr = SecretStr("")
    universe: str = "dev"
    gnf_g_node_alias: str = "dwgps.gnf"
    gnf_admin_addr: str = "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI"
    gnf_graveyard_addr: str = (
        "COA6SYUOBE33F5JDYEGC5XAD43QRG3VGHNNQXLYWFSSQEHDQ5HJ52NDNPI"
    )
    gnf_validator_funding_threshold_algos: int = 100
    ta_deed_consideration_algos: int = 50
    gnf_api_root: str = "0.0.0.0:8000"


class SandboxDemo(BaseModel):
    molly_metermaid_addr: str = (
        "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII"
    )
    holly_homeowner_addr: str = (
        "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI"
    )
    holly_ta_daemon_addr: str = (
        "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA"
    )
    gnr_addr: str = "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU"
    initial_holly_ta_alias: str = "d1.isone.ver.keene.holly.ta"
    holly_daemon_port: str = "8001"


class HollyTaDaemonSettings(BaseSettings):
    sk: SecretStr = SecretStr(
        "tQ8ABbLLR96cnRE3Y2tlrj2d/rNPRFkf8FosJ46tVIlub0lPIBPqkJ4yknqibTR4kTV1+ncKT324feI6iSD2bw=="
    )


class AdaDiscovererSettings(BaseSettings):
    sk: SecretStr = SecretStr(
        "X20eXB/VZilEmzaPCDSn9WsuGZ5/f0+IxuEhfYfVtmZR9q5bcbjpBodPpiUCCkr0Xv11sKYxf08PnAKQFNtW3Q=="
    )
    discovered_ctn_alias = "d1.isone.ver.keene.pwrs"
    original_child_alias_list = ["d1.isone.ver.keene.holly"]
    micro_lat = 44838681
    micro_lon = -68705311


class GnfSettings(BaseSettings):
    """Settings for the gNodeFactory."""

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
    algo: Algo = Algo()
    rabbit: RabbitBrokerClient = RabbitBrokerClient()
    django: DjangoSettings = DjangoSettings()

    class Config:
        env_prefix = "GNF_"
        env_nested_delimiter = "__"


#### Below is just for stubbing out a dev Validator account that does
# not have access to Gnf secrets


class MollyMetermaidSettings(BaseSettings):
    algo: Algo = Algo()
    acct_sk: SecretStr = SecretStr(
        "FCLmrvflibLD6Deu3NNiUQCC9LOWpXLsbMR/cP2oJzH8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBg=="
    )
    validator_cert_name: str = "Molly Metermaid"
    validator_name: str = "Molly Inc Telemetry Surveyors and Purveyors"
    validator_web_page: str = "http://localhost:5000/mollyco/who-we-are/"

    class Config:
        env_prefix = "MM_"
        env_nested_delimiter = "__"


class HollyHomeownerSettings(BaseSettings):
    algo: Algo = Algo()
    sk: SecretStr = SecretStr(
        "sp4SDWmH8Rin0IhPJQq1UMsSR5C0j1IGqzLdcwCMySBVzT8lEUwjwwpS9z6l6dKSg52WWEjRdJDAL+eVt4kvBg=="
    )

    class Config:
        env_prefix = "HH_"
        env_nested_delimiter = "__"


class DevGNodeRegistrySettings(BaseSettings):
    g_node_alias: str = "dwgps.gnr"
    g_node_instance_id: str = "4bab8ea7-e2f4-48fa-be52-51897ffee5ab"
    sk: SecretStr = SecretStr(
        "JDIoOhXNIu8zx3eILJElCfAFopbsq6w8IUCCt9ZrRShjmyG3rLm5ViHHS0SUhqCRvnJmEhEQpIHkfVHcpoyBrw=="
    )
    log_level = "WARNING"
    algo: Algo = Algo()
    rabbit: RabbitBrokerClient = RabbitBrokerClient()

    class Config:
        env_prefix = "GNR_"
        env_nested_delimiter = "__"
