from __future__ import absolute_import
import inspect

from zope.interface import implementer

from pyramid_caching.interfaces import IIdentityInspector

from sqlalchemy import event


def includeme(config):

    config.add_directive('register_sqla_session_caching_hook',
                         register_sqla_session_caching_hook)

    config.add_directive('register_sqla_base_class',
                         register_sqla_base_class)

    identity_inspector = SqlAlchemyIdentityInspector()

    config.registry.registerUtility(identity_inspector)


def register_sqla_base_class(config, base_cls):
    registry = config.registry

    identity_inspector = registry.getUtility(IIdentityInspector)

    def identify(model):
        return identity_inspector.identify(model)

    registry.registerAdapter(identify, required=[base_cls],
                             provided=IIdentityInspector)

    registry.registerAdapter(identify, required=[base_cls.__class__],
                             provided=IIdentityInspector)


def register_sqla_session_caching_hook(config, session_cls):
    model_versioner = config.get_model_versioner()

    def on_before_commit(session):
        dirty = session.dirty

        def incr_models(session):
            # XXX: should increment only cacheable models
            for model in dirty:
                model_versioner.incr(model)

        if dirty:
            event.listen(session_cls, 'after_commit', incr_models)

    event.listen(session_cls, 'before_commit', on_before_commit)


@implementer(IIdentityInspector)
class SqlAlchemyIdentityInspector(object):

    def identify(self, obj_or_cls):
        tablename = obj_or_cls.__tablename__

        if inspect.isclass(obj_or_cls):
            return tablename

        # with a table user_message with a composite primary key user_id and id
        # an object user_message(user_id=123, id=456) will give:
        # 'user_message:user_id=123:id=456'

        # TODO: if table has no primary keys :-/

        table = obj_or_cls.__table__
        ids = ':'.join(['%s=%s' % (col_name, getattr(obj_or_cls, col_name))
                        for col_name in table.primary_key.columns.keys()])

        return '%s:%s' % (obj_or_cls.__tablename__, ids)