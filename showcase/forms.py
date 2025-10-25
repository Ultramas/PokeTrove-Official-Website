from datetime import timezone, timedelta, date
from urllib import request

import self
from _decimal import Decimal
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from django.contrib.admin.widgets import AutocompleteSelect
from mysite import settings
from . import admin
from .models import Idea, OrderItem, EmailField, Item, Questionaire, StoreViewType, LotteryTickets, Meme, TradeOffer, \
    FriendRequest, Game, CurrencyOrder, UploadACard, Room, InviteCode, InventoryObject, CommerceExchange, ExchangePrize, \
    Trade_In_Cards, DegeneratePlaylistLibrary, DegeneratePlaylist, Choice, CATEGORY_CHOICES, CONDITION_CHOICES, \
    SPECIAL_CHOICES, QuickItem, SpinPreference, TradeItem, PrizePool, BattleParticipant, BattleGame, Monstrosity, \
    MonstrositySprite, Ascension, InventoryTradeOffer, VoteOption, Bet, GameChoice, MyPreferences, GiftCode, \
    GiftCodeRedemption, WeBuy, BuyCards, Investments, UserInvestmentFund
from .models import UpdateProfile
from .models import VoteQuery
from .models import StaffApplication
from .models import PartnerApplication
from .models import PunishmentAppeal
from .models import BanAppeal
from .models import ReportIssue
from .models import Shuffler
from .models import NewsFeed
from .models import StaffProfile
from .models import Event
from .models import Comment
from .models import Contact
from .models import BusinessMailingContact
from .models import ProfileDetails
from .models import UserProfile2
from .models import Support
from .models import SettingsModel
from .models import BackgroundImage
from .models import EBackgroundImage
from .models import ShowcaseBackgroundImage
from .models import ChatBackgroundImage
from .models import BilletBackgroundImage
from .models import BlogBackgroundImage
from .models import PostBackgroundImage
from .models import RuleBackgroundImage
from .models import AboutBackgroundImage
from .models import FaqBackgroundImage
from .models import StaffBackgroundImage
from .models import InformationBackgroundImage
from .models import TagBackgroundImage
from .models import UserBackgroundImage
from .models import StaffRanksBackgroundImage
from .models import MegaBackgroundImage
from .models import EventBackgroundImage
from .models import NewsBackgroundImage
from .models import BaseCopyrightTextField
from .models import Battle
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple

users = User.objects.filter()


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '150 Characters or fewer. Letters, digits and @/./+/-/_ only.'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Your email address'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password must be at least 8 characters.'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Please confirm your password.'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please use a different email address.")
        return email


CONTACT_PREFERENCE = [
    ('email', 'Email'),
    ('chat', 'Chat'),
    ('call', 'Call'),
]


class ContactForm(forms.ModelForm):
    prefered_contact = forms.MultipleChoiceField(choices=CONTACT_PREFERENCE, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Contact
        fields = '__all__'


class BusinessContactForm(forms.ModelForm):
    prefered_contact = forms.MultipleChoiceField(choices=CONTACT_PREFERENCE, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = BusinessMailingContact
        fields = '__all__'


class PostForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your name.'}))
    description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your profile description.'}))

    class Meta:
        model = UpdateProfile
        fields = ('name', 'description', 'image')


class Postit(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your name.'}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a category you want your idea to affect.'}))
    description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Please share any ideas you may have.'}))

    class Meta:
        model = Idea
        fields = ('name', 'category', 'description', 'image')


class VoteQueryForm(forms.ModelForm):
    class Meta:
        model = VoteQuery
        fields = ['description', 'category']


VoteOptionFormSet = inlineformset_factory(
    VoteQuery,
    VoteOption,
    fields=('text',),
    extra=2,
    can_delete=False
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


"""class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write Your Review Here"}))

    class Meta:
        model = ProductReview
        fields = '__all__'"""


class ShippingForm(forms.ModelForm):
    class Meta:
        model = UserProfile2
        fields = ('first_name', 'last_name', 'address', 'city', 'state', 'country', 'zip_code', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ShippingForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        self.fields['profile_picture'].required = False
        self.user = user

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.city = self.cleaned_data['city']
        user_profile.state = self.cleaned_data['state']
        user_profile.phone_number = self.cleaned_data['phone_number']
        user_profile.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            if hasattr(self.user, 'userprofile2') and self.user.userprofile2.exists():
                user_profile.save()
            else:
                user_profile.user = self.user
                user_profile.save()
        return user_profile

class StaffJoin(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Lemon Sauce'}))
    role = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What role are you applying for?'}))
    I_have_no_strikes_on_my_account_currently = forms.BooleanField()
    Why_do_you_want_to_apply_for_staff = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Tell us why you want to be a Accomfort Staff Member. Be descriptive.'}),
        label='Why do you want to apply for staff?'
    )
    How_do_you_think_you_can_make_PokeTrove_better = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Tell us what you will do to make Accomfort better as a staff member.'}),
        label='How do you think you can make PokeTrove better?'
    )
    I_confirm_that_I_have_read_all_the_staff_requirements_and_meet_all_of_them = forms.BooleanField(
        label='I confirm that I have read all the staff requirements and meet all of them'
    )

    class Meta:
        model = StaffApplication
        fields = ('name', 'role', 'I_have_no_strikes_on_my_account_currently',
                  'Why_do_you_want_to_apply_for_staff',
                  'overall_time_check', 'previous_role_time_check',
                  'How_do_you_think_you_can_make_PokeTrove_better',
                  'I_confirm_that_I_have_read_all_the_staff_requirements_and_meet_all_of_them')


class Server_Partner(forms.ModelForm):
    class Meta:
        model = PartnerApplication
        fields = (
            'user', 'name', 'category', 'multi_category', 'description', 'resume', 'requirement_check', 'policy_check',
            'voucher',)


class SupportForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your name.'}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Please let us know what type of issue you are dealing with.'}))
    issue = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Describe your issue in detail. We will get back to you ASAP.'}))
    additional_comments = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Put any additional comments you may have here.'}))

    class Meta:
        model = Support
        fields = ('name', 'category', 'issue', 'Additional_comments', 'image',)


