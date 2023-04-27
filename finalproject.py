accounts = {"testuser": ["Asdfg1234$", 0.0]}
user = ""

# This function is O(n) with n being the length of the password as it iterates over the password multiple times throughout the algorithm
def validatePassword(username, password):
  sName = username

  sPassword = password

  sInitials = ""

  for word in sName.split():
    sInitials += word[0]

  checkCount = 0

  if len(sPassword) < 8 or len(sPassword) > 12:
    print("Password must be between 8 and 12 characters.")
  else:
    checkCount += 1
   
  if sPassword.lower().startswith(("Pass", "pass")):
    print("Password can’t start with Pass.")
  else:
    checkCount += 1

  flag = False
  for char in sPassword:
    if char.isupper() == True:
      flag = True
      checkCount += 1
      break
  if (flag == False):
    print("Password must contain at least 1 uppercase letter.")

  flag = False
  for char in sPassword:
    if char.islower() == True:
      flag = True
      checkCount += 1
      break
  if (flag == False):
    print("Password must contain at least 1 lowercase letter.")

  flag = False
  for char in sPassword:
    if char.isdigit() == True:
      flag = True
      checkCount += 1
      break
  if (flag == False):
    print("Password must contain atleast 1 number.")

  sSpecialCharacters = "!@#$%^"
  flag = False
  for char in sPassword:
    if char in sSpecialCharacters:
      flag = True
      checkCount += 1
      break
  if (flag == False):
    print("Password must contain at least 1 of these special characters: ! @ # $ % ^")

  # Use a list to generate the visisted characters to see if the password is unique
  sPasswordList = []
  # Use a dictionary to view the duplicates
  sDuplicates = {}
  uniqueFlag = True

  for char in sPassword:
    if char.lower() in sPasswordList:
      sDuplicates[char.lower()] += 1
      uniqueFlag = False
    else:
      sDuplicates[char.lower()] = 1
      sPasswordList.append(char.lower())

  if(uniqueFlag == False):
    print("These characters appear more than once: ")
    for letter in sDuplicates.keys():
      if(sDuplicates[letter] > 1):
        print(f"{letter}: {sDuplicates[letter]} times")
  else:
    checkCount += 1

  if (checkCount == 7):
    return True
  else:
    return False


print("Welcome to The Bank! Would you like to sign in or create an account?")
while (True):
  try:
    createOrSignIn = int(input("1. Create an account\n2. Sign in\nEnter your choice: "))

    if(createOrSignIn == 1):
      user = input("Please enter a username: ")
      password = input("Please enter a password: ")

      print("---------------------------")
      if(user in accounts):
        print("This username is already taken! Please try again. ")
      if(not validatePassword(user, password)):
        print("Password is invalid, please try again!")
      else:
        accounts[user] = [password, 0.0]
        print("You have successfully created an account! Redirecting to main page.")
    elif(createOrSignIn == 2):
      user = input("Please enter your username: ")
      password = input("Please enter your password: ")

      print("---------------------------")
      if(user in accounts and password == accounts[user][0]):
        print(f"Welcome back {user}!")
        break
      else:
        print("Your username/password may be incorrect, please try again!")
    else:
      print("Please enter a valid option!")
  except:
    print("Please enter a valid option!")
  print("---------------------------")

while (True):
  try:
    question = int(
      input(
        "What would you like to do today?\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\nEnter your choice: "
      ))

    print("---------------------------")

    if(question == 1):
      print(f"Your current balance: {accounts[user][1]}!")
    elif(question == 2):
      try:
        amount = float(input("How much would you like to deposit? "))
        userAccount = accounts[user]
        userAccount[1] += amount
        accounts[user] = userAccount
        print(f"Your new balance is: {accounts[user][1]}")
      except:
        print("Please enter a number!")
    elif(question == 3):
      try:
        amount = float(input("How much would you like to withdraw? "))
        userAccount = accounts[user]
        if(amount > userAccount[1]):
          print("Amount exceeds balance!")
        else:
          userAccount[1] -= amount
          accounts[user] = userAccount
          print(f"Your new balance is: {accounts[user][1]}")
      except:
        print("Please enter a number!")
    elif(question == 4):
      print("Thank you for visiting The Bank! Take care!")
      break
    else:
      print("Please enter a valid option!")
  except:
    print("Please enter a valid option!")
  print("---------------------------")