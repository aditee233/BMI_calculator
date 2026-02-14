def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

print("===== BMI Calculator =====")

try:
    height = float(input("Enter your height (cm): "))
    weight = float(input("Enter your weight (kg): "))

    bmi = calculate_bmi(weight, height)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    print(f"\nYour BMI is: {bmi}")
    print(f"Category: {category}")

except:
    print("Please enter valid numbers.")
