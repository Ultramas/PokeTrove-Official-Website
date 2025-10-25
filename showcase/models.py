import os
import uuid
from datetime import timedelta, time, datetime
import requests
from django.forms import DecimalField
from django.db.models.signals import m2m_changed
from django.utils import timezone
from uuid import uuid4
from decimal import Decimal, getcontext, ROUND_DOWN
import json
from PIL import Image
from django.utils.text import slugify
from decimal import Decimal
from colorfield.fields import ColorField
import logging
import math
from autoslug import AutoSlugField
from autoslug.utils import generate_unique_slug
from django.db.models.signals import post_save, post_delete, pre_delete
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser, Permission
from django.db import models, transaction
from django.db.models import Max, F, Count, Sum, ExpressionWrapper
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils.timezone import now, make_aware
import pytz
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from pydantic import ValidationError
from django.contrib.auth.models import Group
from django.db import connection
from decimal import ROUND_UP
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.base import ContentFile
import random
import string
from random import randint


CATEGORY_CHOICES = (
    ('G', 'Gold'),
    ('P', 'Platinum'),
    ('E', 'Emerald'),
    ('D', 'Diamond'),
)

SPECIAL_CHOICES = (
    ('F', 'Featured'),
    ('N', 'New'),
    ('P', 'Popular'),
    ('PR', 'Premium'),
    ('LE', 'Limited Edition'),
)

CONDITION_CHOICES = (
    ('M', 'Mint'),
    ('NM', 'Near Mint'),
    ('MP', 'Moderately Played'),
    ('HP', 'Heavily Played'),
    ('D', 'Damaged'),
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('BS', 'Best Seller'),
    ('BV', 'Best Value'),
)

SHUFFLE_CHOICES = (
    ('L', 'Luck'),
    ('S', 'Skill'),
    ('G', 'Grade'),
)

COUPON_TYPE = (
    ('S', 'Sale'),
    ('B', 'Bonus'),
)

AVALIABLE_CHOICES = (
    ('OP', 'One Player'),
    ('PVP', 'Player Versus Player'),
    ('MP', 'Multiple Players'),
    ('T', 'Tournament'),
    ('OE', 'Other Event'),
    ('L', 'Limited'),
    ('D', 'Drop'),
)

GAME_MODE = (
    ('STW', 'Spin The Wheel'),
    ('OB', 'Open Box'),
    ('OP', 'Open Pack'),
    ('SR', 'Spin Roulette'),
)

BATTLE_STATUS = (
    ('O', 'Open'),
    ('R', 'Running'),
    ('C', 'Complete'),
)

SPIN_TYPE = (
    ('C', 'Classic'),
    ('S', 'Simultaneous'),
    ('I', 'Instant'),
)

TYPE_CHOICES = (('S', 'Singles'), ('BP', 'Booster Pack'),
                ('BB', 'Booster Box'), ('PP', 'Pokemon Product'), ('O',
                                                                   'Other'))
CARD_CATEGORIES = (('P', 'Pokemon'), ('M', 'Magic The Gathering'),
                ('B', 'Bakugo'), ('Y', 'Yu-Gi-Oh!'), ('A', 'Anime'), ('O', 'Other'))

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

BLOG_TYPE_CHOICES = (
    ('F', 'Featured'),
    ('N', 'New'),
    ('P', 'Popular'),
    ('EC', "Editor's Choice"),
)

HEAT = (
    ('M', 'Mild'),
    ('S', 'Spicy'),
    ('F', 'Fiery'),
    ('W', 'Wild'),
    ('E', 'Explosive'),
)

NOTIFICATIONSTATUS = (
    ('ON', 'Online'),
    ('DND', 'Do Not Disturb'),
    ('OFF', 'Offline'),
)

ASCENSIONFLAVORTEXT = (
    ('A', 'Ate the forbidden cookies'),
    ('B', 'Bit the bullet'),
    ('C', 'Caught in the act'),
    ('D', "Doordash'd "),
    ('E', 'Enigma '),
    ('S', 'Shacked to a galloping horse'),
    ('X', 'Xyster to the keister'),
    ('Z', 'Zapperdoodled'),
)

SHIPPINGTYPE = (
    ('S', 'Standard'),
    ('E', 'Expedited'),
)

SHIPPINGSTATUS = (
    ('P', 'Processing'),
    ('S', 'Shipped'),
    ('D', 'Delivered'),
    ('R', 'Refunded'),
    ('C', 'Canceled'),
    ('D', 'Damaged In Transit'),
    ('O', 'On Hold'),
)

TIMESTATUS = (
    ('P', 'Processing'),
    ('E', 'Earlier Than Expected'),
    ('O', 'On Time'),
    ('L', 'Late'),
    ('N', 'Not Applicable - Down'),
    ('N', 'Not Applicable - Intended'),
)

WITHDRAWSTATE = (
    ('I', 'Incomplete'),
    ('C', 'Complete'),
    ('CA', 'Cancelled'),
)

CAPACITYSTATE = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

POWER = (
    ('1', 'x1'),
    ('2', 'x2'),
    ('5', 'x5'),
    ('10', 'x10'),
    ('100', 'x100'),
    ('1000', 'x1000'),
)

