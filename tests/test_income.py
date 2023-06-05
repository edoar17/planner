

def test_car_value():
    # Test case 1
    initial_value = 25000
    discount_rate = 0.05
    salvage_value = 5000
    years_to_use = 5
    remaining_value, discounted_value = car_value(initial_value, discount_rate, salvage_value, years_to_use)
    assert remaining_value == [20000.0, 15000.0, 10000.0, 5000.0, 0.0]
    assert discounted_value == [19047.62, 13387.55, 9151.08, 5767.54, 3359.75]

    # Test case 2
    initial_value = 10000
    discount_rate = 0.03
    salvage_value = 3000
    years_to_use = 7
    remaining_value, discounted_value = car_value(initial_value, discount_rate, salvage_value, years_to_use)
    assert remaining_value == [8571.43, 7142.86, 5714.29, 4285.71, 2857.14, 1428.57, 0.0]
    assert discounted_value == [8217.17, 6779.97, 5432.11, 4167.92, 2978.38, 1856.0, 975.88]

    # Test case 3
    initial_value = 5000
    discount_rate = 0.08
    salvage_value = 2000
    years_to_use = 3
    remaining_value, discounted_value = car_value(initial_value, discount_rate, salvage_value, years_to_use)
    assert remaining_value == [2666.6666666666665, 1333.3333333333333, 0.0]
    assert discounted_value == [2345.68, 1105.1, 0.0]

    print("All test cases pass")


def test_investments_value():
    # Test case 1
    initial_investments = 5000
    years = 5
    risk_free = 0.03
    expected_investments = {1: 5150.0, 2: 5304.5, 3: 5463.14, 4: 5626.08, 5: 5793.52}
    assert investments_value(initial_investments, years, risk_free) == expected_investments

    # Test case 2
    initial_investments = 10000
    years = 7
    risk_free = 0.05
    expected_investments = {1: 10500.0, 2: 11025.0, 3: 11576.25, 4: 12155.06, 5: 12762.81, 6: 13399.95, 7: 14067.94}
    assert investments_value(initial_investments, years, risk_free) == expected_investments

    # Test case 3
    initial_investments = 2500
    years = 3
    risk_free = 0.01
    expected_investments = {1: 2525.0, 2: 2550.25, 3: 2575.76}
    assert investments_value(initial_investments, years, risk_free) == expected_investments

    print("All test cases pass")



test_investments_value()
test_car_value()