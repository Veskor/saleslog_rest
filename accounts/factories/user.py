
import factory

from accounts.models import User, SALES, ADMIN

class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = factory.fuzzy.FuzzyText(prefix='name_')
    last_name = factory.fuzzy.FuzzyText(prefix='surname_')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.first_name)
    username = factory.fuzzy.FuzzyText()

    gender = factory.fuzzy.FuzzyChoice(choices=User.GENDER_CHOICES)

    user_type = 'sales'
    password = factory.fuzzy.FuzzyText()

class AdminFactory(factory.Factory):
    class Meta:
        model = User

    first_name = factory.fuzzy.FuzzyText(prefix='name_')
    last_name = factory.fuzzy.FuzzyText(prefix='surname_')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.first_name)
    username = factory.fuzzy.FuzzyText()

    gender = factory.fuzzy.FuzzyChoice(choices=User.GENDER_CHOICES)

    user_type = 'admin'
    password = factory.fuzzy.FuzzyText()
