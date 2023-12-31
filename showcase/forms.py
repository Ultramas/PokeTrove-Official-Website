from urllib import request

from django import forms

from mysite import settings
from .models import Idea, OrderItem, EmailField, Item, Questionaire, StoreViewType
from .models import UpdateProfile
from .models import Vote
from .models import StaffApplication
from .models import PartnerApplication
from .models import PunishmentAppeal
from .models import BanAppeal
from .models import ReportIssue
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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from .models import ProfileTwo
# from .models import PublicProfile

users = User.objects.filter()


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '150 Characters or fewer. Letters, digits and @/./+/-/_ only.'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your email address'}))
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your password must be at least 8 characters.'}), label='Password')
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please confirm your password.'}),
                                label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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
    class Meta:
        model = UpdateProfile
        fields = ('name', 'description', 'image')
        # name = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Enter your first name'}))

        # description = forms.CharField(widget = forms.EmailInput
        # (attrs={'placeholder':'Enter your email'}))


class Postit(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('name', 'category', 'description', 'image')


class PosteForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Liam Mannara'}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Choose a category you want your vote to affect.'}))

    # altered image URLField to ImageField, check for bugs please

    class Meta:
        model = Vote
        fields = ('name', 'category')


# Profile Form
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


class StaffJoin(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Lemon Sauce'}))
    role = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What role are you applying for?'}))
    I_have_no_strikes_on_my_account_currently = forms.BooleanField()
    Why_do_you_want_to_apply_for_staff = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Tell us why you want to be a Accomfort Staff Member. Be descriptive.'}))
    How_do_you_think_you_can_make_MC_better = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Tell us what you will do to make Accomfort better as a staff member.'}))
    I_confirm_that_I_have_read_all_the_staff_requirements_and_meet_all_of_them = forms.BooleanField()

    class Meta:
        model = StaffApplication
        fields = ('name', 'role', 'I_have_no_strikes_on_my_account_currently',
                  'Why_do_you_want_to_apply_for_staff',
                  'How_do_you_think_you_can_make_MC_better',
                  'I_confirm_that_I_have_read_all_the_staff_requirements_and_meet_all_of_them')


class Server_Partner(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Your server name goes here.')
    category = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Pick a category you feel your server represents (gaming, community, etc).'}))
    description = forms.CharField(help_text='Describe your server. Tell potential members why they should join.')
    server_invite = forms.URLField(help_text='Idea your server invite link here.')

    class Meta:
        model = PartnerApplication
        fields = '__all__'


class SupportForm(forms.ModelForm):
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


# class EditProfileForm(forms.Form):
# username = forms.CharField()
# about_me = forms.CharField(widget=forms.Textarea())
# image = forms.ImageField(required=False)

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
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = BaseCopyrightTextField
        fields = '__all__'


class BackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = BackgroundImage
        fields = '__all__'


class BackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = BackgroundImage
        fields = '__all__'


class EBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = EBackgroundImage
        fields = '__all__'


class ChatBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = ChatBackgroundImage
        fields = '__all__'


class ShowcaseBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = ShowcaseBackgroundImage
        fields = '__all__'


class BlogBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = BlogBackgroundImage
        fields = '__all__'


class PostBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = PostBackgroundImage
        fields = '__all__'


class RuleBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = RuleBackgroundImage
        fields = '__all__'


class AboutBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = AboutBackgroundImage
        fields = '__all__'


class FaqBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = FaqBackgroundImage
        fields = '__all__'


class StaffBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = StaffBackgroundImage
        fields = '__all__'


class InformationBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = InformationBackgroundImage
        fields = '__all__'


class TagBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = TagBackgroundImage
        fields = '__all__'


class UserBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = UserBackgroundImage
        fields = '__all__'


class StaffRanksBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = StaffRanksBackgroundImage
        fields = '__all__'


class MegaBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = MegaBackgroundImage
        fields = '__all__'


class EventBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = EventBackgroundImage
        fields = '__all__'


class NewsBackgroundImagery(forms.ModelForm):
    #    image = forms.ImageField(widget=forms.TextInput(
    #        attrs={'placeholder': 'Link an image for your post.'}))

    class Meta:
        model = NewsBackgroundImage
        fields = '__all__'


from django import forms
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
                                                                                  'class': 'custom-select d-block w-100', }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(required=False, widget=CountrySelectWidget(
        attrs={'class': 'custom-select d-block w-100', }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


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
    # number = forms.IntegerField(required=True)
    number = forms.CharField(required=True)
    exp_month = forms.IntegerField(required=True)
    expiry = forms.CharField(required=True)
    exp_year = forms.IntegerField(required=True)
    cvc = forms.IntegerField(required=True)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class ProfileDetail(forms.ModelForm):
    class Meta:
        model = ProfileDetails
        fields = ('email', 'avatar', 'alternate', 'about_me')


class StoreViewTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    class Meta:
        model = StoreViewType
        fields = ('type',)



    def save(self, commit=True):

        user = self.request.user if self.request.user.is_authenticated else None

        storeviewtype = super().save(commit=False)

        # Set the user, star rating, and slug if available
        if user and isinstance(user, User):  # Check if user is a User instance
            storeviewtype.user = user
        else:
            storeviewtype.user = None  # Set to None if user is not a valid User instance

        if commit:
            storeviewtype.save()
        return storeviewtype


# class PublicForm(forms.ModelForm):
# class Meta:
# model = PublicProfile
# fields = ['username']


# class NewUserForm(UserCreationForm):
# ...

# class UserForm(forms.ModelForm):
# ...

# class ProfileForm(forms.ModelForm):
# class Meta:
# model = ProfileTwo
# fields = ('products',)


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


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
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
            "message": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Your message.'})
        }

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
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
            # get this instead of Contact.name in views
            "email": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'e.g. Intellex@gmail.com'}),
            "inquiry": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Your inquiry goes here.'}),
            "message": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Your message goes here.'})
        }

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
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
        # might want to replace item with order (check models)
        widgets = {
            # 'slug': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class OrderItemAdmin(admin.ModelAdmin):
    form = OrderItemForm
    # readonly_fields = ('user', 'slug', 'item', 'quantity')


admin.site.register(OrderItem, OrderItemAdmin)

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
        # Get the user who created the feedback
        user = self.request.user if self.request.user.is_authenticated else None

        # Create an instance of the Feedback model
        feedback = super().save(commit=False)

        if feedback.order and feedback.order.item:
            feedback.item = feedback.order.item
        if feedback.order:
            feedback.slug = feedback.order.slug

        # Set the user, star rating, and slug if available
        if user and isinstance(user, User):  # Check if user is a User instance
            feedback.username = user
        else:
            feedback.username = None  # Set to None if user is not a valid User instance

        if 'star_rating' in self.cleaned_data:
            feedback.star_rating = self.cleaned_data['star_rating']
        if 'slug' in self.cleaned_data:
            feedback.slug = self.cleaned_data['slug']

        # Set the 'image' field if an image file is provided
        if 'image' in self.cleaned_data:
            feedback.image = self.cleaned_data['image']

        if commit:
            feedback.save()
        return feedback


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('order', 'star_rating', 'comment', 'slug', 'image')


class EmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))

    class Meta:
        model = EmailField
        fields = ('email', 'confirmation')

    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if not confirmation:
            raise forms.ValidationError("You must agree to the terms to continue.")
        return confirmation
        # name = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Enter your first name'}))

        # description = forms.CharField(widget = forms.EmailInput
        # (attrs={'placeholder':'Enter your email'}))


class QuestionForm(forms.Form):
    text = forms.CharField(max_length=255)

    answer_choices = forms.MultipleChoiceField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'dynamic-input'}),
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a field for answer choices when the question type is 'Multiple Choice'
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
