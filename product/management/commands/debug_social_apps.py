from django.core.management.base import BaseCommand
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = "Debug SocialApp configuration"

    def handle(self, *args, **kwargs):
        print("="*40)
        print("🌐 SITE_ID:", getattr(settings, "SITE_ID", "Not Set"))
        print("="*40)
        
        apps = SocialApp.objects.prefetch_related("sites").all()
        if not apps:
            print("❌ لا يوجد SocialApp")
            return

        domain_to_apps = {}

        for app in apps:
            site_domains = [site.domain for site in app.sites.all()]
            for domain in site_domains:
                domain_to_apps.setdefault(domain, []).append(app)
            print(f"\n🧩 SocialApp: {app.name}")
            print(f"🔑 Provider: {app.provider}")
            print(f"🌍 Linked Sites: {', '.join(site_domains)}")

        print("\n" + "="*40)
        print("📊 عدد SocialApps المرتبطة بكل domain:")
        for domain, apps in domain_to_apps.items():
            print(f"🌍 {domain} → {len(apps)} app(s)")
            if len(apps) > 1:
                print("⚠️⚠️ تحذير: أكثر من SocialApp لنفس الموقع!")

        print("="*40)
