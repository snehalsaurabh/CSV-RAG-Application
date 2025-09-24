from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Generate new hashes for our users
demo_hash = pwd_context.hash('demo')
admin_hash = pwd_context.hash('demo')  
reviewer_hash = pwd_context.hash('demo')

print('Update your USERS_DB with these hashes:')
print(f'\"demo\": \"{demo_hash}\",')
print(f'\"admin\": \"{admin_hash}\",') 
print(f'\"reviewer\": \"{reviewer_hash}\"')

