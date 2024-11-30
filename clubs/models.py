from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model

class Club(models.Model):
    CATEGORY_CHOICES = [
        ('music', '공연ꞏ음악'),
        ('sports', '스포츠ꞏ레저'),
        ('volunteer', '사회ꞏ봉사'),
        ('art', '예술ꞏ창작'),
        ('study', '학술ꞏ탐구'),
        ('religion', '종교'),
        ('gender', '젠더ꞏ페미니즘'),
        ('it', 'IT'),
        ('culture', '문화ꞏ전통'),
        ('etc', '기타')
    ]

    FREQUENCY_CHOICES = [
        ('fluid', '유동적(일정에 따라)'),
        ('once_a_month', '월 1회'),
        ('once_every_other_week', '격주 1회'),
        ('once_a_week', '주 1회'),
        ('more', '주 2회 이상')
    ]

    DAYS_CHOICES = [
        ('mon', '월'),
        ('tue', '화'),
        ('wed', '수'),
        ('thu', '목'),
        ('fri', '금'),
        ('sat', '토'),
        ('sun', '일'),
        ('none', '해당 없음')
    ]

    FEE_TYPE_CHOICES = [
        ('yearly', '연간'),
        ('monthly', '월간'),
        ('one_time', '1회 납부')
    ]

    name = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)

    frequency = models.CharField(max_length=20)
    days = MultiSelectField(max_length=20, choices=DAYS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=100)

    fee_type = models.CharField(max_length=15, choices=FEE_TYPE_CHOICES)
    fee = models.PositiveIntegerField()

    image = models.ImageField(upload_to='upload_filepath', default='default.png')
    content = models.TextField()

    likes_count = models.PositiveBigIntegerField(default=0)

    contact = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ClubLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'club'], name='unique_user_club')
        ]

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            self.club.likes_count += 1
        else:
            self.club.likes_count -= 1
        self.club.save()

    def delete(self, *args, **kwargs):
        club = self.club
        super().delete(*args, **kwargs)
        club.likes_count -= 1
        club.save()

    def __str__(self):
        return f"{self.user} → {self.club} 좋아요"