import random
import uuid

from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model
from slugify import slugify

from .models import UpdateProfile, Questionaire, PollQuestion, Choice, FrequentlyAskedQuestions, SupportLine, \
    SupportInterface, FeaturedNavigationBar, BlogHeader, BlogFilter, SocialMedia, ItemFilter, StoreViewType, Shuffler, \
    Currency, ShuffleType, PrizePool, Lottery, LotteryTickets, Level, CurrencyMarket, SellerApplication, Meme, \
    MemeTextField, CurrencyFullOrder, CurrencyOrder, GameHub, BlackJack, Wager, Inventory, InventoryObject, Trade, \
    FriendRequest, Friend, RespondingTradeOffer, TradeShippingLabel, Game, Outcome, CardCategory, Experience, Endowment, \
    UploadACard, InviteCode, OfficialShipping, Withdraw, Transaction, Battle, BattleParticipant, QuickItem, \
    GeneralMessage, DefaultAvatar, Achievements, AdministrationChangeLog, TradeContract, BlogTips, \
    SpinPreference, WithdrawClass, CommerceExchange, ExchangePrize, BattleGame, Membership, Monstrosity, \
    MonstrositySprite, Affiliation, Ascension, ProfileCurrency, InventoryTradeOffer, Notification, UserNotification, \
    TopHits, Address, Robot, Bet, LevelIcon, Clickable, GameChoice, UserClickable, MyPreferences, GiftCode, \
    GiftCodeRedemption, FavoriteChests, IndividualChestStatistics, TotalChestStatistics, RubyDrop, Season, Tier, \
    Benefits, ChangeLog, BuyCards, WeBuy, UserState, Card, CardSet, Type, Subtype, Supertype, Investments, \
    UserInvestmentFund, InvestmentCards
from .models import Idea
from .models import VoteQuery
from .models import Product
from .models import City
from .models import StaffApplication
from .models import PartnerApplication
from .models import PunishmentAppeal
from .models import BanAppeal
from .models import ReportIssue
from .models import NewsFeed
from .models import StaffProfile
from .models import Event
from .models import Feedback
from .models import Blog
from .models import Preference
from .models import PostLikes
from .models import Idea, Comment
from .models import Profile
from .models import HyperlinkBase
from .models import Room, Message
from .models import SupportMessage
from .models import ProfileDetails
from .models import UserProfile
from .models import UserProfile2
from .models import SettingsModel
from .models import Support
# from .models import ConvertBackgroundImage
# from .models import BackgroundImage
# from .models import BackgroundImage2a
from .models import EBackgroundImage
from .models import ShowcaseBackgroundImage
from .models import ChatBackgroundImage
from .models import SupportChatBackgroundImage
from .models import BilletBackgroundImage
from .models import BlogBackgroundImage
from .models import PostBackgroundImage
from .models import RuleBackgroundImage
from .models import AboutBackgroundImage
from .models import FaqBackgroundImage
from .models import StaffBackgroundImage
from .models import InformationBackgroundImage
from .models import TagBackgroundImage
from .models import StaffRanksBackgroundImage
from .models import MegaBackgroundImage
from .models import UserBackgroundImage
from .models import EventBackgroundImage
from .models import NewsBackgroundImage
from .models import DonorBackgroundImage
from .models import ContentBackgroundImage
from .models import PartnerBackgroundImage
from .models import WhyBackgroundImage
from .models import SettingsBackgroundImage
from .models import PerksBackgroundImage
from .models import DegeneratePlaylistLibrary
from .models import DegeneratePlaylist
from .models import FaviconBase
from .models import LogoBase
from .models import BackgroundImageBase
from .models import TextBase
from .models import Titled
from .models import NavBar
from .models import NavBarHeader
from .models import ImageCarousel
from .models import SupportChat
from .models import BaseCopyrightTextField
from .models import AdvertisementBase
# from .models import ResizeImageMixin
from .models import TradeItem
from .models import TradeOffer
from .models import ImageBase
from .models import DonateIcon
from .models import Coupon
from .models import (Item, OrderItem, Order, CheckoutAddress, Payment)
from .models import OrderItemField
from .models import Contact
from .models import BusinessMailingContact
from .models import Feedback
from .models import Order
from .models import Donate
from .models import EmailField
from .models import AdminRoles
from .models import AdminTasks
from .models import AdminPages
from django.contrib.auth.models import Group

from .views import PlayerInventoryView


class UserProfile2Admin(admin.ModelAdmin):
    fieldsets = (
        ('Edit Profile Information - Personal Information', {
            'fields': ('user', 'first_name', 'last_name')
        }),
        ('Edit Profile Image Information - Attributes', {
            'fields': ('description','address', 'address2', 'city', 'state', 'country',  'zip_code', 'phone_number', 'profile_picture', 'is_active',)
        }),
    )
    pass


class TradeShippingLabelAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Trade Shipping Label Information - Personal Information', {
            'fields': ('user', 'first_name', 'last_name')
        }),
        ('Trade Shipping Label Information - Attributes', {
            'fields': ('description', 'address', 'city', 'state', 'zip_code', 'phone_number', 'profile_picture', 'is_active',)
        }),
    )


admin.site.register(TradeShippingLabel, TradeShippingLabelAdmin)


class TradeContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Trade Contract Information - Personal Information', {
            'fields': ('commission', 'trading_contract',)
        }),
        ('Trade Contract Information - Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(TradeContract, TradeContractAdmin)


class UserStateAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User State Information - Personal Information', {
            'fields': ('user', 'state',)
        }),
        ('User State Information - Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(UserState, UserStateAdmin)


class BuyCardsInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        remaining = 0
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE", False):
                continue
            if not form.cleaned_data and not form.instance.pk:
                continue
            remaining += 1

        if remaining > 5:
            raise ValidationError("You can only attach up to 5 BuyCards to a single WeBuy.")


class BuyCardsInline(admin.StackedInline):
    model = BuyCards
    formset = BuyCardsInlineFormSet
    extra = 1
    max_num = 5
    can_delete = True
    show_change_link = True
    fields = (
        "seller",
        "image", "image2", "image3", "image4", "image5",
        "is_active",
    )


@admin.register(WeBuy)
class WeBuyAdmin(admin.ModelAdmin):
    inlines = [BuyCardsInline]
    list_display = ("id", "seller", "is_active", "buycards_count")
    search_fields = ("seller__username", "seller__email")
    list_filter = ("is_active",)

    def buycards_count(self, obj):
        return obj.cards.count()
    buycards_count.short_description = "BuyCards (#)"


@admin.register(BuyCards)
class BuyCardsAdmin(admin.ModelAdmin):
    list_display = ("id", "webuy", "seller", "is_active")
    search_fields = ("seller__username", "seller__email")
    list_filter = ("is_active", "webuy")


class CardAPIAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Card API Information - Data', {
            'fields': ('card_id', 'name', 'last_name')
        }),
        ('Card API Information - Attributes', {
            'fields': ('description', 'address', 'city', 'state', 'zip_code', 'phone_number', 'profile_picture', 'is_active',)
        }),
    )

class BlogTipsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Blog Tips Information - Personal Information', {
            'fields': ('tip', 'author', 'updated_on',)
        }),
        ('Blog Tips Information - Attributes', {
            'fields': ('position',)
        }),
    )


admin.site.register(BlogTips, BlogTipsAdmin)


class SpinPreferenceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Spin Preference Information - Personal Information', {
            'fields': ('game', 'user', 'quick_spin',)
        }),
        ('Spin Preference Information - Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(SpinPreference, SpinPreferenceAdmin)


class categoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Update Profile Information - Categorial Descriptions', {
            'fields': ('user', 'name', 'description',)
        }),
        ('Update Profile Image Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',)
        }),
        ('Update Profile Image Information - Attributes', {
            'fields': ('is_active',)
        }),
    )
    pass


class publisherAdmin(admin.ModelAdmin):
    pass


class detailsAdmin(admin.ModelAdmin):
    pass


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1


class Prizes(admin.TabularInline):
    model = PrizePool
    extra = 1


class QuickItemInLine(admin.TabularInline):
    model = QuickItem
    extra = 1


class PollQuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Question Information - Categorial Descriptions', {
            'fields': ('question_text', 'choice', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )
    #inlines = [ChoiceInLine]
    readonly_fields = ('pub_date',)


admin.site.register(PollQuestion, PollQuestionAdmin)


class PrizePoolAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Prize Information - Categorial Descriptions', {
            'fields': ('prize_name', 'image', 'number', 'is_active')
        }),
    )
    Prizes = ['prize_name']
    readonly_fields = ('mfg_date',)


admin.site.register(PrizePool, PrizePoolAdmin)


class LotteryTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'lottery', 'lottery_number', 'is_active', 'mfg_date')
    fieldsets = (
        ('Lottery Information - Categorial Descriptions', {
            'fields': ('name', 'flavor_text', 'file', 'user', 'lottery', 'lottery_number', 'image_length', 'image_width', 'is_active')
        }),
    )
    readonly_fields = ('mfg_date',)


admin.site.register(LotteryTickets, LotteryTicketAdmin)


class LotteryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'prize', 'is_active',)
    fieldsets = (
        ('Lottery Information - Categorial Descriptions', {
            'fields': ('name', 'flavor_text', 'file_path', 'slug', 'maximum_tickets', 'price', 'prize', 'currency', 'file', 'image_length', 'image_width', 'is_active')
        }),
    )
    readonly_fields = ('mfg_date',)


