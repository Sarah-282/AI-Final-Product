name = input("Enter your name: ")
email = input("Enter your email: ")
password = input("Enter your password: ")

with open("user_data.txt", "a", encoding="utf-8") as file:
	file.write(f"Name: {name}, Email: {email}, Password: {password}\n")

print("User data saved.")

# Security analysis:
# The password is stored in plain text without encryption or hashing.
# Anyone who can open user_data.txt can read the password.
# In a real application, passwords should be salted and hashed with a
# password-hashing algorithm such as Argon2 or bcrypt. Sensitive data should
# also be protected with appropriate access controls and encryption at rest.

 