class PunishAppeale(forms.ModelForm):
    class Meta:
        model = PunishmentAppeal
        fields = ('name', 'Rule_broken', 'Why_I_should_have_my_punishment_revoked', 'Additional_comments',)


class BanAppeale(forms.ModelForm):
    class Meta:
        model = BanAppeal
        fields = ('name', 'Rule_broken', 'Why_I_should_have_my_ban_revoked', 'Additional_comments',)


class ReportIssues(forms.ModelForm):
    class Meta:
        model = ReportIssue
        fields = ('name', 'category', 'issue', 'Additional_comments', 'image',)


class News_Feed(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Liam_Mannara#6510'}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Please let us know what form of news this is.'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Write the news here.'}))
    image = forms.FileField(widget=forms.TextInput(attrs={'placeholder': 'Please provide a cover image for the news.'}))

    class Meta:
        model = NewsFeed
        fields = '__all__'


class Staffprofile(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Liam_Mannara#6510'}))
    position = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Please let us know what staff position you serve currently.'}))
    description = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Write whatever you want on your profile here (within regulations).'}))
    staff_feats = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Let us know of your transcendental feats of making MegaClan a better place.'}))
    image = forms.FileField(
        widget=forms.TextInput(attrs={'placeholder': 'Please provide a cover image for your profile.'}))

    class Meta:
        model = StaffProfile
        fields = '__all__'


class Eventform(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'The event name goes here'}))
    category = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Please let us know what type of event this is (tournament, stage night, etc).'}))
    description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Give a brief description of the event.'}))
    date_and_time = forms.DateTimeField()
    image = forms.FileField(
        widget=forms.TextInput(attrs={'placeholder': 'Please provide a cover image for the event.'}))

    class Meta:
        model = Event
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'post', 'name', 'email', 'body', 'active'


from django import forms
from django.forms import inlineformset_factory
from .models import Game, Choice


class PlayerInventoryGameForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=PrizePool.objects.filter(is_active=1),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Prizes"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quantity_fields = {}
        for prize in PrizePool.objects.filter(is_active=1):
            field_name = f"quantity_{prize.id}"
            self.fields[field_name] = forms.IntegerField(
                label=f"Quantity for {prize.prize_name}",
                min_value=0,
                max_value=prize.number,
                required=False,
            )
            self.quantity_fields[prize.id] = field_name

    class Meta:
        model = Game
        fields = ['name', 'cost', 'discount_cost', 'type', 'category', 'image', 'power_meter', 'items']


class InventoryGameForm(forms.ModelForm):
    choices = forms.ModelMultipleChoiceField(
        queryset=Choice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Game
        fields = [
            'name', 'cost', 'discount_cost', 'type', 'category', 'image',
        ]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['rarity', 'lower_nonce', 'upper_nonce', 'number_of_choice']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


ChoiceFormSet = modelformset_factory(
    Choice,
    form=ChoiceForm,
    extra=0,
)

from django.utils.safestring import mark_safe


class TypeaheadSelectWidget(forms.Select):
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css',)
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js',
        )

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)

        element_id = attrs.get('id', 'id_%s' % name)
        js = f'''
        <script type="text/javascript">
            (function($) {{
                $(document).ready(function(){{
                    $('#{element_id}').select2({{
                        width: 'resolve',
                        placeholder: 'Select a choice',
                        allowClear: true
                    }});
                }});
            }})(django.jQuery);
        </script>
        '''
        return mark_safe(output + js)


class GameChoiceForm(forms.ModelForm):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.all(),
        widget=TypeaheadSelectWidget,
        required=True
    )

    class Meta:
        model = GameChoice
        fields = '__all__'


class ToggleFavoriteForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput())


class MyPreferencesForm(forms.ModelForm):
    class Meta:
        model = MyPreferences
        fields = ['spintype', 'is_active']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class AscensionCreateForm(forms.ModelForm):
    class Meta:
        model = Ascension
        fields = []


class CardUploading(forms.ModelForm):
    class Meta:
        model = Choice
        fields = 'choice_text', 'file', 'category', 'tier', 'rarity', 'total_number_of_choice', 'value', 'number'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CardUploading, self).__init__(*args, **kwargs)


