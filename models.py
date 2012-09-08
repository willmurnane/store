from django.db import models

class FandomHierarchy(models.Model):
	name = models.CharField(max_length=100)
	parent = models.ForeignKey('self')
	
class Image(models.Model):
	pixel_width = models.IntegerField()
	pixel_height = models.IntegerField()
	name = models.CharField(max_length=100)
	fandoms = models.ManyToManyField(FandomHierarchy)
	image = models.ImageField(upload_to='source_images')
	
class Media(models.Model):
	visible_width = models.FloatField()
	visible_height = models.FloatField()
	cost_cents = models.IntegerField()
	price_cents = models.IntegerField()
	weight_oz = models.FloatField()
	exterior_width = models.FloatField()
	exterior_height = models.FloatField()
	exterior_depth = models.FloatField()
	stock_amount = models.IntegerField()