COLOR = (
    ('gray',   'Gray'),
    ('green',  'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('red',    'Red'),
    ('black',  'Black'),
    ('gold',   'Gold'),
)

PRIVACY = (
    ('PUB', 'Public'),
    ('PRI', 'Private'),
)

LEVEL = (
    ('C', 'Common'),
    ('U', 'Uncommon'),
    ('R', 'Rare'),
    ('E', 'Epic'),
    ('M', 'Mythical'),
    ('T', 'Transcendent'),
    ('P', 'Primordial'),
    ('L', 'Legendary'),
    ('U', 'Ultimate'),
    ('F', 'Final'),
)

INVESTYPE = (
    ('G', 'Graded'),
    ('R', 'Raw'),
    ('S', 'Stock'),
)

AchievementCategory = (
    ('RS', 'Rubies Spent'),
    ('TRE', 'Total Rubies Earned '),
    ('RC', 'Rubies Collected'),
    ('WS', 'Wheels Spun'),
    ('GCH', 'Green Cards Hit'),
    ('YCH', 'Yellow Cards Hit'),
    ('OCH', 'Orange Cards Hit'),
    ('RCH', 'Red Cards Hit'),
    ('BCH', 'Black Cards Hit'),
    ('GOCH', 'Gold Cards Hit'),
    ('RGCH', 'Red Gold Cards Hit'),
    ('BW', 'Battles Won'),
    ('BL', 'Battles Lost'),
    ('BD', 'Battles Drawn'),
    ('FA', 'Friends Added'),
    ('TCS', 'Total Community Size'),
    ('O', 'Other'),
)

PRACTICE = (
    ('P', 'Practice'),
    ('R', 'Real'),
)

MEMBERSHIP_TIER = (
    ('S', 'Sapphire'),
    ('R', 'Ruby'),
    ('E', 'Emerald'),
    ('D', 'Diamond'),
    ('?', '???'),
)

BENEFIT = (
    ('RD', 'Ruby Drop'),
    ('DC', 'Daily Chests'),
    ('RR', 'Referal Rubies'),
)

TIER = (
    ('B', 'Basic'),
    ('F', 'Free'),
    ('G', 'Gambler'),
    ('S', 'Shark'),
    ('D', 'Degen'),
    ('W', 'Whale'),
    ('BA', 'Baller'),
    ('GT', 'GOAT'),
    ('M', 'Monstrosity'),
)

BLACKJACK_OUTCOME = (
    ('W', 'Win'),
    ('L', 'Lose'),
    ('D', 'Draw'),
    ('B', 'BlackJack'),
)

GAMETYPE = (
    ('T', 'Traditional'),
    ('C', 'Club'),
)

GAMEHUB_CHOICES = (
    ('F', 'Featured'),
    ('P', 'Popular'),
    ('N', 'New'),
)

class Idea(models.Model):
    """Model for sharing ideas and getting user feedback"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    profile_number = models.PositiveIntegerField(default=0, editable=False)
    description = models.TextField()
    image = models.ImageField(help_text='Attach an image for your idea (scales to your picture`s dimensions).')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"

    def save(self, *args, **kwargs):
        if not self.pk:
            max_message_number = Idea.objects.aggregate(max_message_number=models.Max('profile_number'))[
                                     'max_message_number'] or 0

            self.profile_number = max_message_number + 1

            profile = ProfileDetails.objects.filter(user=self.user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"http://127.0.0.1:8000/share/#{str(self.profile_number)}"

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

class UpdateProfile(models.Model):
    """Update user profiles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    profile_number = models.PositiveIntegerField(default=0, editable=False)
    date_and_time = models.DateTimeField(null=True, verbose_name="time and date", auto_now_add=True)
    image = models.ImageField(help_text='Attach an image for your profile (scales to your picture`s dimensions.)')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "User Profile Post"
        verbose_name_plural = "User Profile Posts"

    def save(self, *args, **kwargs):
        if not self.pk:
            max_message_number = UpdateProfile.objects.aggregate(max_message_number=models.Max('profile_number'))[
                                     'max_message_number'] or 0

            self.profile_number = max_message_number + 1

            profile = ProfileDetails.objects.filter(user=self.user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"http://127.0.0.1:8000/showcase/#{str(self.profile_number)}"

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

class Affiliation(models.Model):
    type = models.CharField(max_length=200)
    flavor_text = models.TextField()
    icon = models.ImageField()
    unlocking_level = models.OneToOneField('Level', blank=True, null=True, on_delete=models.CASCADE, related_name='level_to_unlock')
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return f"{self.type}" + " " + self.flavor_text

class Level(models.Model):
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]
    level = models.IntegerField(default=1, blank=True, null=True)
    level_name = models.CharField(max_length=200)
    experience = models.IntegerField(default=0, blank=True, null=True)
    full_row = models.BooleanField(default=True)
    affiliation = models.ForeignKey(Affiliation, blank=True, null=True, on_delete=models.CASCADE)
    icon = models.ImageField(blank=True, null=True)
    color_wheel = ColorField(samples=COLOR_PALETTE, blank=True, null=True)
    color = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated hex colors for gradient")
    games = models.ManyToManyField(
        'Game',
        blank=True,
        limit_choices_to={'daily': True},
        related_name='levels',
        verbose_name="Games with Daily Mode"
    )
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return f"{self.level_name} (Level {self.level})"

    @property
    def actual_level(self) -> str:

        getcontext().prec = max(self.level, 28)
        raw = Decimal("1.02") ** self.level

        truncated = raw.quantize(Decimal("0.00"), rounding=ROUND_DOWN)
        s = f"{truncated:.2f}"
        if raw != truncated:
            s += "…"
        return s + "x"

    def save(self, *args, **kwargs):

        if not self.pk:
            super().save(*args, **kwargs)

        if self.full_row:

            last_level = Level.objects.all().order_by('-level').first()
            self.level = (last_level.level + 1) if last_level else 1

            level_instances = []
            for i in range(10):
                new_level = Level(
                    level=self.level + i,
                    level_name=self.level_name,
                    experience=self.experience,
                    full_row=False,
                    is_active=self.is_active
                )
                level_instances.append(new_level)

            self._bulk_create_level_instances(level_instances)

            return

        formulaic_experience = self.level * 2
        self.experience = formulaic_experience ** 2

        if self.pk:
            existing_instance = Level.objects.filter(pk=self.pk).first()
            if existing_instance and existing_instance.level_name != self.level_name:
                Level.objects.filter(level_name=existing_instance.level_name).exclude(pk=self.pk).update(
                    level_name=self.level_name)

        super().save(*args, **kwargs)

        self._correct_level_gaps()

        self._adjust_related_levels()

    def _bulk_create_level_instances(self, level_instances):
        try:
            with transaction.atomic():
                Level.objects.bulk_create(level_instances)
        except Exception as e:

            print(f"Error during bulk creation: {e}")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self._correct_level_gaps()

    def _correct_level_gaps(self):
        try:
            with transaction.atomic():
                levels = Level.objects.order_by('level')
                new_levels = []
                current_level = 1

                for level_obj in levels:
                    if level_obj.level != current_level:
                        level_obj.level = current_level
                        new_levels.append(level_obj)
                    current_level += 1

                if new_levels:
                    Level.objects.bulk_update(new_levels, ['level'])
        except Exception as e:
            print(f"Error correcting level gaps: {e}")

    def _adjust_related_levels(self):
        try:
            with transaction.atomic():

                all_levels = Level.objects.order_by('level', 'id')
                level_groups = {}

                for level_obj in all_levels:
                    if level_obj.level_name not in level_groups:
                        level_groups[level_obj.level_name] = []
                    level_groups[level_obj.level_name].append(level_obj)

                new_levels = []
                current_level = 1

                for group_name, level_group in level_groups.items():
                    for i, level_obj in enumerate(level_group):

                        level_obj.level = current_level
                        current_level += 1
                        new_levels.append(level_obj)

                Level.objects.bulk_update(new_levels, ['level'])

        except Exception as e:
            print(f"Error adjusting related levels: {e}")

    def get_background_style(self):
        """
        Generate a CSS background style and metadata based on the color field.
        """
        if not self.color:
            return {"style": "background: none;", "is_gradient": False}
        colors = self.color.split(",")
        if len(colors) > 1:

            return {
                "style": f"background: linear-gradient(30deg, {', '.join(colors)});",
                "is_gradient": True,
            }

        return f"{colors[0]}"

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"
        ordering = ['level']

class MonstrositySprite(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = str(self.image)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Monstrosity Sprite"
        verbose_name_plural = "Monstrosity Sprites"

class Monstrosity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monstrositysprite = models.ForeignKey(MonstrositySprite, on_delete=models.CASCADE,
                                          verbose_name="Monstrosity Sprite")
    monstrositys_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Monstrosity Name",
                                         unique=True)
    experience = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    currency_amount = models.IntegerField(default=0)
    feed_amount = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + "'s " + str(self.monstrositys_name)

    def save(self, *args, **kwargs):
        if not self.monstrositys_name:
            self.monstrositys_name = str(self.user) + "'s " + str(self.monstrositysprite)

        if not self.currency:
            try:
                self.currency = Currency.objects.all().order_by('id')[2]
            except IndexError:
                self.currency = None
        super().save(*args, **kwargs)

    def get_sprite_images(self):

        return [self.monstrositysprite.image.url]

    @property
    def display_sprite_images(self):
        return self.get_sprite_images()

    class Meta:
        verbose_name = "Monstrosity"
        verbose_name_plural = "Monstrosities"


class Membership(models.Model):
    name = models.CharField(default='Rubies', max_length=200)
    tier = models.CharField(choices=MEMBERSHIP_TIER, max_length=2, blank=True, null=True)
    file = models.FileField(null=True, verbose_name='Sprite')
    description = models.TextField(blank=True, null=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    price = models.FloatField(default=0)
    discount_price = models.FloatField(blank=True, null=True)
    second_price = models.FloatField(blank=True, null=True)
    second_discount_price = models.FloatField(blank=True, null=True)
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Membership Tier"
        verbose_name_plural = "Membership Tiers"


class Benefits(models.Model):
    benefit = models.CharField(max_length=2, choices=BENEFIT)
    multiplier = models.IntegerField(default=1)
    tier = models.ForeignKey(
        'Tier',
        on_delete=models.CASCADE,
        related_name='benefits'
    )
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"


class Tier(models.Model):
    tier = models.CharField(choices=TIER, max_length=2, blank=True, null=True, default='B')
    file = models.FileField(null=True, verbose_name='Sprite')
    description = models.TextField(blank=True, null=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the image (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the image (use for original ratio).',
                                              verbose_name="image width")
    lower_bound = models.IntegerField(default=0)
    upper_bound = models.IntegerField(blank=True, null=True)
    timeframe = models.DurationField(
        default=timedelta(days=30),
        help_text="How far back to include (defaults to 30 days)",
        blank=True, null=True
    )
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def get_recent_data(self):
        cutoff = timezone.now() - self.timeframe
        return Tier.objects.filter(mfg_date__gte=cutoff)

    def __str__(self):
        return str(self.tier)

    class Meta:
        verbose_name = "Tier"
        verbose_name_plural = "Tiers"


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Stamp session on every request
        request.session['last_activity'] = timezone.now().isoformat()
        return self.get_response(request)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_tier = models.ForeignKey(Membership, on_delete=models.CASCADE)
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"


class Currency(models.Model):
    name = models.CharField(default='Rubies', max_length=200)
    code = models.CharField(max_length=3, default='usd')
    flavor_text = models.CharField(max_length=200)
    file = models.FileField(null=True, verbose_name='Sprite')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    weight_thresholds_json = models.TextField(blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.name == "Loricorf" and not self.weight_thresholds_json:
            weight_thresholds = []
            current_threshold = 10
            for i in range(500):
                weight_thresholds.append(current_threshold)
                current_threshold *= 1.03

            self.weight_thresholds_json = json.dumps(weight_thresholds)

        super().save(*args, **kwargs)

    @property
    def weight_thresholds(self):
        if self.weight_thresholds_json:
            return json.loads(self.weight_thresholds_json)
        return []

    class Meta:
        verbose_name = "PokeTrove Currency"
        verbose_name_plural = "PokeTrove Currencies"


class CurrencyMarket(models.Model):
    name = models.CharField(max_length=200)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    unit_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deal = models.BooleanField(default=False)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1000, blank=True,
                             null=True)
    flavor_text = models.CharField(max_length=200)
    file = models.FileField(null=True, verbose_name='Sprite')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("showcase:currencyproduct", kwargs={'slug': self.slug})

    def currency_get_add_to_cart_url(self):
        return reverse("showcase:currency-add-to-cart", kwargs={'slug': self.slug})

    def currency_get_remove_from_cart_url(self):
        return reverse("showcase:currency-remove-from-cart", kwargs={'slug': self.slug})

    def get_profile_url(self):
        return reverse('showcase:product', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            print("Name:", self.name)
            self.slug = slugify(self.name)
            print("Slug after slugify:", self.slug)
        if self.amount != 0:
            self.unit_ratio = self.price / self.amount
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Currency Market"
        verbose_name_plural = "Currency Markets"


class FavoriteCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_market = models.ForeignKey(CurrencyMarket, on_delete=models.CASCADE)
    favorited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'currency_market')


def generate_unique_code(length=16):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not GiftCode.objects.filter(code=code).exists():
            return code


def generate_unique_serial():
    while True:
        serial = random.randint(10**15, (10**16) - 1)
        if not GiftCode.objects.filter(serial=serial).exists():
            return serial


def default_expiration():
    return timezone.now() + timedelta(days=7)


class GiftCode(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(
        max_length=64,
        validators=[MinLengthValidator(16)],
        unique=True,
        blank=True,
        null=True
    )
    serial = models.BigIntegerField(blank=True, null=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=default_expiration)
    value = models.IntegerField(default=1000)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    uses = models.IntegerField(default=1)
    total_uses = models.IntegerField(default=1)
    tracking_total_uses = models.IntegerField(default=0)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return f"{self.code} (Serial: {self.serial})"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_unique_code()
        if self.tracking_total_uses >= self.total_uses:
            self.is_active = 0
        if not self.serial:
            self.serial = generate_unique_serial()

        if self.expiration_date and timezone.now() > self.expiration_date:
            self.is_active = 0

        if not self.currency:
            self.currency = Currency.objects.filter(is_active=1).first()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Gift Code"
        verbose_name_plural = "Gift Codes"


class GiftCodeRedemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gift_code = models.ForeignKey(GiftCode, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, blank=True, null=True)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def save(self, *args, **kwargs):

        if not self.amount:
            self.amount = self.gift_code.value
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('user', 'gift_code')
        verbose_name = "Gift Code Redemption"
        verbose_name_plural = "Gift Codes Redemptions"


class RubyDrop(models.Model):
    amount = models.IntegerField()
    timeframe = models.IntegerField(default=3600)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    rarity = models.CharField(choices=LEVEL, max_length=1)
    opentime = models.IntegerField(default=300)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        self.currency = Currency.objects.filter(is_active=1).first()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ruby Drop"
        verbose_name_plural = "Ruby Drops"


class RubyDropInstance(models.Model):
    rubydrop = models.ForeignKey(RubyDrop, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    rarity = models.CharField(choices=LEVEL, max_length=1)
    opentime = models.IntegerField(default=300)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        self.currency = Currency.objects.filter(is_active=1).first()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ruby Drop"
        verbose_name_plural = "Ruby Drops"


class LevelIcon(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    level_icon = models.ImageField(blank=True, null=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    class Meta:
        verbose_name = "Level Icon"
        verbose_name_plural = "Level Icons"


class ProfileDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    shipping_address = models.CharField(blank=True, null=True, max_length=250)
    billing_address = models.CharField(blank=True, null=True, max_length=250)
    avatar = models.ImageField(upload_to='profile_image', null=True, blank=True, verbose_name="Profile picture")
    alternate = models.TextField(verbose_name="Alternate text", null=True, blank=True)
    about_me = models.TextField(blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    unlocked_daily_chests = models.ManyToManyField('Game', blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    currency_amount = models.IntegerField(default=0)
    total_currency_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_currency_spent_30 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='30-Day Money Spent On Rubies (USD)')
    total_currency_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Total Money Spent On Rubies (USD)')
    total_card_money_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Money Spent On Cards (USD)')
    rubies_spent = models.IntegerField(blank=True, null=True, default=0)
    other_currencies_amount = models.ManyToManyField(Currency, through='ProfileCurrency',
                                                     related_name="profile_currencies")
    green_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    yellow_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    orange_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    red_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    black_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    gold_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    red_gold_cards_hit = models.IntegerField(blank=True, null=True, default=0)
    cards_counter = models.IntegerField(blank=True, null=True, default=0)
    times_subtract_called = models.IntegerField(default=0)
    monstrosity = models.ForeignKey(Monstrosity, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name="monster")
    level_icon = models.ForeignKey(LevelIcon, blank=True, null=True, on_delete=models.CASCADE)
    seller = models.BooleanField(default=False, null=True)
    trader = models.BooleanField(default=False, null=True)
    partner = models.BooleanField(default=False, null=True)
    membership = models.ForeignKey(Membership, blank=True, null=True, on_delete=models.CASCADE)
    tier = models.ForeignKey('Tier', blank=True, null=True, on_delete=models.CASCADE)
    favorite_chests = models.ManyToManyField('FavoriteChests', blank=True)
    position = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Position for sorting",
    )
    free = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + " Selling Status: " + str(self.seller) + " Membership: " + str(self.membership)

    @property
    def rd_multiplier(self):
        benefit = (self.tier.benefits.filter(benefit='RD', is_active=1).first())
        return benefit.multiplier if benefit else 1

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('showcase:profile', kwargs={'pk': self.pk})

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def add_currency(self, amount):
        self.currency_amount += amount
        self.total_currency_amount += amount
        self.save()

    def subtract_currency(self, amount):
        if self.currency_amount >= amount:
            self.currency_amount -= amount
            self.total_currency_spent += amount
            self.times_subtract_called += 1
            self.save()
        else:
            raise ValueError("Not enough currency")

    def update_currencies_for_profile(profile):
        currencies = Currency.objects.all()
        for currency in currencies:
            profile_currency, created = ProfileCurrency.objects.get_or_create(profile=profile, currency=currency)
            if created:
                profile_currency.quantity = 0
                profile_currency.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:

            default_level = Level.objects.first()
            default_currency = Currency.objects.first()
            profile_image = '/bed.jpg'

            ProfileDetails.objects.create(
                user=instance,
                currency=default_currency,
                level=default_level,
                avatar=profile_image
            )

            Inventory.objects.create(
                user=instance,
                name=f"{instance.username}'s Inventory",
                image='a.jpg',
                image_length=100,
                image_width=100,
                is_active=1,
            )

    post_save.connect(create_user_profile, sender=User)

    def save(self, *args, **kwargs):
        is_creating = self._state.adding

        if is_creating:
            # (Optional) set any defaults before the first save:
            if not self.currency:
                from .models import Currency
                self.currency = Currency.objects.filter(is_active=1).first()

            if not self.avatar:
                self.avatar = 'a.jpg'

            # First insert—after this, self.pk and self.created_at exist.
            super().save(*args, **kwargs)
            return  # <— stop here on new objects to avoid a second INSERT

        # ==== from here on, we're updating an existing ProfileDetails ====

        # If still marked free but 7 days have passed since `created_at`, turn off free.
        if self.free and timezone.now() >= (self.created_at + timedelta(days=7)):
            self.free = False

        # Tier‐assignment logic:
        if self.total_currency_spent_30 < 25 and self.free:
            code = 'F'
        elif 0 <= self.total_currency_spent_30 < 25:
            code = 'B'
        elif 25 <= self.total_currency_spent_30 < 100:
            code = 'G'
        elif 100 <= self.total_currency_spent_30 < 250:
            code = 'S'
        elif 250 <= self.total_currency_spent_30 < 500:
            code = 'D'
        elif 500 <= self.total_currency_spent_30 < 1000:
            code = 'W'
        elif 1000 <= self.total_currency_spent_30 < 2000:
            code = 'BA'
        elif 2000 <= self.total_currency_spent_30 < 5000:
            code = 'GT'
        elif self.total_currency_spent_30 >= 5000:
            code = 'M'
        else:
            code = 'B'

        from .models import Tier
        self.tier = Tier.objects.filter(tier=code).first()

        # Handle “rubies_spent” / level‐up logic:
        previous = ProfileDetails.objects.get(pk=self.pk)
        if previous.currency_amount > self.currency_amount:
            spent = previous.currency_amount - self.currency_amount
            from .models import Currency
            first_currency = Currency.objects.filter(is_active=1).first()
            if first_currency and self.currency == first_currency:
                self.rubies_spent = (self.rubies_spent or 0) + spent

        if self.rubies_spent != previous.rubies_spent:
            from .models import Level
            new_level = Level.objects.filter(experience__lte=self.rubies_spent).order_by('-level').first()
            if new_level:
                self.level = new_level

        # Finally, save the updated fields:
        super().save(*args, **kwargs)

    @property
    def is_free(self):
        return timezone.now() < (self.created_at + timedelta(days=7))

    @property
    def is_free(self):
        # Only called after created_at has been set (because save() logic ensures that)
        return timezone.now() < (self.created_at + timedelta(days=7))

    class Meta:
        verbose_name = "Account Profile"
        verbose_name_plural = "Account Profiles"


class ProfileCurrency(models.Model):
    profile = models.ForeignKey('ProfileDetails', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.profile.user}'s {self.currency.name} ({self.quantity})"


class Investments(models.Model):
    investment = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=INVESTYPE, max_length=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    def __str__(self):
        return f"{self.user}'s {self.investment}"

    class Meta:
        verbose_name = "Investment"


class UserInvestmentFund(models.Model):
    fund = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=INVESTYPE, max_length=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    def __str__(self):
        return f"{self.user}'s {self.fund}"

    class Meta:
        verbose_name = "User Investment Fund"


class InvestmentCards(models.Model):
    cards = models.ForeignKey('Item', on_delete=models.CASCADE)
    type = models.CharField(choices=INVESTYPE, max_length=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    def __str__(self):
        return f"{self.user}'s {self.investment}"

    class Meta:
        verbose_name = "Investment Card"


class IndividualChestStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ranking = models.IntegerField(default=0)
    plays = models.IntegerField(default=0)
    chest = models.ForeignKey('Game', blank=True, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    class Meta:
        verbose_name = "Individual Chest Statistic"


class TotalChestStatistics(models.Model):
    ranking = models.IntegerField(default=0)
    plays = models.IntegerField(default=0)
    chests = models.ForeignKey('Game', blank=True, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    class Meta:
        verbose_name = "Total Chest Statistic"


class CurrencyOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField()
    items = models.ForeignKey(CurrencyMarket, on_delete=models.CASCADE)
    itemhistory = models.ForeignKey(CurrencyMarket, on_delete=models.CASCADE, verbose_name="Order history", null=True,
                                    related_name='currency_item_history')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='currency_shipping_address', on_delete=models.SET_NULL,
                                         blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='currency_billing_address', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    id = uuid4()
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")
    '''
   1. Item added to cart
   2. Adding a billing address
   (Failed checkout)
   3. Payment
   (Preprocessing, processing, packaging etc.)
   4. Being delivered
   5. Received
   6. Refunds
   '''

    def __str__(self):
        return self.user.username
        if not self.id:
            self.slug = slugify(self.market.slug)
        super(CurrencyOrder, self).save(*args, **kwargs)

    def get_total_item_price(self):
        if self.items and self.items.price is not None:
            if self.items.discount_price:
                return self.quantity * self.get_discount_item_price()
            return self.quantity * self.items.price
        return 0

    def get_discount_item_price(self):
        return self.quantity * self.items.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def currency_get_add_to_cart_url(self):
        return reverse("showcase:currency-add-to-cart", kwargs={'slug': self.slug})

    def currency_get_remove_from_cart_url(self):
        return reverse("showcase:currency-remove-from-cart", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.items.discount_price:
            self.amount = self.items.discount_price
        else:
            self.amount = self.items.price
        super().save(*args, **kwargs)

    def get_total_price(self):
        total = 0
        total += self.items.price
        if self.coupon:
            if order.coupon.type == 'B':
                if self.coupon.percentDollars:
                    self.amount = self.amount * (1.01 * self.coupon.amount)
                else:
                    self.amount = self.amount + self.coupon.currency_amount
            else:
                if self.coupon.percentDollars:
                    total *= 1 - (0.01 * self.coupon.amount)
                else:
                    total -= self.coupon.amount

        return total

    def get_final_price(self):
        if self.items.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()

    def get_profile_url(self):
        return reverse('showcase:profile', args=[str(self.slug)])

    def get_profile_url2(self):
        return reverse('showcase:currencymarket', args=[str(self.slug)])

    class Meta:
        verbose_name = "Individiual Currency Order"
        verbose_name_plural = "Individiual Currency Orders"


class CurrencyFullOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField('CurrencyOrder')
    itemhistory = models.ForeignKey('CurrencyMarket', on_delete=models.CASCADE, verbose_name="Order history", null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    stripe_transaction_id = models.CharField(max_length=255, blank=True, null=True,
                                             help_text="Stripe charge ID")
    id = uuid4()
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")
    '''
   1. Item added to cart
   2. Adding a billing address
   (Failed checkout)
   3. Payment
   (Preprocessing, processing, packaging etc.)
   4. Being delivered
   5. Received
   6. Refunds
   '''

    def __str__(self):
        return self.user.username

    def get_final_price(self):
        if self.items.discount_price:
            return Decimal(self.get_discount_item_price())
        return Decimal(self.get_total_item_price())

    def get_discount_item_price(self):
        return self.round_decimal(Decimal(self.item.discount_price))

    def get_amount_saved(self):
        return self.round_decimal(self.get_total_item_price() - self.get_discount_item_price())

    def get_total_price(self):
        total = Decimal('0.00')
        for order_item in self.items.all():
            total += Decimal(order_item.get_final_price())

        if self.coupon:
            if self.coupon.percentDollars:
                discount_factor = Decimal('1.00') - (Decimal(self.coupon.amount) / Decimal('100.00'))
                total *= discount_factor
            else:
                total -= Decimal(self.coupon.amount)

        return self.round_decimal(total)

    def round_decimal(self, value):
        """Ensures the decimal always has two places and rounds up."""
        return value.quantize(Decimal('0.01'), rounding=ROUND_UP)

    def get_profile_url(self):
        return reverse('showcase:profile', args=[str(self.slug)])

    def get_profile_url2(self):
        return reverse('showcase:currencyproducts', args=[str(self.slug)])

    class Meta:
        verbose_name = "Total Currency Order"
        verbose_name_plural = "Total Currency Orders"

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileDetails, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ManyToManyField('showcase.Level', blank=True, related_name='current_level')
    amount = models.IntegerField(default=0, blank=True, null=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return f"{self.user}: {self.amount} EXP"

    def save(self, *args, **kwargs):

        if self.user and not self.profile:
            self.profile = ProfileDetails.objects.filter(user=self.user).first()

        if self.profile:
            self.amount = self.profile.rubies_spent or 0

        super().save(*args, **kwargs)

        eligible_levels = Level.objects.filter(experience__lte=self.amount)

        print(f"Eligible levels: {eligible_levels}")
        self.level.set(eligible_levels)
        print(f"Set levels: {self.level.all()}")

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"


class Ascension(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileDetails, on_delete=models.CASCADE)
    ascension = models.CharField(max_length=200, blank=True, null=True)
    flavor_text = models.CharField(choices=ASCENSIONFLAVORTEXT, max_length=1, blank=True, null=True)
    ascension_number = models.IntegerField(blank=True, null=True, editable=False)
    final_level = models.ForeignKey(
        'Level', blank=True, null=True, on_delete=models.CASCADE, related_name='necessary_level_to_unlock'
    )
    reward = models.IntegerField(default=1)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return str(self.ascension)

    def save(self, *args, **kwargs):
        with transaction.atomic():

            if not self.ascension_number:
                last_ascension = Ascension.objects.filter(user=self.user).order_by('-ascension_number').first()
                self.ascension_number = (last_ascension.ascension_number + 1) if last_ascension else 1

            if not self.final_level_id:
                lowest_level = Level.objects.filter(level=1).first()
                if lowest_level:
                    self.final_level = lowest_level

            if not self.ascension:
                ordinal_suffix = self._get_ordinal_suffix(self.ascension_number)
                self.ascension = f"{self.user}'s {self.ascension_number}{ordinal_suffix} Ascension"

            if not self.flavor_text:
                self.flavor_text = random.choice([choice[0] for choice in ASCENSIONFLAVORTEXT])

            super().save(*args, **kwargs)

            profile = ProfileDetails.objects.filter(user=self.user).first()
            if profile and profile.level.level >= 100:
                print('ascending through the rubies')

                if profile.rubies_spent > 0:
                    print('rubies gained: ' + str(profile.rubies_spent))
                    profile.currency_amount += int(profile.rubies_spent * 0.1)

                    profile.rubies_spent = 0
                else:
                    print(
                        'Somehow you gained levels without playing the game properly. Either you are a developer (you are clear) or you hacked the system. Hacking will not be tolerated and your account has been reported.')

                profile.level = Level.objects.filter(level=1).first()
                profile.save(update_fields=['rubies_spent', 'level', 'currency_amount'])

                print(f'User {profile.user} ascended at level {profile.level.level}')
            elif profile and profile.level.level < 100:
                print('User cannot ascend due to not having reached level 100')
            else:
                print('No profile found for this user.')

    def _get_ordinal_suffix(self, number):
        """Helper method to get the ordinal suffix for a given number."""
        if 11 <= number % 100 <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")

    class Meta:
        verbose_name = "Ascension"
        verbose_name_plural = "Ascensions"


class Clickable(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', verbose_name="Clickable Image")
    base_value = models.IntegerField(default=0)
    rarity = models.IntegerField(default=0)
    lore = models.TextField(blank=True, null=True)
    chance_per_second = models.IntegerField(default=1000)
    sound = models.FileField()
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.rarity == 0:
            self.rarity = (1/self.chance_per_second) * 1000

        super().save(*args, **kwargs)

class UserClickable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clickable = models.ForeignKey(Clickable, on_delete=models.CASCADE)
    exponential_level_multiplier = models.FloatField(default=1.00)
    actual_value = models.FloatField(default=0)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(default=0)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def save(self, *args, **kwargs):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        self.currency = Currency.objects.filter(is_active=1).first()

        if profile and profile.level.level >= 1:
            level_value = profile.level.level
            self.exponential_level_multiplier = math.floor(1.02 ** level_value)
            self.actual_value = self.clickable.base_value
        else:
            self.exponential_level_multiplier = 1.00
            self.actual_value = self.clickable.base_value

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.clickable.name}"

    class Meta:
        verbose_name = "User Clickable"
        verbose_name_plural = "User Clickables"


class SecretRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(validators=[MinLengthValidator(24)], max_length=50)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + " " + str(self.code)

    class Meta:
        verbose_name = "Secret Room"
        verbose_name_plural = "Secret Room"


class Endowment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target_user")
    order = models.ForeignKey(CurrencyOrder, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    experience_increase = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + " bestowed a gift upon " + str(self.target)

    def save(self, *args, **kwargs):
        if self.order:
            self.amount = self.order.amount * 5

        self.currency = Currency.objects.filter(is_active=1).first()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Endowment"
        verbose_name_plural = "Endowments"

class EndowmentCurrency(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    endowment = models.ForeignKey(Endowment, on_delete=models.CASCADE, related_name="endowment")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @receiver(post_save, sender=Endowment)
    def create_endowment_currency(sender, instance, created, **kwargs):
        if created:
            EndowmentCurrency.objects.create(sender=instance.user)

    class Meta:
        verbose_name = "Endowment"
        verbose_name_plural = "Endowments"

class PrizePool(models.Model):
    prize_name = models.CharField(max_length=500, verbose_name="Prize Name")
    image = models.FileField(upload_to='images/', verbose_name="Prize Image")
    number = models.IntegerField(default=1, verbose_name="Quantity of Card")
    price = models.IntegerField(default=1)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.prize_name) + "    Quantity-" + str(self.number)

    def save(self, *args, **kwargs):

        self.currency = Currency.objects.filter(is_active=1).first()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventory"

class PollQuestion(models.Model):
    question_text = models.CharField(max_length=500, verbose_name="Question")
    choice = models.ForeignKey('showcase.Choice', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.question_text)

    class Meta:
        verbose_name = "Poll Question"
        verbose_name_plural = "Poll Questions"

class Shuffler(models.Model):
    """Used for voting on different new ideas"""
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    file = models.FileField(null=True, verbose_name='File')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    choices = models.ManyToManyField('showcase.Choice', blank=True)
    category = models.CharField(max_length=100,
                                help_text='Type the category of product getting shuffled.')
    heat = models.CharField(choices=HEAT, max_length=2, blank=True, null=True)
    shuffletype = models.ForeignKey('ShuffleType', on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name="Shuffle Type")
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    demonstration = models.CharField(choices=PRACTICE, max_length=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    total_number_of_choice = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.question)

    @receiver(post_save, sender='showcase.Choice')
    def update_shuffler(sender, instance, **kwargs):
        shufflers = Shuffler.objects.filter(choices=instance)
        for shuffler in shufflers:
            shuffler.tier = instance.tier
            shuffler.rarity = instance.rarity
            shuffler.value = instance.value
            shuffler.number = instance.number
            shuffler.save()

    class Meta:
        verbose_name = "Shuffle Choice"
        verbose_name_plural = "Shuffle Choices"


class Inventory(models.Model):
    """Model for sharing ideas and getting user feedback"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Inventory Name",
                            help_text="Name your inventory. Leave blank to use (your name)'s inventory", blank=True,
                            null=True)
    number_of_cards = models.IntegerField(blank=True, null=True)
    image = models.ImageField(help_text='Inventory Image.')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the inventory (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the inventory (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + "'s Inventory"

    def update_inventory_count(self):
        self.number_of_cards = InventoryObject.objects.filter(inventory=self).count()
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                existing_inventory = Inventory.objects.get(user=self.user)

                raise ValueError("A user can only have one Inventory")
            except Inventory.DoesNotExist:
                pass

        if not self.name:
            self.name = f"{self.user}'s Inventory"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Player Inventory"
        verbose_name_plural = "Player Inventories"

class InventoryObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank=True, null=True)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE, blank=True, null=True)
    choice_text = models.CharField(max_length=200, verbose_name='Choice Text', blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    trade_locked = models.BooleanField(verbose_name="Set Tradable?", default=False)
    condition = models.CharField(choices=CONDITION_CHOICES, default="M", max_length=2, blank=True, null=True)
    quantity = models.IntegerField(default=1, help_text="Number of items available.")
    image = models.ImageField(blank=True, null=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")
    locked = models.BooleanField(default=False, verbose_name='Sell-Locked')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + "'s " + str(self.choice) + " - " + str(self.condition)

    def save(self, *args, **kwargs):
        if self.choice:
            self.choice_text = self.choice.choice_text
            self.image = self.choice.file
            self.image_length = self.choice.image_length
            self.image_width = self.choice.image_width
            self.price = self.choice.value

            if self.pk is None and self.currency is None:
                try:
                    self.currency = Currency.objects.first()
                except Currency.DoesNotExist:

                    pass
            if self.user and not self.inventory:
                try:

                    self.inventory = Inventory.objects.get(user=self.user)
                except Inventory.DoesNotExist:

                    raise ValueError(f"No inventory found for user {self.user}")

        if self.pk is None and self.user:
            self.inventory = Inventory.objects.get(user=self.user)

        if self.trade_locked:
            trade_item, created = TradeItem.objects.get_or_create(
                user=self.user,
                title=self.choice_text,
                defaults={
                    'fees': self.price,
                    'category': self.choice.category,
                    'specialty': self.choice.specialty,
                    'condition': self.condition,
                    'label': self.choice.label,
                    'slug': slugify(self.choice_text),
                    'status': 1,
                    'description': self.choice_text,
                    'image': self.image,
                    'image_length': self.image_length,
                    'image_width': self.image_width,
                    'length_for_resize': self.length_for_resize,
                    'width_for_resize': self.width_for_resize,
                    'is_active': 1,
                }
            )
        super().save(*args, **kwargs)

    def move_to_trading(self, title, fees, category, specialty, condition, label, slug, description, image,
                        image_length, image_width, length_for_resize, width_for_resize):

        if not self.pk:
            raise ValidationError("Inventory item does not exist.")

        trade_item = TradeItem.objects.create(
            user=self.user,
            currency=self.currency,
            value=self.price,
            condition=self.condition,
            image=self.image,
            image_length=image_length,
            image_width=image_width,
            length_for_resize=length_for_resize,
            width_for_resize=width_for_resize,
            is_active=1
        )

        self.delete()

        return trade_item

    class Meta:
        verbose_name = "Player Inventory Object"
        verbose_name_plural = "Player Inventory Objects"

class Trade_In_Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    card_image = models.ImageField()
    card_condition = models.CharField(CONDITION_CHOICES, max_length=2)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Trade-In Card"
        verbose_name_plural = "Trade-In Cards"

class ExchangePrize(models.Model):
    prize = models.ForeignKey('Choice', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    condition = models.CharField(choices=CONDITION_CHOICES, default="M", max_length=2)
    image = models.ImageField(blank=True, null=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.prize:
            self.name = self.prize.choice_text
            self.image = self.prize.file
            self.image_length = self.prize.image_length
            self.image_width = self.prize.image_width
            self.price = self.prize.value
            if self.prize.condition:
                self.condition = self.prize.condition

        if not self.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.currency = first_currency
        if not self.value and self.prize:
            self.value = self.prize.value
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Exchange Prize"
        verbose_name_plural = "Exchange Prizes"

class TradeItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    inventoryobject = models.ForeignKey(InventoryObject, on_delete=models.SET_NULL, null=True, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    specialty = models.CharField(blank=True, null=True, choices=SPECIAL_CHOICES, max_length=2)
    condition = models.CharField(choices=CONDITION_CHOICES, default="M", max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1000, default="N")
    slug = models.SlugField(blank=True, null=True)
    status = models.IntegerField(choices=((0, "Draft"), (1, "Publish")), default=1)
    certified = models.BooleanField(default=False,
                                    help_text="If you are applying to become a partner in more than 1 category, talk to Trove.")
    description = models.TextField()
    value = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length", blank=True, null=True)
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width", blank=True, null=True)

    relateditems = models.ManyToManyField("self", blank=True, verbose_name="Related Items:")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Out of stock?")

    def __str__(self):
        if self.user:
            return self.title + " by " + self.user.username
        else:
            return self.title + " by PokeTrove"

    @staticmethod
    def generate_unique_slug(base_slug, model):
        slug = slugify(base_slug)
        unique_slug = slug
        counter = 1
        while model.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.currency_id:

                self.currency = Currency.objects.first()
            if not self.value and self.inventoryobject:
                self.value = self.inventoryobject.value
            if not self.slug:

                base_slug = self.title
                self.slug = self.generate_unique_slug(base_slug, TradeItem)
            super().save(*args, **kwargs)

            if not TradeOffer.objects.filter(trade_items=self).exists():

                trade_offer_slug = self.generate_unique_slug(self.slug, TradeOffer)
                trade_offer = TradeOffer.objects.create(
                    title=self.title,
                    estimated_trading_value=self.value or 0,
                    user=self.user,
                    slug=trade_offer_slug,
                    trade_status=TradeOffer.PENDING,
                    is_active=self.is_active,
                )
                trade_offer.trade_items.add(self)

    def create_room(self, current_user):
        room_name = f"trade-{self.id}"
        if not Room.objects.filter(name=room_name).exists():
            new_room = Room.objects.create(name=room_name)
            new_room.signed_in_user = current_user
            new_room.save()
            return new_room
        else:
            return Room.objects.get(name=room_name)

    def delete_trade_item(self):
        self.delete()

    class Meta:
        verbose_name = "Trade Item"
        verbose_name_plural = "Trade Items"

class InventoryTradeOffer(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initiated_trades")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_trades")
    offered_items = models.ManyToManyField(TradeItem, related_name="offered_in_trades")
    requested_items = models.ManyToManyField(TradeItem, related_name="requested_in_trades")
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return f"Initiator: {self.initiator} with receiver {self.receiver} - status: {str(self.status)}"

    class Meta:
        verbose_name = "Inventory Trade Offer"
        constraints = [
            models.UniqueConstraint(
                fields=['initiator', 'receiver', 'status'],
                condition=models.Q(status='pending'),
                name='unique_pending_trades'
            )
        ]

    def clean(self):
        if self.status == 'pending':

            existing_trades = InventoryTradeOffer.objects.filter(
                initiator=self.initiator,
                receiver=self.receiver,
                status='pending'
            ).exclude(pk=self.pk)

            for trade in existing_trades:

                existing_offered_items = list(trade.offered_items.all())
                existing_requested_items = list(trade.requested_items.all())

                current_offered_items = list(self.offered_items.all())
                current_requested_items = list(self.requested_items.all())

                if (set(existing_offered_items) == set(current_offered_items) and
                        set(existing_requested_items) == set(current_requested_items)):
                    raise ValidationError(
                        "A pending trade offer with the same items already exists between these users."
                    )

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None
        old_status = None

        if not is_new_instance:
            old_instance = InventoryTradeOffer.objects.filter(pk=self.pk).first()
            old_status = old_instance.status if old_instance else None

        super().save(*args, **kwargs)

        if old_status != self.status and self.status == 'accepted':
            self.handle_trade_offer_acceptance()
            with transaction.atomic():

                for item in self.offered_items.all():
                    item.user = self.receiver
                    item.save()

                for item in self.requested_items.all():
                    item.user = self.initiator
                    item.save()

        if is_new_instance:
            content_type = ContentType.objects.get_for_model(self)
            notification_message = f"You have received a trade offer from {self.initiator.username}."
            notification = Notification.objects.create(
                message=notification_message,
                content_type=content_type,
                object_id=self.id
            )
            notification.user.add(self.receiver)

        elif old_status and old_status != self.status:
            content_type = ContentType.objects.get_for_model(self)
            notification_message = (
                f"The status of your trade offer to {self.receiver.username} has been updated to '{self.status}'."
            )
            notification = Notification.objects.create(
                message=notification_message,
                content_type=content_type,
                object_id=self.id
            )
            notification.user.add(self.initiator)

        @receiver(m2m_changed, sender=InventoryTradeOffer.offered_items.through)
        @receiver(m2m_changed, sender=InventoryTradeOffer.requested_items.through)
        def calculate_final_cost(sender, instance, action, **kwargs):

            if action == "post_add":

                offered_total = sum(item.value for item in instance.offered_items.all() if item.value is not None)
                requested_total = sum(item.value for item in instance.requested_items.all() if item.value is not None)
                instance.final_cost = offered_total - requested_total

                instance.save(update_fields=['final_cost'])

    @transaction.atomic
    def handle_trade_offer_acceptance(self):
        if self.final_cost is not None and self.initiator.profiledetails.currency_amount >= self.final_cost:

            self.initiator.profiledetails.currency_amount += self.final_cost
            self.initiator.profiledetails.save()
            self.receiver.profiledetails.currency_amount -= self.final_cost
            self.receiver.profiledetails.save()
        else:
            raise ValueError("Insufficient funds for the trade.")


class TradeOfferManager(models.Manager):
    def get_queryset(self, user=None):
        queryset = super().get_queryset()
        if user:
            return queryset.filter(
                Q(initiator=user) | Q(receiver=user)
            ).select_related('initiator', 'receiver')
        return queryset


class CommerceExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usercard = models.ManyToManyField(TradeItem)
    total_usercard_value = models.IntegerField(blank=True, null=True)
    prizes = models.ManyToManyField(ExchangePrize)
    total_prize_value = models.IntegerField(blank=True, null=True)
    value_descrepancy = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):

        usercards_list = ", ".join([str(item) for item in self.usercard.all()])

        prizes_list = ", ".join([str(item) for item in self.prizes.all()])

        return f"{self.user} exchanged [{usercards_list}] for [{prizes_list}]"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.currency = first_currency
        self.total_usercard_value = self.usercard.aggregate(Sum('value'))['value__sum'] or 0
        self.total_prize_value = self.prizes.aggregate(Sum('value'))['value__sum'] or 0
        if not self.value_descrepancy:
            self.value_descrepancy = self.total_usercard_value - self.total_prize_value
            if self.value_descrepancy < 0:

                raise ValidationError(
                    "The value of your exchange cards needs to be at least the value of the selected prizes.")

            if self.value_descrepancy > 0:
                profile = ProfileDetails.objects.get(user=self.user)
                profile.currency_amount += self.value_descrepancy
                profile.save()

            super().save(*args, **kwargs)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Commerce Exchange"
        verbose_name_plural = "Commerce Exchanges"

class Notification(models.Model):
    user = models.ManyToManyField(User, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Notification: {self.message}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.user.all():
            created = UserNotification.objects.get_or_create(user=user, notification=self)
            print(f"Created UserNotification for {user.username}: {created}")

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="user_notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"UserNotification: {self.notification.message} for {self.user.username} - Read: {str(self.is_read)}"

    class Meta:
        verbose_name = "User Notification"

class VoteQuery(models.Model):
    """Used for voting on different new ideas"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=100,
                                help_text='Type the category that you are voting on (server layout, event idea, administration position, etc).')
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

class VoteOption(models.Model):
    vote_query = models.ForeignKey(VoteQuery, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)

class Ballot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_query = models.ForeignKey(VoteQuery, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(VoteOption, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vote_query')

class EmailField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(
        unique=True,
        help_text="Sign up for our newsletter to get the latest news and gossip! We will never share your personal information with anyone without your explicit permission. Unsubscribe at any time."
    )
    confirmation = models.BooleanField(
        help_text="By clicking this box, I agree to receive emails, coupons and discounts from PokeTrove. I also understand that I may unsubscribe at any time and PokeTrove will not share my personal information with anyone without my explicit permission."
    )
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def save(self, *args, **kwargs):

        if self.user:

            EmailField.objects.filter(user=self.user).exclude(pk=self.pk).delete()

        super().save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f"{self.user} {self.email}"
        return self.email

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

class Product(models.Model):
    """A product in the storefront"""
    name = models.CharField(max_length=200)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")
    description = models.TextField()
    label = models.CharField(choices=LABEL_CHOICES, max_length=1000, default='N')
    mfg_date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=1, choices=[('b', 'Bad'), ('a', 'Average'), ('e', 'Excellent')])

    def __str__(self):
        return self.name

    def show_desc(self):
        return self.description[:50]

class City(models.Model):
    """Not currently used. NEEDS TO BE DELETED"""
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class SearchResult(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

class StaffApplication(models.Model):
    """For applying for staff"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, help_text='Your full name goes here.')
    strikes_check = models.BooleanField(
        verbose_name="I have no strikes on my account currently",
        default=False,
        choices=((True, 'Yes'), (False, 'No'))
    )
    overall_time_check = models.BooleanField(
        verbose_name="I have been a user for at least 3 months.",
        default=False,
        choices=((True, 'Yes'), (False, 'No'))
    )
    previous_role_time_check = models.BooleanField(
        verbose_name="I already fulfill a role and wish to promote.",
        choices=((True, 'Yes'), (False, 'No'))
    )
    role = models.TextField(help_text='What role are you applying for?', verbose_name="Roles")
    resume = models.FileField(help_text='Your Resume', verbose_name="Resume")
    why = models.TextField(
        help_text='Tell us why you want to be an Accomfort Staff Member. Be descriptive.',
        verbose_name="Why do you want to apply for staff?"
    )
    how_better = models.TextField(
        help_text='Tell us what you will do to make Accomfort better as a staff member.',
        verbose_name="How do you think you can make PokeTrove better?"
    )
    read_requirements = models.BooleanField(
        verbose_name="I confirm that I have read all the staff requirements and meet all of them.",
        default=False,
        choices=((True, 'Yes'), (False, 'No'))
    )
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.role + " submitted by " + str(self.user)

    class Meta:
        verbose_name = "Staff Application"
        verbose_name_plural = "Staff Applications"


class CardCategory(models.Model):
    category = models.CharField(max_length=200)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Card Category"
        verbose_name_plural = "Card Categories"

class PartnerApplication(models.Model):
    """Application to partner with PokeTrove"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, help_text='Your first and last name.')
    category = models.ForeignKey(CardCategory, on_delete=models.CASCADE,
                                 help_text='What category are you applying to partner in? (if more than one, pick your main category and select the box below.)')
    multi_category = models.BooleanField(default=False,
                                         help_text="If you are applying to become a partner in more than 1 category, talk to Trove.")
    description = models.TextField(help_text='Describe yourself. What would entice buyers to play your games?')
    resume = models.FileField(help_text='Upload any accompying information to help streamline the selection process.')
    requirement_check = models.BooleanField(default=False, help_text="I have read and meet or exceed all requirements.")
    policy_check = models.BooleanField(default=False,
                                       help_text="I have read and understand the policies regarding partnership with PokeTrove. I also understand I may be liable if I break these policies..")
    voucher = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="voucher",
                                help_text="This is optional but can help streamline the selection process.")
    accepted = models.BooleanField(default=False)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    class Meta:
        verbose_name = "Partner Application"
        verbose_name_plural = "Partner Applications"

    def __str__(self):
        return self.user + "applicaton for " + self.category


class PunishmentAppeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Your name and tag go here.')
    Rule_broken = models.CharField(max_length=200,
                                   help_text='Tell us the numbers of the rule(s) you broke. Refer to our rules page to see the rules and their corresponding numbers.',
                                   verbose_name="rule broken")
    Why_I_should_have_my_punishment_revoked = models.TextField(
        help_text='Tell us why we should revoke your punishment, and what you can do to fix your mistake. If you think your punishment is a mistake, tell us why.',
        verbose_name="Why I should have my punishment revoked")
    Additional_comments = models.TextField(help_text='Put any additional evidence or comments you may have here.',
                                           verbose_name="additional comments")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.Why_I_should_have_my_punishment_revoked + " submitted by " + str(self.user)

    class Meta:
        verbose_name = "Punishment Appeal"
        verbose_name_plural = "Punishment Appeals"

class BanAppeal(models.Model):
    name = models.CharField(max_length=100, help_text='Your name and tag go here.')
    Rule_broken = models.CharField(max_length=200,
                                   help_text='Tell us the numbers of the rule(s) you broke. Refer to our rules page to see the rules and their corresponding numbers.')
    Why_I_should_have_my_ban_revoked = models.TextField(
        help_text='Tell us why we should unban you, and tell us you can do to fix your mistake. If you think your punishment is a mistake, tell us why.',
        verbose_name="Why I should have my ban revoked.")
    Additional_comments = models.TextField(
        help_text='Put any additional evidence or comments you may have here.')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.Why_I_should_have_my_ban_revoked + " submitted by " + str(self.name)

    class Meta:
        verbose_name = "Ban Appeal"
        verbose_name_plural = "Ban Appeals"

class ReportIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,
                            help_text='Your name and tag go here. If you wish to stay anonymous, put "Anonymous".')
    category = models.CharField(max_length=200, help_text='Please let us know what type of issue this is.')
    issue = models.TextField(help_text='Describe the issue in detail. We will try to get to it as soon as possible.')
    Additional_comments = models.TextField(help_text='Put any additional comments you may have here.',
                                           verbose_name="additional comments")
    image = models.ImageField(help_text='Please put a screenshot of the issue.')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    anonymous = models.BooleanField(default=False, help_text="Report issue anonymously?")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.issue + " reported by " + str(self.user)

    class Meta:
        verbose_name = "Report Issue"
        verbose_name_plural = "Report Issues"

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])


class ChangeLog(models.Model):
    ACTION_CHOICES = [
        ('update', 'Update'),
        ('maintenance', 'Maintenance'),
        ('bugfix', 'Bugfix'),
        ('urgent', 'Urgent'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    action = models.CharField(max_length=11, choices=ACTION_CHOICES)
    object_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    changes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.action} {self.object_id} at {self.timestamp}'

    def save_with_user(self, user, *args, **kwargs):
        if not self.user:
            self.user = user
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Changelog"
        verbose_name_plural = "Changelogs"


class AdministrationChangeLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=6, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    changes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.action} {self.model} {self.object_id} at {self.timestamp}'

    class Meta:
        verbose_name = "Administration Changelog"
        verbose_name_plural = "Administration Changelogs"


class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    issue = models.TextField()
    Additional_comments = models.TextField(verbose_name="additional comments")
    image = models.ImageField(help_text='Please attach a screenshot of your issue.', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.issue + " submitted by " + str(self.user)

    class Meta:
        verbose_name = "Customer Support"
        verbose_name_plural = "Customer Support"

class NewsFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,
                            help_text='Your name and tag go here. If you wish to stay anonymous, put "Anonymous".')
    title = models.TextField(help_text='Write the news headline here.', verbose_name="News Headline")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    category = models.CharField(max_length=200, help_text='Please let us know what form of news this is.')
    description = models.TextField(help_text='Write the news here.')
    image = models.ImageField(help_text='Please provide a cover image for the news.')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    date_and_time = models.DateTimeField(null=True, verbose_name="time and date", auto_now_add=True)
    position = models.IntegerField(verbose_name="Image Position", default=1)
    anonymous = models.BooleanField(default=False, help_text="Remain anonymous? (not recommended)")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title + " authored by " + str(self.user)

    class Meta:
        verbose_name = "News Feed"
        verbose_name_plural = "News Feed"

    def save(self, *args, **kwargs):
        if not self.slug:
            print("Name:", self.name)
            self.slug = slugify(self.name)
            print("Slug after slugify:", self.slug)

        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.user).first()

        print("Position before save:", self.position)
        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_profile_url2(self):
        news = NewsFeed.objects.filter(user=self.user, slug=self.slug).first()
        if news:
            return reverse('showcase:singlenews', args=[str(news.slug)])

class StaffProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,
                            help_text='Your name goes here. If you wish to stay anonymous, put "Anonymous".')
    role_position = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Position")
    description = models.TextField(help_text='Write whatever you want on your profile here (within regulations).')
    staff_feats = models.TextField(
        help_text='Let us know of your transcendental feats of making PokeTrove a better place.',
        verbose_name="Staff feats")
    date_and_time = models.DateTimeField(null=True, verbose_name="Time and date of Staff Profile Creation")
    image = models.ImageField(help_text='Please provide a cover image for your profile.')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.user).first()

            if profile:
                self.position = profile.position

        try:
            existing = StaffProfile.objects.get(user=self.user)
            self.pk = existing.pk
        except StaffProfile.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

class SocialMedia(models.Model):
    social = models.TextField(verbose_name="Social Media Platform", help_text="Follow format 'logo-{platform name}'",
                              blank=True, null=True)
    icon = models.ImageField(verbose_name="Social Media Logo", blank=True, null=True)
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Width of the image (in percent relative).',
                                              verbose_name="image width")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Length of the image (in percent relative).',
                                               verbose_name="image length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resize Width")
    height_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resize Height")
    image_position = models.IntegerField(help_text='Positioning of the image.', verbose_name='Position', blank=True,
                                         null=True)
    alternate = models.TextField(verbose_name="Alternate Text", blank=True, null=True)
    page = models.TextField(verbose_name="Page Name")
    hyperlink = models.URLField(verbose_name="Hyperlink")
    staff_profile = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.social + " in " + self.page

    def save(self, *args, **kwargs):
        if not self.page.endswith('.html'):
            self.page += '.html'
        if not self.pk:
            self.image_position = SocialMedia.objects.filter(page=self.page).count() + 1
        if self.icon and not self.alternate:
            self.alternate = str(self.icon)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"

class FrequentlyAskedQuestions(models.Model):
    question = models.TextField()
    position = models.IntegerField(help_text='Positioning of the image within the carousel.',
                                   verbose_name='position', default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Frequently-Asked Question"
        verbose_name_plural = "Frequently-Asked Questions"


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Event name goes here.')
    category = models.CharField(max_length=200,
                                help_text='Please let us know what type of event this is (tournament, stage night, etc).')
    numeric_quantifier = models.FloatField()
    qualitative_qualifier = models.CharField(max_length=500)
    description = models.TextField(help_text='Give a brief description of the event.')
    date = models.DateField(null=True, help_text='Event date (day, date, and month)')
    time = models.TimeField(null=True, help_text='Event time (hour/minute)')
    date_and_time = models.DateTimeField(null=True, verbose_name="Time and date of Event Creation")
    section = models.IntegerField(verbose_name="Page Section", blank=True, null=True)
    page = models.TextField(verbose_name="Page Name")
    slug = models.SlugField(unique=True)
    anonymous = models.BooleanField(default=False, help_text="Remain anonymous? (not recommended)")
    image = models.ImageField(help_text='Please provide a cover image for the event.', upload_to='images/')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.name + " hosted by " + str(self.user)

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.user).first()
            self.section = Event.objects.filter(page=self.page).count() + 1

            if profile:
                self.position = profile.position
        super().save(*args, **kwargs)

    def get_profile_url(self):
        return reverse('showcase:eventmore', args=[str(self.slug)])

    def get_profile_url2(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])


class Season(models.Model):
    name = models.CharField(max_length=100, help_text='Season name goes here.')
    season_length = models.PositiveIntegerField(help_text='In days')
    description = models.TextField(help_text='Give a brief description of the event.')
    date = models.DateField(null=True, blank=True, help_text='Season date (day, date, and month)')
    time = models.TimeField(null=True, blank=True, help_text='Season time (hour/minute)')
    date_and_time = models.DateTimeField(auto_now_add=True,
                                           verbose_name="Creation time")
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='images/', help_text='Cover image')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                                  help_text='Original length for ratio')
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                                  help_text='Original width for ratio')
    date_and_time = models.DateTimeField(auto_now_add=True)
    season_length = models.PositiveIntegerField(help_text='In days')

    # new, real DB field
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        now     = timezone.now()
        ends_at = self.date_and_time + timedelta(days=self.season_length)
        should  = (self.date_and_time <= now < ends_at)

        if should != self.active:
            Season.objects.filter(pk=self.pk).update(active=should)
        if should:
            Season.objects.exclude(pk=self.pk).filter(active=True).update(active=False)

    @property
    def end_datetime(self):
        if not self.date_and_time:
            return None
        return self.date_and_time + datetime.timedelta(days=self.season_length)

    @property
    def is_active(self):
        if not self.date_and_time:
            return False
        now = timezone.now()
        return self.date_and_time <= now < self.end_datetime

    def get_profile_url(self):
        return reverse('showcase:eventmore', args=[self.slug])

    def get_profile_url2(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])


class BusinessMessageBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Business Message Background Image"
        verbose_name_plural = "Business Message Background Images"


class MemberHomeBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Member Home Background Image"
        verbose_name_plural = "Member Home Background Images"

class PatreonBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Patreon Background Image"
        verbose_name_plural = "Patreon Background Images"

class Partner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Your username goes here.')
    category = models.CharField(max_length=100,
                                help_text='Pick a category you feel your server represents (gaming, community, etc).')
    description = models.TextField(help_text='Describe your server. Tell potential members why they should join.')
    server_invite = models.URLField(help_text='Post your server invite link here.')
    anonymous = models.BooleanField(default=False, help_text="Remain anonymous? (not recommended)")

    def __str__(self):
        return str(self.user) + " " + self.server_invite

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

class Patreon(models.Model):
    patreon_username = models.CharField(max_length=100, verbose_name='Patreon`s Username',
                                        help_text='The patreon`s username goes here.')
    description = models.TextField(help_text='Description of Patreon`s patreonage.')
    image = models.ImageField(
        help_text=
        'The patreon`s avatar goes here.')

    class Meta:
        verbose_name = "Patreon"
        verbose_name_plural = "Patreons"

class BlogHeader(models.Model):
    category = models.CharField(max_length=200, verbose_name="Category")
    image = models.ImageField(upload_to='images/')
    position = models.IntegerField(verbose_name="Position", default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Blog Header"
        verbose_name_plural = "Blog Headers"

    def __str__(self):
        return self.category


from django.template.defaultfilters import slugify, date, register


class BlogFilter(models.Model):
    blog_filter = models.CharField(verbose_name="Hashtag filters", max_length=200, blank=True, null=True)
    clicks = models.IntegerField(verbose_name="Popularity", blank=True, null=True)
    image = models.ImageField(verbose_name="Filter Image", blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.blog_filter

    class Meta:
        verbose_name = "Blog Filter"
        verbose_name_plural = "Blog Filters"

class Blog(models.Model):
    """Each blog post"""
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    type = models.CharField(choices=BLOG_TYPE_CHOICES, max_length=2, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True, verbose_name="updated on: ")
    content = models.TextField()
    filters = models.ForeignKey(BlogFilter, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Hashtag filters")
    created_on = models.DateTimeField(auto_now_add=True)
    position = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(BlogHeader, verbose_name="Category", on_delete=models.CASCADE, blank=True, null=True,
                                 help_text="Optional")
    minute_read = models.IntegerField(verbose_name="Time to read (in minutes)", blank=True, null=True)
    status = models.IntegerField(choices=((0, "Draft"), (1, "Publish")), default=0)
    image = models.ImageField(upload_to='images/')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    likes = models.ManyToManyField(User, blank=True, verbose_name='post likes')

    dislikes = models.ManyToManyField(User, blank=True, verbose_name='post dislikes', related_name="post_dislikes")

    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)

        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.author_id).first()

            if profile:
                self.position = profile.position
            max_position = Blog.objects.all().aggregate(Max('position'))['position__max']
            if max_position is None:
                self.position = 1
            else:
                self.position = max_position + 1
        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.author_id).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("showcase:post_detail", kwargs={"slug": str(self.slug)})

    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    def view_count(self):
        return Blog.objects.filter(post=self).count()

    def delete(self, *args, **kwargs):

        blogs_to_update = Blog.objects.filter(position__gt=self.position)

        super().delete(*args, **kwargs)

        for i, blog in enumerate(blogs_to_update.order_by('position')):
            blog.position = self.position + i
            blog.save()


class BlogTips(models.Model):
    tip = models.TextField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_tips', blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="updated on: ")
    position = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_position = BlogTips.objects.filter(author=self.author).aggregate(models.Max('position'))[
                'position__max']
            self.position = (max_position or 0) + 1

        super(BlogTips, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.tip)

    class Meta:
        verbose_name = "Blog Tip"
        verbose_name_plural = "Blog Tips"

class ShuffleType(models.Model):
    name = models.CharField(default="Pack Opening", max_length=200)
    type = models.CharField(choices=SHUFFLE_CHOICES, default='L',
                            max_length=1)
    circumstance = models.CharField(choices=AVALIABLE_CHOICES, default='OP', max_length=3)
    game_mode = models.CharField(choices=GAME_MODE, default="STP", max_length=3)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Shuffle Type"
        verbose_name_plural = "Shuffle Types"

class DailySpin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_spins")
    cooldown = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'cooldown')

    def __str__(self):
        return f"{self.user.username} - {self.cooldown}"