ChoiceFormSet = inlineformset_factory(Game, Choice, form=CardUploading, extra=1)


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        daily = cleaned_data.get("daily")
        unlocking_level = cleaned_data.get("unlocking_level")

        if daily and not unlocking_level:
            raise ValidationError("An unlocking level must be set for daily games.")

        return cleaned_data


class BattleCreationForm(forms.ModelForm):
    game_values = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': 'readonly'}),
        required=False,
        label="Game Quantities and Values"
    )
    total_value = forms.DecimalField(
        widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
        required=False,
        label="Total Value"
    )
    slots = forms.ChoiceField(
        choices=Battle.BATTLE_SLOTS,
        widget=forms.RadioSelect,
        label="Battle Slots",
        initial='2'
    )
    type = forms.ChoiceField(
        choices=Battle.BATTLE_TYPE,
        widget=forms.RadioSelect,
        label="Battle Type",
        initial='Free For All'
    )

    class Meta:
        model = Battle
        fields = ['battle_name', 'chests', 'min_human_participants', 'slots', 'type', 'bets_allowed', 'game_values',
                  'total_value']
        widgets = {
            'chests': forms.SelectMultiple(attrs={'id': 'id_chests'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['type'] = 'Free For All'

    def clean(self):
        cleaned_data = super().clean()
        chests = cleaned_data.get('chests')
        quantities = {}

        for game in chests:
            quantity_key = f'quantity-{game.id}'
            quantity = self.data.get(quantity_key, 1)
            if not quantity.isdigit() or int(quantity) < 1:
                raise forms.ValidationError(f"Invalid quantity for {game.name}.")
            quantities[game.id] = int(quantity)

        self.cleaned_data['quantities'] = quantities
        return cleaned_data

    def save(self, commit=True):

        battle = super().save(commit=commit)
        quantities = self.cleaned_data.get('quantities', {})

        for game in self.cleaned_data.get('chests'):
            qty = quantities.get(game.id, 1)

            battle_game, created = BattleGame.objects.get_or_create(battle=battle, game=game)
            if battle_game.quantity != qty:
                battle_game.quantity = qty
                battle_game.save()

        battle.price = battle.total_game_values
        battle.save()

        return battle


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('amount',)

    def __init__(self, *args, **kwargs):

        battle = kwargs.pop('battle', None)
        super().__init__(*args, **kwargs)

        if not battle:
            battle = getattr(self.instance, 'battle', None) or \
                     Battle.objects.filter(pk=self.initial.get('battle')).first()

        if battle:
            participant_user_ids = battle.participants.values_list('user_id', flat=True)
        else:
            participant_user_ids = User.objects.none().values_list('id', flat=True)

        if battle and battle.type in ('teams', 'team_fight'):
            self.fields['winning_team'] = forms.ModelChoiceField(
                queryset=User.objects.filter(id__in=participant_user_ids),
                label="Winning Team",
                required=True
            )
        else:
            self.fields['winning_user'] = forms.ModelChoiceField(
                queryset=User.objects.filter(id__in=participant_user_ids),
                label="Winning User",
                required=True
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.instance.user
        if commit:
            instance.save()
        return instance


BattleGameFormSet = inlineformset_factory(
    parent_model=Battle,
    model=BattleGame,
    fields=['game', 'quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'game': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    }
)


class BattleJoinForm(forms.ModelForm):
    class Meta:
        model = BattleParticipant
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.battle = kwargs.pop('battle', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if BattleParticipant.objects.filter(user=self.user, battle=self.battle).exists():
            raise forms.ValidationError("You are already a participant in this battle.")

        return cleaned_data

    def save(self, commit=True):

        participant = super().save(commit=False)
        participant.user = self.user
        participant.battle = self.battle

        if commit:
            participant.save()

            self.battle.participants.add(participant)

        return participant


class MoveToTradeForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    fees = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    specialty = forms.ChoiceField(choices=SPECIAL_CHOICES, required=False)
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, initial="M", required=False)
    label = forms.CharField(max_length=1000, required=False)
    slug = forms.SlugField(required=False)
    value = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    image_length = forms.IntegerField(required=False)
    image_width = forms.IntegerField(required=False)
    length_for_resize = forms.IntegerField(required=False)
    width_for_resize = forms.IntegerField(required=False)

    class Meta:
        model = TradeItem
        fields = '__all__'


class AddTradeForm(forms.ModelForm):
    class Meta:
        model = InventoryObject
        fields = ('trade_locked',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddTradeForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['add_trade_item'].queryset = InventoryObject.objects.filter(user=user)


class Trade_In_Form(forms.ModelForm):
    class Meta:
        model = Trade_In_Cards
        fields = ('card_name', 'card_image', 'card_condition',)


class SettingsForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        fields = ('username', 'password', 'email', 'coupons', 'news')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.instance.user
        if commit:
            instance.save()
        return instance


class BaseCopyrightTextFielde(forms.ModelForm):
    class Meta:
        model = BaseCopyrightTextField
        fields = '__all__'


class BackgroundImagery(forms.ModelForm):
    class Meta:
        model = BackgroundImage
        fields = '__all__'


class BackgroundImagery(forms.ModelForm):
    class Meta:
        model = BackgroundImage
        fields = '__all__'


class EBackgroundImagery(forms.ModelForm):
    class Meta:
        model = EBackgroundImage
        fields = '__all__'


class ChatBackgroundImagery(forms.ModelForm):
    class Meta:
        model = ChatBackgroundImage
        fields = '__all__'


class ShowcaseBackgroundImagery(forms.ModelForm):
    class Meta:
        model = ShowcaseBackgroundImage
        fields = '__all__'


class BlogBackgroundImagery(forms.ModelForm):
    class Meta:
        model = BlogBackgroundImage
        fields = '__all__'


class PostBackgroundImagery(forms.ModelForm):
    class Meta:
        model = PostBackgroundImage
        fields = '__all__'


class RuleBackgroundImagery(forms.ModelForm):
    class Meta:
        model = RuleBackgroundImage
        fields = '__all__'


class AboutBackgroundImagery(forms.ModelForm):
    class Meta:
        model = AboutBackgroundImage
        fields = '__all__'


class FaqBackgroundImagery(forms.ModelForm):
    class Meta:
        model = FaqBackgroundImage
        fields = '__all__'


class StaffBackgroundImagery(forms.ModelForm):
    class Meta:
        model = StaffBackgroundImage
        fields = '__all__'


class InformationBackgroundImagery(forms.ModelForm):
    class Meta:
        model = InformationBackgroundImage
        fields = '__all__'


class TagBackgroundImagery(forms.ModelForm):
    class Meta:
        model = TagBackgroundImage
        fields = '__all__'


class UserBackgroundImagery(forms.ModelForm):
    class Meta:
        model = UserBackgroundImage
        fields = '__all__'


class StaffRanksBackgroundImagery(forms.ModelForm):
    class Meta:
        model = StaffRanksBackgroundImage
        fields = '__all__'


class MegaBackgroundImagery(forms.ModelForm):
    class Meta:
        model = MegaBackgroundImage
        fields = '__all__'


class EventBackgroundImagery(forms.ModelForm):
    class Meta:
        model = EventBackgroundImage
        fields = '__all__'


class NewsBackgroundImagery(forms.ModelForm):
    class Meta:
        model = NewsBackgroundImage
        fields = '__all__'


class RoomSettings(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['public', 'logo']


class UploadCardsForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name of the card.'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UploadCardsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UploadACard
        fields = ('name', 'image', 'public',)


class InviteCodeForm(forms.ModelForm):
    class Meta:
        model = InviteCode
        fields = ['code', 'user', 'expire_time', 'permalink']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.request.user
        if user.is_authenticated:
            self.initial['user'] = user


from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('C', 'Card')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False,
                                                                              widget=CountrySelectWidget(attrs={
                                                                                  'class': 'custom-select d-block w-100'}))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(
        attrs={'class': 'custom-select d-block w-100'}))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        all_items_currency_based = kwargs.pop('all_items_currency_based', False)
        super(CheckoutForm, self).__init__(*args, **kwargs)
        if all_items_currency_based:
            self.fields['payment_option'].required = False
            self.fields['payment_option'].widget = forms.HiddenInput()


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

class GiftCodeForm(forms.Form):
    code = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")

        try:
            gift_code = GiftCode.objects.get(code=code)
        except GiftCode.DoesNotExist:
            raise forms.ValidationError("Invalid gift code.")

        if gift_code.is_active != 1:
            raise forms.ValidationError("This gift code is inactive.")

        if gift_code.expiration_date and gift_code.expiration_date < timezone.now():
            gift_code.is_active = 0
            gift_code.save()
            raise forms.ValidationError("This gift code has expired.")

        redemptions = GiftCodeRedemption.objects.filter(user=self.user, gift_code=gift_code).count()
        if redemptions >= gift_code.uses:
            raise forms.ValidationError("You have already redeemed this gift code the maximum number of times.")

        return cleaned_data


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    number = forms.IntegerField(required=False)
    exp_month = forms.IntegerField(required=False)
    expiry = forms.CharField(required=False)
    exp_year = forms.IntegerField(required=False)
    cvc = forms.IntegerField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class PaypalPaymentForm(forms.Form):
    number = forms.CharField(required=True)
    exp_month = forms.IntegerField(required=True)
    expiry = forms.CharField(required=True)
    exp_year = forms.IntegerField(required=True)
    cvc = forms.IntegerField(required=True)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CurrencyCheckoutForm(forms.Form):
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CurrencyPaymentForm(forms.Form):
    number = forms.IntegerField(required=False)
    exp_month = forms.IntegerField(required=False)
    expiry = forms.CharField(required=False)
    exp_year = forms.IntegerField(required=False)
    cvc = forms.IntegerField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CurrencyPaypalPaymentForm(forms.Form):
    number = forms.CharField(required=True)
    exp_month = forms.IntegerField(required=True)
    expiry = forms.CharField(required=True)
    exp_year = forms.IntegerField(required=True)
    cvc = forms.IntegerField(required=True)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


from .models import Withdraw

from django import forms
from .models import Withdraw, InventoryObject


class WithdrawForm(forms.ModelForm):
    selected_cards = forms.ModelMultipleChoiceField(
        queryset=InventoryObject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Withdraw
        fields = ['number_of_cards', 'shipping_state', 'fees', 'status', 'is_active']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['selected_cards'].queryset = InventoryObject.objects.filter(user=user)


class DegeneratePlaylistForm(forms.ModelForm):
    class Meta:
        model = DegeneratePlaylist
        fields = ['user', 'song', 'audio_file', 'audio_img', 'is_active', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['song'].queryset = DegeneratePlaylistLibrary.objects.filter(user=user)


class TradeProposalForm(forms.ModelForm):
    class Meta:
        model = TradeOffer
        fields = ['title', 'trade_items', 'estimated_trading_value', 'user2', 'message', 'quantity', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TradeProposalForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['trade_items'].queryset = TradeItem.objects.filter(user=user)


class InventoryTradeOfferResponseForm(forms.ModelForm):
    class Meta:
        model = InventoryTradeOffer
        fields = ['status']
        widgets = {
            'status': forms.RadioSelect(choices=[('accepted', 'Accept'), ('declined', 'Decline')]),
        }


class ExchangePrizesForm(forms.ModelForm):
    usercard = forms.ModelMultipleChoiceField(
        queryset=InventoryObject.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Items to Trade"
    )
    exchangeprizes = forms.ModelMultipleChoiceField(
        queryset=ExchangePrize.objects.filter(is_active=1),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Prizes"
    )

    class Meta:
        model = CommerceExchange
        fields = ['usercard', 'exchangeprizes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['usercard'].queryset = InventoryObject.objects.filter(user=user)

        self.fields['usercard'].label_from_instance = self.get_usercard_label
        self.fields['exchangeprizes'].label_from_instance = self.get_exchangeprize_label

    def get_usercard_label(self, obj):
        """Define how InventoryObject details are displayed in the form."""
        return f"{obj.choice_text} - {obj.category} - ${obj.price} ({obj.condition})"

    def get_exchangeprize_label(self, obj):
        """Define how ExchangePrize details are displayed in the form."""
        return f"{obj.name} - ${obj.value} ({obj.condition})"

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('usercard') and not cleaned_data.get('exchangeprizes'):
            raise forms.ValidationError("You must select at least one item to trade or exchange.")
        return cleaned_data

    def save(self, commit=True):
        selected_usercards = self.cleaned_data.get('usercard', [])
        selected_exchangeprizes = self.cleaned_data.get('exchangeprizes', [])

        total_usercard_value = sum([card.price for card in selected_usercards])
        total_exchangeprize_value = sum([prize.value for prize in selected_exchangeprizes])

        difference = total_usercard_value - total_exchangeprize_value

        profile = ProfileDetails.objects.get(user=self.instance.user)

        if difference > 0:
            profile.currency_amount += difference
            profile.save()

        for usercard in selected_usercards:
            usercard.delete()

        for exchangeprize in selected_exchangeprizes:
            InventoryObject.objects.create(
                user=self.instance.user,
                choice=exchangeprize.prize,
                choice_text=exchangeprize.name,
                category=exchangeprize.prize.category,
                currency=exchangeprize.currency,
                price=exchangeprize.value,
                condition=exchangeprize.condition,
                image=exchangeprize.image,
                image_length=exchangeprize.image_length,
                image_width=exchangeprize.image_width,
                is_active=1,
            )

        if commit:
            self.instance.save()
        return self.instance


class InventoryTradeForm(forms.ModelForm):
    trading_user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=True,
        label="Select a User to Trade With"
    )
    usercard = forms.ModelMultipleChoiceField(
        queryset=TradeItem.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'usercard-checkbox'}),
        required=True,
        label="Select Your Items to Trade"
    )
    exchangeprizes = forms.ModelMultipleChoiceField(
        queryset=TradeItem.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'exchangeprizes-checkbox'}),
        required=True,
        label="Select Their Items to Trade"
    )

    class Meta:
        model = CommerceExchange
        fields = ['trading_user', 'usercard', 'exchangeprizes']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['trading_user'].queryset = User.objects.filter(
            tradeitem__is_active=True
        ).distinct().exclude(id=current_user.id)

        self.fields['usercard'].queryset = TradeItem.objects.filter(user=current_user, is_active=True)

        self.fields['exchangeprizes'].queryset = TradeItem.objects.filter(is_active=True)


class AddMonstrosityForm(forms.ModelForm):
    class Meta:
        model = Monstrosity
        fields = ['monstrositysprite', 'monstrositys_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['monstrositysprite'].queryset = MonstrositySprite.objects.filter(is_active=1)
        self.fields['monstrositysprite'].widget = forms.RadioSelect(
            choices=[(sprite.id, sprite) for sprite in self.fields['monstrositysprite'].queryset],
        )


class FeedMonstrosityForm(forms.ModelForm):
    class Meta:
        model = Monstrosity
        fields = ['feed_amount', ]

    def clean_currency_amount(self):
        currency_amount = self.cleaned_data['currency_amount']
        if currency_amount <= 0:
            raise forms.ValidationError("Currency amount must be positive.")
        return currency_amount

from .models import Endowment

class EndowmentForm(forms.Form):
    user = forms.CharField(widget=forms.HiddenInput())
    target = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name of Endowed Individual'}))
    order = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['user'].initial = self.request.user.username
            self.fields['target'].initial = User.objects.exclude(pk=self.request.user.pk).first().username

    def clean_user(self):
        username = self.cleaned_data.get('user')
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid username. Please enter a valid user.')

    def save(self, commit=True):

        user = self.clean_user()

        instance = Endowment(
            user=user,
            target=self.cleaned_data['target'],
            order=self.cleaned_data['order']
        )
        if commit:
            instance.save()
        return instance

class HitStandForm(forms.Form):
    action = forms.ChoiceField(choices=[('hit', 'Hit'), ('stand', 'Stand')], label='Action')

class CreateChest(forms.ModelForm):
    class Meta:
        model = Shuffler
        fields = ('question', 'choice_text', 'file', 'choices', 'category', 'heat', 'shuffletype', 'demonstration',
                  'total_number_of_choice', 'cost',)
        readonly_fields = ('mfg_date',)


from .models import SellerApplication


class SellerApplicationForm(forms.ModelForm):
    class Meta:
        model = SellerApplication
        fields = ['first_name', 'last_name', 'age', 'identification', 'email']

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('age')
        today = date.today()
        if (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) < 18:
            raise ValidationError('You need to be 18 or older to apply to sell!')
        return dob


class ProfileDetail(forms.ModelForm):
    class Meta:
        model = ProfileDetails
        fields = ('email', 'avatar', 'alternate', 'about_me')


class StoreViewTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.type:
            self.fields['type'].initial = self.instance.type

        self.fields['type'].widget.attrs.update({'onchange': 'this.form.submit();'})

    class Meta:
        model = StoreViewType
        fields = ('type',)
        widgets = {
            'type': forms.Select(choices=StoreViewType.VIEW_TYPE_CHOICES),
        }

    def save(self, commit=True):
        user = self.request.user if self.request.user.is_authenticated else None
        storeviewtype = super().save(commit=False)
        if user and isinstance(user, User):
            storeviewtype.user = user
        else:
            storeviewtype.user = None
        if commit:
            storeviewtype.save()
        return storeviewtype


class GameRoomViewTypeForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.type:
            self.fields['type'].initial = self.instance.type

        self.fields['type'].widget.attrs.update({'onchange': 'this.form.submit();'})

    class Meta:
        model = StoreViewType
        fields = ('type', 'slug')
        widgets = {
            'type': forms.Select(choices=StoreViewType.VIEW_TYPE_CHOICES),
        }

    def save(self, commit=True):
        user = self.request.user if self.request.user.is_authenticated else None
        storeviewtype = super().save(commit=False)
        if user and isinstance(user, User):
            storeviewtype.user = user
        else:
            storeviewtype.user = None
        if commit:
            storeviewtype.save()
        return storeviewtype


class ProfileViewTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.type:
            self.fields['type'].initial = self.instance.type

        self.fields['type'].widget.attrs.update({'onchange': 'this.form.submit();'})

    class Meta:
        model = StoreViewType
        fields = ('type',)
        widgets = {
            'type': forms.Select(choices=StoreViewType.VIEW_TYPE_CHOICES),
        }

    def save(self, commit=True):
        user = self.request.user if self.request.user.is_authenticated else None
        storeviewtype = super().save(commit=False)
        if user and isinstance(user, User):
            storeviewtype.user = user
        else:
            storeviewtype.user = None
        if commit:
            storeviewtype.save()
        return storeviewtype


class CurrencyViewTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.type:
            self.fields['type'].initial = self.instance.type

        self.fields['type'].widget.attrs.update({'onchange': 'this.form.submit();'})

    class Meta:
        model = StoreViewType
        fields = ('type',)
        widgets = {
            'type': forms.Select(choices=StoreViewType.VIEW_TYPE_CHOICES),
        }

    def save(self, commit=True):
        user = self.request.user if self.request.user.is_authenticated else None
        storeviewtype = super().save(commit=False)
        if user and isinstance(user, User):
            storeviewtype.user = user
        else:
            storeviewtype.user = None
        if commit:
            storeviewtype.save()
        return storeviewtype


from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data["new_password1"]

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',)


class BilletBackgroundImagery(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'e.g. Liam Mannara'}))
    category = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Choose a category you want your idea to affect.'
        }))
    image = forms.ImageField(widget=forms.TextInput(
        attrs={'placeholder': 'Attach an image for your post.'}))

    class Meta:
        model = BilletBackgroundImage
        fields = '__all__'


