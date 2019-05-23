from core.cloud import CloudProvider

from .s3 import S3Provider


CloudProvider.register_provider('S3', S3Provider)
