from django.db import models
import re
import bcrypt

# Create your models here.
class Usermanager(models.Manager):
    def registervalidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['email']) <1:
            errors['email'] = "You must enter email"
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = ("Invalid email address!")
        else:
            emailtaken = User.objects.filter(email = postData['email'])
            if len(emailtaken)>0:
                errors['emailtaken'] = "email is taken. use a different email"
        if len(postData['password']) <3:
            errors['password'] = "You must enter password of at lease 3 characters"
        if postData['password'] != postData['confirm_password']:
            errors['passwordconfirm'] = "password doesnt match"
        return errors

    def loginvalidator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['emaillength'] = "you must enter an email"
        userinDB = User.objects.filter(email = postData['email'])
        if len(userinDB) == 0:
            errors['emailnotregistered'] = "this email aint reged"
      
        else:  
            print(userinDB)
            userinDB = userinDB[0]
            print(userinDB)
            if bcrypt.checkpw(postData['password'].encode(), userinDB.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['passwordwrong'] = "incorrect password"
        print (errors)
        return errors
class Quotemanager(models.Manager):
    def quotevalidator(self, postData):
        errors = {}
        if len(postData['quoter'])<1:
            errors['quoteshort'] = "You must enter a valid Quoter name"
        if len(postData['quotetxt'])<4:
            errors['quotelen'] = "You must enter a longer quote"
        return errors

class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Usermanager()
class Quote(models.Model):
    quoted = models.CharField(max_length=255)
    quotetxt = models.TextField()
    favorite = models.ManyToManyField(User, related_name = 'favoritelist')
    creator = models.ForeignKey(User, related_name = 'quoteCreator', on_delete = models.CASCADE, default = None, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Quotemanager()
