import csv
import json
import os
from datetime import datetime


employees = []

def load_data_from_csv(file_path):
    global employees
    if not os.path.exists(file_path):
        print("File not found.")
        return

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            employees.append({
                'id': int(row['id']),
                'name': row['name'],
                'position': row['position'],
                'salary': int(row['salary']),
                'skills': set(row['skills'].split(',')),
                'employment_date': row['employment_date']
            })



# Save data to JSON file
def save_data_to_json(file_path):
    with open(file_path, 'w') as file:
        json.dump(employees, file, default=list, indent=4)
    print(f"Data saved to {file_path}.")


# Save data to CSV file
def save_data_to_csv(file_path):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['id', 'name', 'position', 'salary', 'skills', 'employment_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow({
                'id': emp['id'],
                'name': emp['name'],
                'position': emp['position'],
                'salary': emp['salary'],
                'skills': ','.join(emp['skills']),
                'employment_date': emp['employment_date']
            })
    print(f"Data exported to {file_path}.")


# Add employee
def add_employee():
    try:
        emp_id = int(input("Enter employee ID: "))
        if any(emp['id'] == emp_id for emp in employees):
            print("ID already exists.")
            return
        name = input("Enter full name: ")
        position = input("Enter position: ")
        salary = int(input("Enter salary: "))
        skills = set(input("Enter skills (comma-separated): ").split(','))
        employment_date = input("Enter employment date (YYYY-MM-DD): ")
        datetime.strptime(employment_date, "%Y-%m-%d")  # Validate date

        employees.append({
            'id': emp_id,
            'name': name,
            'position': position,
            'salary': salary,
            'skills': skills,
            'employment_date': employment_date
        })
        print("Employee added successfully.")
    except ValueError:
        print("Invalid input. Please try again.")


# Search employee
def search_employee():
    criteria = input("Search by (id/name/skills): ").lower()
    query = input("Enter search term: ").lower()

    matches = [emp for emp in employees if
               (criteria == 'id' and str(emp['id']) == query) or
               (criteria == 'name' and query in emp['name'].lower()) or
               (criteria == 'skills' and any(skill.lower() in emp['skills'] for skill in query.split(',')))]

    if matches:
        for emp in matches:
            print(emp)
    else:
        print("No matches found.")


# Update employee
def update_employee():
    emp_id = int(input("Enter employee ID to update: "))
    for emp in employees:
        if emp['id'] == emp_id:
            emp['salary'] = int(input("Enter new salary: "))
            new_skills = set(input("Enter skills to add (comma-separated): ").split(','))
            emp['skills'].update(new_skills)
            print("Employee updated successfully.")
            return
    print("Employee not found.")


# Display all employees
def display_employees():
    filter_by = input("Filter by position or skills (leave blank for all): ").lower()
    sort_by = input("Sort by salary or employment_date: ").lower()
    reverse = input("Sort descending? (yes/no): ").lower() == 'yes'

    filtered = [emp for emp in employees if
                not filter_by or filter_by in emp['position'].lower() or filter_by in emp['skills']]
    sorted_employees = sorted(filtered,
                              key=lambda x: x[sort_by] if sort_by in ['salary', 'employment_date'] else x['id'],
                              reverse=reverse)

    for emp in sorted_employees:
        print(emp)


# Analytics
def generate_analytics():
    total_payroll = sum(emp['salary'] for emp in employees)
    average_salary = total_payroll // len(employees)
    highest_salary = max(employees, key=lambda x: x['salary'])
    lowest_salary = min(employees, key=lambda x: x['salary'])

    print(f"Total Payroll: {total_payroll}")
    print(f"Average Salary: {average_salary}")
    print(f"Highest Salary: {highest_salary['salary']} - {highest_salary['name']}")
    print(f"Lowest Salary: {lowest_salary['salary']} - {lowest_salary['name']}")


# Delete file
def delete_file():
    file_path = input("Enter file path to delete: ")
    if os.path.exists(file_path):
        os.remove(file_path)
        print("File deleted.")
    else:
        print("File not found.")


# Main menu
def main():
    while True:
        load_data_from_csv('employees.csv')
        print("Welcome to the Advanced Employee Management System!\nMenu:")
        print("1. Add Employee\n2. Search Employee\n3. Update Employee\n4. Display Employees\n5. Generate Analytics\n6. Save to JSON\n7. Export to CSV\n8. Delete File\n9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            search_employee()
        elif choice == '3':
            update_employee()
        elif choice == '4':
            display_employees()
        elif choice == '5':
            generate_analytics()
        elif choice == '6':
            save_data_to_json('employees.json')
        elif choice == '7':
            save_data_to_csv('employees.csv')
        elif choice == '8':
            delete_file()
        elif choice == '9':
            print("Thank you for using our system")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