class TagBackgroundImagery(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'e.g. Liam Mannara'}))
    category = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Choose a category you want your idea to affect.'
        }))
    image = forms.ImageField(widget=forms.TextInput(
        attrs={'placeholder': 'Attach an image for your post.'}))

    class Meta:
        model = TagBackgroundImage
        fields = '__all__'


class StaffRanksBackgroundImagery(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Liam Mannara'}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a category you want your idea to affect.'}))
    image = forms.ImageField(widget=forms.TextInput(attrs={'placeholder': 'Attach an image for your post.'}))

    class Meta:
        model = StaffRanksBackgroundImage
        fields = '__all__'


class MegaBackgroundImagery(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Liam Mannara'}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a category you want your idea to affect.'}))
    image = forms.ImageField(widget=forms.TextInput(attrs={'placeholder': 'Attach an image for your post.'}))

    class Meta:
        model = MegaBackgroundImage
        fields = '__all__'


from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group

User = get_user_model()


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,

        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()

        self.save_m2m()
        return instance


from django.core.mail import send_mail


class ContactForme(forms.ModelForm):
    class Meta:
        model = Contact
        fields = {"name", "email", "inquiry", "message"}

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'e.g. Marinara Sauce'}),
            "email": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'e.g. Intellex@gmail.com'}),
            "inquiry": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Subject of your message.'}),
            "message": forms.Textarea(attrs={"class": "form-control", 'placeholder': 'Your message.'})
        }

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """

        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg, from_email

    def send(self):
        subject, msg, from_email = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=from_email,
            recipient_list=[settings.EMAIL_HOST_USER]
        )


class BusinessMailingForm(forms.ModelForm):
    class Meta:
        model = BusinessMailingContact
        fields = {"name", "email", "inquiry", "message"}

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'e.g. Liam Mannara'}),

            "email": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'e.g. Intellex@gmail.com'}),
            "inquiry": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Your inquiry goes here.'}),
            "message": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Your message goes here.'})
        }

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """

        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg, from_email

    def send(self):
        subject, msg, to_email = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email]
        )


