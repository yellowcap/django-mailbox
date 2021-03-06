import logging

from django.conf import settings
from django.contrib import admin

from django_mailbox.models import MessageAttachment, Message, Mailbox
from django_mailbox.signals import message_received
from django_mailbox.utils import convert_header_to_unicode

logger = logging.getLogger(__name__)


def get_new_mail(mailbox_admin, request, queryset):
    for mailbox in queryset.all():
        logger.debug('Receiving mail for %s' % mailbox)
        mailbox.get_new_mail()
get_new_mail.short_description = 'Get new mail'


def resend_message_received_signal(message_admin, request, queryset):
    for message in queryset.all():
        logger.debug('Resending \'message_received\' signal for %s' % message)
        message_received.send(sender=message_admin, message=message)
resend_message_received_signal.short_description = (
    'Re-send message received signal'
)


class MailboxAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'uri',
        'from_email',
        'active',
    )
    actions = [get_new_mail]


class MessageAttachmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('message', )
    list_display = ('message', 'document',)


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    def attachment_count(self, msg):
        return msg.attachments.count()

    def subject(self, msg):
        return convert_header_to_unicode(msg.subject)

    inlines = [
        MessageAttachmentInline,
    ]
    list_display = (
        'subject',
        'processed',
        'read',
        'mailbox',
        'outgoing',
        'attachment_count',
    )
    ordering = ['-processed']
    list_filter = (
        'mailbox',
        'outgoing',
        'processed',
        'read',
    )
    exclude = (
        'body',
    )
    raw_id_fields = (
        'in_reply_to',
    )
    readonly_fields = (
        'text',
    )
    actions = [resend_message_received_signal]

if getattr(settings, 'DJANGO_MAILBOX_ADMIN_ENABLED', True):
    admin.site.register(Message, MessageAdmin)
    admin.site.register(MessageAttachment, MessageAttachmentAdmin)
    admin.site.register(Mailbox, MailboxAdmin)
