import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        # it is better to store the dates as date objects instead of hard-coded formatted strings
        # the default value should be None, i.e.:
        # def __init__(self, amount, comment, date=None)
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # class names are indeed written in PascalCase, but class instances should be in camel_case
        # so the for loop should be:
        # for record in self.records
        for Record in self.records:
            if Record.date == dt.datetime.now().date(): # same here, Record.date should be record.date
                today_stats = today_stats + Record.amount # it would be slightly more elegant to use the += operator
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Gets the remaining calories for today
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'You can eat something else today,' \
                   f' but with a total calorie content of no more than {x} kcal'
        else: # no need for an else statement here, just return
            return('Stop eating!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # US dollar exchange rate.
    EURO_RATE = float(70)  # Euro exchange rate.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        """
        You could define a dictionary
        CURRENCY_RATES = {
            'usd': (USD_RATE, 'USD'),
            'eur': (EURO_RATE, 'Euro'),
            'rub': (1, 'rub'),
        }
        Then do
        rate, currency_type = CURRENCY_RATES.get(currency)
        cash_remained /= rate
        It is more pythonic and if in the future you want to handle another
        currency, you just have to add it to the dictionary instead of
        adding another elif statement.
        You might also want to implement some sort of error handling in case
        the currency passed is not handled yet (i.e. british pounds).
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            # The == does not make sense here, I think you meant /=
            # it does not matter though, if you use the currency_rates dictionary
            # described above
            currency_type = 'rub'
        if cash_remained > 0:
            return (
                f'Left for today {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'No money, keep it up!'
        elif cash_remained < 0:
            return 'No money, keep it up:' \
                   ' your debt is - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
        """
        The output messages are fine but they do not correspond to what is
        asked for, you can check them here:
        https://praktikum.notion.site/Practicum-Task-8cf8ff1312024e079c5ed6795bf7eb9a
        For example, when cash_remained == 0 you should print
        'There is no money, stay strong' instead of 'No money, keep it up!'.
        """

    def get_week_stats(self):
        super().get_week_stats()
