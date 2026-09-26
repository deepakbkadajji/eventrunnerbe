import logging

from botocore.exceptions import BotoCoreError, ClientError
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

logger = logging.getLogger(__name__)


class LoggingS3Mixin:
    """Log S3 storage failures with context and re-raise."""

    def _storage_extra(self, operation, name):
        return {
            'operation': operation,
            'storage_class': self.__class__.__name__,
            'object_name': name,
            'location': getattr(self, 'location', ''),
        }

    def _log_storage_failure(self, operation, name, exc):
        if isinstance(exc, ClientError):
            error_code = exc.response.get('Error', {}).get('Code', 'unknown')
            logger.error(
                "S3 %s failed code=%s",
                operation,
                error_code,
                extra=self._storage_extra(operation, name),
            )
            return

        logger.exception(
            "S3 %s failed",
            operation,
            extra=self._storage_extra(operation, name),
        )

    def _save(self, name, content):
        try:
            return super()._save(name, content)
        except (ClientError, BotoCoreError, OSError) as exc:
            self._log_storage_failure('save', name, exc)
            raise

    def _open(self, name, mode='rb'):
        try:
            return super()._open(name, mode)
        except (ClientError, BotoCoreError, OSError) as exc:
            self._log_storage_failure('open', name, exc)
            raise

    def delete(self, name):
        try:
            return super().delete(name)
        except (ClientError, BotoCoreError, OSError) as exc:
            self._log_storage_failure('delete', name, exc)
            raise

    def exists(self, name):
        try:
            return super().exists(name)
        except (ClientError, BotoCoreError, OSError) as exc:
            self._log_storage_failure('exists', name, exc)
            raise

    def size(self, name):
        try:
            return super().size(name)
        except (ClientError, BotoCoreError, OSError) as exc:
            self._log_storage_failure('size', name, exc)
            raise

    def url(self, name, parameters=None, expire=None):
        try:
            return super().url(name, parameters=parameters, expire=expire)
        except (ClientError, BotoCoreError, OSError) as exc:
            self._log_storage_failure('url', name, exc)
            raise


class StaticStorage(LoggingS3Mixin, S3Boto3Storage):
    """Used to manage static files for the web server."""

    location = settings.STATIC_LOCATION
    default_acl = settings.STATIC_DEFAULT_ACL


class PublicMediaStorage(LoggingS3Mixin, S3Boto3Storage):
    """Used to store and serve dynamic media files with no access expiration."""

    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = settings.PUBLIC_MEDIA_DEFAULT_ACL
    file_overwrite = False


class PrivateMediaStorage(LoggingS3Mixin, S3Boto3Storage):
    """
    Used to store and serve dynamic media files using access keys
    and short-lived expirations to ensure more privacy control.
    """

    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = settings.PRIVATE_MEDIA_DEFAULT_ACL
    file_overwrite = False
    custom_domain = False