from .models import Feedback

from django.contrib import admin
from django.contrib.auth.models import User


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('user', 'item', 'quantity', 'slug')

        widgets = {

        }


class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemForm


admin.site.register(OrderItem, OrderItemAdmin)

from .models import Wager


class WagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Wager
        fields = ['amount']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if self.user_profile and self.user_profile.currency_amount < amount:
            raise forms.ValidationError("Insufficient funds for this bet.")
        return amount


class DirectedTradeOfferForm(forms.ModelForm):
    class Meta:
        model = TradeOffer
        fields = ['trade_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trade_status'].widget = forms.RadioSelect(choices=TradeOffer.TRADE_STATUS)

    def clean_direct_trade_offer(self):
        user = self.instance.user
        return user


class TradeOfferAcceptanceForm(forms.ModelForm):
    class Meta:
        model = TradeOffer
        fields = ['user', 'user2']


from django.core.exceptions import ValidationError
from django import forms
from django.core.exceptions import ValidationError
from .models import Item
from django import forms
from django.core.exceptions import ValidationError
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'title', 'price', 'discount_price', 'specialty', 'label',
            'slug', 'description', 'image', 'image2', 'image3', 'image4', 'image5'
        )
        widgets = {
            # Floating fields
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            # Choice fields (non-floating selects from choices)
            'specialty': forms.Select(attrs={'class': 'form-select no-float'}),
            'label': forms.Select(attrs={'class': 'form-select no-float'}),
            # File input (non-floating)
            'image': forms.ClearableFileInput(attrs={'class': 'form-file no-float'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        non_float_fields = ('specialty', 'label', 'image')
        float_fields = [n for n in self.fields if n not in non_float_fields]

        # Optional: prepend prompt to specialty (ChoiceField)
        if 'specialty' in self.fields:
            choices = list(self.fields['specialty'].choices)
            if choices and choices[0][0] != '':
                self.fields['specialty'].choices = [('', 'Select specialty')] + choices
            self.fields['specialty'].required = False

        # Floating fields setup
        for name in float_fields:
            field = self.fields[name]
            label_text = field.label or name.replace('_', ' ').title()
            field.widget.attrs['placeholder'] = ' '   # single space for :placeholder-shown
            field.widget.attrs['class'] = (field.widget.attrs.get('class', '') + ' float-input').strip()
            field.label = label_text

        # Ensure no placeholder on non-floating
        for name in non_float_fields:
            self.fields[name].widget.attrs.pop('placeholder', None)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        user = self.instance.user
        if Item.objects.filter(title=title, user=user).exists():
            raise ValidationError("You have already created an item with this title.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')              # Decimal or None
        discount_price = cleaned_data.get('discount_price')  # Decimal or None

        rate = Decimal('0.07')
        base = discount_price if discount_price is not None else price
        if base is not None:
            # Optional: quantize to 2 decimals to match model field
            cleaned_data['fees'] = (base * rate).quantize(Decimal('0.01'))
        else:
            # No price fields supplied (currency-based); leave fees empty
            cleaned_data['fees'] = None

        return cleaned_data


class QuickItemForm(forms.ModelForm):
    class Meta:
        model = QuickItem
        fields = ['image', 'image_length', 'image_width']


from .models import TradeItem

from .models import TradeOffer


class TradeItemForm(forms.ModelForm):
    class Meta:
        model = TradeItem
        fields = ['title', 'category', 'specialty', 'condition', 'slug', 'status', 'description', 'image']

    def __init__(self, *args, **kwargs):
        inventory_object = kwargs.pop('inventory_object', None)
        super().__init__(*args, **kwargs)

        if inventory_object:
            self.fields['title'].initial = inventory_object.title
            self.fields['category'].initial = inventory_object.category
            self.fields['specialty'].initial = inventory_object.specialty
            self.fields['condition'].initial = inventory_object.condition
            self.fields['description'].initial = inventory_object.description
            self.fields['image'].initial = inventory_object.image


class TradeProposalForm(forms.ModelForm):
    class Meta:
        model = TradeOffer
        fields = ['title', 'trade_items', 'estimated_trading_value', 'user2', 'message', 'quantity', ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TradeProposalForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['trade_items'].queryset = TradeItem.objects.filter(user=user)


class FriendRequestForm(forms.ModelForm):
    receiver = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'You can add friends with their username.'}))

    class Meta:
        model = FriendRequest
        fields = ['receiver']

    def clean_receiver(self):
        receiver_username = self.cleaned_data['receiver']
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            raise ValidationError("User with this username does not exist.")
        return receiver


class FriendRequestAcceptanceForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver']


from django import forms
from .models import RespondingTradeOffer, TradeOffer

from django.contrib.auth.decorators import login_required

from django import forms
from .models import TradeItem, RespondingTradeOffer

from .fields import UserRestrictedModelMultipleChoiceField


class RespondingTradeOfferForm(forms.ModelForm):
    offered_trade_items = UserRestrictedModelMultipleChoiceField(user=None, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['offered_trade_items'].queryset = TradeItem.objects.filter(user=user)
        self.fields['offered_trade_items'].user = user

    class Meta:
        model = RespondingTradeOffer
        fields = ['estimated_trading_value', 'offered_trade_items', 'wanted_trade_items', 'message']


from django.utils import timezone


class TicketRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TicketRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = self.user

        now = timezone.now()
        reset_time = now.replace(hour=17, minute=0, second=0)
        if now.hour < 17:
            reset_time -= timedelta(days=1)

        if LotteryTickets.objects.filter(user=user, mfg_date__gte=reset_time).exists():
            raise forms.ValidationError("You have already collected your daily ticket. Please try again after 5pm.")

        return cleaned_data

    class Meta:
        model = LotteryTickets
        fields = ('name',)


from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import get_user_model
from .models import Feedback

"""class FeedbackForm(forms.ModelForm):
    star_rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Outstanding!'}))
    order = forms.ModelChoiceField(queryset=None)
    image = forms.ImageField(required=False)

    class Meta:
        model = Feedback
        fields = ('order', 'star_rating', 'comment', 'slug', 'image')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(initial=self.request.user.username)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['order'].queryset = OrderItem.objects.filter(user=self.request.user)

"""

from django import forms
from .models import Feedback
from .models import OrderItem

from django import forms
from django.utils.text import slugify
from django import forms
from .models import Feedback
from django import forms

from django import forms
from .models import Feedback

from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Feedback
        fields = ('order', 'star_rating', 'comment', 'slug', 'image')

    def save(self, commit=True):

        user = self.request.user if self.request.user.is_authenticated else None

        feedback = super().save(commit=False)

        if feedback.order and feedback.order.item:
            feedback.item = feedback.order.item
        if feedback.order:
            feedback.slug = feedback.order.slug

        if user and isinstance(user, User):
            feedback.username = user
        else:
            feedback.username = None

        if 'star_rating' in self.cleaned_data:
            feedback.star_rating = self.cleaned_data['star_rating']
        if 'slug' in self.cleaned_data:
            feedback.slug = self.cleaned_data['slug']

        if 'image' in self.cleaned_data:
            feedback.image = self.cleaned_data['image']

        if commit:
            feedback.save()
        return feedback


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('order', 'star_rating', 'comment', 'slug', 'image')


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investments
        fields = ['investment', 'type']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'investment': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UserInvestmentFundForm(forms.ModelForm):
    class Meta:
        model = UserInvestmentFund
        fields = ['fund', 'user', 'type']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'investment': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'style': 'height: 50px;'}))

    class Meta:
        model = EmailField
        fields = ('email', 'confirmation')

    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if not confirmation:
            raise forms.ValidationError("You must agree to the terms to continue.")
        return confirmation