admin.site.register(Lottery, LotteryAdmin)


class BenefitsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Benefits Information', {
            'fields': ('benefit', 'is_active',)
        }),
    )


class BenefitsInline(admin.TabularInline):
    model = Benefits
    extra = 1


class TierAdmin(admin.ModelAdmin):
    list_display = ('tier', 'lower_bound', 'upper_bound', 'is_active',)
    inlines = [BenefitsInline]
    fieldsets = (
        ('Membership Information', {
            'fields': ('tier', 'file', 'description', 'image_length', 'image_width',
                       'lower_bound', 'upper_bound', 'timeframe', 'is_active',)
        }),
    )
    readonly_fields = ('mfg_date',)
    @admin.display(description='Sprite')
    def file_thumbnail(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<img src="{}" style="height: 50px; width: auto;"/>',
            obj.file.url
        )

    list_display = (
        'tier', 'lower_bound','upper_bound',
        'is_active', 'file_thumbnail',
    )


admin.site.register(Tier, TierAdmin)


from .models import VoteQuery, VoteOption, Ballot


class VoteOptionInline(admin.TabularInline):
    model = VoteOption
    extra = 2


class authorAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'is_active', 'mfg_date')
    inlines = [VoteOptionInline]

    fieldsets = (
        ('Vote Information', {
            'fields': ('user', 'description', 'category', 'is_active')
        }),
    )


admin.site.register(VoteQuery, authorAdmin)


class StaffApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Staff Application Information - Staff Background Check', {
            'fields': ('name', 'overall_time_check', 'previous_role_time_check', 'strikes_check', 'read_requirements'),
            'classes': ('open',),
        }),
        ('Staff Application Information - Staff Candidate Input', {
            'fields': ('role', 'resume', 'why', 'how_better', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(StaffApplication, StaffApplicationAdmin)


class CardCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Card Category Application Information - Categorial Description', {
            'fields': ('category', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(CardCategory, CardCategoryAdmin)


class PartnerApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Partner Application Information - Categorial Description', {
            'fields': ('user', 'name', 'category', 'multi_category', 'description', 'resume', 'requirement_check', 'policy_check', 'voucher',),
            'classes': ('open',),
        }),
    )


admin.site.register(PartnerApplication, PartnerApplicationAdmin)


class PunishmentAppealAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Punishment Appeal Information - Categorial Description', {
            'fields': (
                'name', 'Rule_broken', 'Why_I_should_have_my_punishment_revoked', 'Additional_comments', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(PunishmentAppeal, PunishmentAppealAdmin)


class ReportIssueAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Report Issue Information - Categorial Description', {
            'fields': ('user', 'name', 'category', 'issue', 'Additional_comments', 'anonymous', 'is_active',),
            'classes': ('open',),
        }),
        ('Report Issue Information - Image Description', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('open',),
        }),
    )


admin.site.register(ReportIssue, ReportIssueAdmin)

from django.contrib import admin
from .models import SocialMedia


class SocialMediaInline(admin.TabularInline):  # Or admin.StackedInline
    model = SocialMedia
    extra = 1  # Allow adding one extra social media link by default


class StaffProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Staff Profile Information - Categorial Description', {
            'fields': ('user', 'name', 'role_position', 'description', 'staff_feats', 'date_and_time', 'is_active',),
            'classes': ('open',),
        }),
        ('Staff Profile Information - Image Description', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('open',),
        }),
    )
    inlines = [SocialMediaInline]


admin.site.register(StaffProfile, StaffProfileAdmin)


class CurrencyOrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Item Information - Categorial Description', {
            'fields': ('user', 'ordered', 'quantity', 'items',),
            'classes': ('open',),
        }),
        ('Order Item Information - Attributes', {
            'fields': ('slug', 'is_active'),
        }),
    )
    readonly_fields = ('ordered_date', 'id',)

    list_display = ('ordered_date', 'quantity', 'items', 'id',)

admin.site.register(CurrencyOrder, CurrencyOrderAdmin)


class CurrencyFullOrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Item Information - Order Outline', {
            'fields': ('user', 'items', 'itemhistory', 'coupon',),
            'classes': ('open',),
        }),
        ('Order Item Information - Personal Information', {
            'fields': ('payment', 'stripe_transaction_id'),
            'classes': ('open',),
        }),
        ('Order Item Information - Attributes', {
            'fields': ('ref_code', 'ordered_date', 'is_active'),
        }),
        ('Order Item Information - Logistics', {
            'fields': ('ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted'),
        }),
    )
    readonly_fields = ('start_date', 'id',)

    list_display = ('user', 'coupon', 'ordered_date', 'display_items', 'display_total_price', 'stripe_transaction_id')

    def display_items(self, obj):
        return ", ".join([str(item) for item in obj.items.all()])
    display_items.short_description = "Items"

    def display_total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    display_total_price.short_description = "Total Price"

admin.site.register(CurrencyFullOrder, CurrencyFullOrderAdmin)


class EndowmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Endowment Information', {
            'fields': ('user', 'target', 'order', 'is_active',)
        }),
    )


admin.site.register(Endowment, EndowmentAdmin)


class TradeItemAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Trade Item Information - Categorial Description', {
            'fields': ('user', 'title', 'category', 'specialty', 'status', 'description', ),
            'classes': ('open',),
        }),
        ('Trade Item Information - Technical Description', {
            'fields': ('fees', 'value', 'condition', 'label', 'slug', 'relateditems', 'is_active',),
            'classes': ('open',),
        }),
        ('Trade Item Information - Image Description', {
            'fields': ('image', 'image_length', 'image_width','length_for_resize', 'width_for_resize',),
            'classes': ('open',),
        }),
    )


admin.site.register(TradeItem, TradeItemAdmin)


class InventoryTradeOfferAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Inventory Trade Offer Information - Categorial Description', {
            'fields': ('initiator', 'receiver', 'offered_items', 'requested_items',  'final_cost', 'status', 'is_active', ),
            'classes': ('open',),
        }),
    )


admin.site.register(InventoryTradeOffer, InventoryTradeOfferAdmin)


class TradeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Trade Offer Information - Categorial Description', {
            'fields': ('trade_offers', 'users', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('timestamp',)
    list_display = ('timestamp', 'is_active')


admin.site.register(Trade, TradeAdmin)


class TradeOfferAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Trade Offer Information - Categorial Description', {
            'fields': ('title', 'trade_items', 'estimated_trading_value', 'user', 'user2', 'trade_status', 'message', 'quantity'),
            'classes': ('open',),
        }),
        ('Trade Offer Information - Technical Description', {
            'fields': ('slug', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('slug', 'timestamp',)


admin.site.register(TradeOffer, TradeOfferAdmin)


@admin.register(RespondingTradeOffer)
class RespondingTradeOfferAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Trade Offer Information - Categorial Description', {
            'fields': ('offered_trade_items', 'wanted_trade_items', 'estimated_trading_value',
                       'slug', 'user', 'user2', 'trade_status', 'message', 'quantity'),
            'classes': ('open',),
        }),
        ('Trade Offer Information - Technical Description', {
            'fields': ('is_active', 'timestamp'),  # include timestamp if you want it visible
            'classes': ('open',),
        }),
    )
    readonly_fields = ('slug', 'timestamp',)
    list_display = ('slug', 'timestamp', 'trade_status')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if not obj:
            return

        # Create a base slug if missing (now that PK and M2M exist)
        if not obj.slug:
            obj.slug = obj._build_slug()

        offered_ids = list(obj.offered_trade_items.values_list("id", flat=True))
        if offered_ids and "o" not in obj.slug:
            from django.utils.text import slugify
            import uuid
            base_parts = []
            if obj.wanted_trade_items_id:
                base_parts.append(f"w{obj.wanted_trade_items_id}")
            if obj.user_id:
                base_parts.append(f"u{obj.user_id}")
            base_parts.append("o" + "-".join(map(str, offered_ids[:5])))
            obj.slug = f"{slugify('-'.join(base_parts))}-{uuid.uuid4().hex[:6]}"

        obj.save(update_fields=["slug"])


class NotificationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Notification Information - Categorial Description', {
            'fields': ('user', 'message', 'content_type', 'object_id',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('created_at',)

    # Define a custom method that returns a string representation of the user(s)
    def display_users(self, obj):
        # If obj.user is a many-to-many field, .all() retrieves them
        return ", ".join([str(user) for user in obj.user.all()])

    display_users.short_description = 'User'

    # Use the custom method in list_display instead of directly using 'user'
    list_display = ('display_users', 'message', 'content_type', 'object_id',)


admin.site.register(Notification, NotificationAdmin)


class UserNotificationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Notification Information - Categorial Description', {
            'fields': ('user', 'notification', 'is_read',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('created_at',)


admin.site.register(UserNotification, UserNotificationAdmin)



class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Profile Information', {
            'fields': ('about_me', 'image', 'user', 'is_active',)
        }),
    )


