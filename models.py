from django.db import models

class FandomHierarchy(models.Model):
	name = models.CharField(max_length=100)
	parent = models.ForeignKey('self')
	def __unicode__(self):
		return "Fandom tree node %s" % self.name
	
class Image(models.Model):
	pixel_width = models.IntegerField()
	pixel_height = models.IntegerField()
	name = models.CharField(max_length=100)
	fandoms = models.ManyToManyField(FandomHierarchy)
	image = models.ImageField(upload_to='source_images')
	def __unicode__(self):
		return "Image instance %s (%dx%d)" % (self.name, self.pixel_width, self.pixel_height)
	
class Media(models.Model):
	name = models.CharField(max_length=100)
	visible_width = models.FloatField()
	visible_height = models.FloatField()
	cost_cents = models.IntegerField()
	price_cents = models.IntegerField()
	weight_oz = models.FloatField()
	exterior_width = models.FloatField()
	exterior_height = models.FloatField()
	exterior_depth = models.FloatField()
	stock_amount = models.IntegerField()
	def __unicode__(self):
		return "Media instance %s, %d in stock" % (self.name, self.stock_amount)
