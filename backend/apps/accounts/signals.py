import secrets
import string

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import MembershipLevel, Profile, User, UserMembership, Wallet


def generate_referral_code():
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(8))


@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    if not created:
        return

    if not instance.referral_code:
        code = generate_referral_code()
        while User.objects.filter(referral_code=code).exists():
            code = generate_referral_code()
        instance.referral_code = code
        instance.save(update_fields=["referral_code"])

    Profile.objects.get_or_create(user=instance)
    Wallet.objects.get_or_create(user=instance)

    default_level = MembershipLevel.objects.filter(name=MembershipLevel.Level.BRONZE).first()
    if default_level:
        UserMembership.objects.get_or_create(user=instance, defaults={"level": default_level})
