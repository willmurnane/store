from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class FandomHierarchy(MPTTModel):
	name = models.CharField(max_length=100)
	parent = TreeForeignKey('self', null=True, related_name='children')
	def __unicode__(self):
		return "|%s%s" % (" " * self.level, self.name)
	
class Image(models.Model):
	pixel_width = models.IntegerField()
	pixel_height = models.IntegerField()
	name = models.CharField(max_length=100)
	fandoms = models.ManyToManyField(FandomHierarchy)
	image = models.ImageField(upload_to='source_images')
	def __unicode__(self):
		return "%s (%dx%d)" % (self.name, self.pixel_width, self.pixel_height)
	
class Media(models.Model):
	name = models.CharField(max_length=100)
	visible_width = models.FloatField(help_text="Inches.")
	visible_height = models.FloatField(help_text="Inches.")
	cost_cents = models.IntegerField(help_text="Amount it costs us to get one of these.")
	price_cents = models.IntegerField(help_text="Amount we will charge someone for one of these.")
	weight_oz = models.FloatField()
	exterior_width = models.FloatField()
	exterior_height = models.FloatField()
	exterior_depth = models.FloatField()
	stock_amount = models.IntegerField(help_text="Number currently in stock.")
	def __unicode__(self):
		return "%s, %d in stock" % (self.name, self.stock_amount)