class GameHub(models.Model):
    name = models.CharField(max_length=200, verbose_name="Game Hub Name")
    type = models.CharField(choices=GAMETYPE, max_length=1, blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    filter = models.CharField(choices=GAMEHUB_CHOICES, max_length=1, blank=True, null=True)
    description = models.CharField(max_length=2000)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    date_and_time = models.DateTimeField(null=True, verbose_name="date and time", auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Game Hub"
        verbose_name_plural = "Game Hub"


class Game(models.Model):
    name = models.CharField(max_length=200, verbose_name="Game Name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.IntegerField(default=0, blank=True, null=True)
    discount_cost = models.IntegerField(blank=True, null=True)
    heat = models.CharField(choices=HEAT, max_length=2, blank=True, null=True)
    type = models.ForeignKey(GameHub, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=2,
                                choices=CARD_CATEGORIES, blank=True, null=True)
    choices = models.ManyToManyField(
        'Choice',
        through='GameChoice',
        blank=True,
        related_name="api_set_cards"
    )
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    power_meter = models.CharField(choices=POWER, max_length=4, default=1)
    items = models.ManyToManyField(PrizePool, related_name='official_items', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    filter = models.CharField(choices=GAMEHUB_CHOICES, max_length=1, blank=True, null=True)
    player_made = models.BooleanField(default=True)
    player_inventory = models.BooleanField(default=True)
    date_and_time = models.DateTimeField(null=True, verbose_name="date and time", auto_now_add=True)
    daily = models.BooleanField(default=False)
    unlocking_level = models.OneToOneField(Level, blank=True, null=True, on_delete=models.CASCADE)
    cooldown = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    def clean(self):
        """Ensure player_made & daily cannot both be True."""
        if self.player_made and self.daily:
            raise ValidationError("A game cannot be both player-made and daily.")
        if self.daily and not self.unlocking_level:
            raise ValidationError("An unlocking level must be set for daily games.")

    def get_absolute_url(self):
        return reverse("showcase:game", kwargs={'slug': self.slug})

    def increase_on_card(self):
        if self.cost:
            self.cost = self.cost * 1.05

    def is_favorited(self, user):
        from django.db.models import Q
        return FavoriteChests.objects.filter(user=user, chest=self, is_active=1).exists()

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.type:
            first_gamehub = GameHub.objects.first()
            if first_gamehub:
                self.type = first_gamehub

        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 0
            while Game.objects.filter(slug=slug).exists():
                num += 1
                slug = f"{base_slug}-{num}"
            self.slug = slug

        if self.daily and not self.discount_cost:
            self.discount_cost = 0
        super().save(*args, **kwargs)

        total_cost = 0
        if self.choice_fk_set.exists():
            for choice in self.choice_fk_set.all():
                if choice.value and choice.rarity:
                    choice_cost = (choice.value * float(choice.rarity)) / 100
                    total_cost += choice_cost

                    if not self.heat and (total_cost or self.discount_cost):
                        total_lower_rarity = 0
                        total_lower_value = 0
                        total_upper_rarity = 0
                        total_upper_value = 0
                        if choice.value < total_cost:
                            lower_rarity = choice.rarity / 100
                            lower_value = choice.value / total_cost
                            total_lower_rarity += lower_rarity
                            total_lower_value += lower_value
                        else:
                            upper_rarity = choice.rarity / 100
                            upper_value = choice.value / total_cost
                            total_upper_rarity += upper_rarity
                            total_upper_value += upper_value

                        if total_lower_rarity * total_lower_value < 1:
                            self.heat = 'M'
                        if total_lower_rarity * total_lower_value < 1:
                            self.heat = 'S'
                        if total_lower_rarity * total_lower_value < 1:
                            self.heat = 'F'
                        if total_lower_rarity * total_lower_value < 1:
                            self.heat = 'W'
                        if total_lower_rarity * total_lower_value < 1:
                            self.heat = 'E'
            self.cost = int(total_cost * 1.12)
            print('the cost was edited')

        pst = pytz.timezone('US/Pacific')
        current_time_pst = now().astimezone(pst)
        today = current_time_pst.date()
        today_5pm_pst = make_aware(datetime.combine(today, time(17, 0)), pst)

        if current_time_pst < today_5pm_pst:
            cycle_start = today_5pm_pst - timedelta(days=1)
        else:
            cycle_start = today_5pm_pst

        if not self.cooldown or self.cooldown < cycle_start:
            self.cooldown = cycle_start + timedelta(days=1)

        if self.daily:
            self.locked = not (current_time_pst >= self.cooldown)

        super().save(*args, **kwargs)

    def _get_pst_time(self):
        """Get the current time in PST and determine today's 5 PM PST."""
        pst = pytz.timezone('US/Pacific')
        current_time_pst = now().astimezone(pst)
        today = current_time_pst.date()
        today_5pm_pst = make_aware(datetime.combine(today, time(17, 0)), pst)

        if current_time_pst < today_5pm_pst:
            cycle_start = today_5pm_pst - timedelta(days=1)
        else:
            cycle_start = today_5pm_pst

        return cycle_start, current_time_pst

    def spin_daily(self, user):
        """
        Allow the user to spin the daily chest if they haven't spun during the current cycle.
        """
        if not self.daily:
            raise ValueError("This game is not configured as daily.")

        cycle_start, current_time_pst = self._get_pst_time()

        existing_spin = DailySpin.objects.filter(user=user, cooldown=cycle_start).first()

        if existing_spin:
            raise ValueError("You have already spun the chest for today. Come back after 5:00 PM PST!")

        DailySpin.objects.create(user=user, cooldown=cycle_start)

        print(f"{user.username} spun the daily chest successfully!")

        self.cooldown = cycle_start + timedelta(days=1)
        self.locked = True
        self.save()

    def is_user_locked(self, user):
        """
        Check if a user is locked from spinning the chest.
        """
        cycle_start, _ = self._get_pst_time()
        return DailySpin.objects.filter(user=user, cooldown=cycle_start).exists()

    def check_locked_status(self, user):
        if self.daily and self.unlocking_level:

            if user.level.level >= self.unlocking_level.level:
                self.locked = False
            else:
                self.locked = True
        return self.locked

    def get_time_until_5pm(self):
        """
        Calculate the remaining time until 5:00 PM today.
        Only activates if locked is True.
        """
        if not self.locked:
            return timedelta(seconds=0)

        current_time = now()

        today_5pm = current_time.replace(hour=17, minute=0, second=0, microsecond=0)

        if current_time >= today_5pm:
            today_5pm += timedelta(days=1)

        remaining_time = today_5pm - current_time
        return remaining_time

    def get_time_until_5pm_formatted(self):
        remaining_time = self.get_time_until_5pm()
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"

    def get_color(self, choice):
        thresholds = {
            "gray": self.cost * 0.8,
            "green": self.cost,
            "yellow": self.cost * 2,
            "orange": self.cost * 5,
            "red": self.cost * 100,
            "black": self.cost * 1000,
            "redblack": self.cost * 1000000,
        }

        if choice.value is None:
            choice.value = random.randint(0, 1000000)

        for color, threshold in thresholds.items():
            if choice.value <= threshold:
                return color

        return 'redgold'

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_profile_url2(self):
        return reverse('showcase:game', args=[str(self.slug)])

    def get_effective_cost(self):
        """Return the discount cost if available, otherwise the regular cost."""
        return self.discount_cost if self.discount_cost else self.cost

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

class GameChoice(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    choice = models.ForeignKey('Choice', on_delete=models.CASCADE)
    number = models.IntegerField(
        help_text="Position ordered by value (from highest to lowest)",
        blank=True, null=True, default=1
    )
    total_number = models.IntegerField(
        help_text="Position ordered by value (from highest to lowest)",
        blank=True, null=True, default=1
    )
    value = models.IntegerField(blank=True, null=True)
    rarity = models.DecimalField(max_digits=9, decimal_places=6, help_text="Rarity of choice in percent (optional).",
                                 blank=True, null=True,
                                 verbose_name="Rarity (%)")
    lower_nonce = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
        help_text="Lower bound nonce of Choice", blank=True, null=True
    )
    upper_nonce = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
        help_text="Upper bound nonce of Choice"
    )

    class Meta:
        unique_together = (('game', 'choice'),)

    def save(self, *args, **kwargs):

        if not self.pk and self.game:
            existing_choices = Choice.objects.filter(game=self.game).count()
            existing_gamechoices = GameChoice.objects.filter(game=self.game).count()

            self.number = existing_choices + existing_gamechoices + 1

        if self.number:
            last_choice = Choice.objects.filter(game=self.game, number=self.number-1).first()
            last_gamechoice = GameChoice.objects.filter(game=self.game, number=self.number-1).first()
            if last_choice:
                self.lower_nonce = last_choice.upper_nonce + 1
            elif last_gamechoice:
                self.lower_nonce = last_gamechoice.upper_nonce + 1
            else:
                pass

        if self.upper_nonce and self.lower_nonce:
            self.rarity = (self.upper_nonce - self.lower_nonce) / 10000

        if not self.choice.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.choice.currency = first_currency

        if self.upper_nonce is not None:
            if self.upper_nonce % 10 == 0:
                print("The last digit of upper_nonce is 0")
                if self.upper_nonce > 0 and self.upper_nonce != 1000000:
                    self.upper_nonce -= 1

        if self.upper_nonce is None:
            self.upper_nonce = random.randint(0, 1000000)

        if self.upper_nonce is not None and self.lower_nonce is not None:
            rarity_value = (self.upper_nonce - self.lower_nonce) / 10000
            self.rarity = round(rarity_value, 6)

        if not self.value and self.choice.value:
            self.value = self.choice.value
        print('save committed of gamechoice')
        super().save(*args, **kwargs)


class Choice(models.Model):
    """Used for voting on different new ideas"""
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, verbose_name='Name', blank=True, null=True)
    file = models.FileField(null=True, verbose_name='File', blank=True)
    image_length = models.PositiveIntegerField(
        blank=True, null=True, default=100,
        help_text='Original length of the advertisement (use for original ratio).',
        verbose_name="image length"
    )
    image_width = models.PositiveIntegerField(
        blank=True, null=True, default=100,
        help_text='Original width of the advertisement (use for original ratio).',
        verbose_name="image width"
    )
    color = models.CharField(choices=COLOR, max_length=6, blank=True, null=True)
    votes = models.IntegerField(default=0)
    category = models.CharField(max_length=2,
                                choices=CARD_CATEGORIES, blank=True, null=True)
    midcategory = models.CharField(max_length=200, help_text='Middle category of choice.',
                                   blank=True, null=True)
    subcategory = models.CharField(max_length=200, help_text='Subcategory of choice (Pokemon, trainers, etc.).',
                                   blank=True, null=True)
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    tier = models.CharField(choices=LEVEL, max_length=1, blank=True, null=True)
    rarity = models.DecimalField(
        max_digits=9, decimal_places=6,
        help_text="Rarity of choice in percent (optional).",
        blank=True, null=True,
        verbose_name="Rarity (%)"
    )
    prizes = models.ForeignKey(PrizePool, on_delete=models.CASCADE, blank=True, null=True)
    shufflers = models.ForeignKey(Shuffler, on_delete=models.CASCADE, blank=True, null=True)
    condition = models.CharField(choices=CONDITION_CHOICES, default="M", max_length=2, blank=True, null=True)
    number_of_choice = models.IntegerField(default=1)
    total_number_of_choice = models.IntegerField(blank=True, null=True)
    lower_nonce = models.IntegerField(
        validators=[MaxValueValidator(1000000), MinValueValidator(0)],
        help_text="Lower bound nonce of Choice",
        blank=True, null=True
    )
    upper_nonce = models.IntegerField(
        validators=[MaxValueValidator(1000000), MinValueValidator(0)],
        help_text="Upper bound nonce of Choice",
        blank=True, null=True
    )
    generated_nonce = models.IntegerField(
        validators=[MaxValueValidator(1000000), MinValueValidator(0)],
        help_text="Do NOT fill out manually.",
        blank=True, null=True,
        verbose_name='Generated Nonce'
    )
    nodes = models.IntegerField(
        help_text="Number of the choice included", blank=True, null=True,
        verbose_name="Quantity Displayed"
    )
    value = models.IntegerField(
        help_text="Value of item in Rubies.", blank=True, null=True,
        verbose_name="Value (Rubies)"
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    number = models.IntegerField(
        help_text="Position ordered by value (from highest to lowest)",
        blank=True, null=True, default=1
    )
    total_number = models.IntegerField(
        help_text="Position ordered by value (from highest to lowest)",
        blank=True, null=True, default=1
    )

    card_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    supertype = models.CharField(max_length=50, null=True, blank=True)
    subtypes = models.CharField(max_length=100, null=True, blank=True)
    hp = models.CharField(max_length=10, null=True, blank=True)
    types = models.CharField(max_length=100, null=True, blank=True)
    evolves_to = models.CharField(max_length=100, null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    attacks = models.TextField(null=True, blank=True)
    weaknesses = models.TextField(null=True, blank=True)
    retreat_cost = models.CharField(max_length=50, null=True, blank=True)
    set_name = models.CharField(max_length=100, null=True, blank=True)
    set_series = models.CharField(max_length=100, null=True, blank=True)
    set_release_date = models.DateField(null=True, blank=True)
    image_small = models.URLField(null=True, blank=True)
    image_large = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.IntegerField(
        default=1, blank=True, null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='choice_fk_set',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.total_number_of_choice and self.number_of_choice:
            if self.total_number_of_choice != 1:
                self.rarity = (Decimal(self.number_of_choice) / Decimal(self.total_number_of_choice)) * Decimal(100)
            else:
                self.rarity = Decimal(0)

        if not self.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.currency = first_currency

        if not self.pk and self.game:
            existing_choices = Choice.objects.filter(game=self.game).count()
            existing_gamechoices = GameChoice.objects.filter(game=self.game).count()

            self.number = existing_choices + existing_gamechoices + 1

        if self.upper_nonce is not None:
            if self.upper_nonce % 10 == 0:
                print("The last digit of upper_nonce is 0")
                if self.upper_nonce > 0 and self.upper_nonce != 1000000:
                    self.upper_nonce -= 1

        if self.upper_nonce is None:
            self.upper_nonce = random.randint(0, 1000000)

        if self.upper_nonce is not None and self.lower_nonce is not None:
            rarity_value = (self.upper_nonce - self.lower_nonce) / 10000
            self.rarity = round(rarity_value, 6)

        if not self.choice_text and self.name:
            self.choice_text = self.name
        if not self.subcategory and self.subtypes:
            self.subcategory = self.subtypes
        if self.image_large and not self.file:
            try:
                response = requests.get(self.image_large, stream=True)
                if response.status_code == 200:
                    file_name = self.image_large.split("/")[-1]
                    self.file.save(file_name, ContentFile(response.content), save=False)
            except requests.RequestException:
                pass

        elif self.image_small and not self.file:
            try:
                response = requests.get(self.image_small, stream=True)
                if response.status_code == 200:
                    file_name = self.image_small.split("/")[-1]
                    self.file.save(file_name, ContentFile(response.content), save=False)
            except requests.RequestException:
                pass

        if self.pk:
            previous = Choice.objects.filter(pk=self.pk).only('value').first()
            if previous and previous.value != self.value:
                self.value = self.value + self.value * Decimal('0.05')
                print('value updated')
        super().save(*args, **kwargs)

    def __str__(self):
        if self.prizes:
            return f"{self.choice_text} with prize {self.prizes}"
        else:
            if self.price:
                cost_value =  self.price
            else:
                cost_value =  self.value

            return f"{self.choice_text} (Value: {cost_value})"

    def asave(self):
        if self.value:
            self.value = self.value * Decimal('1.05')
        elif self.price:
            self.value = self.price * Decimal('1.05')
        self.save()

    def formatted_rarity(self):
        if self.rarity is not None:
            return str(self.rarity).rstrip('0').rstrip('.') if '.' in str(self.rarity) else str(self.rarity)
        return None

    @classmethod
    def get_choice_by_nonce(cls, nonce):
        try:
            return cls.objects.get(Q(lower_nonce__lte=nonce) & Q(upper_nonce__gte=nonce))
        except cls.DoesNotExist:
            return None

    def returned_nonce(self):
        self.nonce = random.randint(0, 1000000)
        return self.nonce

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"


# app/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.utils import timezone

# Lookups populated from API
class Supertype(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Subtype(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class CardSet(models.Model):
    # Use API id (e.g., "swsh1") as primary key for stability
    id = models.CharField(primary_key=True, max_length=50)     # API set id
    name = models.CharField(max_length=100)
    series = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)     # from API releaseDate
    def __str__(self): return f"{self.name} ({self.series})"

class Card(models.Model):
    # Core identifiers
    card_id = models.CharField(max_length=50, unique=True)     # API card id (e.g., "swsh1-1")
    name = models.CharField(max_length=200)

    # Categorical / relations (choices from API-backed tables)
    supertype = models.ForeignKey(Supertype, null=True, blank=True, on_delete=models.SET_NULL)
    subtypes = models.ManyToManyField(Subtype, blank=True)
    types = models.ManyToManyField(Type, blank=True)

    # Set info (normalized + denormalized for convenience)
    set = models.ForeignKey(CardSet, null=True, blank=True, on_delete=models.SET_NULL)
    set_name = models.CharField(max_length=100, blank=True)
    set_series = models.CharField(max_length=100, blank=True)
    set_release_date = models.DateField(null=True, blank=True)

    # Card details
    hp = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    evolves_to = ArrayField(models.CharField(max_length=100), blank=True, default=list)

    # Textual / rules content (store raw JSON blobs from API)
    rules = models.JSONField(blank=True, null=True)            # list[str]
    attacks = models.JSONField(blank=True, null=True)          # list[dict]
    weaknesses = models.JSONField(blank=True, null=True)       # list[dict]
    retreat_cost = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    # Pricing (simple single number; you can expand as needed)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Images
    image_small = models.URLField(blank=True)
    image_large = models.URLField(blank=True)

    # Bookkeeping
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return f"{self.card_id} — {self.name}"


class TopHits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(choices=COLOR, max_length=6, blank=True, null=True)
    file = models.FileField(null=True, verbose_name='File')
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    button_pressed = models.CharField(max_length=10)
    demonstration = models.BooleanField(default=False)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f'{self.user} - {self.game} - {self.choice} - {self.color} - {self.mfg_date}'

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = self.choice.color
        if not self.file:
            self.file = self.choice.file
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Top Hit"

class SpinPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="spinpreferer")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    quick_spin = models.BooleanField(default=False)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Spin Preference"
        verbose_name_plural = "Spin Preferences"

class Outcome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="player")
    quick_spin = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='nonce', unique=True)
    value = models.IntegerField(blank=True, null=True)
    ratio = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(GameHub, on_delete=models.CASCADE)
    file = models.FileField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    color = models.CharField(choices=COLOR, max_length=6, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="creator")
    green_counter = models.IntegerField(blank=True, null=True, default=0)
    yellow_counter = models.IntegerField(blank=True, null=True, default=0)
    orange_counter = models.IntegerField(blank=True, null=True, default=0)
    red_counter = models.IntegerField(blank=True, null=True, default=0)
    black_counter = models.IntegerField(blank=True, null=True, default=0)
    gold_counter = models.IntegerField(blank=True, null=True, default=0)
    redgold_counter = models.IntegerField(blank=True, null=True, default=0)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    nonce = models.DecimalField(max_digits=7, decimal_places=0)
    date_and_time = models.DateTimeField(null=True, verbose_name="date and time", auto_now_add=True)
    demonstration = models.BooleanField(default=False)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f'{self.user} - {self.game} - {self.choice} - Nonce: {self.nonce}  - Color: {self.color} - {self.date_and_time}'

    def generate_nonce(self):
        return random.randint(0, 1000000)

    def save(self, *args, **kwargs):
        if not self.color and self.choice:
            self.color = self.choice.color
        if not self.slug and self.choice:
            self.slug = slugify(self.choice)
        if not self.nonce:
            self.nonce = random.randint(0, 1000000)
        if not self.game_creator:
            self.game_creator = self.game.user
        if not self.file:
            self.file = self.choice.file
        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_color(self, choice):
        cost_threshold_80 = self.game.cost * 0.8
        cost_threshold_100 = self.game.cost
        cost_threshold_200 = self.game.cost * 2
        cost_threshold_500 = self.game.cost * 5
        cost_threshold_10000 = self.game.cost * 100
        cost_threshold_100000 = self.game.cost * 1000
        cost_threshold_100000000 = self.game.cost * 1000000

        if choice.game.value is None:
            choice.value = random.randint(0, 1000000)

        if choice.game.value >= cost_threshold_100000000:
            self.redgold_counter += 1
            return 'redgold'
        elif choice.game.value >= cost_threshold_100000:
            self.gold_counter += 1
            return 'redblack'
        elif choice.game.value >= cost_threshold_10000:
            self.black_counter += 1
            return 'black'
        elif choice.game.value >= cost_threshold_500:
            self.red_counter += 1
            return 'red'
        elif choice.game.value >= cost_threshold_200:
            self.orange_counter += 1
            return 'orange'
        elif choice.game.value >= cost_threshold_100:
            self.yellow_counter += 1
            return 'yellow'
        elif choice.game.value >= cost_threshold_80:
            self.green_counter += 1
            return 'green'
        else:
            return 'gray'

class Achievements(models.Model):
    user = models.ManyToManyField(User, related_name="achiever", blank=True)
    title = models.TextField(verbose_name="Achievement Title")
    description = models.TextField(verbose_name="Description")
    difficulty = models.CharField(choices=HEAT, default='M', max_length=1)
    slug = AutoSlugField(populate_from='title', unique=True)
    value = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    rubies_spent = models.IntegerField(blank=True,
                                       null=True)
    rubies_collected = models.IntegerField(blank=True,
                                           null=True)
    total_rubies_earned = models.IntegerField(blank=True,
                                              null=True)
    type = models.ForeignKey(GameHub, on_delete=models.CASCADE)
    category = models.CharField(choices=AchievementCategory, max_length=4, blank=True, null=True)
    earned = models.BooleanField(default=False)
    green_counter = models.IntegerField(blank=True, null=True, default=0)
    yellow_counter = models.IntegerField(blank=True, null=True, default=0)
    orange_counter = models.IntegerField(blank=True, null=True, default=0)
    red_counter = models.IntegerField(blank=True, null=True, default=0)
    black_counter = models.IntegerField(blank=True, null=True, default=0)
    gold_counter = models.IntegerField(blank=True, null=True, default=0)
    redgold_counter = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f"{self.title}"

    def get_card_images(self):
        if self.image:
            images = self.image.url
            return images

    def check_and_add_user(self, user):
        """
        Check if the user fulfills the requirements for this achievement and add them to the user field.
        """

        if self.requirement_fulfilled(user):
            self.user.add(user)
            self.earned = True
            self.save()

    def save(self, *args, **kwargs):

        if not self.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.currency = first_currency
        if not self.type:
            first_type = GameHub.objects.first()
            if first_type:
                self.type = first_type
        if self.category == 'RS':
            rubies_spent = self.rubies_spent
            self.description = "Spend " + str(self.rubies_spent) + " Rubies"
        super().save(*args, **kwargs)

    def calculate_rubies_spent(self):
        if self.AchievementCategory == 'RS':
            profile = self.user.profiledetails
            rubies_spent = profile.total_currency_spent
            self.rubies = rubies_spent
            self.description = f"Spend {rubies_spent} Rubies"
            self.save()

        elif self.AchievementCategory == 'TRE':
            profile = self.user.profiledetails
            rubies_collected = profile.total_currency_amount
            self.description = f"Spend {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'RC':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Spend {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'WS':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Spend {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'GCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Spend {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'YCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Spend {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'OCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Hit {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'RCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Hit {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'BCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Hit {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'GCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Hit {rubies_collected} Rubies"
            self.save()

        elif self.AchievementCategory == 'RGCH':
            profile = self.user.profiledetails
            rubies_spent = profile.currency_spent
            rubies_collected = profile.total_currency_amount
            self.rubies = rubies_spent
            self.description = f"Hit {rubies_collected} Rubies"
            self.save()

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"


class SpinnerChoiceRenders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="game_player")
    slug = AutoSlugField(populate_from='nonce', unique=True)
    value = models.IntegerField(blank=True, null=True)
    ratio = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(GameHub, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    color = models.CharField(choices=COLOR, max_length=6, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="game_creator")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    nonce = models.DecimalField(max_digits=6, decimal_places=0)
    lower_nonce = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        validators=[MaxValueValidator(1000000), MinValueValidator(0)],
        help_text="Lower bound nonce of Choice",
        blank=True,
        null=True
    )
    upper_nonce = models.DecimalField(
        max_digits=7,
        decimal_places=0,
        validators=[MaxValueValidator(1000000), MinValueValidator(0)],
        help_text="Upper bound nonce of Choice",
        blank=True,
        null=True
    )
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f'{self.user} - {self.game} - {self.choice} - Nonce: {self.nonce}'

    def generate_nonce(self):
        return random.randint(0, 1000000)
        if self.lower_nonce is None:
            self.lower_nonce = self.choice.lower_nonce
        if self.upper_nonce is None:
            self.upper_nonce = self.choice.upper_nonce

    def save(self, *args, **kwargs):
        if not self.slug and self.choice:
            self.slug = slugify(self.choice)
        if not self.nonce:
            self.nonce = self.generate_nonce()
        if not self.game_creator:
            self.game_creator = self.game.user

        super().save(*args, **kwargs)

    def get_related_choice(self):
        related_choices = Choice.objects.filter(game=self.game)
        for choice in related_choices:
            if choice.lower_nonce is not None and choice.upper_nonce is not None:
                if int(choice.lower_nonce) <= self.nonce <= int(choice.upper_nonce):
                    return choice
        return None

    @classmethod
    def take_up_slot(cls, user, game, choice, value=None, ratio=None, type=None, image=None, color=None, is_active=1):
        nonce = random.randint(0, 1000000)
        instance = cls(
            user=user,
            game=game,
            choice=choice,
            value=value,
            ratio=ratio,
            type=type,
            image=image,
            color=color,
            nonce=nonce,
            is_active=is_active
        )
        instance.save()
        return instance


class Robot(models.Model):
    name = models.CharField(max_length=200)
    is_bot = models.BooleanField(default=True)
    image = models.FileField()
    sound = models.FileField(blank=True, null=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?",
    )

    def __str__(self):
        return self.name


class BattleParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    robot = models.ForeignKey(Robot, blank=True, null=True, on_delete=models.CASCADE)
    battle = models.ForeignKey('Battle', on_delete=models.CASCADE, blank=True, null=True,  related_name='participants')

    def __str__(self):
        if self.user:
            return str(self.user) + " " + str(self.battle)
        else:
            return "Robot: " +  str(self.robot.name) + " " + str(self.battle)

    class Meta:
        verbose_name = "Battle Participant"
        verbose_name_plural = "Battle Participants"


class BattleGame(models.Model):
    battle = models.ForeignKey('Battle', on_delete=models.CASCADE, related_name='battle_games')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_battles')
    quantity = models.PositiveIntegerField(default=1)
    outcome_created = models.BooleanField(blank=True, null=True, default=0)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.game.name} x{self.quantity} in {self.battle.battle_name}"

    class Meta:
        unique_together = ('battle', 'game')
        verbose_name = "Battle Game"
        verbose_name_plural = "Battle Games"
        ordering = ['order']

    def game_cost(self):
        return self.game.cost

    game_cost.short_description = "Game Cost"

    def game_discount_cost(self):
        return self.game.discount_cost

    game_discount_cost.short_description = "Discounted Cost"


class Battle(models.Model):
    BATTLE_SLOTS = (
        ('2', '1v1'),
        ('3', '1v1v1'),
        ('4', '1v1v1v1'),
        ('5', '1ve5'),
        ('6', '1ve6'),
        ('7', '1ve7'),
        ('8', '1ve8'),
        ('9', '1ve9'),
        ('10', '1ve10'),
        ('2v2', '2v2'),
        ('2ve3', '2v2v2'),
        ('2ve4', '2v2v2v2'),
        ('2ve5', '2ve5'),
        ('3v3', '3v3'),
        ('3ve3', '3v3v3'),
        ('4v4', '4v4'),
        ('5v5', '5v5'),
    )
    BATTLE_TYPE = (
        ('Free For All', 'Free For All'),
        ('upside_down', 'Upside-Down'),
        ('teams', 'Teams'),
        ('dual_win', 'Dual Win'),
        ('team_fight', 'Team Fight'),
        ('do_not_lose', 'Do Not Lose'),
        ('share', 'Share'),
    )
    battle_name = models.CharField(max_length=100, blank=True, null=True)
    chests = models.ManyToManyField('Game', through='BattleGame', related_name='battles')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    min_human_participants = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Minimum number of human participants required.',
    )
    game_values = models.TextField(blank=True, null=True)
    status = models.CharField(choices=BATTLE_STATUS, max_length=1, default="O")
    slots = models.CharField(choices=BATTLE_SLOTS, max_length=4, default="2")
    type = models.CharField(
        choices=BATTLE_TYPE,
        max_length=20,
        default='Free For All'
    )
    team_battle = models.BooleanField(default=False)
    bets_allowed = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now, blank=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?",
    )

    def get_game_quantities(self):
        return {bg.game: bg.quantity for bg in self.battle_games.all()}

    def get_total_participants(self):
        return self.participants.count()

    def __str__(self):
        return f"{self.battle_name} submitted by {self.creator}"

    logger = logging.getLogger(__name__)

    def get_absolute_url(self):
        return reverse("showcase:battle_detail", kwargs={"battle_id": self.id})

    def get_total_capacity(self):
        if 've' in self.slots:
            parts = self.slots.split('ve')
            return int(parts[0]) + int(parts[1])
        parts = self.slots.split('v')
        return sum(int(part) for part in parts if part.isdigit())

    def is_full(self):
        return self.get_total_participants() >= self.get_total_capacity()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        team_slots = ['2v2', '2ve3', '2ve4', '2ve5', '3v3', '3ve3', '4v4', '5v5']
        if self.slots in team_slots and (self.type != 'teams' or self.type != 'team_fight'):
            self.type = 'teams'

        for participant in self.participants.all():
            if participant.battle != self:
                participant.battle = self
                participant.save()

        if not self.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.currency = first_currency

        total_price = 0
        for game in self.chests.all():
            if game.discount_cost is not None:
                total_price += game.discount_cost
            else:
                total_price += game.cost

        self.price = total_price
        print('price set to total_price')
        super().save(*args, **kwargs)

    @property
    def total_game_values(self):
        return sum(
            bg.quantity * (bg.game.discount_cost if bg.game.discount_cost is not None else bg.game.cost)
            for bg in self.battle_games.all()
        )

    class Meta:
        verbose_name = "Battle"
        verbose_name_plural = "Battles"


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileDetails, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.IntegerField(default=5, validators=[MinValueValidator(1)],)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    winning_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='winninguser')
    winning_team = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='winningteam')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + " " + str(self.amount) + " " + str(self.battle)

    def clean(self):
        if not self.winning_user and not self.winning_team:
            raise ValidationError('Either user or team must be provided.')

    def save(self, *args, **kwargs):
        print('winning user: ' + str(self.winning_user))
        print('winning team: ' + str(self.winning_team))

        with atomic():
            if self.amount <= 0:
                print('put a positive amount')
                raise ValidationError("Bet amount must be positive.")

            try:
                self.profile = ProfileDetails.objects.get(user=self.user)
                print('put here profile')
            except ProfileDetails.DoesNotExist:
                raise ValidationError("User profile does not exist.")

            if self.profile.currency_amount:
                print('currency amount: ' + str(self.profile.currency_amount))
            else:
                print('no currency amount added')

            if self.profile.currency_amount < self.amount:
                print('insufficient funds')
                raise ValidationError(
                    f"Insufficient funds for this bet. You have {self.profile.currency_amount}, but the bet is {self.amount}."
                )

            self.profile.currency_amount -= self.amount
            self.profile.save()

            super().save(*args, **kwargs)

    class Meta:
        unique_together = ("user", "battle")

