# -*- coding: utf-8 -*-

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from jira.models import Task, UserProfile, User


@receiver(pre_save, sender=Task, dispatch_uid='blockinfo_pre_save')
def blockinfo_pre_save(sender, instance, **kwargs):
    print('raw', kwargs.get('raw'))
    if not kwargs.get('raw'):
        old_block = Task.objects.filter(id=instance.id).first()
        if old_block and old_block.block != instance.block:
            print("in func")
            instance.send_message_about_block_status()


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])
