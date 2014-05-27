import inspect
import logging

from zope.interface import implementer

from pyramid_caching.interfaces import (
    IIdentityInspector,
    IVersioner,
    )

log = logging.getLogger(__name__)


def includeme(config):
    registry = config.registry

    def identify(model_obj_or_cls):
        return registry.queryAdapter(model_obj_or_cls, IIdentityInspector)

    registry.registerAdapter(lambda x: x, required=[str],
                             provided=IIdentityInspector)

    registry.registerAdapter(lambda x: str(x), required=[unicode],
                             provided=IIdentityInspector)

    registry.registerAdapter(lambda x: str(x), required=[int],
                             provided=IIdentityInspector)

    registry.registerAdapter(lambda x: str(x), required=[float],
                             provided=IIdentityInspector)

    registry.registerAdapter(
        lambda x: TupleIdentityInspector(identify).identify(x),
        required=[tuple],
        provided=IIdentityInspector,
        )

    registry.registerAdapter(
        lambda x: DictIdentityInspector(identify).identify(x),
        required=[dict],
        provided=IIdentityInspector,
        )

    config.add_directive('get_versioner', get_versioner, action_wrap=False)
    config.add_request_method(get_versioner, 'versioner', reify=True)

    def register():
        key_versioner = config.get_key_version_client()
        versioner = Versioner(key_versioner, identify)
        config.registry.registerUtility(versioner)
        log.debug('registering versioner %r', versioner)

    config.action((__name__, 'versioner'), register, order=1)


def get_versioner(config_or_request):
    return config_or_request.registry.getUtility(IVersioner)


@implementer(IIdentityInspector)
class TupleIdentityInspector(object):

    def __init__(self, identify):
        self._identify = identify

    def identify(self, tuple_or_list):
        return ':'.join([self._identify(elem) for elem in tuple_or_list])


@implementer(IIdentityInspector)
class DictIdentityInspector(object):

    def __init__(self, identify):
        self._identify = identify

    def identify(self, dict_like):
        elems = ['%s=%s' % (self._identify(k), self._identify(v))
                 for k, v in dict_like.iteritems()]
        return ':'.join(elems)


@implementer(IVersioner)
class Versioner(object):

    def __init__(self, key_versioner, identify):
        self.key_versioner = key_versioner
        self.identify = identify

    def get_multi_keys(self, things):
        keys = [self.identify(anything) for anything in things]

        versiontuples = self.key_versioner.get_multi(keys)

        return ['%s:v=%s' % (key, version) for (key, version) in versiontuples]

    def incr(self, obj_or_cls, start=0):
        self.key_versioner.incr(self.identify(obj_or_cls))

        if not inspect.isclass(obj_or_cls):  # increment model class version
            identity = self.identify(obj_or_cls.__class__)
            self.key_versioner.incr(identity)