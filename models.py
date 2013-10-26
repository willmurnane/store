import datetime
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class FandomHierarchy(MPTTModel):
	name = models.CharField(max_length=100)
	parent = TreeForeignKey('self', null=True, related_name='children')
	def _get_path(self):
		ancs = [x.name for x in self.get_ancestors(include_self=True)]
		return ancs
	def _get_full_name(self):
		return " &rsquo; ".join(self._get_path())
	fullName = property(_get_full_name)
	path = property(_get_path)
	def __unicode__(self):
		return "|%s%s" % (" " * self.level, self.name)

class Image(models.Model):
	name = models.CharField(max_length=100)
	fandoms = models.ManyToManyField(FandomHierarchy)
	def __unicode__(self):
		return "%s (%dx%d)" % (self.name, self.pixel_width, self.pixel_height)

class Pattern(models.Model):
	pixel_width = models.PositiveIntegerField()
	pixel_height = models.PositiveIntegerField()
	image = models.ImageField(upload_to='source_images')
	fandoms = models.ManyToManyField(FandomHierarchy)
	patternof = models.ForeignKey(Image)

class Media(models.Model):
	name = models.CharField(max_length=100)
	visible_width = models.FloatField(help_text="Inches.")
	visible_height = models.FloatField(help_text="Inches.")
	cost_cents = models.PositiveIntegerField(help_text="Amount it costs us to get one of these.")
	price_cents = models.PositiveIntegerField(help_text="Amount we will charge someone for one of these.")
	weight_oz = models.FloatField()
	exterior_width = models.FloatField()
	exterior_height = models.FloatField()
	exterior_depth = models.FloatField()
	stock_amount = models.IntegerField(help_text="Number currently in stock.")
	rotateable = models.BooleanField()
	def __unicode__(self):
		return "%s, %d in stock" % (self.name, self.stock_amount)
class RotatedMedia(Media):
	vk = models.AutoField(primary_key=True)
	orientation = models.CharField(max_length=10)
	def __unicode__(self):
		return "%s oriented %s, %d in stock" % (self.name, self.orientation, self.stock_amount)
	class Meta:
		managed = False
		db_table = 'store_rotatedmedia'

class Customer(models.Model):
	email = models.EmailField()

CART_ID = 'CART-ID'

class Cart(models.Model):
	creation_date = models.DateTimeField(verbose_name=_('creation date'))
	checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

	class Meta:
		verbose_name = _('cart')
		verbose_name_plural = _('carts')
		ordering = ('-creation_date',)

	def __unicode__(self):
		return unicode(self.creation_date)

class ItemManager(models.Manager):
	def get(self, *args, **kwargs):
		if 'product' in kwargs:
			kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
			kwargs['object_id'] = kwargs['product'].pk
			del(kwargs['product'])
		return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
	cart = models.ForeignKey(Cart, verbose_name=_('cart'))
	quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
	unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
	# product as generic relation
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()

	objects = ItemManager()

	class Meta:
		verbose_name = _('item')
		verbose_name_plural = _('items')
		ordering = ('cart',)

	def __unicode__(self):
		return '%d units of %s' % (self.quantity, self.product.__class__.__name__)

	def total_price(self):
		return self.quantity * self.unit_price
	total_price = property(total_price)

	# product
	def get_product(self):
		return self.content_type.get_object_for_this_type(pk=self.object_id)

	def set_product(self, product):
		self.content_type = ContentType.objects.get_for_model(type(product))
		self.object_id = product.pk
		print("Setting product to %s; pk=%s; content_type=%s" % (product, product.pk, self.content_type))
		print(dir(self.content_type))
		print(self.content_type.pk)
		print(self.content_type.id)
		
	product = property(get_product, set_product)

class ImageItem(models.Model):
	pattern = models.ForeignKey(Pattern)
	media = models.ForeignKey(RotatedMedia)
	extra_text = models.CharField(max_length = 100)
	special_instructions = models.TextField()
	def __unicode__(self):
		return "%s in %s" % (self.pattern, self.media)

class Order(models.Model):
	customer = models.ForeignKey(Customer)
	items = models.ManyToManyField(ImageItem)
	shippingAddress = models.TextField()
	order_date = models.DateTimeField(auto_now=True)
