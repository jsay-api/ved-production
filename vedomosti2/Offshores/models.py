# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.encoding import smart_text
from django.utils.text import slugify
from unidecode import unidecode
import uuid

class Asset(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4 and max_length = 32
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	asset_name = models.CharField(verbose_name = "название актива", max_length = 100, unique=True)
	asset_link = models.CharField(verbose_name = "ссылка", max_length = 200, blank = True)
	slug = models.SlugField(unique = True, allow_unicode = True, max_length = 200)

	class Meta:
		verbose_name = "актив"
		verbose_name_plural = "активы"

	def save(self, *args):
		self.slug = slugify(self.asset_name+'-'+str(self.uuid))
		super(Asset, self).save(*args)

	def __unicode__(self):
		return self.asset_name

	def __str__(self):
		return self.asset_name

	def get_absolute_url(self):
		return reverse('asset', kwargs = {"slug": self.slug})


class Beneficiary(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	ben_name = models.CharField(verbose_name = "имя", max_length = 50)
	ben_lastname = models.CharField(verbose_name = "фамилия", max_length = 100)
	ben_midname = models.CharField(verbose_name = "отчество", max_length = 30, blank = True)
	ben_holding = models.CharField(verbose_name = "холдинговая компания бенефициара", max_length = 70, blank = True)
	ben_link = models.CharField(verbose_name = "ссылка", max_length = 200, blank = True)
	slug = models.SlugField(unique = True, allow_unicode = True, max_length = 200)

	class Meta:
		unique_together = ('ben_name', 'ben_lastname', 'ben_midname',)
		ordering = ['ben_lastname', 'ben_name']
		verbose_name = "бенефициар"
		verbose_name_plural = "бенефициары"

	def save(self, *args):
		self.slug = slugify(self.ben_name+'-'+self.ben_lastname+'-'+str(self.uuid))
		super(Beneficiary, self).save(*args)
	
	def clean(self):
		self.ben_name = self.ben_name.capitalize()
		self.ben_lastname = self.ben_lastname.capitalize()

	def __unicode__(self):
		return u'%s %s' % (self.ben_name, self.ben_lastname)

	def __str__(self):
		return u'%s %s' % (self.ben_name, self.ben_lastname)

	def get_absolute_url(self):
		return reverse('beneficiary', kwargs = {"slug": self.slug})



class Offshore(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	off_name = models.CharField(verbose_name = "название офшора", max_length = 50, unique=True)
	off_jurisdiction = models.CharField(verbose_name = "юрисдикция офшора", max_length = 50, blank = True)
	file = models.FileField(upload_to = "offshores/", blank = True, null = True)
	image = models.ImageField(upload_to = "offshores/", blank = True, null = True)
	off_parent = models.CharField(verbose_name = "материнский офшор", max_length = 50, blank = True)
	off_link = models.URLField(verbose_name = "ссылка", max_length = 300, blank = True)
	slug = models.SlugField(unique = True, allow_unicode = True, max_length = 200)
	

	class Meta:
		verbose_name = "офшор"
		verbose_name_plural = "офшоры"
		ordering = ["off_name"]

	def clean(self):
		self.off_name = self.off_name.title()

	def save(self, *args):
		self.slug = slugify(self.off_name+'-'+str(self.uuid))
		super(Offshore, self).save(*args)

	def __unicode__(self):
		return self.off_name

	def __str__(self):
		return self.off_name

	def image_thumb(self):
		return '<img src="/media/%s" width="100" height="100" />' % (self.image)
	image_thumb.allow_tags = True

	def get_absolute_url(self):
		return reverse('offshore', kwargs = {"slug": self.slug})

# def create_slug(instance, new_slug = None):
# 	slug = slugify(instance.off_name)
# 	if new_slug is not None:
# 		slug = new_slug
# 	qs = Offshore.objects.filter(slug = slug).order_by("-id")
# 	exists = qs.exists()
# 	if exists:
# 		new_slug = "%s-%s" % (slug, qs.first().id)
# 		return create_slug(instance, new_slug = new_slug)
# 	return slug


# def pre_save_off_receiver(sender, instance, *args, **kwargs):
# 	if not instance.slug:
# 		instance.slug = create_slug(instance)


# pre_save.connect(pre_save_off_receiver, sender = Offshore)

	
class AssetsBeneficiaries(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	beneficiary = models.ForeignKey(Beneficiary,verbose_name = "бенефициар", on_delete = models.SET(""))
	asset = models.ForeignKey(Asset, verbose_name = "актив", on_delete = models.SET(""))
	share = models.DecimalField(verbose_name = "доля бенефициара в активе, %", max_digits = 6, decimal_places = 4, blank = True, default = 0.0)
	rel_date = models.DateField(verbose_name = "дата актуальности", null = True, blank = True)
	source = models.CharField(verbose_name = "источник", max_length = 150, blank = True)
	link = models.CharField(verbose_name = "ссылка", max_length = 200, blank = True)

	class Meta:
		verbose_name = "Бенефициар-Актив"
		verbose_name_plural = "Бенефициры-Активы"
		ordering = ["beneficiary__ben_lastname"]

	def __unicode__(self):
		return "связь"

	def __str__(self):
		return "связь"

	def get_absolute_url(self):
		return reverse('detail', kwargs = {"slug": self.slug})


class BeneficiariesOffshores(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	beneficiary = models.ForeignKey(Beneficiary, verbose_name = "бенефициар", on_delete = models.SET(""))
	offshore = models.ForeignKey(Offshore, verbose_name = "офшор", on_delete = models.SET(""))
	share = models.DecimalField(verbose_name = "доля бенефициара в офшоре, %", max_digits = 7, decimal_places = 4, blank = True, default = 0.0)
	rel_date = models.DateField(verbose_name = "дата актуальности", blank = True, null = True)
	source = models.CharField(verbose_name = "источник", max_length = 150, blank = True)
	link = models.CharField(verbose_name = "ссылка", max_length = 200, blank = True)

	class Meta:
		verbose_name = "Офшор-Бенефициар"
		verbose_name_plural = "Офшоры-Бенефициары"
		ordering = ["offshore"]

	def __unicode__(self):
		return "связь"

	def __str__(self):
		return "связь"

	def get_absolute_url(self):
		return reverse('detail', kwargs = {"id": self.id})



class OffshoresAssets(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	offshore = models.ForeignKey(Offshore, verbose_name = "офшор", on_delete = models.SET(""))
	asset = models.ForeignKey(Asset, verbose_name = "актив", on_delete = models.SET(""))
	share = models.DecimalField(verbose_name = "доля офшора в активе, %", max_digits = 6, decimal_places = 4, blank = True, default = 0.0)
	rel_date = models.DateField(verbose_name = "дата актуальности", blank = True, null = True)
	source = models.CharField(verbose_name = "источник", max_length = 150, blank = True)
	link = models.CharField(verbose_name = "ссылка", max_length = 200, blank = True)

	class Meta:
		verbose_name = "Офшор-Актив"
		verbose_name_plural = "Офшоры-Активы"
		ordering = ["offshore"]

	def __unicode__(self):
		return "связь"

	def __str__(self):
		return "связь"

	def get_absolute_url(self):
		return reverse('detail', kwargs = {"slug": self.slug})


class Links(models.Model):
	#FIXME: when DEBUG == False: add to uuid default=uuid.uuid4
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	link = models.CharField(verbose_name = "ссылка", max_length = 200)
	link_name = models.CharField(verbose_name = "название ресурса", max_length = 150)
	link_login = models.CharField(verbose_name = "логин для ресурса", max_length = 50)
	link_pass = models.CharField(verbose_name = "пароль для ресурса", max_length = 50)
	link_dscr = models.TextField(verbose_name = "примечания")

	class Meta:
		verbose_name = "Ресурс"
		verbose_name_plural = "Ресурсы"
		ordering = ["link_name"]

	def __unicode__(self):
		return self.link_name

	def __str__(self):
		return self.link_name