admin.site.register(Profile, ProfileAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
   fieldsets = (
       ('Room Information', {
           'fields': ('sender', 'receiver', 'status',),
           'classes': ('collapse-open',),
       }),
   )


admin.site.register(FriendRequest, FriendRequestAdmin)


class FriendAdmin(admin.ModelAdmin):
   fieldsets = (
       ('Room Information', {
           'fields': ('user', 'friend', 'friend_username', 'latest_messages', 'last_messaged', 'currently_active', 'created_at', 'online', 'is_active',),
           'classes': ('collapse-open',),
       }),
   )
   readonly_fields = ('created_at',)


admin.site.register(Friend, FriendAdmin)


class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Settings Information - Personal Information', {
            'fields': ('user', 'username', 'password', 'email',)
        }),
        ('Settings Information - Personal Preferences', {
            'fields': ('coupons', 'news',)
        }),
        ('Settings Information - Active Settings', {
            'fields': ('notifications_status', 'is_active',)
        }),
    )


admin.site.register(SettingsModel, SettingsAdmin)


# admin.site.register(SettingsBackgroundImage)
# admin.site.register(ConvertBackgroundImage)
class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Partner Application Information - Categorial Description', {
            'fields': ('user', 'stripe_customer_id', 'one_click_purchasing', 'currency', 'level', 'currency_amount', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfile2, UserProfile2Admin)


class GameHubAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Game Hub Information - Categorial Description', {
            'fields': ('name', 'type', 'image', 'filter', 'description', 'slug', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(GameHub, GameHubAdmin)


from django.utils.html import format_html
from decimal import Decimal
from django.contrib.admin.widgets import AutocompleteSelect
from django.core.validators import MinValueValidator, MaxValueValidator


class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ('choice_text', 'name',)

    fieldsets = (
        ('Choice Information - Categorial Descriptions', {
            'fields': ('user', 'choice_text', 'category', 'tier',),
            'classes': ('collapse-open',),
        }),
        ('Choice Information - Attributes', {
            'fields': (
            'votes', 'mfg_date', 'rarity', 'condition', 'number_of_choice', 'total_number_of_choice', 'value',
            'number', 'prizes', 'lower_nonce', 'upper_nonce', 'generated_nonce', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Choice Information - Card API Information', {
            'fields': ('card_id', 'name', 'supertype', 'subtypes', 'hp', 'types', 'evolves_to', 'rules', 'attacks',
                       'weaknesses', 'retreat_cost', 'set_name', 'set_series', 'set_release_date', 'image_small',
                       'image_large', 'price',),
            'classes': ('collapse-open',),
        }),
        ('Choice Information - Image Display', {
            'fields': ('file', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
    )
    # inlines = [Prizes]

    readonly_fields = ('mfg_date',)

    list_display = (
        'user',
        'choice_text',
        'category',
        'condition',
        'value',
        'is_active',
    )

admin.site.register(Choice, ChoiceAdmin)


class GameChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1
    fields = (
        'user', 'choice_text', 'file', 'image_length', 'image_width',
        'color', 'value', 'number', 'total_number', 'category', 'midcategory', 'subcategory', 'tier', 'rarity', 'condition', 'number_of_choice', 'lower_nonce', 'upper_nonce', 'is_active',
    )
    readonly_fields = ('mfg_date',)


class GameChoiceMiddleInline(admin.TabularInline):
    model = GameChoice
    autocomplete_fields = ['choice']
    extra = 1
    fields = ('game', 'choice',
              'value', 'rarity', 'number', 'lower_nonce', 'upper_nonce', 'get_image',)
    readonly_fields = ('value', 'rarity', 'get_image',)

    def save_model(self, request, obj, form, change):
        if obj.choice:
            obj.choice.asave()  # Save the related Choice instance
        obj.save()  # Save the GameChoice instance

    def save(self, commit=True):
        instances = super().save(commit=False)
        for instance in instances:
            if instance.lower_nonce is not None:
                instance.choice.lower_nonce = instance.lower_nonce
            if instance.upper_nonce is not None:
                instance.choice.upper_nonce = instance.upper_nonce
            if commit:
                instance.choice.save()
                instance.save()
        self.save_m2m()
        return instances

    def get_image(self, obj):
        if obj.choice and getattr(obj.choice, 'image', None):
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.choice.image.url)
        return "No Image"
    get_image.short_description = "Image"


class GameAdmin(admin.ModelAdmin):
    inlines = [GameChoiceInline, GameChoiceMiddleInline]

    def save_related(self, request, form, formsets, change):
        """Ensure GameChoice instances are saved properly when Game is saved."""
        super().save_related(request, form, formsets, change)

        game = form.instance
        game_choices = GameChoice.objects.filter(game=game)

        for game_choice in game_choices:
            if game_choice.choice:
                if game_choice.choice.total_number_of_choice and game_choice.choice.number_of_choice:
                    if game_choice.choice.total_number_of_choice != 0:
                        game_choice.choice.rarity = (Decimal(game_choice.choice.number_of_choice) /
                                                            Decimal(game_choice.choice.total_number_of_choice)
                                                    ) * Decimal(100)
                    else:
                        game_choice.choice.rarity = Decimal(0)

                if not game_choice.choice.currency:
                    first_currency = Currency.objects.first()
                    if first_currency:
                        game_choice.choice.currency = first_currency

                if game_choice.choice.lower_nonce is None:
                    game_choice.choice.lower_nonce = random.randint(0, 1000000)
                if game_choice.choice.upper_nonce is None:
                    game_choice.choice.upper_nonce = random.randint(0, 1000000)

                if game_choice.choice.upper_nonce is not None and game_choice.choice.lower_nonce is not None:
                    rarity_value = (game_choice.choice.upper_nonce - game_choice.choice.lower_nonce) / 10000
                    game_choice.choice.rarity = round(rarity_value, 6)

                if not game_choice.choice.choice_text and game_choice.choice.name:
                    game_choice.choice.choice_text = game_choice.choice.name
                if not game_choice.choice.value and game_choice.choice.price:
                    game_choice.choice.value = game_choice.choice.price * 100
                if not game_choice.choice.subcategory and game_choice.choice.subtypes:
                    game_choice.choice.subcategory = game_choice.choice.subtypes

                game_choice.choice.save()

            game_choice.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        game = form.instance
        game_choices = GameChoice.objects.filter(game=game)
        for game_choice in game_choices:
            if game_choice.choice:
                game_choice.choice.asave()
                game_choice.choice.save()
            game_choice.save()

    fieldsets = (
        ('Game Information - Categorial Description', {
            'fields': (
                'name', 'user', 'type', 'category', 'cost', 'discount_cost',
                'heat', 'image', 'power_meter', 'slug', 'filter',
                'player_made', 'player_inventory', 'daily', 'is_active'
            ),
            'classes': ('open',),
        }),
        ('Unlocking (Daily Games Only)', {
            'fields': ('unlocking_level', 'cooldown', 'locked',),
            'classes': ('collapse',),
        }),
        ('Player Inventory (Player Only)', {
            'fields': ('items',),
            'classes': ('collapse',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and not obj.player_made:
            readonly_fields += ('player_inventory', 'items')
        if obj and not obj.daily:
            readonly_fields += ('unlocking_level', 'cooldown', 'locked')
        return readonly_fields

    list_display = (
        'name',
        'user',
        'cost',
        'discount_cost',
        'heat',
        'type',
        'category',
        'is_active',
    )

admin.site.register(Game, GameAdmin)


class IndividualChestStatisticsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Individual Chest Statistics Information - Categorial Description', {
            'fields': ('user', 'ranking', 'plays', 'chest', 'is_active',),
            'classes': ('open',),
        }),
    )
    list_display = (
        'user',
        'ranking',
        'plays',
        'chest',
        'is_active',
    )
admin.site.register(IndividualChestStatistics, IndividualChestStatisticsAdmin)


class TotalChestStatisticsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Individual Chest Statistics Information - Categorial Description', {
            'fields': ('ranking', 'plays', 'chests', 'is_active',),
            'classes': ('open',),
        }),
    )
    list_display = (
        'ranking',
        'plays',
        'chests',
        'is_active',
    )
admin.site.register(TotalChestStatistics, TotalChestStatisticsAdmin)


class TopHitsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Top Hits Information - Categorial Description', {
            'fields': ('user', 'game', 'choice', 'color', 'file', 'demonstration', 'is_active',),
            'classes': ('open',),
        }),
    )
    list_display = (
        'user',
        'game',
        'choice',
        'color',
        'file',
        'demonstration',
        'is_active',
    )
    readonly_fields = ('mfg_date',)


admin.site.register(TopHits, TopHitsAdmin)


