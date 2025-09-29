from dataclasses import dataclass

from pyiceberg.catalog import load_catalog

@dataclass
class S3TableConfig:
    type: str
    warehouse: str
    uri: str
    rest_sigv4_enabled: str = "true"
    rest_signing_name: str = "s3tables"
    rest_signing_region: str = "ap-northeast-2"
    
    def to_catalog_config(self) -> dict:
        return {
            "type": self.type,
            "warehouse": self.warehouse,
            "uri": self.uri,
            "rest.sigv4-enabled": self.rest_sigv4_enabled,
            "rest.signing-name": self.rest_signing_name,
            "rest.signing-region": self.rest_signing_region,
        }

class S3TableCatalog:
    def __init__(self, catalog_name: str, config: S3TableConfig):
        self.catalog = load_catalog(
            catalog_name,
            **config.to_catalog_config()
        )
        
    def __getattr__(self, name: str):
        return getattr(self.catalog, name)