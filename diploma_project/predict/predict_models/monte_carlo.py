def monte_carlo(func, param):
    resultsClosePrice = []
    resultsMeanPrice = []

    for index in range(0, 100):
        closingPrices, mean_end_price = func(param)
        resultsClosePrice.append(closingPrices)
        resultsMeanPrice.append(mean_end_price)