from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.IntegerField(default=0)
    product_name=models.CharField(max_length=100)
    Disc=models.CharField(max_length=400) #Discription
    pub_date=models.DateField() # Published date of product
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    Disc=models.CharField(max_length=400,default="") #Discription
    phone=models.CharField(max_length=70,default="") # Published date of product
    email=models.CharField(max_length=50,default="")
    
    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key= True)
    Items_list = models.CharField(max_length= 5000)
    amount = models.IntegerField(default=0)
    name= models.CharField(max_length=100)
    email= models.CharField(max_length= 100)
    phone = models.CharField(max_length= 50)
    address = models.CharField(max_length= 100)
    city= models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zipcode= models.CharField(max_length=20)

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key= True)
    order_id = models.IntegerField(default="")
    update_disc = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_disc[0:10] + "..."

class Login(models.Model):
   username = models.CharField(max_length = 50)
   password = models.CharField(max_length=100)

   class Meta:
      db_table = "login"

   def __str__(self):
        return self.username