from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=254, unique=True)
    currency = models.CharField(max_length=800)

    def __str__(self):
        return self.country_name

class Zone(models.Model):
    zone_name = models.CharField(max_length=254, unique=True)
    zone_describe = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.zone_name

class State(models.Model):
    state_name = models.CharField(max_length=254, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    gst_code = models.CharField(max_length=2)

    def __str__(self):
        return self.state_name

class City(models.Model):
    city_name = models.CharField(max_length=254, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name

class Pincode(models.Model):
    pincode_no = models.IntegerField(default=421301,unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zoneid=models.IntegerField(null=True,default="1")

    def __str__(self):
        return str(self.pincode_no)