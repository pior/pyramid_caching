Changelog
=========


TODO
----

* DOCUMENTATION.
* Introspectables
* Content negociation: we should add content type in cache key.

Development
-----------

* Fix invalid Graphite metric names (replace periods/colon with underscore)

0.2.3
-----

* New release to fix packaging issue

0.2.2
-----

* Add the HTTP scheme to the cache key (mostly for generated links in response)

0.2.1
-----

* Bypass cache when an error occurs while getting the cache key version or the
  cached data.

0.2.0
-----

* ext.sqlalchemy: Increment new and deleted entities and table identities.
* Simple dependency resolution for location-aware resources.
* ext.royal: New extension for caching pyramid_royal resources.
* Allow key identity generators to define resources that don't need to be
  invalidated.

0.1.2
-----

* Breaking changes: ``cache_factory`` keyword arguments ``depends_on`` is a
  list of callables which receiving request as positional argument. Callables
  return the dependency to be identified by cache manager.
* Add arguments ``predicates`` to ``cache_factory`` which permits to add
  predicates to cache key used for the view (useful for query strings).

0.1.1
-----

* Switch back to d2to1.

0.1
---

* First draft of interfaces
* Add a highly not efficient implementation of a key versioner
* Add a model versioner which depends on key versioner and model identity
  inspector
* Add an example application with dummy sqla model to run tests against
* Add an sqla specific extention with hook on session events to get model
  modifications.
* Add and remove `cache_basic` decorator to cache basic function with primitive
  typed argument. Let's focus at view level. We'll do basic decoraor later.
* Add `cache_factory` to construct a decorator to pass to `config.add_view`
  method.
* Add a cache manager which plug all components.
* Add serializers to adapt objects to store on cache. Serializer objects follow
  a standard `loads`/`dumps` interface.
* Add Redis client for caching and versioning
* Implement master-version in redis version-store
* The cache manager emits CacheHit and CacheMiss events. These events can be
  forwarded to a statistics aggregator by using the pyramid_metrics extension.
* Sets the reponse ETag and custom X-View-Cache HTTP headers based on the
  versioned key of the resource.
