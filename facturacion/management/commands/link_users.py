from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from facturacion.models import Usuario


class Command(BaseCommand):
    help = 'Link existing Usuario records to auth User by matching email. Reports matched and unmatched.'

    def add_arguments(self, parser):
        parser.add_argument('--create-missing', action='store_true', help='Create Django User for Usuario without matching User (with unusable password).')

    def handle(self, *args, **options):
        User = get_user_model()
        created = 0
        linked = 0
        unmatched = []
        for u in Usuario.objects.all():
            if u.user:
                continue
            if u.email:
                user = User.objects.filter(email=u.email).first()
                if user:
                    u.user = user
                    u.save()
                    linked += 1
                    self.stdout.write(self.style.SUCCESS(f'Linked Usuario {u.pk} ({u.email}) -> User {user.pk}'))
                else:
                    if options['create_missing']:
                        username = u.email if u.email else u.nombre
                        user = User.objects.create_user(username=username, email=u.email or '', password=None)
                        # set unusable password
                        user.set_unusable_password()
                        user.save()
                        u.user = user
                        u.save()
                        created += 1
                        self.stdout.write(self.style.SUCCESS(f'Created User {user.pk} and linked to Usuario {u.pk}'))
                    else:
                        unmatched.append((u.pk, u.email))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Linked: {linked}'))
        if options['create_missing']:
            self.stdout.write(self.style.SUCCESS(f'Created: {created}'))
        if unmatched:
            self.stdout.write(self.style.WARNING('Unmatched usuarios (no User with same email):'))
            for pk, email in unmatched:
                self.stdout.write(self.style.WARNING(f' - Usuario {pk}: {email}'))
