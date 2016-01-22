from django.core.exceptions import (FieldError, MultipleObjectsReturned,
                                    ObjectDoesNotExist)
from django.db.models import QuerySet
from django.test import TestCase

from queryset_sequence import QuerySetSequence

from .models import (Article, Author, BlogPost, Book, OnlinePublisher,
                     PeriodicalPublisher, Publisher)

class TestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set-up some data to be tested against."""
        alice = Author.objects.create(name="Alice")
        bob = Author.objects.create(name="Bob")

        # Purposefully ordered such that the pks will be in the opposite order
        # than the names.
        mad_magazine = PeriodicalPublisher.objects.create(name="Mad Magazine")
        unused_publisher = Publisher.objects.create(name="Unused Publisher")
        big_books = Publisher.objects.create(name="Big Books",
                                             address="123 Street")
        wacky_website = OnlinePublisher.objects.create(name="Wacky Website")

        # Alice wrote some articles.
        Article.objects.create(title="Django Rocks", author=alice,
                               publisher=mad_magazine)
        Article.objects.create(title="Alice in Django-land", author=alice,
                               publisher=mad_magazine)

        # Bob wrote a couple of books, an article, and a blog post.
        Book.objects.create(title="Fiction", author=bob, publisher=big_books,
                            pages=10)
        Book.objects.create(title="Biography", author=bob, publisher=big_books,
                            pages=20)
        Article.objects.create(title="Some Article", author=bob,
                               publisher=mad_magazine)
        BlogPost.objects.create(title="Post", author=bob,
                                publisher=wacky_website)

        # Save the authors and publishers for later.
        cls.alice = alice
        cls.bob = bob
        cls.big_books = big_books
        cls.mad_magazine = mad_magazine
        cls.wacky_website = wacky_website

        # Many tests start with the same QuerySetSequence.
        cls.all = QuerySetSequence(Book.objects.all(), Article.objects.all())

    @classmethod
    def tearDownClass(cls):
        del cls.alice
        del cls.bob
        del cls.all

        # Clear the database.
        Author.objects.all().delete()
        Article.objects.all().delete()
        Book.objects.all().delete()


class TestLength(TestBase):
    """
    Ensure that count() and len() are properly summed over the children
    QuerySets.
    """

    def test_count(self):
        qss = self.all._clone()

        # The proper length should be returned via database queries.
        self.assertEqual(qss.count(), 5)
        self.assertIsNone(qss._result_cache)

    def test_len(self):
        qss = self.all._clone()

        # Calling len() evaluates the QuerySet.
        self.assertEqual(len(qss), 5)
        self.assertIsNotNone(qss._result_cache)

        # Count should still work (and not hit the database) by using the cache.
        qss.query = None
        self.assertEqual(qss.count(), 5)


class TestFilter(TestBase):
    def test_filter(self):
        """
        Ensure that filter() properly filters the children QuerySets, note that
        no QuerySets are actually evaluated during this.
        """
        # Filter to just Bob's work.
        bob_qss = self.all.filter(author=self.bob)
        self.assertEqual(bob_qss.count(), 3)
        self.assertIsNone(bob_qss._result_cache)

    def test_filter_by_relation(self):
        """
        Ensure that filter() properly filters the children QuerySets when using
        a related model, note that no QuerySets are actually evaluated during
        this.
        """
        # Filter to just Bob's work.
        bob_qss = self.all.filter(author__name=self.bob.name)
        self.assertEqual(bob_qss.count(), 3)
        self.assertIsNone(bob_qss._result_cache)

    def test_simplify(self):
        """
        Ensure that filter() properly filters the children QuerySets and
        simplifies to a single child QuerySet when all others become empty.
        """
        # Filter to just Alice's work.
        alice_qss = self.all.filter(author=self.alice)
        self.assertEqual(alice_qss.count(), 2)
        # TODO
        #self.assertIsNone(alice_qss._result_cache)

        # Since we've now filtered down to a single QuerySet, we shouldn't be a
        # QuerySetSequence any longer.
        self.assertIsInstance(alice_qss, QuerySet)

    def test_empty(self):
        """
        Ensure that filter() works when it results in an empty QuerySet.
        """
        # Filter to nothing.
        qss = self.all.filter(title='')
        self.assertEqual(qss.count(), 0)
        self.assertIsInstance(qss, QuerySetSequence)

        # This should not throw an exception.
        data = list(qss)
        self.assertEqual(len(data), 0)


class TestExclude(TestBase):
    """
    Note that this is the same test as TestFilter, but we exclude the other
    author instead of filtering.
    """

    def test_exclude(self):
        """
        Ensure that exclude() properly filters the children QuerySets, note that
        no QuerySets are actually evaluated during this.
        """
        # Filter to just Bob's work.
        bob_qss = self.all.exclude(author=self.alice)
        self.assertEqual(bob_qss.count(), 3)
        self.assertIsNone(bob_qss._result_cache)

    def test_exclude_by_relation(self):
        """
        Ensure that exclude() properly filters the children QuerySets when using
        a related model, note that no QuerySets are actually evaluated during
        this.
        """
        # Filter to just Bob's work.
        bob_qss = self.all.exclude(author__name=self.alice.name)
        self.assertEqual(bob_qss.count(), 3)
        self.assertIsNone(bob_qss._result_cache)

    def test_simplify(self):
        """
        Ensure that filter() properly filters the children QuerySets and
        simplifies to a single child QuerySet when all others become empty.
        """
        # Filter to just Alice's work.
        alice_qss = self.all.exclude(author=self.bob)
        self.assertEqual(alice_qss.count(), 2)
        # TODO
        #self.assertIsNone(alice_qss._result_cache)

        # Since we've now filtered down to a single QuerySet, we shouldn't be a
        # QuerySetSequence any longer.
        self.assertIsInstance(alice_qss, QuerySet)

    def test_empty(self):
        """
        Ensure that filter() works when it results in an empty QuerySet.
        """
        # Filter to nothing.
        qss = self.all.exclude(author__in=[self.alice, self.bob])
        self.assertEqual(qss.count(), 0)
        self.assertIsInstance(qss, QuerySetSequence)

        # This should not throw an exception.
        data = list(qss)
        self.assertEqual(len(data), 0)


class TestGet(TestBase):
    def test_get(self):
        """
        Ensure that get() returns the expected element or raises DoesNotExist.
        """
        # Get a particular item.
        book = self.all.get(title='Biography')
        self.assertEqual(book.title, 'Biography')
        self.assertIsInstance(book, Book)

        # An exception is rasied if get() is called and nothing is found.
        self.assertRaises(ObjectDoesNotExist, self.all.get, title='')

        # ...or if get() is called and multiple objects are found.
        self.assertRaises(MultipleObjectsReturned, self.all.get, author=self.bob)


class TestOrderBy(TestBase):
    def test_order_by(self):
        """Ensure that order_by() propagates to QuerySets and iteration."""
        # Order by author and ensure it takes.
        qss = self.all.order_by('title')
        self.assertEqual(qss.query.order_by, ['title'])

        # Check the titles are properly ordered.
        data = map(lambda it: it.title, qss)
        self.assertEqual(data[0], 'Alice in Django-land')
        self.assertEqual(data[1], 'Biography')
        self.assertEqual(data[2], 'Django Rocks')
        self.assertEqual(data[3], 'Fiction')
        self.assertEqual(data[4], 'Some Article')

    def test_order_by_non_existent_field(self):
        qss = self.all.order_by('pages')
        self.assertEqual(qss.query.order_by, ['pages'])
        self.assertRaises(FieldError, list, qss)

    def test_order_by_multi(self):
        """Test ordering by multiple fields."""
        # Add another object with the same title, but a later release date.
        fiction2 = Book.objects.create(title="Fiction", author=self.alice,
                                       publisher=self.big_books, pages=1)

        qss = self.all.order_by('title', '-release')
        self.assertEqual(qss.query.order_by, ['title', '-release'])

        # Check the titles are properly ordered.
        data = map(lambda it: it.title, qss)
        self.assertEqual(data[0], 'Alice in Django-land')
        self.assertEqual(data[1], 'Biography')
        self.assertEqual(data[2], 'Django Rocks')
        self.assertEqual(data[3], 'Fiction')
        self.assertEqual(data[4], 'Fiction')
        self.assertEqual(data[5], 'Some Article')

        # Ensure the ordering is correct.
        self.assertLess(qss[4].release, qss[3].release)
        self.assertEqual(qss[3].author, self.alice)
        self.assertEqual(qss[4].author, self.bob)

        # Clean-up this test.
        fiction2.delete()

    def test_order_by_relation(self):
        """
        Apply order_by() with a field that is a relation to another model's id.
        """
        # Order by author and ensure it takes.
        qss = self.all.order_by('author_id')
        self.assertEqual(qss.query.order_by, ['author_id'])

        # The first two should be Alice, followed by three from Bob.
        for expected, element in zip([self.alice] * 2 + [self.bob] * 3, qss):
            self.assertEqual(element.author, expected)

    def test_order_by_relation_pk(self):
        """
        Apply order_by() with a field that returns a model without a default
        ordering (i.e. using the pk).
        """
        # Order by publisher and ensure it takes.
        qss = self.all.order_by('publisher')
        self.assertEqual(qss.query.order_by, ['publisher'])

        # Ensure that the test has any hope of passing.
        self.assertLess(self.mad_magazine.pk, self.big_books.pk)

        # The first three should be from Mad Magazine, followed by three from
        # Big Books.
        for expected, element in zip([self.mad_magazine] * 3 + [self.big_books] * 2, qss):
            self.assertEqual(element.publisher, expected)

    def test_order_by_relation_with_ordering(self):
        """
        Apply order_by() with a field that returns a model with a default
        ordering.
        """
        # Order by author and ensure it takes.
        qss = self.all.order_by('author')
        self.assertEqual(qss.query.order_by, ['author'])

        # The first two should be Alice, followed by three from Bob.
        for expected, element in zip([self.alice] * 2 + [self.bob] * 3, qss):
            self.assertEqual(element.author, expected)

    def test_order_by_relation_with_different_ordering(self):
        """
        Apply order_by() with a field that returns a model with different
        ordering on sub-QuerySets.
        """
        # Both of these have publishers with the same fields, but different
        # ordering.
        all = QuerySetSequence(Article.objects.all(), BlogPost.objects.all())

        # Order by publisher and ensure it takes.
        qss = all.order_by('publisher')
        self.assertEqual(qss.query.order_by, ['publisher'])

        self.assertRaises(FieldError, list, qss)

    def test_order_by_relation_field(self):
        """Apply order_by() with a field through a model relationship."""
        # Order by author name and ensure it takes.
        qss = self.all.order_by('author__name')
        self.assertEqual(qss.query.order_by, ['author__name'])

        # The first two should be Alice, followed by three from Bob.
        for expected, element in zip([self.alice] * 2 + [self.bob] * 3, qss):
            self.assertEqual(element.author, expected)

    def test_order_by_relation_no_existent_field(self):
        """Apply order_by() with a field through a model relationship."""
        qss = self.all.order_by('publisher__address')
        self.assertEqual(qss.query.order_by, ['publisher__address'])
        self.assertRaises(FieldError, list, qss)


class TestSlicing(TestBase):
    """Test indexing and slicing."""

    def test_single_element(self):
        """Single element."""
        qss = self.all._clone()
        result = qss[0]
        self.assertEqual(result.title, 'Fiction')
        self.assertIsInstance(result, Book)
        # qss never gets evaluated since the underlying QuerySet is used.
        self.assertIsNone(qss._result_cache)

    def test_one_QuerySet(self):
        """Test slicing only from one QuerySet."""
        qss = self.all._clone()
        result = qss[0:2]
        self.assertIsInstance(result, QuerySet)
        # qss never gets evaluated since the underlying QuerySet is used.
        self.assertIsNone(qss._result_cache)
        # Check the data.
        for element in result:
            self.assertIsInstance(element, Book)

    def test_multiple_QuerySets(self):
        """Test slicing across elements from multiple QuerySets."""
        qss = self.all._clone()
        result = qss[1:3]
        self.assertIsInstance(result, QuerySetSequence)
        data = list(result)
        # Requesting the data above causes it to be cached.
        self.assertIsNotNone(result._result_cache)
        self.assertIsInstance(data[0], Book)
        self.assertIsInstance(data[1], Article)
        self.assertEqual(len(data), 2)

    def test_multiple_slices(self):
        """Test multiple slices taken."""
        qss = self.all._clone()
        result = qss[1:3]
        self.assertIsInstance(result, QuerySetSequence)
        article = result[1]
        # Still haven't evaluated the QuerySetSequence!
        self.assertIsNone(result._result_cache)
        self.assertEqual(article.title, 'Django Rocks')

    def test_step(self):
        """Test behavior when a step is provided to the slice."""
        qss = self.all._clone()
        result = qss[0:4:2]
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    def test_all(self):
        """Test slicing to all elements."""
        qss = self.all._clone()
        qss = qss[:]
        self.assertIsInstance(qss, QuerySetSequence)

        # No data evaluated.
        self.assertIsNone(qss._result_cache)
        self.assertEqual(qss.count(), 5)

    def test_slicing_order_by(self):
        """Test slicing when order_by has already been called."""
        # Order by author and ensure it takes.
        qss = self.all.order_by('title')
        self.assertEqual(qss.query.order_by, ['title'])

        # Take a slice.
        qss = qss[1:3]
        self.assertIsInstance(qss, QuerySetSequence)
        # No data yet.
        self.assertIsNone(qss._result_cache)
        data = map(lambda it: it.title, qss)
        self.assertEqual(data[0], 'Biography')
        self.assertEqual(data[1], 'Django Rocks')


class TestIterating(TestBase):
    def test_iterating(self):
        """By default iteration just chains the iterables together."""
        qss = self.all._clone()

        # There are two books and three articles.
        for expected, element in zip([Book] * 2 + [Article] * 3, qss):
            self.assertIsInstance(element, expected)