class BlackJackAdmin(admin.ModelAdmin):
    fieldsets = (
        ('BlackJack Game Information - Categorial Description', {
            'fields': ('name', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(BlackJack, BlackJackAdmin)


class BlackJackWagerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Wager Game Information - Categorial Description', {
            'fields': ('user_profile', 'amount', 'outcome',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('timestamp',)


admin.site.register(Wager, BlackJackWagerAdmin)


from django.utils.html import mark_safe

class AchievementsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Achievement Information - Categorial Descriptions', {
            'fields': ('title', 'description', 'difficulty', 'value', 'type', 'currency',)
        }),
        ('Achievement Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width', 'display_image'),
            'classes': ('open',),
        }),
        ('Achievement Information - Technical Description', {
            'fields': ('is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('slug', 'display_image')

    # Display user, selling status, and membership as separate columns in the admin list view
    list_display = ('title', 'difficulty', 'value', 'type', 'display_image')

    def display_image(self, obj):
        """Custom method to display the image in the admin."""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto;" />')
        return "No image available"
    display_image.short_description = "Image Preview"

admin.site.register(Achievements, AchievementsAdmin)

# admin.site.register(BackgroundImage)
# admin.site.register(BackgroundImage2a)
# admin.site.register(EBackgroundImage)
# admin.site.register(ShowcaseBackgroundImage)
# admin.site.register(ChatBackgroundImage)
# admin.site.register(SupportChatBackgroundImage)
# admin.site.register(BilletBackgroundImage)
# admin.site.register(PostBackgroundImage)
# admin.site.register(RuleBackgroundImage)
# admin.site.register(AboutBackgroundImage)
# admin.site.register(FaqBackgroundImage)
# admin.site.register(StaffBackgroundImage)
# admin.site.register(InformationBackgroundImage)
# admin.site.register(TagBackgroundImage)
# admin.site.register(StaffRanksBackgroundImage)
# admin.site.register(MegaBackgroundImage)
# admin.site.register(UserBackgroundImage)
# admin.site.register(EventBackgroundImage)
# admin.site.register(NewsBackgroundImage)
# admin.site.register(DonorBackgroundImage)
# admin.site.register(ContentBackgroundImage)
# admin.site.register(PartnerBackgroundImage)
# admin.site.register(WhyBackgroundImage)
# admin.site.register(PerksBackgroundImage)

class TitledAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Page Title Information - Categorial Descriptions', {
            'fields': ('overtitle', 'page',),
            'classes': ('collapse-open',),
        }),
        ('Page Title Information - Categorial Descriptions', {
            'fields': ('url', 'position', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(Titled, TitledAdmin)
# admin.site.register(ResizeImageMixin)
# admin.site.register(BackgroundImages)
# admin.site.register(Feedback)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# from .models import User, SecurityQuestions, ProxyUser

# admin.site.register(ProxyUser, UserAdmin)
# admin.site.register(SecurityQuestions)




# Admin Action Functions
def change_rating(modeladmin, request, queryset):
    queryset.update(rating='e')


# Action description
change_rating.short_description = "Mark Selected Products as Excellent"


# ModelAdmin Class
class ProductA(admin.ModelAdmin):
    fieldsets = (
        ('Item Information - Categorial Descriptions', {
            'fields': ('name', 'description', 'rating', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )
    readonly_fields = ('mfg_date',)
    list_display = ('name', 'description', 'mfg_date', 'rating')
    list_filter = (
        'name',
        'description',
        'mfg_date',
    )
    actions = [change_rating]


admin.site.register(Product, ProductA)


class CityAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Item Information - Categorial Descriptions', {
            'fields': ('name', 'state',),
            'classes': ('collapse-open',),
        }),
    )
    list_display = (
        "name",
        "state",
    )


admin.site.register(City, CityAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


# admin.site.register(Blog, PostAdmin)


"""@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
"""


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Item Information - Order Outline', {
            'fields': ('user', 'items', 'itemhistory', 'coupon', 'orderprice', 'currencyorderprice',),
            'classes': ('open',),
        }),
        ('Order Item Information - Personal Information', {
            'fields': ('shipping_address', 'billing_address', 'payment',),
            'classes': ('open',),
        }),
        ('Order Item Information - Attributes', {
            'fields': ('ref_code', 'feedback_url', 'ordered_date', 'is_active'),
        }),
        ('Order Item Information - Logistics', {
            'fields': ('ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted'),
        }),
    )

    readonly_fields = ('start_date', 'id',)

    def display_items(self, obj):
        return ", ".join([str(item) for item in obj.items.all()])

    display_items.short_description = "Items"

    list_display = ('user', 'display_items', 'coupon', 'orderprice', 'currencyorderprice')


admin.site.register(Order, OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Item Information - Categorial Description', {
            'fields': ('user', 'amount', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('stripe_charge_id', 'timestamp',)


admin.site.register(Payment, PaymentAdmin)


class DegeneratePlaylistLibraryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Degenerate Playist Library Information - Categorial Description', {
            'fields': ('user', 'title', 'category', 'artist', 'audio_file', 'audio_img', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('created_at',)


admin.site.register(DegeneratePlaylistLibrary, DegeneratePlaylistLibraryAdmin)


class DegeneratePlaylistAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Degenerate Playist Information - Categorial Description', {
            'fields': ('user', 'song', 'artist', 'audio_file', 'audio_img', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('created_at',)


admin.site.register(DegeneratePlaylist, DegeneratePlaylistAdmin)





from django.contrib import messages
from .models import State


class StateAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Feedback Information', {
            'fields': ('name', 'is_active', 'created_on', 'updated_on',)
        }),
    )
    list_display = ('name', 'active', 'created_on')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

    def make_active(modeladmin, request, queryset):
        queryset.update(is_active=1)
        messages.success(
            request, "Selected Record(s) Marked as Active Successfully !!")

    def make_inactive(modeladmin, request, queryset):
        queryset.update(is_active=0)
        messages.success(
            request, "Selected Record(s) Marked as Inactive Successfully !!")

    admin.site.add_action(make_active, "Make Active")
    admin.site.add_action(make_inactive, "Make Inactive")


admin.site.register(State, StateAdmin)

# from .models import ExtendUser
# Register your models here.
# admin.site.register(ExtendUser)

# from .models import Group
from .forms import GroupAdminForm, MemeForm

admin.site.unregister(Group)


# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)

from .models import Feedback
from .forms import FeedbackForm


class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Feedback Information', {
            'fields': ('item', 'order', 'star_rating', 'comment', 'image', 'showcase')
        }),
        ('Feedback Information - Read-only Fields', {
            'fields': ('slug', 'username'),
            'classes': ('open',),
        }),
    )


admin.site.register(Feedback, FeedbackAdmin)


class HyperlinkBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hyperlink Information - Text Display', {
            'fields': ('display_text',),
            'classes': ('open',),
        }),
        ('Hyperlink Information - Image Display', {
            'fields': (
                'display_image', 'alternate', 'image_length', 'image_width', 'length_for_resize', 'width_for_resize',),
            'classes': ('open',),
        }),
        ('Hyperlink Information - Attributes', {
            'fields': ('hyperlink', 'section', 'page', 'hyperlink_type', 'is_active'),
        }),
    )


admin.site.register(HyperlinkBase, HyperlinkBaseAdmin)

admin.site.unregister(OrderItem)


class OrderItemAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Item Information - Categorial Description', {
            'fields': ('user', 'ordered', 'quantity', 'item', 'orderprice', 'currencyorderprice',),
            'classes': ('open',),
        }),
        ('Order Item Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('open',),
        }),
        ('Order Item Information - Attributes', {
            'fields': ('slug', 'is_active'),
        }),
    )
    readonly_fields = ('order_date', 'id',)


admin.site.register(OrderItem, OrderItemAdmin)


class OrderItemFieldAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Order Item Field Information - Categorial Description', {
            'fields': ('user', 'ordered', 'quantity', 'item',),
            'classes': ('open',),
        }),
        ('Order Item Field Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('open',),
        }),
        ('Order Item Field Information - Attributes', {
            'fields': ('slug', 'is_active'),
        }),
    )
    readonly_fields = ('orderitem_id',)


admin.site.register(OrderItemField, OrderItemFieldAdmin)


class AdministrationChangeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model', 'object_id', 'timestamp')
    list_filter = ('action', 'model', 'timestamp', 'user')
    search_fields = ('user__username', 'model', 'object_id')

    def has_add_permission(self, request):
        # Disable adding logs manually
        return False

    def has_change_permission(self, request, obj=None):
        # Disable editing logs manually
        return False


admin.site.register(AdministrationChangeLog, AdministrationChangeLogAdmin)


class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'object_id', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'model', 'object_id')


admin.site.register(ChangeLog, ChangeLogAdmin)


class RoomAdmin(admin.ModelAdmin):
   fieldsets = (
       ('Room Information', {
           'fields': ('name', 'signed_in_user', 'members', 'public', 'logo', 'is_active'),
           'classes': ('collapse-open',),
       }),
   )


admin.site.register(Room, RoomAdmin)


class OfficialShippingAdmin(admin.ModelAdmin):
   fieldsets = (
       ('Room Information', {
           'fields': ('user', 'street_address', 'apartment_address', 'country', 'zip', 'status', 'is_active'),
           'classes': ('collapse-open',),
       }),
   )


admin.site.register(OfficialShipping, OfficialShippingAdmin)


class StoreViewTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Store View Type Information', {
            'fields': ('user', 'type'),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(StoreViewType, StoreViewTypeAdmin)


class ItemFilterAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Item Information - Categorial Descriptions', {
            'fields': ('product_filter', 'clicks', 'image', 'category', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(ItemFilter, ItemFilterAdmin)


class ItemAdmin(admin.ModelAdmin):
    inlines = [QuickItemInLine]
    fieldsets = (
        ('Item Information - Categorial Descriptions', {
            'fields': ('user', 'title', 'is_currency_based', 'category', 'type', 'specialty', 'label', 'slug', 'description',),
            'classes': ('collapse-open',),
        }),
        ('Item Information - Prices', {
            'fields': ('price', 'discount_price',),
            'classes': ('open',),
        }),
        ('Item Information - Currency Prices', {
            'fields': ('currency', 'currency_price', 'discount_currency_price',),
            'classes': ('open',),
        }),
        ('Item Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width', 'length_for_resize', 'width_for_resize', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Item Information - Related Items', {
            'fields': ('relateditems',),
            'classes': ('collapse-open',),
        }),
    )

    class Media:
        js = ('admin-collapse-default.js',)
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(Item, ItemAdmin)


class QuickItemAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Quick Item Information - Categorial Descriptions', {
            'fields': ('user', 'item', 'price', 'discount_price', 'image', 'image_length', 'image_width', 'quantity', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(QuickItem, QuickItemAdmin)


class UploadACardAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Item Information - Categorial Descriptions', {
            'fields': ('user', 'name', 'image', 'public', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(UploadACard, UploadACardAdmin)


class InviteCodeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Item Information - Categorial Descriptions', {
            'fields': ('code','user', 'created_at', 'permalink', 'expire_time', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(InviteCode, InviteCodeAdmin)


class LogoBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Logo Information - Categorial Descriptions', {
            'fields': ('title', 'hyperlink', 'section', 'page', 'alternate',),
            'classes': ('collapse-open',),
        }),
        ('Logo Information - Logo Image Display', {
            'fields': ('logocover', 'logo_length', 'logo_width', 'length_for_resize', 'width_for_resize', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(LogoBase, LogoBaseAdmin)


class BlogHeaderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Blog Header Information - Categorial Descriptions', {
            'fields': ('category', 'image', 'position', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(BlogHeader, BlogHeaderAdmin)


class BlogFilterAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Blog Information - Categorial Descriptions', {
            'fields': ('blog_filter', 'clicks', 'image', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(BlogFilter, BlogFilterAdmin)


class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Blog Information - Categorial Descriptions', {
            'fields': ('title', 'slug', 'type', 'author', 'content', 'filters', 'position', 'category', 'minute_read', 'status', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Blog Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),

        ('Blog Information - Likes/Dislikes', {
            'fields': ('likes', 'dislikes',),
            'classes': ('collapse-open',),
        }),
    )
    readonly_fields = ('updated_on', 'created_on',)

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(Blog, BlogAdmin)


class TextBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Text Base Information - Categorial Descriptions', {
            'fields': ('text', 'page', 'url', 'created_at', 'text_color',),
            'classes': ('collapse-open',),
        }),
        ('Text Base  Information - Attributes', {
            'fields': ('header_or_textfield', 'section', 'text_size', 'hyperlink', 'is_active'),
            'classes': ('collapse-open',),
        }),
    )
    list_display = (
        'text',
        'page',
        'text_color',
        'header_or_textfield',
        'section',
        'hyperlink',
        'is_active',
    )

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }
    ordering = ['page', '-section', 'created_at']


admin.site.register(TextBase, TextBaseAdmin)

from django import forms


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    hours = [(f'{hour:02d}:{minute:02d}', f'{hour:02d}:{minute:02d}')
             for hour in range(24) for minute in range(0, 60, 15)]
    time = forms.ChoiceField(choices=hours)


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    fieldsets = (
        ('Event Information - Categorial Descriptions', {
            'fields': ('user', 'name', 'category', 'numeric_quantifier', 'qualitative_qualifier', 'description', 'section', 'page',),
            'classes': ('collapse-open',),
        }),
        ('Event Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
        ('Event  Information - Attributes', {
            'fields': ('date', 'time', 'date_and_time', 'slug', 'anonymous', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(Event, EventAdmin)


class SeasonAdmin(admin.ModelAdmin):
    form = EventAdminForm
    fieldsets = (
        ('Season Information - Categorial Descriptions', {
            'fields': ('name', 'season_length', 'description',),
            'classes': ('collapse-open',),
        }),
        ('Season Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
        ('Season Information - Attributes', {
            'fields': ('date', 'time', 'slug',),
            'classes': ('collapse-open',),
        }),
    )
    readonly_fields = ('date_and_time',)


admin.site.register(Season, SeasonAdmin)


class FaviconBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Event Information - Categorial Descriptions', {
            'fields': ('favicontitle', 'faviconlink',),
            'classes': ('collapse-open',),
        }),

        ('Event  Information - Image Display', {
            'fields': ('faviconcover', 'favicon_length', 'favicon_width', 'length_for_resize', 'width_for_resize',),
            'classes': ('collapse-open',),
        }),
        ('Event  Information - Attributes', {
            'fields': ('faviconpage', 'faviconurl', 'faviconsizes', 'faviconrelationship', 'favicontype', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(FaviconBase, FaviconBaseAdmin)


class FrequentlyAskedQuestionsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Administration Role Information', {
            'fields': ('question', 'position', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(FrequentlyAskedQuestions, FrequentlyAskedQuestionsAdmin)


class AdvertisementBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Advertisement Base Information - Categorial Descriptions', {
            'fields': ('advertisementtitle', 'page', 'type',),
            'classes': ('collapse-open',),
        }),
        ('Advertisement Base Information - Advertisement', {
            'fields': (
                'advertisement', 'advertisement_length', 'advertisement_width', 'length_for_resize', 'width_for_resize',
                'advertisement_file', 'xposition', 'yposition',),
            'classes': ('collapse-open',),
        }),
        ('Advertisement Base  Information - Attributes', {
            'fields': (
                'advertisement_position', 'relevance', 'correlating_product', 'advertisement_hyperlink', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(AdvertisementBase, AdvertisementBaseAdmin)


class NewsFeedAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Advertisement Base Information - Categorical Descriptions', {
            'fields': ('user', 'name', 'title', 'category', 'description', 'anonymous',),
            'classes': ('collapse-open',),
        }),
        ('Advertisement Base Information - Advertisement', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
        ('Advertisement Base  Information - Attributes', {
            'fields': ('slug', 'position', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )
    readonly_fields = ('date_and_time',)

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(NewsFeed, NewsFeedAdmin)


class MemeTextFieldAdmin(admin.ModelAdmin):
    form = MemeForm
    fieldsets = (
        ('Meme Text Information - Categorial Descriptions', {
            'fields': ('meme', 'text', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(MemeTextField, MemeTextFieldAdmin)


class MemeAdmin(admin.ModelAdmin):
    form = MemeForm
    fieldsets = (
        ('Meme Information - Categorial Descriptions', {
            'fields': ('user', 'title', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Event Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
    )
    readonly_fields = ('uploaded_at',)


admin.site.register(Meme, MemeAdmin)


class ShufflerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Shuffler Information - Categorial Descriptions', {
            'fields': ('question', 'choice_text', 'choices', 'category', 'heat', 'shuffletype',),
            'classes': ('collapse-open',),
        }),
        ('Shuffler Information - Attributes', {
            'fields': ('cost', 'currency', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Shuffler Information - Image Display', {
            'fields': ('file', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
    )

    readonly_fields = ('mfg_date',)


admin.site.register(Shuffler, ShufflerAdmin)


class ShuffleTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Shuffle Type Information - Categorial Descriptions', {
            'fields': ('name', 'type', 'circumstance', 'game_mode', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(ShuffleType, ShuffleTypeAdmin)


from django.contrib import admin


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Card Information - Categorial Descriptions', {
            'fields': ('card_id', 'name', 'hp', 'types', 'evolves_to',),
            'classes': ('collapse-open',),
        }),
        ('Card Information - Card Description', {
            'fields': ('supertype', 'subtypes', 'set', 'set_name', 'set_series', 'set_release_date', 'price',),
            'classes': ('collapse-open',),
        }),
        ('Card Information - Card Text', {
            'fields': ('rules', 'attacks', 'weaknesses', 'retreat_cost',),
            'classes': ('collapse-open',),
        }),
        ('Card Information - Image', {
            'fields': ('image_small', 'image_large',),
            'classes': ('collapse-open',),
        }),
    )
    list_display = ('card_id', 'name', 'set', 'price', 'updated_at')
    search_fields = ('card_id', 'name', 'set__name', 'set__series')
    list_filter = ('supertype', 'types', 'subtypes', 'set')
    filter_horizontal = ('types', 'subtypes')

@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'series', 'release_date')
    search_fields = ('id', 'name', 'series')

admin.site.register(Type)
admin.site.register(Subtype)
admin.site.register(Supertype)


class InvestmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Investment Type Information - Categorial Descriptions', {
            'fields': ('investment', 'user', 'type', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(Investments, InvestmentAdmin)


class UserInvestmentFundAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User Investment Information - Categorial Descriptions', {
            'fields': ('fund', 'user', 'type', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(UserInvestmentFund, UserInvestmentFundAdmin)


class InvestmentCardsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User Investment Information - Categorial Descriptions', {
            'fields': ('cards', 'type', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(InvestmentCards, InvestmentCardsAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Currency Information - Categorial Descriptions', {
            'fields': ('name', 'flavor_text',),
            'classes': ('collapse-open',),
        }),
        ('Currency Information - Attributes', {
            'fields': ('code', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Currency Information - Image Display', {
            'fields': ('file', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
    )

    readonly_fields = ('mfg_date',)


admin.site.register(Currency, CurrencyAdmin)


class CurrencyMarketAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Currency Information - Categorial Descriptions', {
            'fields': ('name', 'currency', 'amount', 'price', 'discount_price', 'unit_ratio', 'flavor_text',),
            'classes': ('collapse-open',),
        }),
        ('Shuffler Information - Attributes', {
            'fields': ('slug', 'deal', 'label', 'mfg_date', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Shuffler Information - Image Display', {
            'fields': ('file', 'image_length', 'image_width',),
            'classes': ('collapse-open',),
        }),
    )

    readonly_fields = ('mfg_date',)


admin.site.register(CurrencyMarket, CurrencyMarketAdmin)


class SellerApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Seller Application Information - Categorial Descriptions', {
            'fields': ('user', 'age', 'email', 'email_verified', 'accepted'),
            'classes': ('collapse-open',),
        }),
        ('Seller Application Information - Image Display', {
            'fields': ('identification',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(SellerApplication, SellerApplicationAdmin)


class AdministrationRoleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Administration Role Information', {
            'fields': ('role', 'role_description', 'is_active',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(AdminRoles, AdministrationRoleAdmin)

admin.site.register(BattleGame)

class InventoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Inventory Application Information - Categorial Description', {
            'fields': ('user', 'name', 'number_of_cards', 'image', 'image_length', 'image_width', 'is_active',),
            'classes': ('open',),
        }),
    )




class InventoryObjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Inventory Application Information - Categorial Description', {
            'fields': ('user', 'inventory', 'choice', 'choice_text', 'currency', 'price', 'trade_locked', 'condition', 'image', 'image_length', 'image_width', 'length_for_resize', 'width_for_resize', 'is_active',),
            'classes': ('open',),
        }),
    )

    list_display = (
        'user',
        'inventory',
        'choice',
        'choice_text',
        'currency',
        'price',
        'condition',
        'created_at',
        'is_active',
    )

admin.site.register(InventoryObject, InventoryObjectAdmin)


class WithdrawAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Withdraws - Categorial Description', {
            'fields': ('user', 'cards', 'number_of_cards', 'shipping_state', 'fees', 'slag', 'condition', 'status', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('date_and_time',)

    list_display = (
        'user',
        'number_of_cards',
        'shipping_state',
        'fees',
        'condition',
        'date_and_time',
        'status',
        'is_active',
        'display_card_images',
    )

    def display_card_images(self, obj):
        images, names, prices, conditions = obj.get_card_images()  # Unpack the tuple into images and names
        if images and names and prices and conditions:
            html_output = []
            # For each card, display the name above the image
            for name, img, price, condition in zip(names, images, prices, conditions):
                html_output.append(
                    f'<div style="margin-bottom: 10px;">'
                    f'<strong>{name}</strong> - <strong>{price}💎</strong>  - <strong>{condition}</strong><br>'
                    f'<img src="{img}" style="width: 100px; height: auto;" />'
                    f'</div>'
                )
            return mark_safe('<br>'.join(html_output))
        return 'No cards'

    display_card_images.short_description = 'Cards'


admin.site.register(Withdraw, WithdrawAdmin)


class WithdrawClassAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Withdraw Classes - Categorial Description', {
            'fields': ('user', 'withdraw', 'number_of_cards', 'fees', 'currency', 'status', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('date_and_time',)


admin.site.register(WithdrawClass, WithdrawClassAdmin)


from django.contrib import admin
from django.utils.html import format_html
from .models import Clickable


class ClickableAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Clickable Information', {
            'fields': (
                'name',
                'image',
                'get_image',        # show thumbnail on edit page
                'base_value',
                'rarity',
                'chance_per_second',
                'sound',
                'is_active',
            ),
            'classes': ('open',),
        }),
    )

    list_display = (
        'name',
        'get_image',            # add here so it appears as a column
        'base_value',
        'rarity',
        'chance_per_second',
        'is_active',
    )
    readonly_fields = ('get_image',)  # prevents editing and lets it render

    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:50px;"/>',
                obj.image.url
            )
        return "No Image"
    get_image.short_description = "Image"


admin.site.register(Clickable, ClickableAdmin)


class UserClickableAdmin(admin.ModelAdmin):
    fieldsets = (
        (' User Clickable Information - Categorial Description', {
            'fields': ('user', 'clickable', 'exponential_level_multiplier', 'actual_value', 'count', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(UserClickable, UserClickableAdmin)


class ExchangePrizeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Exchange Prize Information - Categorial Description', {
            'fields': ('prize', 'name', 'value', 'currency', 'condition', 'image_length', 'image_width', 'is_active',),
            'classes': ('open',),
        }),
    )


admin.site.register(ExchangePrize, ExchangePrizeAdmin)


class CommerceExchangeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Commerce Exchange Information - Categorial Description', {
            'fields': ('user', 'usercard', 'total_usercard_value', 'prizes', 'total_prize_value', 'value_descrepancy', 'currency', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('mfg_date',)


admin.site.register(CommerceExchange, CommerceExchangeAdmin)


class AdministrationTaskAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Administration Task Information - Categorial Descriptions', {
            'fields': ('task', 'hyperlink',),
            'classes': ('collapse-open',),
        }),
        ('Administration Task Information - Attributes', {
            'fields': ('opennew', 'section', 'page_name',),
            'classes': ('collapse-open',),
        }),
        ('Administration Task Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width', 'length_for_resize', 'width_for_resize', 'alternate',),
            'classes': ('collapse-open',),
        }),
    )


admin.site.register(AdminTasks, AdministrationTaskAdmin)


class BackgroundImageBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Background Image Base Information - Categorial Descriptions', {
            'fields': ('backgroundtitle', 'cover', 'alternate', 'file')
        }),
        ('Background Image Base Information - Attributes', {
            'fields': ('page', 'url', 'position', 'is_active',)
        }),
    )
    ordering = ['page', '-position']


admin.site.register(BackgroundImageBase, BackgroundImageBaseAdmin)


class ImageBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Image Base Information - Categorial Descriptions', {
            'fields': ('title', 'hyperlink', 'type')
        }),
        ('Image Base Information - Image Display', {
            'fields': ('image', 'image_width', 'image_length', 'image_ratio', 'image_measurement', 'width_for_resize',
                       'height_for_resize', 'file', 'image_position', 'alternate', 'xposition', 'yposition',)
        }),
        ('Image Base Information - Attributes', {
            'fields': ('page', 'relevance', 'correlating_product', 'is_active',)
        }),
    )


admin.site.register(ImageBase, ImageBaseAdmin)


class ImageCarouselAdmin(admin.ModelAdmin):
    fieldsets = (
        ('ImageCarousel Information - Categorial Descriptions', {
            'fields': ('carouseltitle', 'carouselcaption', 'carouselnumber', 'carouselposition',)
        }),
        ('ImageCarousel Information - Carousel Image Display', {
            'fields': (
                'carouselimage', 'carouselimage_length', 'carouselimage_width', 'length_for_resize', 'width_for_resize',
                'carouselpage', 'hyperlink',)
        }),
        ('ImageCarousel Information - Carousel Attributes', {
            'fields': ('associated_product', 'carouseltotal', 'is_active',)
        }),
        ('ImageCarousel Information - Specialty', {
            'fields': ('specialty',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Return a tuple of fields to be read-only
        return ('specialty',)


admin.site.register(ImageCarousel, ImageCarouselAdmin)


class MessageAdmin(admin.ModelAdmin):
   fieldsets = (
       ('Message Information - Categorial Descriptions', {
           'fields': ('value', 'user', 'signed_in_user', 'room',)
       }),
       ('Message Information - Image Display', {
           'fields': ('file', 'image_length', 'image_width',)
       }),
       ('Message Information - Attributes', {
           'fields': ('date', 'is_active',)
       }),
   )
   readonly_fields = ('message_number',)


admin.site.register(Message, MessageAdmin)


class SupportMessageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Support Message Information - Categorial Descriptions', {
            'fields': ('value', 'user', 'signed_in_user', 'room',)
        }),
        ('Support Message Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',)
        }),
        ('Support Message Information - Attributes', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('date',)


admin.site.register(SupportMessage, SupportMessageAdmin)


class SupportInterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Support Interface Information - Categorial Descriptions', {
            'fields': ('name', 'room', 'is_active',)
        }),
    )
    readonly_fields = ('date',)


admin.site.register(SupportInterface, SupportInterfaceAdmin)


class GeneralMessageAdmin(admin.ModelAdmin):
   fieldsets = (
       ('General Information - Categorial Descriptions', {
           'fields': ('value', 'user', 'signed_in_user',)
       }),
       ('General Information - Image Display', {
           'fields': ('file', 'image_length', 'image_width',)
       }),
       ('General Information - Attributes', {
           'fields': ('date', 'is_active',)
       }),
   )


admin.site.register(GeneralMessage, GeneralMessageAdmin)

class SocialMediaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Social Media Information - Categorial Descriptions', {
            'fields': ('social', 'page', 'hyperlink', 'is_active',)
        }),
        ('Social Media Information - Image Display', {
            'fields': ('icon', 'image_width', 'image_length', 'width_for_resize', 'height_for_resize', 'image_position', 'alternate',)
        }),
    )


