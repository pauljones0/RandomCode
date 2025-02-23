def calculate_future_value(pv, rate, periods):
    """
    Calculate the future value given a present value, interest rate, and number of periods.
    
    Parameters:
        pv (float): The present value.
        rate (float): The interest rate per period (in decimal form, e.g., 0.05 for 5%).
        periods (int): The number of periods.
    
    Returns:
        float: The future value.
    """
    return pv * (1 + rate) ** periods

def calculate_present_value(fv, rate, periods):
    """
    Calculate the present value given a future value, interest rate, and number of periods.
    
    Parameters:
        fv (float): The future value.
        rate (float): The interest rate per period (in decimal form).
        periods (int): The number of periods.
    
    Returns:
        float: The present value.
    """
    return fv / ((1 + rate) ** periods)

def calculate_annuity_payment(principal, rate, periods):
    """
    Calculate the annuity payment for a given principal, interest rate, and number of periods.
    
    The formula used is:
        Payment = principal * [rate*(1+rate)^periods] / [(1+rate)^periods - 1]
    
    For a zero interest rate, the payment is simply principal/periods.
    
    Parameters:
        principal (float): The amount to be annuitized.
        rate (float): The interest rate per period (in decimal form).
        periods (int): The number of periods.
    
    Returns:
        float: The annuity payment.
    """
    if rate == 0:
        return principal / periods
    return principal * (rate * (1 + rate) ** periods) / (((1 + rate) ** periods) - 1)

def main():
    print("Financial Calculator")
    print("--------------------")
    print("1: Calculate Future Value (Financial Value)")
    print("2: Calculate Present Value")
    print("3: Calculate Annuity Payment")
    
    try:
        choice = int(input("Enter your choice (1, 2, or 3): "))
    except ValueError:
        print("Invalid input. Please enter a number (1, 2, or 3).")
        return

    if choice == 1:
        try:
            pv = float(input("Enter the present value: "))
            rate = float(input("Enter the interest rate (as a decimal, e.g., 0.05 for 5%): "))
            periods = int(input("Enter the number of periods: "))
            if periods < 0:
                raise ValueError("Number of periods cannot be negative.")
            fv = calculate_future_value(pv, rate, periods)
            print(f"Future Value: {fv:.2f}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
    elif choice == 2:
        try:
            fv = float(input("Enter the future value: "))
            rate = float(input("Enter the interest rate (as a decimal, e.g., 0.05 for 5%): "))
            periods = int(input("Enter the number of periods: "))
            if periods < 0:
                raise ValueError("Number of periods cannot be negative.")
            pv = calculate_present_value(fv, rate, periods)
            print(f"Present Value: {pv:.2f}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
    elif choice == 3:
        try:
            principal = float(input("Enter the principal amount: "))
            rate = float(input("Enter the interest rate (as a decimal, e.g., 0.05 for 5%): "))
            periods = int(input("Enter the number of periods: "))
            if periods <= 0:
                raise ValueError("Number of periods must be greater than zero.")
            annuity_payment = calculate_annuity_payment(principal, rate, periods)
            print(f"Annuity Payment: {annuity_payment:.2f}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
    else:
        print("Invalid choice. Please run the program again and select 1, 2, or 3.")

if __name__ == "__main__":
    main()