class Hits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.choice)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.choice:
            self.user = self.choice.user
        self.save()

    class Meta:
        verbose_name = "Hit"
        verbose_name_plural = "Hits"


class SelectRelatedConstraint(object):
    def __init__(self, limit_value):
        self.limit_value = limit_value

    def compile(self, compiler, connection):
        qs = compiler.expression_compiler.compile(self.limit_value)
        return {'limit_choices_to': qs}

class BlackJack(models.Model):
    name = models.CharField(max_length=200, verbose_name="BlackJack Game Name")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "BlackJack Game"
        verbose_name_plural = "BlackJack Games"

from django.core.mail import send_mail
from django.conf import settings

class SellerApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.DateField(verbose_name='Date of birth')
    identification = models.FileField(
        help_text="Please provide a valid government-issued ID (Passport, Driver's License, Birth Certificate, etc)"
    )
    email = models.EmailField(help_text="Please input your email", unique=True)
    email_verified = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if self.pk:
            previous_instance = SellerApplication.objects.get(pk=self.pk)
            if previous_instance.accepted != self.accepted:
                if self.accepted:

                    self.send_email(
                        subject="Your Seller Application Was Accepted",
                        message=f"Dear {self.first_name},\n\nCongratulations! Your seller application has been reviewed & you have been accepted. \n\nBest regards,\n Monstrosity?",
                    )
                else:

                    self.send_email(
                        subject="Your Seller Application Was Revoked",
                        message=f"Dear {self.first_name},\n\nWe regret to inform you that your seller application status has been revoked. For further details, please contact our support team.\nIf you believe this was a mistake, please reach out to us at poketrovecompany@gmail.com. \n\nBest regards,\n Monstrosity?",
                    )
        super().save(*args, **kwargs)

    def send_email(self, subject, message):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False,
        )

    def __str__(self):
        if str(self.email):
            return f"{self.user} - Email: {self.email} - Registered: {self.accepted}"
        else:
            return f"{self.user} - No Email Registered"

    class Meta:
        verbose_name = "Seller Application"
        verbose_name_plural = "Seller Applications"

