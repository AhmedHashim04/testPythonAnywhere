# Generated by Django 5.2.1 on 2025-07-26 02:14

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_alter_order_options_alter_order_shipping_method"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={
                "ordering": ["-is_default", "-updated_at"],
                "verbose_name": "Address",
                "verbose_name_plural": "العناوين",
            },
        ),
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "طلب",
                "verbose_name_plural": "الطلبات",
            },
        ),
        migrations.AlterModelOptions(
            name="orderitem",
            options={
                "verbose_name": "عنصر الطلب",
                "verbose_name_plural": "عناصر الطلب",
            },
        ),
        migrations.AlterField(
            model_name="address",
            name="city",
            field=models.CharField(max_length=100, verbose_name="المدينة/المركز"),
        ),
        migrations.AlterField(
            model_name="address",
            name="governorate",
            field=models.CharField(
                choices=[
                    ("C", "القاهرة"),
                    ("GZ", "الجيزة"),
                    ("ALX", "الإسكندرية"),
                    ("ASN", "أسوان"),
                    ("AST", "أسيوط"),
                    ("BNS", "بني سويف"),
                    ("BH", "البحيرة"),
                    ("IS", "الإسماعيلية"),
                    ("MN", "المنيا"),
                    ("MNF", "المنوفية"),
                    ("MT", "مطروح"),
                    ("KFS", "كفر الشيخ"),
                    ("DK", "الدقهلية"),
                    ("SHG", "سوهاج"),
                    ("SHR", "الشرقية"),
                    ("PTS", "بورسعيد"),
                    ("DT", "دمياط"),
                    ("FYM", "الفيوم"),
                    ("GH", "الغربية"),
                    ("KB", "القليوبية"),
                    ("LX", "الأقصر"),
                    ("WAD", "الوادي الجديد"),
                    ("SUZ", "السويس"),
                    ("SIN", "شمال سيناء"),
                    ("SIS", "جنوب سيناء"),
                    ("QH", "قنا"),
                    ("RSH", "Red Sea"),
                ],
                max_length=10,
                verbose_name="محافظة",
            ),
        ),
        migrations.AlterField(
            model_name="address",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="المعرف",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="order.address",
                verbose_name="عنوان الشحن",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء"),
        ),
        migrations.AlterField(
            model_name="order",
            name="full_name",
            field=models.CharField(max_length=100, verbose_name="الاسم الكامل"),
        ),
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="المعرف",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="invoice_pdf",
            field=models.FileField(
                blank=True, null=True, upload_to="invoices/", verbose_name="فاتورة PDF"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="notes",
            field=models.TextField(
                blank=True, null=True, verbose_name="ملاحظات إضافية"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="paid",
            field=models.BooleanField(default=False, verbose_name="مدفوع"),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[("cod", "الدفع عند الاستلام")],
                default="cod",
                max_length=20,
                verbose_name="طريقة الدفع",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.CharField(
                max_length=11,
                validators=[
                    django.core.validators.RegexValidator(
                        message="يجب أن يبدأ رقم الهاتف بـ 010، أو 011، أو 012، أو 015 ويتكون من 11 رقمًا.",
                        regex="^(01[0125])[0-9]{8}$",
                    )
                ],
                verbose_name="رقم الهاتف",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_cost",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=10, verbose_name="تكلفة الشحن"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_method",
            field=models.CharField(
                choices=[("standard", "شحن عادي")],
                default="standard",
                max_length=20,
                verbose_name="طريقة الشحن",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "قيد الانتظار"),
                    ("processing", "قيد المعالجة"),
                    ("shipped", "تم الشحن"),
                    ("delivered", "تم التوصيل"),
                    ("cancelled", "تم الإلغاء"),
                    ("returned", "تم الإرجاع"),
                    ("failed", "فشل"),
                ],
                default="pending",
                max_length=20,
                verbose_name="الحالة",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status_changed_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="تاريخ تغيير الحالة"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="إجمالي السعر",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
                verbose_name="المستخدم",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="discount",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="خصم"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="السعر"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1, verbose_name="الكمية"),
        ),
        migrations.AlterField(
            model_name="shippingoption",
            name="place",
            field=models.CharField(max_length=100, verbose_name="مكان الشحن"),
        ),
    ]
