"""
Script to validate images being submitted for transformation.
"""

from .errors import ConfigError, ITSLoaderError
from .loaders import BaseLoader
from .settings import NAMESPACES


def loader(namespace, filename):

    """
    Loads image using the IMAGE_LOADER specified in settings.
    """
    image = None

    loader_classes = BaseLoader.__subclasses__()

    if namespace in NAMESPACES:
        loader_parameters = NAMESPACES[namespace]
        loader_slug = loader_parameters["loader"]

        image_loader = [
            loader for loader in loader_classes if loader.slug == loader_slug
        ]

        if len(image_loader) == 1:
            if filename.endswith(".svg"):
                image = image_loader[0].get_fileobj(namespace, filename)
            else:
                image = image_loader[0].load_image(namespace, filename)
        elif not image_loader:
            raise ITSLoaderError("No Image Loader with slug '%s' found." % loader_slug)
        elif len(image_loader) > 1:
            raise ConfigError("Two or more Image Loaders have slug '%s'." % loader_slug)
    else:
        raise ConfigError("No Backend for namespace '%s'." % namespace)

    return image
