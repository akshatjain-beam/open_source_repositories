```
        for date in date_range(
            self.start_date, self.end_date + datetime.timedelta(days=365), "yearly"
        ):
            end_date = datetime.date(date.year, 12, 31)
```