admin.site.register(SocialMedia, SocialMediaAdmin)


class SupportThreadAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Administration Thread Information - Categorial Descriptions', {
            'fields': ('value', 'user', 'signed_in_user', 'room',)
        }),
        ('Administration Thread Information - Image Display', {
            'fields': ('image', 'image_length', 'image_width',)
        }),
        ('Administration Thread Information - Attributes', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('date', 'message_number')


admin.site.register(SupportLine, SupportThreadAdmin)


class OutcomeAdmin(admin.ModelAdmin):

   fieldsets = (
       ('Outcome Information - Categorial Descriptions', {
           'fields': ('user', 'value', 'ratio', 'type', 'color',)
       }),
       ('Outcome Information - Image Display', {
           'fields': ('file', 'image_length', 'image_width',)
       }),
       ('Outcome Information - Attributes', {
           'fields': ('game', 'game_creator', 'choice', 'nonce', 'demonstration', 'is_active',)
       }),
   )

   list_display = (
       'user',
       'value',
       'color',
       'file',
       'game',
       'choice',
       'nonce',
       'demonstration',
       'is_active',
   )
   readonly_fields = ('date_and_time',)


admin.site.register(Outcome, OutcomeAdmin)


class BanAppealAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ban Appeals Information - Categorial Descriptions', {
            'fields': ('name', 'Rule_broken', 'Why_I_should_have_my_ban_revoked', 'Additional_comments',)
        }),
        ('Ban Appeals Information - Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(BanAppeal, BanAppealAdmin)


class RubyDropAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ruby Drop Information - Categorial Descriptions', {
            'fields': ('amount', 'timeframe', 'currency', 'rarity', 'opentime',)
        }),
        ('Ruby Drop Information - Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(RubyDrop, RubyDropAdmin)


class MyPreferencesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('My Preferences Information - Categorial Descriptions', {
            'fields': ('user', 'spintype',)
        }),
        ('My Preferences Information - Attributes', {
            'fields': ('is_active',)
        }),
    )

    list_display = (
        'user',
        'spintype',
        'is_active',
    )