class Preference(models.Model):
    DoesNotExist = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_posts')
    value = models.IntegerField(help_text="1->Like, 2->Dislike")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) + ':' + str(self.value)

    class Meta:
        unique_together = ("user", "post", "value")
        verbose_name = "Blog Like"
        verbose_name_plural = "Blog Likes"

class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, verbose_name="Post comment?")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)

        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.commentator).first()

            if profile:
                self.position = profile.position
        super().save(*args, **kwargs)

    def get_profile_url(self):
        return reverse('showcase:profile', args=[str(self.slug)])

    def get_absolute_url(self):

        return reverse("showcase:post_detail", kwargs={"slug": self.post.slug})


class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    post = models.ForeignKey(Idea, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"


class Profile(models.Model):
    about_me = models.TextField()
    image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user)


class FaviconBase(models.Model):
    favicontitle = models.TextField(verbose_name="Favicon Title")
    faviconcover = models.ImageField(upload_to='images/', verbose_name="Favicon")
    favicon_length = models.PositiveIntegerField(blank=True, null=True, default="100",
                                                 help_text='Original length of the favicon (use for original ratio).',
                                                 verbose_name="favicon length")
    favicon_width = models.PositiveIntegerField(blank=True, null=True, default="100",
                                                help_text='Original width of the favicon (use for original ratio).',
                                                verbose_name="favicon width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    faviconpage = models.TextField(verbose_name="Page Name")
    faviconurl = models.URLField(verbose_name="Page URL")
    faviconlink = models.URLField(verbose_name="Favicon Link")
    faviconsizes = models.TextField(verbose_name="Favicon Sizes", help_text="example: 180x180")
    faviconrelationship = models.TextField(verbose_name="Favicon Relationship", help_text="example: icon")
    favicontype = models.TextField(verbose_name="Favicon Type", help_text="example: ico")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.favicontitle

    class Meta:
        verbose_name = "Favicon"
        verbose_name_plural = "Favicons"

class LogoBase(models.Model):
    title = models.TextField(verbose_name="Background Title")
    logocover = models.ImageField(upload_to='images/', verbose_name="Logo")
    hyperlink = models.TextField(verbose_name="Hyperlink")
    section = models.IntegerField(verbose_name="Page Section", default=1)
    page = models.TextField(verbose_name="Page Name")
    alternate = models.TextField(verbose_name="Alternate Text")
    logo_length = models.PositiveIntegerField(blank=True, null=True, default="100",
                                              help_text='Original length of the advertisement (use for original ratio).',
                                              verbose_name="logo length")
    logo_width = models.PositiveIntegerField(blank=True, null=True, default="100",
                                             help_text='Original width of the advertisement (use for original ratio).',
                                             verbose_name="logo width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.section = LogoBase.objects.filter(page=self.page).count() + 1
        if not self.page.endswith('.html'):
            self.page += '.html'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logos"

class HyperlinkBase(models.Model):
    display_text = models.TextField(verbose_name="Text Display", blank=True, null=True, help_text="Display text")
    display_image = models.ImageField(upload_to='images/', verbose_name="Image Display", blank=True, null=True,
                                      help_text="Display an image")
    hyperlink = models.TextField(verbose_name="Hyperlink")
    section = models.IntegerField(verbose_name="Page Section")
    page = models.TextField(verbose_name="Page Name")
    alternate = models.TextField(verbose_name="Alternate Text", blank=True, null=True,
                                 help_text="Alternate text for Display Image")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    hyperlink_type = models.IntegerField(default=4,
                                         blank=True,
                                         null=True,
                                         help_text='Pick the type of hyperlink (optional)',
                                         choices=((4, 'Home Hyperlink'), (3, 'Member Hyperlink'),
                                                  (2, 'Administration Hyperlink'), (2, 'Form Hyperlink'),
                                                  (1, 'Store Hyperlink'), (0, 'Other')), verbose_name="Hyperlink Type")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.hyperlink

    def save(self, *args, **kwargs):
        if not self.pk:
            self.section = HyperlinkBase.objects.filter(page=self.page).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Hyperlink Base"
        verbose_name_plural = "Hyperlink Base"

class BackgroundImageBase(models.Model):
    backgroundtitle = models.TextField(verbose_name="Background Title", blank=True, null=True)
    cover = models.ImageField(blank=True, null=True, upload_to='images/', verbose_name="Images")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Width of the image (in percent relative).',
                                              verbose_name="image width")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Length of the image (in percent relative).',
                                               verbose_name="image length")
    file = models.FileField(blank=True, null=True, upload_to='images/', verbose_name="Non-image File")
    alternate = models.TextField(verbose_name="Alternate Text", blank=True, null=True)
    page = models.TextField(verbose_name="Page Name")
    url = models.CharField(verbose_name="Page URL", max_length=250, blank=True, null=True)
    position = models.IntegerField(verbose_name="Image Position", blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.backgroundtitle + " in " + self.page + " at Section " + str(self.position)

    def save(self, *args, **kwargs):
        if not self.url and self.page == "index":
            self.url = 'http://127.0.0.1:8000/'
        elif not self.url and self.page == "login":
            self.url = 'http://127.0.0.1:8000/accounts/login'
        elif not self.url:
            self.url = f'http://127.0.0.1:8000/{self.page}'
        elif not self.url.startswith('http://127.0.0.1:8000/'):
            self.url = f'http://127.0.0.1:8000/{self.url}'
        if not self.page.endswith('.html'):
            self.page += '.html'
        if not self.pk:
            self.position = BackgroundImageBase.objects.filter(page=self.page).count() + 1
            self.backgroundtitle = f'background {self.position}'
        if self.cover and not self.alternate:
            self.alternate = str(self.cover)
        elif self.file and not self.alternate:
            self.alternate = str(self.file)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Background Image Base"
        verbose_name_plural = "Background Image Base"

    def set_image_position(image_id, xposition, yposition):

        image = ImageBase.objects.get(id=image_id)
        print("Current coordinates: x={image.x}, y={image.y}")

        image.x = xposition
        image.y = yposition

        image.save()

class StoreViewType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    VIEW_TYPE_CHOICES = (
        ('stream', 'Streamlined View'),
        ('detail', 'Detailed View'),
    )
    type = models.CharField(choices=VIEW_TYPE_CHOICES, default='stream', max_length=6)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.type + "filter set by " + str(self.user)

    def save(self, *args, **kwargs):
        if self.user_id is not None:
            StoreViewType.objects.filter(user=self.user).delete()

            super().save(*args, **kwargs)
        else:
            view_type_choice = 'stream'

            store_view_type = StoreViewType(type=view_type_choice)

            print(store_view_type.type)

    class Meta:
        verbose_name = "Store View Type"
        verbose_name_plural = "Store View Types"

class TextBase(models.Model):
    TEXT_MEASUREMENT_CHOICES = (
        ('px', 'Pixels'),
        ('%', 'Percent'),
        ('vh', 'View Height'),
        ('em', 'em'),
        ('rem', 'Root em'),
        ('pt', 'Points'),
        ('pc', 'Picas'),
    )
    text = models.TextField(verbose_name="Text")
    page = models.TextField(verbose_name="Page Name")
    url = models.URLField(verbose_name="Page URL", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    text_color = models.CharField(blank=True, null=True, default="white", verbose_name="Text Color",
                                  help_text="Color of the text (accepts color names, hex codes or RGBA values in format (R, G, B, A))",
                                  max_length=200)
    header_or_textfield = models.BooleanField(verbose_name="Header or Body Text", default=1,
                                              choices=((1, 'Header'), (0, 'Body')))
    section = models.IntegerField(verbose_name="Text Section", help_text="Section Number of Text", default="1")
    exists = models.BooleanField(verbose_name="Section Taken", help_text="Is this section taken?", default=1,
                                 choices=((1, 'Yes'), (0, 'No')))
    hyperlink = models.TextField(blank=True, null=True, verbose_name="Hyperlink")
    text_size = models.IntegerField(default=0,
                                    help_text='6->Body 3, 5->Body 2, 4->Body 1, 3-> Heading 3,2-> Heading 2, 1-> Heading 1,',
                                    choices=(
                                        (6, 'H6'), (5, 'H5'), (4, 'H4'), (3, 'H3'), (2, 'H2'), (1, 'H1'), (0, 'p')),

                                    verbose_name="Text Type")
    font_size = models.IntegerField(blank=True, null=True, verbose_name="Font Size")
    font_measurement = models.CharField(blank=True, null=True, choices=TEXT_MEASUREMENT_CHOICES, max_length=3)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.text + " in " + self.page + " at Section " + str(self.section)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = 'http://127.0.0.1:8000/'
        if not self.page.endswith('.html'):
            self.page += '.html'
        elif not self.url.startswith('http://127.0.0.1:8000/'):
            self.url = f'http://127.0.0.1:8000/{self.url}'
        if not self.pk:
            self.section = TextBase.objects.filter(page=self.page).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Text Base"
        verbose_name_plural = "Text Base"

class BackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    page = models.TextField()
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self.slug

        super().save(*args, **kwargs)

    def get_profile_url(self):
        return reverse('showcase:profile', args=[str(self.slug)])

    class Meta:
        verbose_name = "Background Image"
        verbose_name_plural = "Background Images"

class ContentBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Content Background Image"
        verbose_name_plural = "Content Background Images"

class SupportBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Support Background Image"
        verbose_name_plural = "Support Background Images"

class ProductBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Background Image"
        verbose_name_plural = "Product Background Images"

class NavBar(models.Model):
    text = models.TextField()
    url = models.TextField(blank=True, null=True)
    row = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    opennew = models.BooleanField(verbose_name="Open In New Tab?", default=False,
                                  choices=((True, 'Yes'), (False, 'No')))
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.text + " at Row " + str(self.row) + ", Position " + str(self.position)

    def save(self, *args, **kwargs):
        if not self.url.startswith('http'):
            self.url = f'http://127.0.0.1:8000/{self.url}'
        if not self.pk:
            self.position = NavBar.objects.filter(row=self.row).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Navigational Bar Dropdown"
        verbose_name_plural = "Navigational Bar Dropdowns"

class NavBarHeader(models.Model):
    text = models.TextField(help_text='This is a header.')
    section = models.TextField(max_length=200,
                               blank=True,
                               null=True,
                               help_text='ID Section of page.')
    row = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.pk:
            self.row = NavBarHeader.objects.count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Navigational Bar Header"
        verbose_name_plural = "Navigational Bar Headers"

class FeaturedNavigationBar(models.Model):
    default_header = models.TextField(help_text="Only set if occupying 1'st position", blank=True, null=True,
                                      default='IntelleX', verbose_name='Heading')
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(verbose_name="Navigational image", blank=True, null=True)
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Width of the image (in percent relative).',
                                              verbose_name="image width")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Length of the image (in percent relative).',
                                               verbose_name="image length")
    url = models.TextField(blank=True, null=True)
    position = models.IntegerField()
    opennew = models.BooleanField(verbose_name="Open In New Tab?", default=False,
                                  choices=((True, 'Yes'), (False, 'No')))
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        if self.text:
            return self.text
        elif self.image:
            return self.image.url
        else:
            return self.default_header

    def save(self, *args, **kwargs):
        if not self.pk:
            self.position = FeaturedNavigationBar.objects.count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Featured Navigation Bar"
        verbose_name_plural = "Featured Navigation Bar"

class SettingsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settings')
    username = models.CharField(help_text='Your username', max_length=200)
    password = models.CharField(help_text='Your password', max_length=200)
    email = models.EmailField(help_text='Your password', max_length=200, blank=True, null=True)
    notifications_status = models.CharField(choices=NOTIFICATIONSTATUS, max_length=3, default='OFF')
    coupons = models.BooleanField(verbose_name="Send me coupons", default=False, blank=True, null=True,
                                  choices=((True, 'Yes'), (False, 'No')))
    news = models.BooleanField(verbose_name="Keep me in the loop", default=False, blank=True, null=True,
                               choices=((True, 'Yes'), (False, 'No')))

    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

class MyPreferences(models.Model):
    SPIN_TYPE = (
        ('C', 'Classic'),
        ('S', 'Simultaneous'),
        ('I', 'Instant'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spintype = models.CharField(choices=SPIN_TYPE, max_length=1, default='C')
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    class Meta:
        unique_together = ('user',)
        verbose_name = 'My Preference'

    def __str__(self):
        return f"{self.user.username}'s Preferences - {self.get_spintype_display()}"

class FavoriteChests(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chest = models.ForeignKey(Game, on_delete=models.CASCADE)
    precedence = models.IntegerField(default=1)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            FavoriteChests.objects.filter(
                user=self.user,
                precedence__gte=self.precedence
            ).update(precedence=models.F('precedence') + 1)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Favorite Chest"
        verbose_name_plural = "Favorite Chests"

        unique_together = ('user', 'chest')

class Donate(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)

    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False, help_text="Donate anonymously?")

    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f"Donation by {self.donor} ({self.amount} USD)"

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.donor).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.donor).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

class DonorBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    donor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Donors Background Image"
        verbose_name_plural = "Donors Background Images"

class ContributorBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Contributors Background Image"
        verbose_name_plural = "Contributors Background Images"


class UserProfile2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ship_profile')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    country = CountryField(multiple=False, default="United States of America")
    zip_code = models.CharField(max_length=5, default='00000')
    phone_number = models.CharField(default='000-000-0000', max_length=12)
    profile_picture = models.ImageField(upload_to='profile_image', null=True, blank=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?",
    )

    def __str__(self):
        return str(self.user) + "'s shipping profile"

    class Meta:
        verbose_name = "Shipping Profile"
        verbose_name_plural = "Shipping Profiles"
        unique_together = ('user', 'id',)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def save(self, *args, **kwargs):
        with transaction.atomic():

            try:
                existing_profile = UserProfile2.objects.get(user=self.user)
                if existing_profile and existing_profile != self:
                    existing_profile.delete()
            except UserProfile2.DoesNotExist:
                pass

            super().save(*args, **kwargs)

            Address.objects.filter(user=self.user, is_active=1).update(is_active=0)

            defaults = {
                'street_address': self.address or '',
                'zip': self.zip_code,
                'country': self.country,
                'address_type': 'shipping',
                'default': True,
            }

            if self.address2:
                defaults['apartment_address'] = self.address2
            else:
                defaults['apartment_address'] = 'None'

            address, created = Address.objects.update_or_create(
                user=self.user,
                is_active=1,
                defaults=defaults,
            )

            print(f"{'Created' if created else 'Updated'} address for user {self.user.username}.")

class SettingsBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Settings Background Image"
        verbose_name_plural = "Settings Background Images"

class DonateIcon(models.Model):
    row = models.IntegerField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Donation Icon"
        verbose_name_plural = "Donation Icons"

class Titled(models.Model):
    overtitle = models.TextField(verbose_name="Title")
    page = models.TextField(verbose_name="Page Name", blank=True, null=True, )
    url = models.URLField(verbose_name="Page URL", blank=True, null=True, )
    position = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.overtitle + " at " + self.page

    class Meta:
        verbose_name = "Page Title"
        verbose_name_plural = "Page Titles"

    def save(self, *args, **kwargs):
        if not self.url and self.page == "index":
            self.url = 'http://127.0.0.1:8000/'
        elif not self.url and self.page == "login":
            self.url = 'http://127.0.0.1:8000/accounts/login'
        elif not self.url:
            self.url = f'http://127.0.0.1:8000/{self.page}'
        elif not self.url.startswith('http://127.0.0.1:8000/'):
            self.url = f'http://127.0.0.1:8000/{self.url}'
        if not self.page.endswith('.html'):
            self.page += '.html'
        super().save(*args, **kwargs)

class Meme(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             verbose_name="Meme Creator")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    font_size = models.IntegerField(blank=True, null=True, verbose_name="Font Size")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    class Meta:
        verbose_name = "Meme Text"
        verbose_name_plural = "Meme Texts"

class MemeTextField(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='text_fields')
    text = models.TextField(null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.text

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    class Meta:
        verbose_name = "Meme Text Field"
        verbose_name_plural = "Meme Texts Fields"

class BaseCopyrightTextField(models.Model):
    copyright = models.TextField(verbose_name="Copyright Field", help_text="Copyright And Year")
    page = models.TextField(verbose_name="Page Name")
    hyperlink = models.TextField(verbose_name="Hyperlink")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.copyright

    def save(self, *args, **kwargs):
        if not self.page.endswith('.html'):
            self.page += '.html'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Base Text Field Copyright"
        verbose_name_plural = "Base Text Field Copyright"

class ShowcaseBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Showcase Background Image"
        verbose_name_plural = "Showcase Background Images"

class BilletBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Billet Background Image"
        verbose_name_plural = "Billet Background Images"

class BlogBackgroundImage(models.Model):
    title = models.TextField(verbose_name="Title")
    cover = models.ImageField(upload_to='images/', verbose_name="Cover")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Background Image"
        verbose_name_plural = "Blog Background Images"

class PostBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Idea Background Image"
        verbose_name_plural = "Idea Background Images"

class PosteBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Idea Background Image"
        verbose_name_plural = "Idea Background Images"

class VoteBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Vote Background Image"
        verbose_name_plural = "Vote Background Images"

class RuleBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Rule Background Image"
        verbose_name_plural = "Rule Background Images"

class AboutBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Background Image"
        verbose_name_plural = "About Background Images"

class FaqBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "FAQ Background Image"
        verbose_name_plural = "FAQ Background Images"

class StaffBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Staff Background Image"
        verbose_name_plural = "Staff Background Images"

class StaffApplyBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Staff Application Background Image"
        verbose_name_plural = "Staff Application Background Images"

class InformationBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Information Background Image"
        verbose_name_plural = "Information Background Images"

class TagBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tag Background Image"
        verbose_name_plural = "Tag Background Images"

class UserBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "User Background Image"
        verbose_name_plural = "Users Background Images"

class StaffRanksBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Staff Ranks Background Image"
        verbose_name_plural = "Staff Ranks Background Images"

class MegaBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Mega Background Image"
        verbose_name_plural = "Mega Background Images"

class EventBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event Background Image"
        verbose_name_plural = "Event Background Images"

class NewsBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News Background Image"
        verbose_name_plural = "News Background Images"

class ShareBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Share Background Image"
        verbose_name_plural = "Share Background Images"

class WhyBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Why Background Image"
        verbose_name_plural = "Why Background Images"

class WebsiteBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Website Background Image"
        verbose_name_plural = "Website Background Images"

class PerksBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Perks Background Image"
        verbose_name_plural = "Perks Background Images"

class CommitmentBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Commitment Background Image"
        verbose_name_plural = "Commitment Background Images"

class PriceBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Price Background Image"
        verbose_name_plural = "Price Background Images"

class ServerBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Server Background Image"
        verbose_name_plural = "Server Background Images"

class ContactBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Contact Background Image"
        verbose_name_plural = "Contact Background Images"

class MantenienceBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Mantenience Background Image"
        verbose_name_plural = "Mantenience Background Images"

class CostBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Cost Background Image"
        verbose_name_plural = "Cost Background Images"


class TiersBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tiers Background Image"
        verbose_name_plural = "Tiers Background Images"

class AccountBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Account Background Image"
        verbose_name_plural = "Account Background Images"

class AddonsBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Addons Background Image"
        verbose_name_plural = "Addons Background Images"

class PunishAppsBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Punishment Applications Background Image"
        verbose_name_plural = "Punishment Applications Background Images"

class BanAppealBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ban Appliciations Background Image"
        verbose_name_plural = "Ban Applications Background Images"

from django.db.models import Q

def get_friends(self):
    from .models import FriendRequest
    accepted_friend_requests = FriendRequest.objects.filter(
        Q(sender=self, status=FriendRequest.ACCEPTED) | Q(receiver=self, status=FriendRequest.ACCEPTED))
    friends = set()
    for friend_request in accepted_friend_requests:
        if friend_request.sender == self:
            friends.add(friend_request.receiver)
        else:
            friends.add(friend_request.sender)
    print('friends here')
    return friends

User.add_to_class('get_friends', get_friends)

class FriendRequest(models.Model):
    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.get_status_display()}'

    def get_profile_url(self, current_user):
        if current_user == self.sender or current_user == self.receiver:
            profile = ProfileDetails.objects.filter(user=current_user).first()
            if profile:
                return reverse('showcase:profile', args=[str(profile.pk)])

    class Meta:
        verbose_name = "Friend Request"
        verbose_name_plural = "Friend Requests"
        unique_together = ('sender', 'receiver')


class Room(models.Model):
    name = models.CharField(max_length=1000)
    signed_in_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='room',
                                       verbose_name="Room Creator")
    members = models.ManyToManyField(User, blank=True, related_name="members")
    time = models.DateTimeField(default=timezone.now, blank=True)
    public = models.BooleanField(default=False, verbose_name="Make Public?")
    logo = models.FileField(blank=True, null=True, verbose_name="Logo")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return str('Guest')

    def user_can_join(self, user):
        if self.public:
            print('public server')
            return True
        else:
            print('private server')

            if user.is_authenticated:

                if self.signed_in_user == user:
                    return True

                return FriendRequest.objects.filter(
                    Q(sender=self.signed_in_user, receiver=user, status=FriendRequest.ACCEPTED) |
                    Q(sender=user, receiver=self.signed_in_user, status=FriendRequest.ACCEPTED)
                ).exists()
            else:
                return False

    def get_absolute_url(self):

        if self.name == '':
            return reverse("showcase:room", kwargs={'room': ''})

        room_url = reverse("showcase:room", kwargs={'room': self.name})

        final_url = f"{room_url}?username={self.name}"

        return final_url

from django.contrib.auth.models import User

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=1000000, verbose_name="Username")
    signed_in_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='messages',
                                       verbose_name="User")
    room = models.CharField(max_length=1000000)
    message_number = models.PositiveIntegerField(default=0, editable=False)
    file = models.FileField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1, blank=True, null=True, help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        if self.value:
            return f"{self.value} in {self.room}"
        else:
            return f"blank message in {self.room}"

    def save(self, *args, **kwargs):
        if not self.pk:

            max_message_number = Message.objects.aggregate(max_message_number=Max('message_number'))[
                                     'max_message_number'] or 0

            self.message_number = max_message_number + 1

            profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()

            if profile and hasattr(self, 'position'):
                self.position = profile.position

        super().save(*args, **kwargs)

        if self.signed_in_user and self.room:

            friends = Friend.objects.filter(
                (Q(user=self.signed_in_user) & Q(friend__username=self.room)) |
                (Q(user__username=self.room) & Q(friend=self.signed_in_user))
            )

            for friend in friends:
                friend.latest_messages = self
                friend.last_messaged = self.date
                friend.save(update_fields=['latest_messages', 'last_messaged'])

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_absolute_url(self):

        room_url = reverse("showcase:room", kwargs={'room': str(self.room)})

        final_url = f"{room_url}?username={self.signed_in_user.username}"
        return final_url

        """
   def _get_current_user(self):

       return User.objects.get(username='example_user')

   def get_profile_url(self):
       return reverse('showcase:profile', args=[str(self.signed_in_user_id)])

"""

class GeneralMessage(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=1000000, verbose_name="Username")
    signed_in_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='generalmessages', verbose_name="User")
    file = models.FileField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    message_number = models.PositiveIntegerField(default=0, editable=False)
    cutoff = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1, blank=True, null=True, help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f"{self.value or 'blank message'}"

    def save(self, *args, **kwargs):
        if not self.pk:

            max_message_number = GeneralMessage.objects.aggregate(max_message_number=Max('message_number'))[
                                     'max_message_number'] or 0
            self.message_number = max_message_number + 1

            profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()
            if profile:

                pass

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    class Meta:
        verbose_name = "General Message"
        verbose_name_plural = "General Messages"

class DegeneratePlaylistLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, default=None)
    artist = models.CharField(max_length=100, null=True)
    audio_file = models.FileField(upload_to='audio/')
    audio_img = models.FileField(upload_to='audio_img/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Degenerate Playist Library"
        verbose_name_plural = "Degenerate Playist Libraries"

class DegeneratePlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ManyToManyField(DegeneratePlaylistLibrary)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    audio_img = models.FileField(upload_to='audio_img/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Degenerate Playist"
        verbose_name_plural = "Degenerate Playists"

class InviteCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    permalink = models.BooleanField(default=False)
    expire_time = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f"{self.code} - {self.user.username}"

    def is_valid(self):
        """Checks if the invite code is not expired"""
        if self.expire_time is None:
            return True
        return self.expire_time > timezone.now()

    class Meta:
        verbose_name = "Invite Code"
        verbose_name_plural = "Invite Codes"

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend_username = models.CharField(max_length=500, blank=True, null=True)
    latest_messages = models.ForeignKey(Message, blank=True, null=True, on_delete=models.CASCADE)
    last_messaged = models.DateTimeField(blank=True, null=True)
    currently_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    online = models.BooleanField(default=False)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + " is friends with " + str(self.friend) + "!"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.currently_active:

            Friend.objects.exclude(pk=self.pk).filter(user=self.user).update(currently_active=False)
        self.friend_username = self.friend.username
        latest_message_queryset = Message.objects.filter(Q(signed_in_user=self.user) | Q(signed_in_user=self.friend))

        latest_message = latest_message_queryset.order_by('-date').first()
        if latest_message:
            self.latest_messages = latest_message
            self.last_messaged = latest_message.date
        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.friend).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_profile_url2(self):

        if self.friend_username == None:
            return reverse("showcase:room", kwargs={'room': ''})

        room_url = reverse("showcase:room", kwargs={'room': self.friend_username})

        final_url = f"{room_url}?username={self.user.username}"

        return final_url

    @receiver(post_save, sender=FriendRequest)
    def handle_friend_request(sender, instance, created, **kwargs):
        if instance.status == FriendRequest.ACCEPTED:
            Friend.objects.get_or_create(user=instance.sender, friend=instance.receiver)
        elif instance.status == FriendRequest.DECLINED:
            Friend.objects.filter(
                (Q(user=instance.sender) & Q(friend=instance.receiver)) |
                (Q(user=instance.receiver) & Q(friend=instance.sender))
            ).delete()

    post_save.connect(handle_friend_request, sender=FriendRequest)

    class Meta:
        unique_together = ('user', 'friend')

def update_friend_username(sender, instance, created, **kwargs):
    if created:
        instance.friend_username = instance.friend.username
        instance.save()

post_save.connect(update_friend_username, sender=Friend)

class SupportChat(models.Model):
    name = models.CharField(max_length=1000)
    signed_in_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                       verbose_name="User")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.signed_in_user)

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_absolute_url(self):

        room_url = reverse('showcase:supportroom', args=[str(self.signed_in_user)])
        return room_url

    class Meta:
        verbose_name = "Support Chat"
        verbose_name_plural = "Support Chat"

