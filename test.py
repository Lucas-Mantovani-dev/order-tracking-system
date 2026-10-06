import bcrypt

password = b"lucas"

wp = b"Lucas"


salt = bcrypt.gensalt()
hpw = bcrypt.hashpw(password, salt)

print(password, hpw)

if bcrypt.checkpw(password, hpw):
    print("cool")
else:
    print("not cool")