admin.site.register(MyPreferences, MyPreferencesAdmin)


class FavoriteChestsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Favorite Chests Information - Categorial Descriptions', {
            'fields': ('user', 'chest', 'precedence',)
        }),
        ('Favorite Chests Information - Attributes', {
            'fields': ('is_active',)
        }),
    )

    list_display = (
        'user',
        'chest',
        'precedence',
        'is_active',
    )


admin.site.register(FavoriteChests, FavoriteChestsAdmin)


class BaseCopyrightTextFieldAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ban Appeals Information', {
            'fields': ('copyright', 'page', 'hyperlink', 'is_active',)
        }),
    )


admin.site.register(BaseCopyrightTextField, BaseCopyrightTextFieldAdmin)


class PreferenceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Blog Like Information', {
            'fields': ('user', 'post', 'value',)
        }),
    )
    readonly_fields = ('date',)


admin.site.register(Preference, PreferenceAdmin)


class CheckoutAddressAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Checkout Address Information-Personal Information', {
            'fields': ('user', 'street_address', 'apartment_address', 'country', 'zip')
        }),
        ('Checkout Address Information-Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(CheckoutAddress, CheckoutAddressAdmin)

class AddressAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Saved Address Information-Personal Information', {
            'fields': ('user', 'street_address', 'apartment_address', 'country', 'zip')
        }),
        ('Saved Address Information-Attributes', {
            'fields': ('is_active',)
        }),
    )

    list_display = (
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'is_active',
    )


admin.site.register(Address, AddressAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentator', 'slug', 'name', 'body', 'post', 'created_on', 'active', 'is_active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    # Define your custom fieldsets below
    fieldsets = (
        ('Ban Appeals Information - Categorial Description', {
            'fields': ('commentator', 'post', 'name', 'email', 'body',)
        }),
        ('Ban Appeals Information - Moderation', {
            'fields': ('slug', 'active', 'is_active',)
        })
    )
    readonly_fields = ('created_on',)


class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Message Information', {
            'fields': ('name', 'email', 'inquiry', 'message',)
        }),
    )


admin.site.register(Contact, ContactAdmin)


class BusinessMailingContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Business Mailing Message Information', {
            'fields': ('name', 'email', 'inquiry', 'message',)
        }),
    )


admin.site.register(BusinessMailingContact, BusinessMailingContactAdmin)


class EmailFieldAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Email Information', {
            'fields': ('user', 'email', 'confirmation', 'is_active',)
        }),
    )


admin.site.register(EmailField, EmailFieldAdmin)


class NavBarAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Navigational Bar Dropdown Information - Categorial Descriptions', {
            'fields': ('text', 'url',)
        }),
        ('Navigational Bar Dropdown Information', {
            'fields': ('row', 'position', 'opennew', 'is_active',)
        }),

    )
    list_display = ('text', 'url', 'is_active',)
    list_filter = (
        'text',
        'url',
        'is_active',
    )


admin.site.register(NavBar, NavBarAdmin)


class NavBarHeaderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Navigational Bar Header Information - Categorial Descriptions', {
            'fields': ('text',)
        }),
        ('Navigational Bar Header Information', {
            'fields': ('section', 'row', 'is_active',)
        }),
    )
    list_display = ('text', 'section', 'row', 'is_active',)
    list_filter = (
        'text',
        'section',
        'row',
        'is_active',
    )


admin.site.register(NavBarHeader, NavBarHeaderAdmin)


class FeaturedNavBarAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Featured Navigational Bar Dropdown Information - Categorial Descriptions', {
            'fields': ('default_header', 'text', 'url',)
        }),
        ('Featured Navigational Bar Dropdown Information', {
            'fields': ('position', 'opennew', 'is_active',)
        }),
        ('Featured Navigational Bar Dropdown Information - Image Display', {
            'fields': ('image', 'image_width', 'image_length',)
        }),
    )


admin.site.register(FeaturedNavigationBar, FeaturedNavBarAdmin)


class CouponAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Coupon Information', {
            'fields': ('user', 'code', 'type', 'amount', 'percentDollars', 'currency_amount', 'expiration_date', 'uses', 'is_active',)
        }),
    )
    readonly_fields = ('created_date',)
admin.site.register(Coupon, CouponAdmin)


class GiftCodeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Gift Code Information', {
            'fields': ('user', 'code', 'serial', 'expiration_date', 'value', 'currency', 'uses', 'total_uses', 'tracking_total_uses', 'is_active',)
        }),
    )
    readonly_fields = ('created_date',)
    list_display = (
        'code',
        'expiration_date',
        'value',
        'total_uses',
        'tracking_total_uses',
        'is_active',
    )


admin.site.register(GiftCode, GiftCodeAdmin)


class GiftCodeRedemptionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Gift Code Information', {
            'fields': ('user', 'gift_code', 'amount', 'is_active',)
        }),
    )
    readonly_fields = ('redeemed_at',)

    list_display = ('user', 'gift_code', 'amount', 'redeemed_at',)


admin.site.register(GiftCodeRedemption, GiftCodeRedemptionAdmin)


class CustomerSupportAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Message Information-Categorial Descriptions', {
            'fields': ('user', 'name', 'category', 'issue', 'Additional_comments',)
        }),
        ('Contact Message Information-Image Display', {
            'fields': ('image', 'image_length', 'image_width',)
        }),
        ('Contact Message Information-Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(Support, CustomerSupportAdmin)


class SupportChatAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Support Room  Information - Categorial Descriptions', {
            'fields': ('name', 'signed_in_user', 'is_active',)
        }),
    )


admin.site.register(SupportChat, SupportChatAdmin)


class FormBaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Form Base Information - Categorial Descriptions', {
            'fields': ('user', 'form_name', 'form_type', 'text', 'image', 'is_active',),
            'classes': ('collapse-open',),
        }),
        ('Form Base Information - Multiple Choice', {
            'fields': ('correct_answer_multiple_choice',),
            'classes': ('open',),
        }),

        ('Form Base Information - Short Answer', {
            'fields': ('correct_answer_short_answer',),
            'classes': ('open',),
            # answers may vary
        }),
        ('Form Base Information - Free Response', {
            'fields': ('correct_answer_free_response',),
            'classes': ('open',),
            # answers may vary
        }),

        ('Form Base Information - True or False', {
            'fields': ('correct_answer_true_false',),
            'classes': ('open',),
        }),
        ('Form Base Information - Image Display', {
            'fields': ('correct_answer_image_field',),
            'classes': ('open',),
            # answers may vary
        }),
        ('Form Base Information - Decimal Field', {
            'fields': ('correct_answer_decimal_field',),
            'classes': ('open',),
            # answers may vary
        }),
        ('Form Base Information - Infinite Decimal Field', {
            'fields': ('correct_answer_infinite_decimal_field',),
            'classes': ('open',),
            # answers may vary
        }),
    )

    class Media:
        js = ('admin-collapse-default.js',)  # Include the custom JavaScript file
        css = {
            'all': ('admin-collapse-default.css',)
        }


admin.site.register(Questionaire, FormBaseAdmin)


class DefaultAvatarAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Default Avatar Information - Categorial Descriptions', {
            'fields': ('default_avatar_name', 'default_avatar',)
        }),
        ('Default Avatar Information - Attributes', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(DefaultAvatar, DefaultAvatarAdmin)


class ProfileCurrencyInline(admin.TabularInline):
    model = ProfileCurrency
    extra = 1

User = get_user_model()

class UserTypeFilter(admin.SimpleListFilter):
    title = 'User Type'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return (
            ('registered', 'Registered Users'),
            ('guest', 'Guest Users'),
        )

    def queryset(self, request, queryset):
        user_ids = queryset.values_list('user', flat=True)
        guest_ids = [
            profile.user.id for profile in queryset.select_related('user')
            if hasattr(profile.user, 'is_guest_user') and callable(
                profile.user.is_guest_user) and profile.user.is_guest_user()
        ]

        for uid in user_ids:
            try:
                user = User.objects.get(id=uid)
                if hasattr(user, 'is_guest_user') and callable(user.is_guest_user) and user.is_guest_user():
                    guest_ids.append(user.id)
            except User.DoesNotExist:
                continue

        if self.value() == 'registered':
            return queryset.exclude(user_id__in=guest_ids)
        if self.value() == 'guest':
            return queryset.filter(user_id__in=guest_ids)
        return queryset


class ProfileDetailsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Profile Information - User', {
            'fields': (
                'user', 'email', 'about_me', 'level', 'unlocked_daily_chests', 'subscription', 'is_active'
            )
        }),
        ('Profile Information - Avatar', {
            'fields': (
                'avatar', 'alternate',
            )
        }),
        ('Profile Information - Currency', {
            'fields': (
                'currency', 'currency_amount', 'total_currency_amount', 'total_currency_spent_30', 'total_currency_spent', 'total_card_money_spent', 'rubies_spent',
            )
        }),
        ('Profile Information - Cards Hit', {
            'fields': (
                'green_cards_hit', 'yellow_cards_hit', 'orange_cards_hit', 'red_cards_hit', 'black_cards_hit',
                'gold_cards_hit', 'red_gold_cards_hit', 'cards_counter',
            )
        }),
        ('Profile Information - Miscellaneous Statistics', {
            'fields': (
                'times_subtract_called', 'monstrosity',
                'seller', 'trader', 'membership', 'tier', 'position'
            )
        }),
    )
    readonly_fields = ('position', 'is_free_display', 'created_at',)
    inlines = [ProfileCurrencyInline]

    list_display = ('display_user_with_tag', 'level', 'trader', 'currency_amount', 'rubies_spent', 'get_selling_status', 'get_membership',
        'is_free_display', 'created_at',)
    list_filter = [UserTypeFilter, 'trader', 'membership', 'is_active']

    def display_user_with_tag(self, obj):
        user = obj.user
        if hasattr(user, 'is_guest_user') and callable(user.is_guest_user) and user.is_guest_user():
            return f"👤 Guest ({str(user.username)[:8]}…)"
        return str(user)
    display_user_with_tag.short_description = 'User'

    def get_selling_status(self, obj):
        return 'Yes' if obj.seller else 'No'
    get_selling_status.short_description = 'Selling Status'

    def get_membership(self, obj):
        return obj.membership if obj.membership else 'None'
    get_membership.short_description = 'Membership'

    def is_free_display(self, obj):
        return obj.is_free
    is_free_display.boolean = True
    is_free_display.short_description = 'Free?'


class LevelInline(admin.TabularInline):
    model = Experience.level.through
    extra = 1


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'display_levels', 'amount', 'is_active')
    inlines = [LevelInline]
    filter_horizontal = ('level',)

    def display_levels(self, obj):
        """Custom method to display levels as a comma-separated list."""
        levels = obj.level.all()
        if levels.exists():
            return ", ".join([level.level_name for level in levels])
        return "No levels assigned"

    display_levels.short_description = "Levels"  # Rename column header

    def save_model(self, request, obj, form, change):
        """Override save_model to calculate and set eligible levels."""
        super().save_model(request, obj, form, change)  # Save the instance first

        # Fetch eligible levels and update ManyToMany field
        eligible_levels = Level.objects.filter(experience__lte=obj.amount)
        obj.level.set(eligible_levels)  # Set eligible levels to the ManyToMany field


admin.site.register(Experience, ExperienceAdmin)


class AscensionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ascension Information - Categorial Description', {
            'fields': ('user', 'ascension', 'flavor_text', 'final_level', 'reward', 'is_active',),
            'classes': ('open',),
        }),
    )
    readonly_fields = ('ascension_number',)


admin.site.register(Ascension, AscensionAdmin)


class TransactionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Transaction Information', {
            'fields': ('inventory_object', 'user', 'currency', 'amount', 'is_active',)
        }),
    )
    readonly_fields = ('date_and_time',)
    list_display = ('inventory_object', 'user', 'currency', 'amount', 'date_and_time', 'is_active',)


admin.site.register(Transaction, TransactionAdmin)


admin.site.register(BattleParticipant)


class RobotAdmin(admin.ModelAdmin):
    model = Robot
    fieldsets = (
        ('Robot Information', {
            'fields': ('name', 'is_bot', 'image', 'sound', 'is_active'),
        }),
    )


admin.site.register(Robot, RobotAdmin)


class BattleGameInline(admin.TabularInline):
    model = BattleGame
    extra = 1  # Number of empty forms to display
    fields = ('game', 'quantity', 'game_cost', 'game_discount_cost')
    readonly_fields = ('game', 'quantity', 'game_cost', 'game_discount_cost')  # Make these fields read-only


class BattleParticipantInline(admin.TabularInline):
    model = BattleParticipant
    extra = 1
    verbose_name = "Participant"
    verbose_name_plural = "Participants"
    fields = ('user', 'robot', 'is_bot')


class BattleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Battle Information', {
            'fields': ('battle_name', 'currency', 'price', 'creator', 'min_human_participants', 'game_values', 'status', 'slots', 'type', 'bets_allowed', 'time', 'is_active'),
        }),
    )
    list_display = ('battle_name', 'creator', 'price', 'currency', 'status', 'is_active', 'time', 'bets_allowed')
    list_filter = ('status', 'is_active', 'currency', 'creator')
    search_fields = ('battle_name', 'creator__username')
    inlines = [BattleGameInline, BattleParticipantInline]


admin.site.register(Battle, BattleAdmin)


class BetAdmin(admin.ModelAdmin):
    model = Bet
    fieldsets = (
        ('Bet Information', {
            'fields': ('user', 'amount', 'battle', 'winning_user', 'winning_team', 'is_active'),
        }),
    )

    list_display = (
        'user',
        'amount',
        'battle',
        'is_active',
    )


admin.site.register(Bet, BetAdmin)


class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('type', 'flavor_text', 'icon', 'unlocking_level', 'is_active')


admin.site.register(Affiliation, AffiliationAdmin)


def validate_colors(value):
    colors = value.split(",")
    hex_pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    for color in colors:
        if not re.match(hex_pattern, color.strip()):
            raise ValidationError(f"'{color.strip()}' is not a valid hex color.")


class LevelAdminForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = "__all__"

    def clean_color(self):
        color = self.cleaned_data.get("color")
        if color:
            validate_colors(color)
        return color


class LevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'level_name', 'experience',  'icon', 'color', 'affiliation', 'is_active')
    filter_horizontal = ('games',)  # Use horizontal filter for the ManyToManyField
    ordering = ('level',)
    list_per_page = 1000

    # Define the action
    def mass_save(self, request, queryset):
        """
        Mass save selected Level instances.
        """
        for level in queryset:
            formulaic_experience = level.level * 2
            level.experience = formulaic_experience ** 2
            level.save()  # Save the instance
        self.message_user(request, f"{queryset.count()} levels have been saved successfully.")

    actions = ['mass_save']

admin.site.register(Level, LevelAdmin)


class LevelIconAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_icon','is_active')
    fieldsets = (
        ('Monstrosity Information', {
            'fields': ('name', 'level_icon', 'is_active',)
        }),
    )

admin.site.register(LevelIcon, LevelIconAdmin)


class MonstrosityAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Monstrosity Information', {
            'fields': ('user', 'monstrositysprite', 'monstrositys_name', 'level', 'is_active',)
        }),
    )

    list_display = (
        'user',
        'monstrositysprite',
        'monstrositys_name',
        'level',
        'is_active',
        'display_sprite_images'  # Add this method to list display
    )

    def display_sprite_images(self, obj):
        images = obj.get_sprite_images()  # Use the method defined in Withdraw model
        if images:
            return mark_safe(
                '<br>'.join([f'<img src="{img}" style="width: 100px; height: auto;" />' for img in images])
            )
        return 'No images'

    display_sprite_images.short_description = 'Monstrosity Sprites'


admin.site.register(Monstrosity, MonstrosityAdmin)


class MonstrositySpriteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Monstrosity Sprite Information', {
            'fields': ('name', 'image', 'is_active',)
        }),
    )


admin.site.register(MonstrositySprite, MonstrositySpriteAdmin)


class MembershipAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Membership Information', {
            'fields': ('name', 'tier', 'file', 'description', 'image_length', 'image_width', 'price', 'discount_price',  'second_price', 'second_discount_price', 'is_active',)
        }),
    )
    readonly_fields = ('mfg_date',)


admin.site.register(Membership, MembershipAdmin)


class AdministrationPagesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Administration Pages Information', {
            'fields': ('pages', 'hyperlink', 'opennew',)
        }),
        ('Administration Pages Information - Attributes', {
            'fields': ('section', 'page_name', 'is_active',)
        }),
    )


admin.site.register(AdminPages, AdministrationPagesAdmin)


class DonateAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Donation Information - Categorial Descriotions', {
            'fields': ('amount', 'nickname', 'donor',)
        }),
        ('Donation Pages Information - Attributes', {
            'fields': ('anonymous', 'is_active',)
        }),
    )
    readonly_fields = ('timestamp',)


admin.site.register(Donate, DonateAdmin)


class DonateIconAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Donation Information', {
            'fields': ('row', 'cover',)
        }),
    )


admin.site.register(DonateIcon, DonateIconAdmin)

class GroupedProfile(ProfileDetails):
    class Meta:
        proxy = True
        app_label = 'user_management'
        verbose_name = 'Account Profile'


class PlayerInventory(Inventory):
    class Meta:
        proxy = True
        app_label = 'user_management'
        verbose_name = 'Player Inventory'
        verbose_name_plural = 'Player Inventories'


@admin.register(GroupedProfile)
class GroupedProfileAdmin(ProfileDetailsAdmin):
    pass


@admin.register(PlayerInventory)
class PlayerInventoryAdmin(InventoryAdmin):
    pass