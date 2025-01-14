API Reference
=============

Much of the ``QuerySet`` API is implemented by ``QuerySetSequence``, but it is
not fully compatible.

.. |check| unicode:: U+2713
.. |xmark| unicode:: U+2717

Summary of Supported APIs
-------------------------

.. list-table:: Methods that return new ``QuerySets``
    :widths: 15 10 30
    :header-rows: 1

    * - Method
      - Implemented?
      - Notes

    * - |filter|_
      - |check|
      - See [1]_ for information on the ``QuerySet`` lookup: ``'#'``.
    * - |exclude|_
      - |check|
      - See [1]_ for information on the ``QuerySet`` lookup: ``'#'``.
    * - |annotate|_
      - |check|
      -
    * - |alias|_
      - |xmark|
      -
    * - |order_by|_
      - |check|
      - Does not support random ordering (e.g. ``order_by('?')``). See [1]_ for
        information on the ``QuerySet`` lookup: ``'#'``.
    * - |reverse|_
      - |check|
      -
    * - |distinct|_
      - |check|
      - Does not support calling ``distinct()`` if there are multiple underlying
        ``QuerySet`` instances of the same model.
    * - |values|_
      - |check|
      - See [1]_ for information on including the ``QuerySet`` index: ``'#'``.
    * - |values_list|_
      - |check|
      - See [1]_ for information on including the ``QuerySet`` index: ``'#'``.
    * - |dates|_
      - |xmark|
      -
    * - |datetimes|_
      - |xmark|
      -
    * - |none|_
      - |check|
      -
    * - |all|_
      - |check|
      -
    * - |union|_
      - |xmark|
      -
    * - |intersection|_
      - |xmark|
      -
    * - |difference|_
      - |xmark|
      -
    * - |select_related|_
      - |check|
      -
    * - |prefetch_related|_
      - |check|
      -
    * - |extra|_
      - |check|
      -
    * - |defer|_
      - |check|
      -
    * - |only|_
      - |check|
      -
    * - |using|_
      - |check|
      -
    * - |select_for_update|_
      - |xmark|
      -
    * - |raw|_
      - |xmark|
      -

.. list-table:: Operators that return new ``QuerySets``
    :widths: 15 10 30
    :header-rows: 1

    * - Operator
      - Implemented?
      - Notes

    * - |AND (&)|_
      - |check|
      - A ``QuerySetSequence`` can be combined with a ``QuerySet``. The
        ``QuerySets`` in the ``QuerySetSequence`` are filtered to ones matching
        the same ``Model``. Each of those is ANDed with the other ``QuerySet``.
    * - |OR (\|)|_
      - |check|
      - A ``QuerySetSequence`` can be combined with a ``QuerySet`` or
        ``QuerySetSequence``. When combining with a ``QuerySet``, it is added to
        the ``QuerySetSequence``. Combiningg with another ``QuerySetSequence``
        adds together the two underlying sets of ``QuerySets``.

.. list-table:: Methods that do not return ``QuerySets``
    :widths: 15 10 30
    :header-rows: 1

    * - Method
      - Implemented?
      - Notes

    * - |get|_
      - |check|
      - See [1]_ for information on the ``QuerySet`` lookup: ``'#'``.
    * - |create|_
      - |xmark|
      - Cannot be implemented in ``QuerySetSequence``.
    * - |get_or_create|_
      - |xmark|
      - Cannot be implemented in ``QuerySetSequence``.
    * - |update_or_create|_
      - |xmark|
      - Cannot be implemented in ``QuerySetSequence``.
    * - |bulk_create|_
      - |xmark|
      - Cannot be implemented in ``QuerySetSequence``.
    * - |bulk_update|_
      - |xmark|
      - Cannot be implemented in ``QuerySetSequence``.
    * - |count|_
      - |check|
      -
    * - |in_bulk|_
      - |xmark|
      - Cannot be implemented in ``QuerySetSequence``.
    * - |iterator|_
      - |check|
      -
    * - |latest|_
      - |check|
      - If no fields are given, ``get_latest_by`` on each model is required to
        be identical.
    * - |earliest|_
      - |check|
      - See the docuemntation for ``latest()``.
    * - |first|_
      - |check|
      - If no ordering is set this is essentially the same as calling
        ``first()`` on the first ``QuerySet``, if there is an ordering, the
        result of ``first()`` for each ``QuerySet`` is compared and the "first"
        value is returned.
    * - |last|_
      - |check|
      - See the documentation for ``first()``.
    * - |aggregate|_
      - |xmark|
      -
    * - |exists|_
      - |check|
      -
    * - |contains|_
      - |check|
      -
    * - |update|_
      - |check|
      -
    * - |delete|_
      - |check|
      -
    * - |as_manager|_
      - |check|
      -
    * - |explain|_
      - |check|
      -