class SpinPreferenceForm(forms.ModelForm):
    class Meta:
        model = SpinPreference
        fields = ['quick_spin']


class WeBuyForm(forms.ModelForm):
    class Meta:
        model = WeBuy
        fields = ['is_active']


class BuyCardsForm(forms.ModelForm):
    class Meta:
        model = BuyCards
        fields = ['image', 'image2', 'image3', 'image4', 'image5',]


BuyCardsFormSet = inlineformset_factory(
    parent_model=WeBuy,
    model=BuyCards,
    form=BuyCardsForm,
    fields=['image', 'image2', 'image3', 'image4', 'image5',],
    extra=1,                # show 1 extra empty form by default
    can_delete=True,        # allow deleting existing rows
    min_num=0,
    validate_min=False,
    max_num=None,           # no upper limit
    validate_max=False,
)


class QuestionForm(forms.Form):
    text = forms.CharField(max_length=255)

    answer_choices = forms.MultipleChoiceField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'dynamic-input'}),
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.form_type == 'option1':
            self.fields['answer_choices'] = forms.CharField(
                label='Answer Choices (comma-separated)',
                required=True,
                widget=forms.TextInput(attrs={'placeholder': 'Choice 1, Choice 2, ...'}),
            )


class QuestionCountForm(forms.Form):
    num_questions = forms.IntegerField(label="Number of Questions", )
    form_name = forms.CharField()

    class Meta:
        model = Questionaire
        fields = {"form_name", "form_text", "text"}


from .models import Answer


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super(AnswerForm, self).__init__(*args, **kwargs)

        for question in questions:
            field_name = f'answer_{question.id}'
            self.fields[field_name] = forms.CharField(
                label=question.text,
                required=True,
                widget=forms.TextInput(attrs={'class': 'form-control'})
            )


class MemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['title', 'image']
