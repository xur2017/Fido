
from django.contrib.syndication.views import Feed
from .models import Pet

class LatestPetUpdates(Feed):
    title = 'latest pet updates'
    link = '/feed/'
    description = 'latest pet updates'
    
    def items(self):
        return Pet.objects.order_by('-created_at')[:10]
        
    def item_title(self, item):
        list1 = [item.name, item.get_pet_type_display(), item.get_breed_display(), item.get_sex_display(), str(item.age)]
        s1 = " # "
        s1 = s1.join(list1) 
        return s1
        
    def item_description(self, item):
        s1 = item.description
        return s1