class SupportMessage(models.Model):
    value = models.CharField(max_length=1000000)

    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=1000000)
    signed_in_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='support_messages',
                                       verbose_name="User")
    room = models.CharField(max_length=1000000)
    avatar = models.ImageField(upload_to='profile_image', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        if not self.pk:

            profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_absolute_url(self):

        room_url = reverse('showcase:supportroom', args=[str(self.signed_in_user)])
        return room_url

    class Meta:
        verbose_name = "Support Message"
        verbose_name_plural = "Support Messages"

class SupportInterface(models.Model):
    name = models.CharField(max_length=1000, null=True)
    room = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='supportinterfaceroom',
                             verbose_name="Room Creator")
    date = models.DateTimeField(default=timezone.now, blank=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return str('Guest')

    def get_absolute_url(self):

        if self.name == '':
            return reverse("showcase:supportline", kwargs={'room': ''})

        room_url = reverse("showcase:supportline", kwargs={'room': self.name})

        final_url = f"{room_url}?username={self.name}"

        return final_url

    class Meta:
        verbose_name = "Administration Chat Thread"
        verbose_name_plural = "Administration Chat Thread"

class SupportLine(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    signed_in_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='supportlinemessages',
                                       verbose_name="User")
    room = models.CharField(max_length=1000000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_number = models.PositiveIntegerField(default=0, editable=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        if not self.pk:

            max_message_number = SupportLine.objects.aggregate(max_message_number=models.Max('message_number'))[
                                     'max_message_number'] or 0

            self.message_number = max_message_number + 1

            profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()

            if profile:
                self.position = profile.position

        super().save(*args, **kwargs)

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.signed_in_user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_absolute_url(self):

        room_url = reverse("showcase:room", kwargs={'room': str(self.room)})

        final_url = f"{room_url}?username={self.signed_in_user.username}"

        return final_url

    class Meta:
        verbose_name = "Administration Thread Message"
        verbose_name_plural = "Administration Thread Messages"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    one_click_purchasing = models.BooleanField(default=False)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey('Level', on_delete=models.CASCADE, default=1)
    currency_amount = models.IntegerField(default=0, verbose_name='Currency Amount')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

from django.db.models import signals
from django.db.transaction import atomic

class Wager(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Bet Amount')
    outcome = models.CharField(max_length=1, choices=BLACKJACK_OUTCOME, default=None, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print('bet: ' + str(self.amount))
        print('currency: ' + str(self.user_profile.currency_amount))
        with atomic():

            if self.amount <= 0:
                print('put a positive amount')
                raise ValidationError("Bet amount must be positive.")
            if self.user_profile.currency_amount < self.amount:
                print('insufficient funds')
                raise ValidationError("Insufficient funds for this bet. You have {}, but the bet is {}.".format(
                    self.user_profile.currency_amount, self.amount))

            self.user_profile.currency_amount -= self.amount
            self.user_profile.save()

            super().save(*args, **kwargs)

    def resolve(self, outcome):
        self.outcome = outcome
        win_multiplier = 1.5 if outcome == 'B' else 1.0
        if outcome in ('W', 'B'):
            self.user_profile.currency_amount += self.amount * win_multiplier
        elif outcome == 'D':
            self.user_profile.currency_amount += self.amount
        self.user_profile.save()
        self.save()

def print_amount_before_save(sender, instance, **kwargs):
    print("Wager amount before atomic block:", instance.amount)

signals.pre_save.connect(print_amount_before_save, sender=Wager)

"""class Settings(models.Model):
 username = models.OneToOneField(User, on_delete=models.CASCADE)

 full_name = models.CharField(max_length=200, blank=True, null=True)

 class Meta:
     verbose_name_plural = "Settings"
     """

from django.db.models.signals import pre_save

from django.http import JsonResponse
from django.core import serializers


class ItemFilter(models.Model):
    product_filter = models.CharField(verbose_name="Hashtag filters", max_length=200, blank=True, null=True)
    clicks = models.IntegerField(verbose_name="Popularity", blank=True, null=True)
    image = models.ImageField(verbose_name="Filter Image", blank=True, null=True)
    category = models.IntegerField(default=0, blank=True,
                                   null=True, verbose_name='Make the Filter a Category?', help_text='1->Yes, 0->No',
                                   choices=((1, 'Yes'), (0, 'No')))
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.product_filter

    class Meta:
        verbose_name = "Item Filter"
        verbose_name_plural = "Item Filters"


class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True,
                                 blank=True)
    currency_price = models.IntegerField(blank=True, null=True)
    is_currency_based = models.BooleanField(default=False)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    discount_currency_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, blank=True, null=True)
    card_category = models.CharField(choices=CARD_CATEGORIES, max_length=1, default='P')
    condition = models.CharField(choices=CONDITION_CHOICES, default="M", max_length=2, blank=True, null=True)

    type = models.ForeignKey(ItemFilter, on_delete=models.CASCADE, blank=True, null=True)
    specialty = models.CharField(blank=True, null=True, choices=SPECIAL_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1000, default='N')
    slug = models.SlugField(unique=True, blank=True, null=True)
    status = models.IntegerField(choices=((0, "Draft"), (1, "Publish")), default=1)
    description = models.TextField()
    image = models.FileField()
    image2 = models.FileField(blank=True, null=True)
    image3 = models.FileField(blank=True, null=True)
    image4 = models.FileField(blank=True, null=True)
    image5 = models.FileField(blank=True, null=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    image = models.ImageField()
    multi_listing = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    relateditems = models.ManyToManyField("self", blank=True, verbose_name="Related Items:")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Out of stock?")

    def __str__(self):
        if self.user:
            return self.title + " by " + self.user.username
        else:
            return self.title + " by PokeTrove"

    def get_absolute_url(self):
        return reverse("showcase:product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("showcase:add-to-cart", kwargs={'slug': self.slug})

    def get_buy_it_now_url(self):
        return reverse("showcase:buy-it-now", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("showcase:remove-from-cart", kwargs={'slug': self.slug})

    def clean(self):
        if not self.price and not self.currency_price:
            raise ValidationError('Either price or currency price must be provided.')

    def save(self, *args, **kwargs):
        if not self.currency:
            first_currency = Currency.objects.first()
            if first_currency:
                self.currency = first_currency

        if not self.slug:
            self.slug = slugify(self.title)
            print('selugified')

        if self.price is None and self.discount_price is None:
            self.is_currency_based = True

        if not self.category and self.discount_price:
            if self.discount_price <= 100:
                self.category = 'G'
            elif self.discount_price <= 500:
                self.category = 'P'
            elif self.discount_price <= 1000:
                self.category = 'E'
            else:
                self.category = 'D'
        elif not self.category and self.price:
            if self.price <= 100:
                self.category = 'G'
            elif self.price <= 500:
                self.category = 'P'
            elif self.price <= 1000:
                self.category = 'E'
            else:
                self.category = 'D'

            print('selugified')

        super().save(*args, **kwargs)

    def get_profile_url(self):
        return reverse('showcase:product', args=[str(self.slug)])

    def get_profile_url2(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])


class GameHistory(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="gamecreator")
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='gameplayers')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='games', null=True, blank=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    image_length = models.PositiveIntegerField(
        blank=True, null=True, default=100,
        help_text='Original length of the advertisement (use for original ratio).',
        verbose_name="image length"
    )
    image_width = models.PositiveIntegerField(
        blank=True, null=True, default=100,
        help_text='Original width of the advertisement (use for original ratio).',
        verbose_name="image width"
    )
    plays = models.IntegerField(help_text="Number of plays", blank=True, null=True)
    value = models.IntegerField(help_text="Value of item in Rubies.", blank=True,
                                null=True, verbose_name="Value (Rubies)")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True, )
    number = models.IntegerField(help_text="Position ordered by value (from highest to lowest)", blank=True, null=True,
                                 default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.choice + " on " + self.game + " by " + self.user.username

    def save(self, *args, **kwargs):

        if not self.creator:
            self.creator = self.game.user
        if not self.image:
            self.file = self.game.image
        super().save(*args, **kwargs)


class QuickItem(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    image_length = models.PositiveIntegerField(
        blank=True, null=True, default=100,
        help_text='Original length of the advertisement (use for original ratio).',
        verbose_name="image length"
    )
    image_width = models.PositiveIntegerField(
        blank=True, null=True, default=100,
        help_text='Original width of the advertisement (use for original ratio).',
        verbose_name="image width"
    )
    quantity = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Out of stock?")

    def __str__(self):
        if self.user:
            return self.title + " by " + self.user.username
        else:
            return self.title + " by PokeTrove"

    def number(self):
        count = QuickItem.objects.filter(item=self.item).count()
        number = count + 1
        return number

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Picture {self.number()}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Quick Item"
        verbose_name_plural = "Quick Items"

class EBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    items = Item.objects.filter(is_active=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ecommerce Background Image"
        verbose_name_plural = "Ecommerce Background Images"

from django.utils.crypto import get_random_string

class Transaction(models.Model):
    inventory_object = models.ForeignKey(InventoryObject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_and_time = models.DateTimeField(null=True, verbose_name="time and date", auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        if self.user:
            return str(self.inventory_object) + " by " + str(self.user.username)
        else:
            return self.title + " by PokeTrove"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


class TradeOffer(models.Model):
    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2

    TRADE_STATUS = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined')
    )
    title = models.CharField(max_length=100, help_text="Name of your trade offer.")
    trade_items = models.ManyToManyField(TradeItem)
    estimated_trading_value = models.DecimalField(
        help_text="Estimated Market Price of Trade Item (will be displayed to potential traders)", decimal_places=2,
        max_digits=12)
    message = models.CharField(max_length=2000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Trader')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Receiver', blank=True,
                              null=True, help_text="Optional", verbose_name="Recipient")
    trade_status = models.IntegerField(choices=TRADE_STATUS, default=PENDING)
    slug = models.SlugField(unique=True, blank=True)
    trade_agreement = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Out of stock?")

    def __str__(self):
        item_titles = ", ".join([item.title for item in self.trade_items.all()])
        if self.user and self.user2:
            return f'Offer: {item_titles} between {self.user.username} and {self.user2.username}'
        elif self.user:
            return f'Offer: {item_titles} offered by {self.user.username}'
        else:
            return f'Offer: {item_titles} fulfilled by PokeTrove'

    def get_profile_url(self):
        return reverse('showcase:directedtradeoffers', args=[str(self.pk)])

    def get_profile_url2(self):
        return reverse('showcase:responsetradeitems', args=[str(self.slug)])

    def get_absolute_url(self):

        return reverse('showcase:directedtradeoffers', args=[str(self.slug)])

    def save(self, *args, **kwargs):

        if not self.slug:
            print("Title:", self.title)
            self.slug = slugify(self.title)
            print("Slug after slugify:", self.slug)

            while TradeOffer.objects.filter(slug=self.slug).exists():
                print("Slug already exists. Regenerating...")
                self.slug = f"{self.slug}-{get_random_string(length=32)}"
                print("Slug after regeneration:", self.slug)

        if self.trade_status == self.ACCEPTED and self.pk is not None:

            trade = Trade.objects.create()

            trade.trade_offers.add(self)

            trade.users.add(self.user)
            if self.user2:
                trade.users.add(self.user2)

            if self.offered_trade_items:
                trade_offer = self.offered_trade_items
                user = trade_offer.user
                self.user2 = user

            if self.pk is None:
                print('new trade offer')
                related_offer = self.offered_trade_items
                trade_items = related_offer.trade_items.all()
                self.wanted_trade_items.set(trade_items)

            trade.save()

        super().save(*args, **kwargs)

    def get_trade_item_details(self):
        details = []
        for item in self.trade_items.all():
            detail = {
                'title': item.title,
                'category': item.category,
                'specialty': item.specialty,
                'condition': item.condition,
                'label': item.label,
                'description': item.description,
                'image': item.image.url if item.image else None,
            }
            details.append(detail)
        return details

    class Meta:
        verbose_name = "Trade Offer"
        verbose_name_plural = "Trade Offers"


class TradeShippingLabel(models.Model):
    trade_offer = models.ForeignKey(TradeOffer, on_delete=models.CASCADE)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_profile = models.ForeignKey(UserProfile2, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=250, blank=True, null=True)
    address2 = models.CharField(max_length=250, blank=True, null=True, help_text="Optional")
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=5, default=00000)
    phone_number = models.CharField(default='000-000-0000', max_length=12)
    profile_picture = models.ImageField(upload_to='profile_image', null=True, blank=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.user) + "'s shipping label"

    def save(self, *args, **kwargs):
        if self.user.shipping_profile:
            if not self.first_name:
                self.first_name = self.user.first_name()
                self.last_name = self.user.last_name()
                self.address = self.user.address()
                self.address2 = self.user.address2()
                self.city = self.user.city()
                self.state = self.user.state()
                self.zip_code = self.user.zip_code()
                self.phone_number = self.user.phone_number()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Trade Shipping Label"
        verbose_name_plural = "Trade Shipping Labels"

    unique_together = ('user', 'id',)

"""
    def save(self, *args, **kwargs):
       try:

            existing_profile = TradeShippingLabel.objects.get(responding_trade_offer=self.responding_trade_offer)

            if existing_profile:
                existing_profile.delete()
                print("Previous shipping profile deleted successfully.")
        except UserProfile2.DoesNotExist:

            pass

        super().save(*args, **kwargs)"""


class RespondingTradeOffer(models.Model):
    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2

    TRADE_STATUS = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined')
    )

    wanted_trade_items = models.ForeignKey(TradeOffer, on_delete=models.CASCADE, blank=True, null=True)
    trade_offer_exists = models.BooleanField(default=False,
        help_text="Indicates if the trade has been completed previously.")
    offered_trade_items = models.ManyToManyField(TradeItem)
    trade_shipping_label = models.ForeignKey(TradeShippingLabel, on_delete=models.CASCADE, null=True, blank=True)
    estimated_trading_value = models.DecimalField(
        help_text="Estimated Market Price of Trade Item (will be displayed to potential traders)",
        decimal_places=2, max_digits=12
    )
    message = models.CharField(max_length=2000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='Dealer', blank=True, null=True, verbose_name="Dealer")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='Recipient', blank=True, null=True, help_text="Optional", verbose_name="Recipient")
    slug = models.SlugField(unique=True, editable=False, blank=True, null=True)
    trade_status = models.IntegerField(choices=TRADE_STATUS, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    is_active = models.IntegerField(
        default=1, blank=True, null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Out of stock?"
    )

    def __str__(self):
        title_bits = " ".join(str(item) for item in self.offered_trade_items.all())
        return f"{self.slug or 'unslugged'} - {title_bits}".strip()

    def get_profile_url(self):
        return reverse('showcase:directedtradeoffers', args=[str(self.pk)])

    def get_profile_url2(self):
        return reverse('showcase:responsetradeitems', args=[str(self.slug)])

    def get_absolute_url(self):
        return reverse('showcase:directedtradeoffers', args=[str(self.pk)])

    def _build_slug(self) -> str:
        parts = []
        if self.wanted_trade_items_id:
            parts.append(f"w{self.wanted_trade_items_id}")
        if self.user_id:
            parts.append(f"u{self.user_id}")
        base = "-".join(parts) or "rto"
        return f"{slugify(base)}-{uuid.uuid4().hex[:8]}"


    def save(self, *args, **kwargs):
        # If you infer user from offered items, keep this for updates
        if self.pk and self.offered_trade_items.exists():
            first_trade_item = self.offered_trade_items.first()
            if first_trade_item and first_trade_item.user:
                self.user = first_trade_item.user

        super().save(*args, **kwargs)

        # Ensure slug exists on both create and update
        if not self.slug:
            self.slug = self._build_slug()
            super().save(update_fields=["slug"])

        # --- your linking logic (trades, labels) ---
        if self.pk is not None:
            related_trade = Trade.objects.filter(trade_offers=self.wanted_trade_items).first()
            responding_related_trade = Trade.objects.filter(users__in=[self.user, self.user2]).first()
            if related_trade is not None:
                related_trade.responding_trade_offers.add(self)
            if responding_related_trade is not None:
                responding_related_trade.responding_trade_offers.clear()
                responding_related_trade.responding_trade_offers.add(self)

        if self.pk is not None and self.trade_status == self.ACCEPTED and self.trade_shipping_label is None:
            userprofile = self.user2.ship_profile if self.user2 else None
            self.trade_shipping_label = TradeShippingLabel.objects.create(
                trade_offer=self.wanted_trade_items,
                user=self.user2,
                first_name=userprofile.first_name if userprofile else '',
                last_name=userprofile.last_name if userprofile else '',
                address=userprofile.address if userprofile else '',
                address2=userprofile.address2 if userprofile else '',
                city=userprofile.city if userprofile else '',
                state=userprofile.state if userprofile else '',
                zip_code=userprofile.zip_code if userprofile else '',
                phone_number=userprofile.phone_number if userprofile else '',
            )

        if self.pk is not None and self.trade_status == self.ACCEPTED:
            # NOTE: see warning below about this query
            trade_offers = TradeOffer.objects.filter(
                id__in=[self.wanted_trade_items.id, self.offered_trade_items.first().id]
            )
            trade = Trade.objects.create()
            trade.trade_offers.set(trade_offers)
            trade.users.set([self.user, self.user2])

    def get_trade_item_details(self):
        details = []
        for item in self.trade_items.all():
            detail = {
                'title': item.title,
                'category': item.category,
                'specialty': item.specialty,
                'condition': item.condition,
                'label': item.label,
                'description': item.description,
                'image': item.image.url if item.image else None,
            }
            details.append(detail)
        return details

    class Meta:
        verbose_name = "Trade Offer Response"
        verbose_name_plural = "Trade Offer Responses"


class Trade(models.Model):
    trade_offers = models.ManyToManyField(TradeOffer)
    responding_trade_offers = models.ManyToManyField('RespondingTradeOffer', related_name="responding_trades",
                                                     blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='traders')
    trade_user = models.ForeignKey(UserProfile2, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name="Dealer", related_name='dealer_trades')
    trade_user2 = models.ForeignKey(UserProfile2, on_delete=models.CASCADE, blank=True,
                                    null=True, help_text="Optional", verbose_name="Recipient",
                                    related_name='recipient_trades')
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    printed = models.BooleanField(default=False)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Out of stock?")

    def __str__(self):
        offer_titles = " & ".join([str(offer) for offer in self.trade_offers.all()])
        user_names = " & ".join([user.username for user in self.users.all()])
        return f'{offer_titles} by {user_names}'

    def save(self, *args, **kwargs):
        if not self.slug:

            random_uuid = uuid.uuid4()

            self.slug = slugify(random_uuid)
        super().save(*args, **kwargs)

    def get_profile_url(self):
        return [reverse('showcase:profile', args=[str(user.pk)]) for user in self.users.all()]

    class Meta:
        verbose_name = "Trade"
        verbose_name_plural = "Trades"

class TradeContract(models.Model):
    commission = models.FloatField(default=10, help_text="(%)")
    trading_contract = models.TextField()
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.trading_contract)

    class Meta:
        verbose_name = "Trade Contract"
        verbose_name_plural = "Trade Contracts"


class TradeConfirmation(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='tradeconfirm')
    trader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='traderconfirm')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    trade_confirmation = models.BooleanField('I confirm that I agree to these terms & conditions for the trade.',
                                             default=False)
    trading_contract = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='contract')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.trader) + "'s confirmed trade with " + str(self.recipient)

    class Meta:
        verbose_name = "Trade Confirmation"
        verbose_name_plural = "Trade Confirmations"


class WeBuy(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    class Meta:
        verbose_name = "Seller To PokeTrove"
        verbose_name_plural = "Sellers To PokeTrove"

    def __str__(self):
        return f"WeBuy #{self.pk} - {self.seller}"


class BuyCards(models.Model):
    webuy = models.ForeignKey(WeBuy, related_name='cards', on_delete=models.CASCADE)

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField()
    image2 = models.FileField()
    image3 = models.FileField(blank=True, null=True)
    image4 = models.FileField(blank=True, null=True)
    image5 = models.FileField(blank=True, null=True)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    class Meta:
        verbose_name = "Buy A Card"
        verbose_name_plural = "Buy Cards"

    def __str__(self):
        return f"BuyCards #{self.pk} for WeBuy #{self.webuy_id}"


class UserState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userstate")
    state = models.BooleanField(default=False)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Set active?"
    )

    class Meta:
        verbose_name = "User State"
        verbose_name_plural = "User States"

    def __str__(self):
        return f"{self.user.username}: {int(self.state)}"


class ChatBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Chat Background Image"
        verbose_name_plural = "Chat Background Images"


class SupportChatBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Support Chat Background Image"
        verbose_name_plural = "Support Chat Background Images"

class UploadACard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(verbose_name="Card", max_length=200)
    public = models.BooleanField(default=False, verbose_name="Submit To Public")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.name + " by " + str(self.user)

    class Meta:
        verbose_name = "Upload A Card"
        verbose_name_plural = "Upload Cards"

class PartnerBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Partner Background Image"
        verbose_name_plural = "Partner Background Images"

class ConvertBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Convert Background Image"
        verbose_name_plural = "Convert Background Images"

class ReasonsBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Reasons Background Image"
        verbose_name_plural = "Reasons Background Images"


class OrderBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Order Background Image"
        verbose_name_plural = "Order Background Images"


class CheckoutBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Checkout Background Image"
        verbose_name_plural = "Checkout Background Images"


class SignupBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Signup Background Image"
        verbose_name_plural = "SignupBackground Images"


class ChangePasswordBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Change Password Background Image"
        verbose_name_plural = "Change Password Background Images"


class FeedbackBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Feedback Background Image"
        verbose_name_plural = "Feedback Background Images"


class IssueBackgroundImage(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Issue Background Image"
        verbose_name_plural = "Issue Background Images"


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    slug = models.SlugField(max_length=200, blank=True, null=True,
                            help_text="Leave blank to use corresponding product slug.")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField()
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order date")
    orderprice = models.FloatField(verbose_name="Order price", default=0)
    currencyorderprice = models.IntegerField(verbose_name="Currency order price", default=0)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        if self.item and self.item.price is not None:
            if self.item.discount_price:
                return self.quantity * self.get_discount_item_price()
            self.orderprice = self.quantity * self.item.price
            return self.quantity * self.item.price
        return 0

    def get_total_item_currency_price(self):
        if self.item and self.item.currency_price is not None:
            if self.item.discount_currency_price:
                return self.quantity * self.get_discount_item_currency_price()
            self.currencyorderprice = self.quantity * self.item.currency_price
            return self.quantity * self.item.currency_price
        return 0

    def get_item_price(self):
        return self.quantity * self.item.price

    def get_item_currency_price(self):
        return self.quantity * self.item.currency_price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_discount_item_currency_price(self):
        return self.quantity * self.item.discount_currency_price

    def get_amount_saved(self):
        return self.get_item_price() - self.get_discount_item_price()

    def get_currency_amount_saved(self):
        return self.get_item_currency_price() - self.get_discount_item_currency_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()

    def get_final_currency_price(self):
        if self.item.discount_currency_price:
            return self.get_discount_item_currency_price()
        return self.get_total_item_currency_price()

    def get_profile_url(self):
        order = OrderItem.objects.filter(user=self.user).first()
        if order:
            return reverse('showcase:product', args=[str(self.slug)])

    def get_profile_url2(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.item.slug if self.item else None
        if not self.image:
            self.image = self.item.image if self.item else None
        if not self.orderprice and self.item and self.item.price is not None:
            self.orderprice = self.item.price
        if not self.currencyorderprice and self.item and self.item.currency_price is not None:
            self.currencyorderprice = self.item.currency_price
        super().save(*args, **kwargs)
        OrderItemField.objects.create(
            user=self.user,
            ordered=self.ordered,

            slug=self.slug,
            item=self.item,
            image=self.image,
            orderitem_id=self,
            quantity=self.quantity,
            is_active=self.is_active,
        )
        if not self.orderprice and self.item and self.item.price:
            self.orderprice = self.item.price

        elif not self.currencyorderprice and self.item and self.item.currency_price:
            self.currencyorderprice = self.item.currency_price

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Order Items'

""" def save(self, *args, **kwargs):
       if not self.slug:
           self.slug = slugify(self.item.slug)
       super().save(*args, **kwargs)"""


class OrderItemField(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    slug = models.SlugField(max_length=200, blank=True, null=True,
                            help_text="Leave blank to use corresponding product slug.")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField()
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    quantity = models.IntegerField(default=1)
    orderitem_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name="Order item id", null=True)
    is_active = models.IntegerField(default=1, blank=True, null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    class Meta:
        verbose_name_plural = 'Order Item Fields'

class AdminRoles(models.Model):
    role = models.CharField(max_length=30, verbose_name="Administration role")
    role_description = models.TextField(verbose_name="Role Overview", blank='True', null='True')

    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')),
                                    verbose_name="Is this role currently active?")

    def __str__(self):
        return self.role

    class Meta:
        verbose_name_plural = 'Administrative Roles'

class AdminTasks(models.Model):
    task = models.CharField(max_length=30, verbose_name="Administration tasks")
    hyperlink = models.CharField(max_length=100, verbose_name="Task hyperlink", help_text='Only add if necessary',
                                 blank='True', null='True')
    opennew = models.BooleanField(verbose_name="Open In New Tab?", default=False,
                                  choices=((True, 'Yes'), (False, 'No')),
                                  help_text="Please note all Administration Interface Pages should open in a new tab.")
    section = models.IntegerField(help_text='Position of the page link.', verbose_name='position')
    page_name = models.TextField(verbose_name="Page Name", blank="True", null="True")
    image = models.ImageField(verbose_name="Task image")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    alternate = models.TextField(verbose_name="Alternate text")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')),
                                    verbose_name="Is this task currently active?")

    def __str__(self):
        return self.task

    def save(self, *args, **kwargs):
        if not self.pk:
            self.section = AdminTasks.objects.filter(page_name=self.page_name).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Administrative Tasks'

class AdminPages(models.Model):
    pages = models.CharField(max_length=30, verbose_name="Administration pages")
    description = models.TextField(help_text='Page description', default='')
    hyperlink = models.CharField(max_length=100, verbose_name="Page hyperlinks")
    opennew = models.BooleanField(verbose_name="Open In New Tab?", default=False,
                                  choices=((True, 'Yes'), (False, 'No')),
                                  help_text="Please note all Administration Interface Pages should open in a new tab.")
    section = models.IntegerField(help_text='Position of the page link.',
                                  verbose_name='position')
    page_name = models.TextField(verbose_name="Page Name", blank="True", null="True")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active page?")

    def __str__(self):
        return self.pages

    def save(self, *args, **kwargs):
        if not self.pk:
            self.section = AdminPages.objects.filter(page_name=self.page_name).count() + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Administrative Pages'

class Questionaire(models.Model):
    RADIO_CHOICES = (
        ('option1', 'Multiple Choice'),
        ('option2', 'Short Answer'),
        ('option3', 'True or False'),
        ('option4', 'Free Response'),
        ('option5', 'Image Field'),
        ('option6', 'Integer Field'),
        ('option7', 'Decimal Field'),
        ('option8', 'Other'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    form_name = models.TextField(verbose_name="Form Name")
    form_type = models.CharField(max_length=10, choices=RADIO_CHOICES)
    text = models.TextField(verbose_name="Question")
    image = models.TextField(verbose_name="Image", blank=True, null=True)

    answer_choices = models.CharField(max_length=255, blank=True, null=True)

    correct_answer_multiple_choice = models.CharField(max_length=255, blank=True, null=True)
    correct_answer_short_answer = models.CharField(max_length=255, blank=True, null=True)
    correct_answer_true_false = models.BooleanField(blank=True, null=True)
    correct_answer_free_response = models.TextField(blank=True, null=True)
    correct_answer_image_field = models.ImageField(upload_to='correct_answers/', blank=True, null=True)
    correct_answer_integer_field = models.IntegerField(blank=True, null=True)
    correct_answer_decimal_field = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    correct_answer_infinite_decimal_field = models.FloatField(blank=True, null=True)
    correct_answer_other = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Question Form Base'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questionaire, on_delete=models.CASCADE)

    multiple_choice_response = models.CharField(max_length=100, null=True, blank=True)
    short_answer_response = models.TextField(null=True, blank=True)
    true_or_false_response = models.BooleanField(null=True, blank=True)
    free_response_response = models.TextField(null=True, blank=True)
    image_field_response = models.ImageField(upload_to='responses/', null=True, blank=True)
    integer_field_response = models.IntegerField(null=True, blank=True)
    decimal_field_response = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_response = models.TextField(null=True, blank=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")

    def __str__(self):
        return f"{self.user.username}'s answer to '{self.question.text}'"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    orderprice = models.DecimalField(verbose_name="Order price",
        default=Decimal('0.00'),
        max_digits=20,
        decimal_places=2)
    currencyorderprice = models.IntegerField(verbose_name="Currency order price", default=0)
    itemhistory = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Order history", blank=True, null=True)
    feedback_url = models.URLField(blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL,
                                         blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    profile = models.ForeignKey(ProfileDetails, blank=True, null=True, on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    id = uuid4()
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active order?")
    '''
   1. Item added to cart
   2. Adding a billing address
   (Failed checkout)
   3. Payment
   (Preprocessing, processing, packaging etc.)
   4. Being delivered
   5. Received
   6. Refunds
   '''

    def __str__(self):
        if not self.pk:
            return "Unsaved Order"

        try:
            items_list = ", ".join([str(item) for item in self.items.all()])
            return f"Order #{self.pk} with items: {items_list}"
        except:
            return f"Order #{self.pk} (items unavailable)"

        if self.profile:
            self.shipping_address = self.profile.shipping_address
            self.billing_address = self.profile.billing_address

    def update_total_prices(self):
        self.orderprice = sum(item.get_final_price() for item in self.items.all() if item.get_final_price())
        self.currencyorderprice = sum(item.get_final_currency_price() for item in self.items.all() if item.get_final_currency_price())

    def save(self, *args, **kwargs):
        is_creating = self._state.adding

        super().save(*args, **kwargs)  # Save first

        if is_creating:
            self.update_total_prices()

    def get_total_price(self):
        return Decimal(self.orderprice) or 0

    def get_total_currency_price(self):
        return str(self.currencyorderprice) or 0

    def deduct_currency_amount(self):
        profile = ProfileDetails.objects.get(user=self.user)
        total_currency_price = self.get_total_currency_price()
        if profile.currency_amount >= total_currency_price:
            profile.currency_amount -= total_currency_price
            profile.save()
        else:
            raise ValueError("Not enough currency")

    def get_profile_url(self):
        return reverse('showcase:profile', args=[str(self.slug)])

    def get_profile_url2(self):
        return reverse('showcase:products', args=[str(self.slug)])


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1000, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    is_active = models.IntegerField(
        default=1,
        blank=True,
        null=True,
        help_text='1->Active, 0->Inactive',
        choices=((1, 'Active'), (0, 'Inactive')),
        verbose_name="Is this an active address?",
    )

    def save(self, *args, **kwargs):

        if self.is_active == 1:
            Address.objects.filter(user=self.user, is_active=1).exclude(pk=self.pk).update(is_active=0)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Saved Address'
        verbose_name_plural = 'Saved Addresses'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(unique=True, max_length=150)
    type = models.CharField(choices=COUPON_TYPE, default='B', max_length=1)
    amount = models.FloatField(blank=True, null=True, default=0)
    percentDollars = models.BooleanField(default=False, verbose_name="Percent-off Coupon")
    currency_amount = models.IntegerField(blank=True, null=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    uses = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active coupon?")

    def __str__(self):
        return self.code

    def clean(self):
        super().clean()
        if (str(self.amount) is None or str(self.amount == 0)) and (str(self.currency_amount) is None or str(self.currency_amount == 0)):
            raise ValidationError("Either 'amount' or 'currency_amount' must be filled with a non-zero value.")

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active refund?")

    def __str__(self):
        return f"{self.pk}"


from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(InventoryObject)
    number_of_cards = models.IntegerField(blank=True, null=True, verbose_name='Quantity')
    shipping_state = models.CharField(choices=SHIPPINGSTATUS, max_length=1, default='P')
    fees = models.IntegerField(null=True, blank=True, default=599)

    slag = models.SlugField(unique=True, max_length=16, blank=True, null=True, verbose_name='Slug')
    date_and_time = models.DateTimeField(null=True, verbose_name="time and date", auto_now_add=True)
    condition = models.CharField(choices=CONDITION_CHOICES, default="M", max_length=2, blank=True, null=True)
    status = models.CharField(choices=TIMESTATUS, max_length=1, default='P')
    withdraw_state = models.CharField(choices=WITHDRAWSTATE, max_length=2, default='I')
    capacity_state = models.CharField(choices=CAPACITYSTATE, max_length=1, default='N')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this withdraw active?")

    def __str__(self):
        if self.user:
            card_choices = ", ".join([str(card.choice_text) for card in self.cards.all()])
            if self.number_of_cards == 1:
                return f"{self.user.username} withdrew {self.number_of_cards} card: {card_choices}"
            else:
                return f"{self.user.username} withdrew {self.number_of_cards} cards: {card_choices}"

    def get_card_images(self):
        images = [card.image.url for card in self.cards.all() if card.image]
        names = [card.choice_text for card in self.cards.all() if card.choice_text]
        prices = [card.price for card in self.cards.all() if card.price]
        conditions = [card.condition for card in self.cards.all() if card.condition]
        return images, names, prices, conditions

    def generate_unique_slug(self):
        while True:
            random_slug = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            if not Withdraw.objects.filter(slag=random_slug).exists():
                return random_slug

    def mark_complete(self):
        self.withdraw_state = 'C'
        self.save(update_fields=['withdraw_state'])

    def save(self, *args, **kwargs):
        self.clean()
        if self.number_of_cards == 25:
            self.capacity_state = 'Y'
        else:
            self.capacity_state = 'N'
        if not self.slag:
            self.slag = self.generate_unique_slug()
        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)

            time_threshold = timezone.now() - timedelta(hours=48)
            withdraw_class = WithdrawClass.objects.annotate(
                withdraw_count=Count('withdraw')
            ).filter(
                user=self.user,
                date_and_time__gte=time_threshold,
                withdraw_count__lte=29,
                open=True
            ).first()

            if withdraw_class:
                withdraw_class.withdraw.add(self)
            else:
                withdraw_class = WithdrawClass.objects.create(
                    user=self.user,
                    shipping_state=self.shipping_state,
                    fees=self.fees,
                    status=self.status,
                    is_active=self.is_active,
                    currency=Currency.objects.filter(is_active=1).first(),
                    number_of_cards=self.number_of_cards
                )
                withdraw_class.withdraw.add(self)
        else:

            self.number_of_cards = self.cards.count()
            super().save(*args, **kwargs)

    @receiver(pre_delete, sender=InventoryObject)
    def update_withdraw_on_inventory_object_delete(sender, instance, **kwargs):
        withdraws = Withdraw.objects.filter(cards=instance)
        for withdraw in withdraws:
            withdraw.number_of_cards -= 1
            withdraw.cards.remove(instance)
            withdraw.save()

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    class Meta:
        verbose_name = 'Withdrawal Card'
        verbose_name_plural = 'Withdrawal Cards'

@receiver(m2m_changed, sender=Withdraw.cards.through)
def update_number_of_cards(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.number_of_cards = instance.cards.count()
        print('number of cards is ' + str(instance.number_of_cards))
        instance.save(update_fields=['number_of_cards'])

@receiver(post_save, sender=Withdraw)
def handle_withdraw_class_logic(sender, instance, created, **kwargs):
    if created:
        time_threshold = timezone.now() - timedelta(hours=48)
        withdraw_class = WithdrawClass.objects.annotate(
            withdraw_count=Count('withdraw')
        ).filter(
            user=instance.user,
            date_and_time__gte=time_threshold,
            withdraw_count__lte=29,
            open=True
        ).first()

        if withdraw_class:
            withdraw_class.withdraw.add(instance)
        else:
            withdraw_class = WithdrawClass.objects.create(
                user=instance.user,
                shipping_state=instance.shipping_state,
                fees=instance.fees,
                status=instance.status,
                is_active=instance.is_active,
                currency=Currency.objects.filter(is_active=1).first(),
                number_of_cards=instance.number_of_cards
            )
            withdraw_class.withdraw.add(instance)


class WithdrawClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    withdraw = models.ManyToManyField(Withdraw)
    number_of_cards = models.IntegerField(blank=True, null=True)
    shipping_state = models.CharField(choices=SHIPPINGSTATUS, max_length=1, default='S')
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    open = models.BooleanField(default=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    date_and_time = models.DateTimeField(null=True, verbose_name="time and date", auto_now_add=True)
    status = models.CharField(choices=SHIPPINGSTATUS, max_length=1, default='P')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this withdraw active?")

    def __str__(self):
        if self.user:
            if self.number_of_cards == 1:
                return f"{self.user.username} withdrew {self.number_of_cards} card"
            else:
                return f"{self.user.username} withdrew {self.number_of_cards} cards"

    def get_profile_url(self):
        profile = ProfileDetails.objects.filter(user=self.user).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def save(self, *args, **kwargs):
        self.currency = Currency.objects.filter(is_active=1).first()

        if self.pk:

            self.number_of_cards = self.withdraw.count()
        else:

            super().save(*args, **kwargs)
            self.number_of_cards = self.withdraw.count()
        super().save(update_fields=['number_of_cards'])

    class Meta:
        verbose_name = 'Withdrawal Class'
        verbose_name_plural = 'Withdrawal Classes'

"""
@receiver(m2m_changed, sender=WithdrawClass.withdraw.through)
def update_number_of_cards(sender, instance, **kwargs):
    if kwargs.get('action') in ['post_add', 'post_remove', 'post_clear']:
        instance.number_of_cards = instance.withdraw.count()
        instance.save(update_fields=['number_of_cards'])
"""

class OfficialShipping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    status = models.CharField(choices=SHIPPINGSTATUS, max_length=1, default='P')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this actively shipping?")

    def __str__(self):
        if self.street_address:
            return str(self.user.username) + " to " + str(self.street_address)
        elif self.apartment_address:
            return str(self.user.username) + " to " + str(self.apartment_address)
        else:
            return str(self.user.username) + " has no address on file."

    class Meta:
        verbose_name_plural = 'Official Shipping'

def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

class Contact(models.Model):
    name = models.TextField()
    email = models.EmailField(max_length=200, verbose_name="Recipient")
    inquiry = models.CharField(max_length=100, verbose_name="Subject")
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

class BusinessMailingContact(models.Model):
    name = models.TextField()
    email = models.EmailField(max_length=200, verbose_name="Recipient")
    inquiry = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Business Mailing Message"
        verbose_name_plural = "Business Mailing Messages"

class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Is this an active address?")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Checkout Addresses'

from django.db import IntegrityError

class ImageCarousel(models.Model):
    carouseltitle = models.CharField(max_length=100, help_text='Title of the image.', verbose_name="title", blank=True,
                                     null=True)
    carouselcaption = models.TextField(help_text='Caption for the image.', verbose_name="caption")
    carouselimage = models.ImageField(help_text='Upload an image for the carousel.)',
                                      upload_to='images/', verbose_name='image')
    carouselimage_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                                       help_text='Original length of the image (use for original ratio).',
                                                       verbose_name="image length")
    carouselimage_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                                      help_text='Original width of the image (use for original ratio).',
                                                      verbose_name="image width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    associated_product = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True,
                                           verbose_name="Associated Product")
    specialty = models.CharField(blank=True, null=True, choices=SPECIAL_CHOICES, max_length=2)
    carouselnumber = models.IntegerField(help_text='What carousel number is this?.',
                                         verbose_name='Carousel number')
    carouselposition = models.IntegerField(help_text='Positioning of the image within the carousel.',
                                           verbose_name='position', blank=True, null=True)
    carouseltotal = models.IntegerField(help_text='Total number of images within the carousel.',
                                        verbose_name='total images', default=9)
    carouselpage = models.TextField(verbose_name="Page Name")
    hyperlink = models.TextField(verbose_name="Hyperlink")
    alternate = models.TextField(verbose_name="Alternate Text", blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return self.carouseltitle

    class Meta:
        verbose_name = "Image Carousel Post"
        verbose_name_plural = "Image Carousel Posts"

    def save(self, *args, **kwargs):

        if not self.carouselpage.endswith('.html'):
            self.carouselpage += '.html'
        if not self.pk:
            self.carouselposition = ImageCarousel.objects.filter(carouselpage=self.carouselpage,
                                                                 carouselnumber=self.carouselnumber).count() + 1
            self.carouseltitle = f'background {self.carouselposition}'
        if self.carouselimage and not self.alternate:
            self.alternate = str(self.carouselimage)

        if self.associated_product and self.associated_product.specialty:
            self.specialty = self.associated_product.specialty
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:

            print(f"IntegrityError during save: {e}")
        super().save(*args, **kwargs)

class AdvertisementBase(models.Model):
    advertisementtitle = models.CharField(max_length=100, help_text='Advertisement title.',
                                          verbose_name="advertisement title")
    advertisement = models.ImageField(help_text='Image of the advertisement.', upload_to='images/',
                                      height_field="advertisement_width",
                                      width_field="advertisement_length")
    advertisement_file = models.FileField(blank=True, null=True, upload_to='images/', verbose_name="Non-image File")
    advertisement_length = models.PositiveIntegerField(blank=True, null=True, default="100",
                                                       help_text='Original length of the advertisement (use for original ratio).',
                                                       verbose_name="advertisement length")
    advertisement_width = models.PositiveIntegerField(blank=True, null=True, default="100",
                                                      help_text='Original width of the advertisement (use for original ratio).',
                                                      verbose_name="advertisement width")
    length_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Length")
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resized Width")
    advertisement_position = models.IntegerField(help_text='Positioning of the advertisement.', verbose_name='Position')
    page = models.TextField(verbose_name="Page Name")
    xposition = models.IntegerField(help_text='x-position.', verbose_name="x-position")
    yposition = models.IntegerField(help_text='x-position.', verbose_name="y-position")
    relevance = models.TextField(help_text='Relevance of advertisement')
    correlating_product = models.OneToOneField(Item, blank=True, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, help_text='Type of product.')
    advertisement_hyperlink = models.TextField(verbose_name="Hyperlink")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:
        verbose_name = "Advertisement Base"
        verbose_name_plural = "Advertisement Base"

        def __unicode__(self):
            return self.advertisementtitle

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            img = Image.open(self.advertisement.path)
            img = img.resize((self.width_for_resize, self.length_for_resize), Image.LANCZOS)
            self.advertisement_length, self.advertisement_width = img.size
            super().save(*args, **kwargs)
        else:
            img = Image.open(self.advertisement.path)
            img = img.resize((self.width_for_resize, self.length_for_resize), Image.LANCZOS)
            self.advertisement_width, self.advertisement_length = img.size
            super().save(*args, **kwargs)
        if not self.pk:
            self.advertisement_position = AdvertisementBase.objects.filter(page=self.page).count() + 1
        super().save(*args, **kwargs)

class Advertising(AdvertisementBase):
    pass

class ImageBase(models.Model):
    IMAGE_MEASUREMENT_CHOICES = (
        ('px', 'Pixels'),
        ('%', 'Percent'),
        ('vh', 'View Height'),
        ('em', 'em'),
        ('rem', 'Root em'),
        ('pt', 'Points'),
        ('pc', 'Picas'),
    )
    title = models.CharField(max_length=100, help_text='title.', blank=True, null=True,
                             verbose_name="title")
    image = models.ImageField(blank=True, null=True, help_text='Image of the advertisement.', upload_to='images/',
                              height_field="image_length",
                              width_field="image_width")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Width of the image (in percent relative).',
                                              verbose_name="image width")
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Length of the image (in percent relative).',
                                               verbose_name="image length")
    image_ratio = models.FloatField(blank=True, null=True, default=1.0,
                                    help_text='Length to Width Ratio of the Image (Length/Width).',
                                    verbose_name="image ratio")
    file = models.FileField(blank=True, null=True, upload_to='images/', verbose_name="Non-image File")
    image_measurement = models.CharField(blank=True, null=True, choices=IMAGE_MEASUREMENT_CHOICES, max_length=3)
    width_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resize Width")
    height_for_resize = models.PositiveIntegerField(default=100, verbose_name="Resize Height")
    image_position = models.IntegerField(help_text='Positioning of the image.', verbose_name='Position', blank=True,
                                         null=True)
    alternate = models.TextField(verbose_name="Alternate Text", blank=True, null=True)
    page = models.TextField(verbose_name="Page Name")
    xposition = models.IntegerField(help_text='x-position.', verbose_name="x-position", default="0")
    yposition = models.IntegerField(help_text='x-position.', verbose_name="y-position", default="0")
    relevance = models.TextField(help_text='Relevance of image')
    correlating_product = models.OneToOneField(Item, blank=True, null=True, on_delete=models.CASCADE)

    type = models.CharField(max_length=200, help_text='Type of image.')
    hyperlink = models.TextField(verbose_name="Hyperlink", blank=True, null=True)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    class Meta:

        verbose_name = 'Image Base'
        verbose_name_plural = 'Image Base'

    def __str__(self):
        return self.title + " in " + self.page + " at Image Position " + str(self.image_position)

    def image_save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        else:

            img = Image.open(self.image.path)

            img = img.resize((self.width_for_resize, self.height_for_resize), Image.ANTIALIAS)

            self.image_length, self.image_width = img.size
            if self.image_width and self.image_length:
                self.image_ratio = self.image_length / self.image_width
                print("the ratio is: " + str(self.image_ratio))

            super().save(*args, **kwargs)

    def set_image_position(image_id, xposition, yposition):

        image = ImageBase.objects.get(id=image_id)
        print("Current coordinates: x={image.x}, y={image.y}")

        image.x = xposition
        image.y = yposition

        image.save()

    def save(self, *args, **kwargs):
        if not self.page.endswith('.html'):
            self.page += '.html'
        if not self.pk:
            self.image_position = ImageBase.objects.filter(page=self.page).count() + 1
            self.title = f'background {self.image_position}'
        if self.image and not self.alternate:
            self.alternate = str(self.image)
        elif self.file and not self.alternate:
            self.alternate = str(self.file)
        super().save(*args, **kwargs)

class State(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.IntegerField(default=1, blank=True, null=True, help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now,
                                      null=True,
                                      blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state'

        verbose_name = 'Website'


class FileBase(models.Model):
    file_field = models.FileField(blank=True, null=True, verbose_name="File Field")


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile2.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Feedback(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True,
                             null=True, editable=False)
    """orderitem = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)"""
    order = models.OneToOneField(OrderItem, on_delete=models.CASCADE)

    """order = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='feedback', null=True)"""
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    comment = models.TextField()
    feedbackpage = models.TextField(verbose_name="Page Name", blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True,
                            help_text="Leave blank to use corresponding product slug.")

    star_rating = models.IntegerField(verbose_name='Star Rating',
                                      validators=[MinValueValidator(1), MaxValueValidator(5)])
    showcase = models.IntegerField(default=0, blank=True,
                                   null=True, verbose_name='Showcase on Cover Page?', help_text='1->Yes, 0->No',
                                   choices=((1, 'Yes'), (0, 'No')))
    image = models.ImageField(verbose_name="Images", upload_to='images/', help_text='Please upload any product images',
                              blank=True, null=True)
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the image (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the image (use for original ratio).',
                                              verbose_name="image width")
    timestamp = models.DateTimeField(default=timezone.now)
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return "%s %s" % (self.username, self.order)

    def get_current_username(self):
        User = get_user_model()
        return User.objects.get(pk=self.request.user.pk).username

    def get_profile_url(self):
        return reverse('showcase:review_detail', args=[str(self.slug)])

    def get_profile_url2(self):
        profile = ProfileDetails.objects.filter(user=self.username).first()
        if profile:
            return reverse('showcase:profile', args=[str(profile.pk)])

    def get_absolute_url(self):

        return reverse('showcase:review_detail', args=[str(self.slug)])

    @property
    def item_name(self):
        if self.item:
            return self.item.name
        elif self.order and self.order.item:
            return self.order.item.name
        return ""

    @property
    def item_slug(self):
        if self.item:
            return self.item.slug
        elif self.order and self.order.item:
            return self.order.item.slug
        return ""

@receiver(pre_save, sender=Feedback)
def set_slug(sender, instance, *args, **kwargs):

    if not instance.slug and instance.item:
        instance.slug = instance.item.slug

class PlayerVersusPlayer(models.Model):
    name = models.CharField(default="Pack Opening", max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    privacy = models.CharField(choices=PRIVACY, max_length=3)
    locked_in = models.BooleanField(default=0,
                                    help_text='0->Open, 1->Locked In',
                                    verbose_name="Open or Locked In?")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Player Versus Player"
        verbose_name_plural = "Player Versus Players"


def create_unique_lottery_number():
    return str(randint(1_000_000_000, 9_999_999_999))


class Lottery(models.Model):
    name = models.CharField(default='Daily Lotto', max_length=200)
    flavor_text = models.CharField(max_length=200)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    profile_number = models.PositiveIntegerField(default=0, editable=False)
    maximum_tickets = models.PositiveIntegerField(blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    prize = models.PositiveIntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(null=True, verbose_name='Sprite')
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_message_number = Lottery.objects.aggregate(max_message_number=models.Max('profile_number'))[
                                     'max_message_number'] or 0
            self.profile_number = max_message_number + 1
        if not self.slug:
            if self.name != "Daily Lotto" and self.name != "Daily Lottery" and self.name != "daily lotto" and self.name != "daily lottery":
                self.slug = slugify(self.name)

        self.file_path = reverse('showcase:lottery', kwargs={'slug': self.slug})

        if not self.currency:
            self.currency = Currency.objects.first()

        super().save(*args, **kwargs)

    def select_winner(self):

        tickets = list(self.tickets.all())

        count = len(tickets)

        if count == 0:

            return None

        random_index = random.randint(0, count - 1)
        winner_ticket = tickets[random_index]

        return winner_ticket.user

    class Meta:
        verbose_name = "Lottery"
        verbose_name_plural = "Lotteries"


class LotteryTickets(models.Model):
    name = models.CharField(default='Daily Lotto', max_length=200)
    flavor_text = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(null=True, verbose_name='Sprite')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    lottery_number = models.CharField(
        max_length=10,
        unique=True,
        default=create_unique_lottery_number
    )
    image_length = models.PositiveIntegerField(blank=True, null=True, default=100,
                                               help_text='Original length of the advertisement (use for original ratio).',
                                               verbose_name="image length")
    image_width = models.PositiveIntegerField(blank=True, null=True, default=100,
                                              help_text='Original width of the advertisement (use for original ratio).',
                                              verbose_name="image width")
    mfg_date = models.DateTimeField(auto_now_add=True, verbose_name="date")
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        return str(self.name) + " #" + str(self.lottery_number) + " - " + str(self.user)

    class Meta:
        verbose_name = "Lottery Ticket"
        verbose_name_plural = "Lottery Tickets"


class DefaultAvatar(models.Model):
    default_avatar_name = models.CharField(max_length=300, blank=True, null=True)
    default_avatar = models.ImageField(upload_to='images/')
    is_active = models.IntegerField(default=1,
                                    blank=True,
                                    null=True,
                                    help_text='1->Active, 0->Inactive',
                                    choices=((1, 'Active'), (0, 'Inactive')), verbose_name="Set active?")

    def __str__(self):
        if self.default_avatar_name:
            return str(self.default_avatar_name)

    def save(self, *args, **kwargs):
        if not self.default_avatar_name and self.default_avatar:
            self.default_avatar_name = self.default_avatar.name
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "default_avatar_name": self.default_avatar_name,
            "default_avatar_url": self.default_avatar.url if self.default_avatar else None,
            "is_active": self.is_active,
        }

    class Meta:
        verbose_name = "Default Avatar"
        verbose_name_plural = "Default Avatar"