```
        for date in date_range(self.start_date, self.end_date.replace(year=self.end_date.year + 1), step=1, date_format="%Y"):
            end_date = datetime.date(date.year, 12, 31)
```