.. list-table:: Additional methods specific to ``QuerySetSequence``
    :widths: 15 30
    :header-rows: 1

    * - Method
      - Notes

    * - |get_querysets|
      - Returns the list of ``QuerySet`` objects that comprise the sequence.
        Note, if any methods have been called which modify the
        ``QuerySetSequence``, the ``QuerySet`` objects returned by this
        method will be similarly modified. The order of the ``QuerySet``
        objects within the list is not guaranteed.

.. |filter| replace:: ``filter()``
.. _filter: https://docs.djangoproject.com/en/dev/ref/models/querysets/#filter
.. |exclude| replace:: ``exclude()``
.. _exclude: https://docs.djangoproject.com/en/dev/ref/models/querysets/#exclude
.. |annotate| replace:: ``annotate()``
.. _annotate: https://docs.djangoproject.com/en/dev/ref/models/querysets/#annotate
.. |alias| replace:: ``alias()``
.. _alias: https://docs.djangoproject.com/en/dev/ref/models/querysets/#alias
.. |order_by| replace:: ``order_by()``
.. _order_by: https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
.. |reverse| replace:: ``reverse()``
.. _reverse: https://docs.djangoproject.com/en/dev/ref/models/querysets/#reverse
.. |distinct| replace:: ``distinct()``
.. _distinct: https://docs.djangoproject.com/en/dev/ref/models/querysets/#distinct
.. |values| replace:: ``values()``
.. _values: https://docs.djangoproject.com/en/dev/ref/models/querysets/#values
.. |values_list| replace:: ``values_list()``
.. _values_list: https://docs.djangoproject.com/en/dev/ref/models/querysets/#values-list
.. |dates| replace:: ``dates()``
.. _dates: https://docs.djangoproject.com/en/dev/ref/models/querysets/#dates
.. |datetimes| replace:: ``datetimes()``
.. _datetimes: https://docs.djangoproject.com/en/dev/ref/models/querysets/#datetimes
.. |none| replace:: ``none()``
.. _none: https://docs.djangoproject.com/en/dev/ref/models/querysets/#none
.. |all| replace:: ``all()``
.. _all: https://docs.djangoproject.com/en/dev/ref/models/querysets/#all
.. |union| replace:: ``union()``
.. _union: https://docs.djangoproject.com/en/dev/ref/models/querysets/#union
.. |intersection| replace:: ``intersection()``
.. _intersection: https://docs.djangoproject.com/en/dev/ref/models/querysets/#intersection
.. |difference| replace:: ``difference()``
.. _difference: https://docs.djangoproject.com/en/dev/ref/models/querysets/#difference
.. |select_related| replace:: ``select_related()``
.. _select_related: https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related
.. |prefetch_related| replace:: ``prefetch_related()``
.. _prefetch_related: https://docs.djangoproject.com/en/dev/ref/models/querysets/#prefetch-related
.. |extra| replace:: ``extra()``
.. _extra: https://docs.djangoproject.com/en/dev/ref/models/querysets/#extra
.. |defer| replace:: ``defer()``
.. _defer: https://docs.djangoproject.com/en/dev/ref/models/querysets/#defer
.. |only| replace:: ``only()``
.. _only: https://docs.djangoproject.com/en/dev/ref/models/querysets/#only
.. |using| replace:: ``using()``
.. _using: https://docs.djangoproject.com/en/dev/ref/models/querysets/#using
.. |select_for_update| replace:: ``select_for_update()``
.. _select_for_update: https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-for-update
.. |raw| replace:: ``raw()``
.. _raw: https://docs.djangoproject.com/en/dev/ref/models/querysets/#raw

