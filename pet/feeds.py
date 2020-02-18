
from django.contrib.syndication.views import Feed
from .models import Pet

class LatestPetUpdates(Feed):
    title = 'pet updates'
    link = '/feed'
    description = 'pet updates'
    
    def items(self):
        return Pet.objects.order_by('-created_at')[:2]
        
    def item_title(self, item):
        return item.name
    
    def item_description(self, item):
        return item.description
