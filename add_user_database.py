from email_validator import validate_email, EmailNotValidError
from data_manager import DataManager

print("Welcome to Raul's Flight Club.")
print("We find the best flight deals and email you.")
fname = input("What is your first name?\n")
lname = input("What is your last name?\n")

def check_email(email):
    """Function to validate an email, returns true/false"""
    try:
      # validate and get info
        v = validate_email(email)
        # replace with normalized form
        #email = v["email"]
        result = True
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        result = False
    return result

correct_email = False
valid_email = False
while not correct_email or not valid_email:
    email = input("What is your email?\n")
    if input("Type your email again as confirmation:\n") == email:
        correct_email = True
        valid_email = check_email(email)
    else:
        print ("Entries did not match. Please confirm your email correctly:\n")
users = DataManager()
users.update_emails(fname, lname, email)