.. |AND (&)| replace:: AND (``&``)
.. _AND (&): https://docs.djangoproject.com/en/dev/ref/models/querysets/#and
.. |OR (|)| replace:: OR (``|``)
.. _OR (\|): https://docs.djangoproject.com/en/dev/ref/models/querysets/#or

.. |get| replace:: ``get()``
.. _get: https://docs.djangoproject.com/en/dev/ref/models/querysets/#get
.. |create| replace:: ``create()``
.. _create: https://docs.djangoproject.com/en/dev/ref/models/querysets/#create
.. |get_or_create| replace:: ``get_or_create()``
.. _get_or_create: https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create
.. |update_or_create| replace:: ``update_or_create()``
.. _update_or_create: https://docs.djangoproject.com/en/dev/ref/models/querysets/#update-or-create
.. |bulk_create| replace:: ``bulk_create()``
.. _bulk_create: https://docs.djangoproject.com/en/dev/ref/models/querysets/#bulk-create
.. |bulk_update| replace:: ``bulk_update()``
.. _bulk_update: https://docs.djangoproject.com/en/dev/ref/models/querysets/#bulk-update
.. |count| replace:: ``count()``
.. _count: https://docs.djangoproject.com/en/dev/ref/models/querysets/#count
.. |in_bulk| replace:: ``in_bulk()``
.. _in_bulk: https://docs.djangoproject.com/en/dev/ref/models/querysets/#in_bulk
.. |iterator| replace:: ``iterator()``
.. _iterator: https://docs.djangoproject.com/en/dev/ref/models/querysets/#iterator
.. |latest| replace:: ``latest()``
.. _latest: https://docs.djangoproject.com/en/dev/ref/models/querysets/#latest
.. |earliest| replace:: ``earliest()``
.. _earliest: https://docs.djangoproject.com/en/dev/ref/models/querysets/#earliest
.. |first| replace:: ``first()``
.. _first: https://docs.djangoproject.com/en/dev/ref/models/querysets/#first
.. |last| replace:: ``last()``
.. _last: https://docs.djangoproject.com/en/dev/ref/models/querysets/#last
.. |aggregate| replace:: ``aggregate()``
.. _aggregate: https://docs.djangoproject.com/en/dev/ref/models/querysets/#aggregate
.. |exists| replace:: ``exists()``
.. _exists: https://docs.djangoproject.com/en/dev/ref/models/querysets/#exists
.. |contains| replace:: ``contains()``
.. _contains: https://docs.djangoproject.com/en/dev/ref/models/querysets/#contains
.. |update| replace:: ``update()``
.. _update: https://docs.djangoproject.com/en/dev/ref/models/querysets/#update
.. |delete| replace:: ``delete()``
.. _delete: https://docs.djangoproject.com/en/dev/ref/models/querysets/#delete
.. |as_manager| replace:: ``as_manager()``
.. _as_manager: https://docs.djangoproject.com/en/dev/ref/models/querysets/#as-manager
.. |explain| replace:: ``explain()``
.. _explain: https://docs.djangoproject.com/en/dev/ref/models/querysets/#explain

.. |get_querysets| replace:: ``get_querysets()``

.. [1]  ``QuerySetSequence`` supports a special field lookup that looks up the
        index of the ``QuerySet``, this is represented by ``'#'``. This can be
        used in any of the operations that normally take field lookups (i.e.
        ``filter()``, ``exclude()``, and ``get()``), as well as ``order_by()``
        and ``values()``.

        A few examples are below:

        .. code-block:: python

            # Order first by QuerySet, then by the value of the 'title' field.
            QuerySetSequence(...).order_by('#', 'title')

            # Filter out the first QuerySet.
            QuerySetSequence(...).filter(**{'#__gt': 0})

        .. note::

            Ordering first by ``QuerySet`` allows for a more optimized code path
            when iterating over the entries.

        .. warning::

            Not all lookups are supported when using ``'#'`` (some lookups
            simply don't make sense; others are just not supported). The
            following are allowed:

            * ``exact``
            * ``iexact``
            * ``contains``
            * ``icontains``
            * ``in``
            * ``gt``
            * ``gte``
            * ``lt``
            * ``lte``
            * ``startswith``
            * ``istartswith``
            * ``endswith``
            * ``iendswith``
            * ``range``
