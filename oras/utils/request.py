__author__ = "Vanessa Sochat"
__copyright__ = "Copyright The ORAS Authors."
__license__ = "Apache-2.0"

import os
import urllib.parse as urlparse
from urllib.parse import urlencode


def iter_localhosts(name: str):
    """
    Given a url with localhost, always resolve to 127.0.0.1.

    :param name : the name of the original host string
    :type name: str
    """
    names = [name]
    if "localhost" in name:
        names.append(name.replace("localhost", "127.0.0.1"))
    elif "127.0.0.1" in name:
        names.append(name.replace("127.0.0.1", "localhost"))
    for name in names:
        yield name


def find_docker_config():
    """
    Return the docker default config path.
    """
    path = os.path.expanduser("~/.docker/config.json")

    # Allow the caller to request the path regardless of existing
    return path if os.path.exists(path) else None


def append_url_params(url: str, params: dict) -> str:
    """
    Given a dictionary of params and a url, parse the url and add extra params.

    :param url: the url string to parse
    :type url: str
    :param params: parameters to add
    :type params: dict
    """
    parts = urlparse.urlparse(url)
    query = dict(urlparse.parse_qsl(parts.query))
    query.update(params)
    updated = list(parts)
    updated[4] = urlencode(query)
    return urlparse.urlunparse(updated)


def get_docker_client(tls_verify: bool = True, **kwargs):
    """
    Get a docker client.

    :param tls_verify : enable tls
    :type tls_verify: bool
    """
    import docker

    return docker.DockerClient(tls=tls_verify, **kwargs)
