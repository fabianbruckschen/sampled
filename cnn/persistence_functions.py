

# daily persistence model
def daily_persistence(data):
    # get the total active power for the last day
    value = data[-1, 0]
    # return 7 day forecast
    return [value for _ in range(7)]


# weekly persistence model
def weekly_persistence(data, n_days=7):
    # return last n_days
    return data[-n_days:]


# week one year ago persistence model
def yearly_persistence(data):
    # get the data for the prior week
    return data[:, 0]
