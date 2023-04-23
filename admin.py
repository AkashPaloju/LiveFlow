from django.contrib import admin
from .models import Video
from .models import Watch_later
from .models import History
from .models import Channel
from .models import Pay
from .models import BoughtVideoB
from .models import MovieSeries
from .models import Ad

# Register your models here.


admin.site.register(Video)
admin.site.register(Watch_later)
admin.site.register(History)
admin.site.register(Channel)
admin.site.register(Pay)
admin.site.register(BoughtVideoB)
admin.site.register(MovieSeries)
admin.site.register(Ad)
